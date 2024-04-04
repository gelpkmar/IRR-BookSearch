import query_funcs, user_input_funcs
import pandas as pd

LOCATION_DATA_POOL_ABS = "/Users/thealteredmg/Desktop/IRR_src/books/"
LOCATION_METADATA_ABS = "/Users/thealteredmg/Desktop/IRR_src/metadata.csv"
LEGAL_QUERY_PARAMS = {"a": "author",
                      "t": "title",
                      "p": "text passage",
                      "c": "category"}
QUERY_FUNCS = {
    "simple": query_funcs.query_simple,
    "structured": query_funcs.query_structured
}

# Load the CSV file into a Pandas DataFrame
metadata_df = pd.read_csv(LOCATION_METADATA_ABS)

# Get user query choice
user_query_type = user_input_funcs.user_query_choice()
user_query_param = None

if user_query_type == "structured":
    user_query_param = user_input_funcs.query_structured_params(LEGAL_QUERY_PARAMS)
    query_funcs.query_structured(LOCATION_DATA_POOL_ABS, metadata_df, user_query_param)
else:
    pass

