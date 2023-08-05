# Copyright (c) 2021 Mark Crowe <https://github.com/markcrowe-com>. All rights reserved.

from IPython.core.display import display, HTML
from pandas import DataFrame
import data_analytics.exploratory_data_analysis as eda

def print_dataframe_analysis_report(dataframe: DataFrame) -> None:
    """
    Print an analysis report of the data frame. 
    - Show the top five rows of the data frame as a quick sample.
    - Show the data types of each column.
    - Report count of any duplicates.
    - Report count of any missing values.
    - Report any single value columns.
    :param dataframe: The data frame to be analysed
    """
    display(HTML(f'<h2>{dataframe.name}</h2>'))
    print('Row, Column Count: ', dataframe.shape)
    display(HTML('<h3>Sample: Top five rows</h3>'))
    display(dataframe.head())
    display(HTML('<h3>Data Types</h3>'))
    display(dataframe.dtypes)
    display(HTML('<h3>Duplicates</h3>'))
    duplicate_rows_dataframe = dataframe[dataframe.duplicated()]
    print("Number of duplicate rows: ", duplicate_rows_dataframe.shape[0])
    display(HTML('<h3>Null Values</h3>'))
    print(dataframe.isnull().sum())
    display(HTML('<h3>Single Value Columns</h3>'))
    report_single_value_columns(dataframe)
    display(HTML('<h3>Outlier Analysis</h3>'))
    report_outliers_columns(dataframe)


def report_single_value_columns(dataframe: DataFrame) -> None:
    """
    Report any columns that have only one value
    :param dataframe: DataFrame
    """
    has_no_single_value_columns = True
    for column in dataframe.columns:
        if eda.is_single_value_column(dataframe, column):
            print(
                f'- The column "{column}" has only one value. Recommend removing.')
            has_no_single_value_columns = False
    if(has_no_single_value_columns):
        print('No single value columns found.')


def report_outliers_columns(dataframe: DataFrame) -> None:
    """
    Report any columns that have outliers
    :param dataframe: DataFrame
    """
    has_no_outlier_columns = True
    for column_label in dataframe.columns:
        if eda.is_numeric_data_type_column(dataframe[column_label]):
            outlier_count = eda.count_outliers(dataframe, column_label)
            if outlier_count > 0:
                print(
                    f'- The column "{column_label}" has {outlier_count} outliers. Recommend removing outliers.')
                has_no_outlier_columns = False

    if(has_no_outlier_columns):
        print('No columns with outliers found.')
