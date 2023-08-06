# BloomTechLib
BloomTech Labs Python Library of General Data Science Solutions


## BloomTechLib Developer Guidelines
1. No PEP8 violations.
2. No global state.
3. Must be backwards compatible to 3.6.x
4. Must be forward compatible up to the latest version of Python 3.9.x
5. Should avoid dependencies outside the standard library.
6. Every feature will be documented in detail.
7. Code examples will be included for each feature.


## Analysis

### CSV Similarity Score
Compares two csv files and returns a score between 0.0 and 1.0 to indicate how 
similar the data is. 

#### Assumptions
- The data files have the same header, delimiter and number of rows.
- Each row of data should be a unique observation, each column representing a single aspect.
- CSV is a convenient format, but a database adapter could be useful in the future.
- Data will be primitive strings or numbers and not more complex types.


## DataBase Ops

### DataModelMongo Class
- `find(dict) -> dict`
- `insert(dict)`
- `find_many(dict, int) -> Iterator[dict]`
- `insert_many(dict)`
- `get_df() -> DataFrame`

### DataModelSQL Class
- `db_action(str)`
- `db_query(str) -> list`

#### HTML to DataFrame
- `html_to_df(str, int) -> DataFrame`

## DevOps API
- WIP
