# import libraries
from typing import Union, List
import numpy as np
import pandas as pd
import logging
import json

# define functions

def read_my_data(filepath: str, low_memory: bool) -> Union[pd.DataFrame, None]:
    """
    Use pandas to read a csv file located at filepath.

    filepath: the location of the csv file.
    low_memory: a boolean flag used to control the memory usage when reading large CSV files.
    return: a pandas DataFrame object, or None if an error occurs.
    """
    try:
        logging.info("Reading the file located at {}".format(filepath))
        df = pd.read_csv(filepath, low_memory=low_memory)
        return df
    except FileNotFoundError as e:
        logging.error("File not found at {}".format(filepath))
    except Exception as e:
        logging.error("An error occurred while reading the file: {}".format(str(e)))
    return None

def get_unique_values(data: pd.DataFrame, column: str) -> Union[int, None]:
    """
    Calculate the number of uniques values in a pandas DataFrame column.

    data: pandas DataFrame as input.
    column: the name of a column.
    return: the number of unique values, or None if an error occurs.
    """
    try:
        logging.info("Calculating the unique values for {}.".format(column))
        unique_values = data[column].nunique()
        return unique_values
    except KeyError:
        logging.error("Column {} not found in the DataFrame.".format(column))
    except Exception as e:
        logging.error("An error occurred while calculating unique values for column {} : {}".format(column, str(e)))
    return None

def calculate_average_value(data: pd.DataFrame, column: str) -> Union[float, None]:
    """
    Calculate the mean value of a numeric column, rounded to two digits.

    data: pandas DataFrame as input.
    column: name of the column.
    return: the average value of the column, or None if an error occurs.
    """
    try:
        if pd.api.types.is_numeric_dtype(data[column]):
            logging.info("Calculating the mean value for column: {}".format(column))
            average_rating = np.mean(data[column])
            rounded_rating = round(average_rating, 2)
            return rounded_rating
        else:
            raise ValueError("Column {} is not numeric.".format(column))
    except KeyError as e:
        logging.error("Column {} not found in DataFrame.".format(column))
    except Exception as e:
        logging.error("An error occurred while calculating the average value for column {} : {}".format(column, str(e)))
    return None

def merge_two_dataframes(data_1: pd.DataFrame,
                         data_2: pd.DataFrame,
                         how: str, on: str) -> Union[pd.DataFrame, None]:
    """
    Merge two pandas dataframes by specifying the join operation and the column used for the join.

    data_1: the first pandas DataFrame.
    data_2: the second pandas DataFrame.
    how: possible variations are: ['inner', 'outer', 'left', 'right']
    on: name of the column used to join the DataFrames.
    return: a merged pandas DataFrame, or None if an error occurs.
    """
    try:
        logging.info('Merging dataframes using {} operation on {} column.'.format(how, on))
        merged_df = pd.merge(data_1, data_2, how=how, on=on)
        return merged_df
    except KeyError as e:
        logging.error("Column {} not found in one of the DataFrames.".format(on))
    except Exception as e:
        logging.error("An error occurred while merging the DataFrames: {}.".format(str(e)))
    return None

def groupby_and_sort(data: pd.DataFrame,
                     groupby_column: str,
                     column: str) -> Union[pd.DataFrame, None]:
    """
    Groupby operation on a specified column, followed by sorting operation.

    data: pandas DataFrame.
    groupby_column: the column on which groupby operation will be performed.
    column: the column on which an average value will be calculated, the values must be numeric.
    return: pandas DataFrame, or None if an error occurs.
    """
    try:
        if pd.api.types.is_numeric_dtype(data[column]):
            logging.info("Performing a GroupBy operation on {} and calculating average on column {}.".format(groupby_column, column))
            average_column_value = data.groupby(groupby_column)[column].mean()
            sorted_df = average_column_value.sort_values(ascending=False)
            return sorted_df
        else:
            raise ValueError("Column '{}' is not numeric.".format(column))
    except KeyError as e:
        logging.error("Column {} not found in DataFrame.".format(column))
    except Exception as e:
        logging.error("An error occurred while performing GroupBy and sorting: {}.".format(str(e)))
    return None

def extract_from_json(genre_list_str: str) -> Union[list, None]:
    """
    Extract movie genres from a JSON-formatted string.

    genre_list_str: A string representing a JSON list containing dictionaries with genre information.
    return: A list of movie genres, or None if an error occurs.
    """
    try:
        logging.info("Extracting genres from JSON string")

        # Replace single quotes with double quotes to ensure JSON compatibility.
        genre_list_str = genre_list_str.replace("'", '"')

        # Load JSON string into a Python list of dictionaries
        genre_list = json.loads(genre_list_str)

        # Extract genre names from dictionaries and return as a list
        return [genre['name'] for genre in genre_list]

    except json.JSONDecodeError as e:
        logging.error("Error decoding JSON string: {}".format(e))
    except KeyError as e:
        logging.error("Key 'name' not found in genre dictionary: {}".format(e))
    except Exception as e:
        logging.error("An error occurred while extracting genres: {}".format(e))
    return None
