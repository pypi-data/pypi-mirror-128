# Copyright (c) 2021 Mark Crowe <https://github.com/markcrowe-com>. All rights reserved.

from pandas import DataFrame
import matplotlib.pyplot as pyplot


def plot_lines(dataframe: DataFrame, x_axis: str, y_line_configurations: list, size: list, x_axis_label: str, y_axis_label: str) -> None:
    pyplot.subplots(figsize=size)

    for column, color in y_line_configurations:
        pyplot.plot(dataframe[x_axis], dataframe[column],
                    color, label=column, marker='.')

    pyplot.xlabel(x_axis_label)
    pyplot.ylabel(y_axis_label)
    pyplot.legend()
    pyplot.show()
