import query_funcs, user_input_funcs
import pandas as pd

LOCATION_INVERTED_INDEX = "/Users/thealteredmg/Desktop/IRR_src/books_preprocessed/inverted_index_medium_large.json"
LOCATION_METADATA_ABS = "/Users/thealteredmg/Desktop/IRR_src/metadata.csv"
LEGAL_QUERY_PARAMS = {"a": "author",
                      "t": "title",
                      "c": "category",
                      "s": "simple full-text search"}
QUERY_FUNCS = {
    "structured": query_funcs.query_structured
}

# Load the CSV file into a Pandas DataFrame
metadata_df = pd.read_csv(LOCATION_METADATA_ABS)

# Get user query choice
user_query_type = user_input_funcs.user_query_choice()
user_query_param = None

if user_query_type == "structured":
    user_query_param = user_input_funcs.query_structured_params(LEGAL_QUERY_PARAMS)
    query_funcs.query_structured(LOCATION_INVERTED_INDEX, metadata_df, user_query_param)
else:
    pass

