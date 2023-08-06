import os

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.gridspec as gridspec

from guide_bot.logging.log_plotter_helpers import LogParameter
from guide_bot.logging.log_plotter_helpers import GuideElementLog
from guide_bot.logging.log_plotter_helpers import sort_permutation
from guide_bot.logging.log_plotter_helpers import extract_parameters


import guide_bot.elements.Element_straight as Straight
import guide_bot.elements.Element_elliptic as Elliptic
import guide_bot.elements.Element_slit as Slit


class LogPlotter:
    def __init__(self, filename):
        if not os.path.isfile(filename):
            raise NameError("Filename not found!" + str(filename))

        self.filename = filename

        self.legend = None
        self.parameters = None
        self.data = None
        self.scan_name = None

        self.read_log_file()

        file_location = os.path.split(self.filename)[0]
        self.guide_log_filename = os.path.join(file_location, self.scan_name + ".guide_log")
        if not os.path.isfile(self.guide_log_filename):
            raise NameError("Filename not found!" + str(self.guide_log_filename))
        self.guide_element_logs = None
        self.read_guide_log_file()

        self.fom = self.data[:, 0]
        self.fom_sort_indices = sort_permutation(self.fom, reverse=True)

        self.data_fom_sorted = self.data[self.fom_sort_indices, :]
        self.fom_sorted = self.data_fom_sorted[:, 0]

    def read_log_file(self):
        with open(self.filename) as file:
            file.readline()

            second_line = file.readline()
            try:
                n_parameters = int(second_line)
                self.scan_name = None
                skip = n_parameters + 3
            except:
                scan_name = second_line.split(" ")[1]
                self.scan_name = scan_name.strip()
                n_parameters = int(file.readline())
                skip = n_parameters + 4

            parameters = []
            for _ in range(n_parameters):
                par = LogParameter()
                par.read_line(file.readline())
                parameters.append(par)

            self.legend = file.readline().strip().split()

        self.parameters = parameters
        self.data = np.loadtxt(self.filename, skiprows=skip)

    def read_guide_log_file(self):

        with open(self.guide_log_filename) as file:
            line = file.readline()
            guide_logs = []
            current_log = None
            while line:

                if line.strip() == "":
                    line = file.readline()
                    continue

                if line.startswith("Element"):
                    if current_log is not None:
                        guide_logs.append(current_log)

                    element_type = line.split(" ")[1]
                    element_name = line.split(" ")[2]
                    current_log = GuideElementLog(element_name, element_type)

                elif current_log is not None:
                    par_key = line.split()[0].strip()
                    par_type = line.split()[1].strip()
                    par_name = line.split()[2].strip()

                    current_log.add_parameter(par_key, par_type, par_name)

                line = file.readline()

            if current_log is not None:
                guide_logs.append(current_log)

        self.guide_element_logs = guide_logs

    def plot_best_guide(self):
        fig, axs = plt.subplots(figsize=(10,10), nrows=2, ncols=1)
        self.plot_guide_ax(axs[0], horizontal=True)
        self.plot_guide_ax(axs[1], horizontal=False)

    def plot_guide_ax(self, ax, horizontal=True, data_line=None):

        # If no data is given, plot best configuration
        if data_line is None:
            data_line = self.data_fom_sorted[-1, :]


        # plot source
        par_dict = extract_parameters(self.guide_element_logs[0], self.legend, data_line)
        if horizontal:
            if "start_width" in par_dict and "start_point" in par_dict:
                start_point = par_dict["start_point"]
                start_width = par_dict["start_width"]
                ax.plot([start_point, start_point], [-0.5*start_width, 0.5*start_width], "k")
        else:
            if "start_height" in par_dict and "start_point" in par_dict:
                start_point = par_dict["start_point"]
                start_height = par_dict["start_height"]
                ax.plot([start_point, start_point], [-0.5*start_height, 0.5*start_height], "k")

        color = "k"
        for guide_element in self.guide_element_logs:

            if color == "k":
                color = "b"
            elif color == "b":
                color = "k"

            par_dict = extract_parameters(guide_element, self.legend, data_line)
            if guide_element.element_type == "Slit":
                if horizontal:
                    Slit.plot_element_horizontal(ax, par_dict, color=color)
                else:
                    Slit.plot_element_vertical(ax, par_dict, color=color)

            if guide_element.element_type == "Straight":
                if horizontal:
                    Straight.plot_element_horizontal(ax, par_dict, color=color)
                else:
                    Straight.plot_element_vertical(ax, par_dict, color=color)

            if guide_element.element_type == "Elliptic":
                if horizontal:
                    Elliptic.plot_element_horizontal(ax, par_dict, color=color)
                else:
                    Elliptic.plot_element_vertical(ax, par_dict, color=color)

        """
        # Plot samlple (parameters not in log files yet, really should be)
        par_dict = extract_parameters(self.guide_element_logs[-1], self.legend, data_line)
        print(self.guide_element_logs[-1].parameters)
        if horizontal:
            if "end_width" in par_dict and "next_start_point" in par_dict:
                end_point = par_dict["next_start_point"]
                print(end_point)
                end_width = par_dict["end_width"]
                ax.plot([end_point, end_point], [-0.5 * end_width, 0.5 * end_width], "k")
        else:
            if "end_height" in par_dict and "next_start_point" in par_dict:
                end_point = par_dict["next_start_point"]
                print(end_point)
                end_height = par_dict["end_height"]
                ax.plot([end_point, end_point], [-0.5 * end_height, 0.5 * end_height], "k")
        """

        ax.set_xlabel("Distance from source [m]")
        if horizontal:
            ax.set_ylabel("Horizontal [m]")
        else:
            ax.set_ylabel("Vertical [m]")

    def plot_1D_fom_ax(self, ax, highlight_sorted_index=None, **kwargs):
        ax.scatter(range(len(self.fom)), self.fom, marker=".", label=self.scan_name, **kwargs)
        ax.plot(self.fom_sorted, color="orange")
        ax.set_xlabel("Optimizer iteration")
        ax.set_ylabel("FOM")

        if highlight_sorted_index is not None:
            raw_index = self.fom_sort_indices[highlight_sorted_index]
            ax.scatter(raw_index, self.fom[raw_index], s=30,
                       marker="o", label=self.scan_name, color='r', **kwargs)

            ax.scatter(highlight_sorted_index, self.fom_sorted[highlight_sorted_index], s=30,
                       marker="x", label=self.scan_name, color='r', **kwargs)

    def plot_1D_cps_ax(self, ax, sorted=False, **kwargs):
        n_guides = len(self.data[:, 0])
        pars_length_system_names = [par.name for par in self.parameters if par.owner == "length_system"]
        pars_length_system_indices = [self.legend.index(par) for par in pars_length_system_names]

        if sorted:
            start_points = self.data_fom_sorted[:, pars_length_system_indices]
        else:
            start_points = self.data[:, pars_length_system_indices]
        start_points_first = start_points[0, :]
        sort_key = sort_permutation(start_points_first)

        ax.plot(range(n_guides), start_points[:, sort_key], **kwargs)
        if sorted:
            ax.set_xlabel("iteration (sorted, fom worst to best)")
        else:
            ax.set_xlabel("iteration")
        ax.set_ylabel("start point [m]")

    def plot_1D_given_type_ax(self, ax, type="horizontal", sorted=False, only_free=True, **kwargs):
        found_par_names = set()
        for guide_element in self.guide_element_logs:
            for simple_parameter_name in guide_element.parameter_type:
                if guide_element.parameter_type[simple_parameter_name] == type:
                    found_par_names.add(guide_element.parameters[simple_parameter_name])

        if only_free:
            for parameter in self.parameters:
                if parameter.name in found_par_names:
                    if parameter.type not in ("FreeInstrumentParameter", "RelativeFreeInstrumentParameter"):
                        found_par_names.remove(parameter.name)

        plotted_par_indices = [self.legend.index(par) for par in found_par_names if par in self.legend]

        if sorted:
            data = self.data_fom_sorted
        else:
            data = self.data

        n_guides = len(data[:, 0])
        for index in plotted_par_indices:
            ax.scatter(range(n_guides), data[:, index], marker=".", label=self.legend[index], **kwargs)

        ax.legend()
        ax.set_ylabel("Parameter value")
        if sorted:
            ax.set_xlabel("Optimizer iteration (fom sorted, worst to best)")
        else:
            ax.set_xlabel("Optimizer iteration")

    def plot_all(self):

        self.plot_best_guide()

        fig, axs = plt.subplots(figsize=(15, 20), nrows=4, ncols=2)

        self.plot_1D_fom_ax(axs[0, 0])
        self.plot_1D_cps_ax(axs[1, 0])
        self.plot_1D_cps_ax(axs[1, 1], sorted=True)
        self.plot_1D_given_type_ax(axs[2, 0], type="horizontal", sorted=False)
        self.plot_1D_given_type_ax(axs[2, 1], type="horizontal", sorted=False)
        self.plot_1D_given_type_ax(axs[3, 0], type="vertical", sorted=False)
        self.plot_1D_given_type_ax(axs[3, 1], type="vertical", sorted=False)

    def plot_overview(self):

        fig = plt.figure(figsize=(13, 12), tight_layout=True)
        fig.suptitle(self.scan_name, fontsize=16)
        gs = gridspec.GridSpec(3, 3)

        self.plot_1D_fom_ax(fig.add_subplot(gs[0, 0:2]))
        self.plot_1D_cps_ax(fig.add_subplot(gs[0, 2]))

        geometry_h_ax = fig.add_subplot(gs[1, 0:2])
        self.plot_guide_ax(geometry_h_ax, horizontal=True)

        geometry_v_ax = fig.add_subplot(gs[2, 0:2])
        self.plot_guide_ax(geometry_v_ax, horizontal=False)

        par_h_ax = fig.add_subplot(gs[1, 2])
        self.plot_1D_given_type_ax(par_h_ax, type="horizontal")

        par_v_ax = fig.add_subplot(gs[2, 2])
        self.plot_1D_given_type_ax(par_v_ax, type="vertical")


