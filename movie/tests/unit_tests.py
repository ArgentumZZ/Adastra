import pytest
import pandas as pd
from movie.functions.my_functions import get_unique_values

# Execute the test by using "Run" command in PyCharm; or
# pytest .\unit_test.py

# if we use pytest on the terminal
# from my_functions import get_unique_values

# Create a sample DataFrame for testing
@pytest.fixture
def sample_data():

    data = {'A': [10, 10, 30, 40],
            'B': [1, 1, 2, 2]}
    return pd.DataFrame(data)

# Test if the function calculates the number of unique values correctly.
def test_get_unique_values(sample_data):

    # column A has 3 unique values, assert unique_count == 3
    # column B has 2 unique values, assert unique_count == 2

    unique_count = get_unique_values(sample_data, 'A')
    assert unique_count == 3

# Test if the function returns None for a non-existent column.
def test_get_unique_values_nonexistent_column(sample_data):

    # column C doesn't exist in my sample data

    result = get_unique_values(sample_data, 'C')
    assert result is None

