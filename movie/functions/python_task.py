# import libraries
from my_functions import *

# 1. Load the dataset from a CSV file.

# Remove the restriction on the number of displayed columns
pd.options.display.max_columns = None

# Load the dataset
df = read_my_data(filepath="C:/Users/Mihail/Downloads/archive/movies_metadata.csv", low_memory=False)

# The shape is (number of rows, number of columns)
print(df.shape)

# General info about the dataset
print(df.info())

# Explore the first 5 rows
print(df.head())

# Column "id" contains dates that have to be removed
df = df[~df['id'].str.contains(r'\d{4}-\d{2}-\d{2}', na=False)]

# Here, column "id" is actually "tmdbId", so we rename it
df.rename(columns={'id': 'tmdbId'}, inplace=True)

# fix the data type of the column "tmdbId"
df["tmdbId"] = df["tmdbId"].astype('int64')

# reset the index
df = df.reset_index(drop=True)

# Won't use the other columns, so we'll build a smaller dataset
df_movies = df[ ['tmdbId', 'title', 'genres', 'release_date'] ]
print(df_movies.head(5))

# General info about the smaller dataset
print(df_movies.info())

# check for missing values
print(df_movies.isnull().sum())

# drop the rows with missing values
df_movies = df_movies.dropna(axis=0)

# check again
print(df_movies.isnull().sum())

# check again
print(df_movies.info())

# 2. Print the number of the unique movies in the dataset.
print("The number of unique movies is:", df_movies['title'].nunique())
print("The number of unique movies is:", get_unique_values(df_movies, 'title'))

 # 3. Print the average rating of all the movies.
# Load the ratings dataset
df_ratings = read_my_data("C:/Users/Mihail/Downloads/archive/ratings_small.csv", low_memory=False)
df_ratings.head(5)

# rows, columns
print(df_ratings.shape)

# general info
print(df_ratings.info())

# check for missing values
print(df_ratings.isnull().sum())

# calculate the average rating
average_rating = np.mean(df_ratings['rating'])
print("The average ratings of all movies is:", round(average_rating, 2))

# using the function to calculate the average
calculate_average_value(df_ratings, 'rating')

# 4. Print the top 5 highest rated movies.

# Load the small "links" dataset.
df_links = read_my_data("C:/Users/Mihail/Downloads/archive/links_small.csv", low_memory=False)
print(df_links.head())

# numbers of rows and columns
print(df_links.shape)

# general info
print(df_links.info())

# check for missing values
print(df_links.isnull().sum())

# drop the missing values
df_links = df_links.dropna(axis=0)

# check again
print(df_links.isna().sum())

# fix the data type of the column "tmdbId"
df_links['tmdbId'] = df_links["tmdbId"].astype('int64')

# reset the index
df_links = df_links.reset_index(drop=True)

# Inner SQL Join
merged_df = merge_two_dataframes(df_ratings, df_links, how='inner', on='movieId')

print(merged_df.shape)

print(merged_df.info())

# another SQL inner join with pandas
df_rated_movies = merge_two_dataframes(merged_df, df_movies, how='inner', on='tmdbId')

print(df_rated_movies.shape)

print(df_rated_movies.head())

print(df_rated_movies.info())

print(df_rated_movies.isnull().sum())

# group by 'title' and sort by average 'rating'
sorted_df_ratings = groupby_and_sort(df_rated_movies, 'title', 'rating')

print(sorted_df_ratings.head())

# 5. Print the number of movies released each year.

# Extract the year and assign it to the same column
df_rated_movies['release_date'] = (pd.to_datetime(df_rated_movies['release_date'])).dt.year

print(df_rated_movies.shape)

print(df_rated_movies.info())

print(df_rated_movies.head(3))


# group by 'release_date' and count 'title'
average_ratings = df_rated_movies.groupby('release_date')['title'].count()

print(average_ratings.sort_values(ascending=False))


# 6. Print the number of movies in each genre.

# Apply the function 'extract_genre_names' to 'genres' column 
df_rated_movies['genre_names'] = df_rated_movies['genres'].apply(extract_from_json)

# Explode the list of genre names to create multiple rows for each movie
# Transform each element of a list-like to a row, replicating index values.
df_exploded = df_rated_movies.explode('genre_names')

print(df_exploded.head(5))

# Movie genres: Counts
genre_counts = df_exploded.groupby('genre_names')["movieId"].count()
print(genre_counts)


# 7. Save the dataset to a JSON file.

df_exploded.reset_index(inplace=True, drop=False)
df_exploded.head()

my_path = 'C:/Users/Mihail/Downloads/archive/dataset_exploded.json'
df_exploded.to_json(my_path, orient='index')

# 8. Upload the code in public GIT repository

# Uploaded it to my public git repository - https://github.com/ArgentumZZ 

# 9. Provide setup.py or pyproject.toml
# 
#     movie/
#     │    
#     ├── __init__.py
#     ├── setup.py
#     ├── movie/
#     │   ├── __init__.py
#     │   ├── functions.py
#     │   └── data_analysis.py
#     │
#     └── tests/
#         ├── __init__.py
#         └── unittests.py




