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
            # if row['gutenberg_id'] == 15202:
            #     print(row['title'].replace('\\n',' '))
            results.append((row['gutenberg_id'], row['title'].replace('\n', ''), row['author'], similarity))
    results = sorted(results, key=lambda x: x[3], reverse=True) # Sort results by similarity in descending order
    return results

# Define a function to search for authors, title and category and rank the results
def search_author(author_query, metadata_df):
    return search_df('author', author_query, metadata_df)

def search_title(title_query, metadata_df):
    return search_df('title', title_query, metadata_df)

def search_category(cat_query, metadata_df):
    return search_df('gutenberg_bookshelf', cat_query, metadata_df)

def export_results(results, destination_path):
    if len(results) < 1:
        print("Unfortunately your search query doesn't return anything useful.")
        print("Please try another search term.")
    else:
        with open(destination_path, 'w', encoding='utf-8') as f:
            # Write header
            f.write("Rank\tBook ID\tTitle\tAuthor\tResult Score\n")
            # Write results
            rank_of_result = 1
            for result in results:
                if result[-1] > 0.1:
                    # if result[0] == 15202:
                    #     print(result[1].replace('\n', ''))
                    #     print(result[2])
                    #     print(result[3])
                    title = result[1].replace('\n', '')
                    f.write(f"{rank_of_result}\t{result[0]}\t{title}\t{result[2]}\t{result[3]:.2f}\n")
                    rank_of_result += 1
                    # fields = [str(field).strip() for field in result]
                    # f.write('\t'.join(fields) + '\n')

        print(f"Results have been exported to {destination_path}")

# Query style definitions
def query_structured(location_data_pool, metadata_df, user_query_param):
    # Read the metadata file
    if user_query_param[0] == "a":
        result = search_author(user_query_param[1], metadata_df)
        export_results(result, user_query_param[2])
    if user_query_param[0] == "t":
        result = search_title(user_query_param[1], metadata_df)
        export_results(result, user_query_param[2])
    if user_query_param[0] == "c":
        result = search_category(user_query_param[1], metadata_df)
        export_results(result, user_query_param[2])

def query_simple():
    return 0


