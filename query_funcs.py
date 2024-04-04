import nltk, csv
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import Counter

# Define a function to preprocess text
def preprocess(text):
    # Tokenize the text
    tokens = word_tokenize(text.lower())

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    # Lemmatize tokens
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]
    return lemmatized_tokens

# Define a function to compute similarity between two texts
def compute_similarity(text1, text2):
    tokens1 = preprocess(text1)
    tokens2 = preprocess(text2)
    # Compute Jaccard similarity
    jaccard_similarity = len(set(tokens1).intersection(tokens2)) / len(set(tokens1).union(tokens2))
    return jaccard_similarity

# Search Pandas Dataframe
def search_df(df_col, user_query, metadata_df):
    results = []
    for index, row in metadata_df.iterrows():
        if type(row[df_col]) != str:
            pass
        else:
            similarity = compute_similarity(user_query, row[df_col])
            results.append((row['gutenberg_id'], row['title'], row['author'], similarity))    # Sort results by similarity in descending order
    results = sorted(results, key=lambda x: x[1], reverse=True)
    return results

# Define a function to search for authors, title and category and rank the results
def search_author(author_query, metadata_df):
    return search_df('author', author_query, metadata_df)

def search_title(title_query, metadata_df):
    return search_df('title', title_query, metadata_df)

def search_category(cat_query, metadata_df):
    return search_df('gutenberg_bookshelf', cat_query, metadata_df)

def export_results(results):
    if len(results) < 1:
        print("Unfortunately your search query doesn't return anything useful.")
        print("Please try another search term.")
    else:
        with open("./query.tsv", 'w', encoding='utf-8') as f:
            # Write header
            f.write("Rank\tBook ID\tTitle\tAuthor\tResult Score\n")
            # Write results
            rank_of_result = 1
            for result in results:
                if result[-1] > 0.25:
                    f.write(f"{rank_of_result}\t{result[0]}\t{result[1]}\t{result[2]}\t{result[3]}\n")
                    rank_of_result += 1

# Query style definitions
def query_structured(location_data_pool, metadata_df, user_query_param):
    # Read the metadata file
    if user_query_param[0] == "a":
        result = search_author(user_query_param[1], metadata_df)
        export_results(result)
    if user_query_param[0] == "t":
        result = search_title(user_query_param[1], metadata_df)
        export_results(result)
    if user_query_param[0] == "c":
        result = search_category(user_query_param[1], metadata_df)
        export_results(result)

def query_simple():
    return 0


