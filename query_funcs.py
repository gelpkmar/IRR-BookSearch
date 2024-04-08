import ijson, json
from tqdm import tqdm
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import Counter

# Initialize NLTK components
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

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
    for index, row in tqdm(metadata_df.iterrows()):
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

# Define function for text search in books

def search_text(text_query, location_inverted_index):
    # Function to load inverted index from a JSON file
    with open(location_inverted_index, 'r') as f:
        inverted_index = json.load(f)

        query_tokens = []
        
        for token in text_query.split():
            if token not in stop_words and len(token) > 1:
                processed_token = lemmatizer.lemmatize(token)
                query_tokens.append(processed_token.lower())

        relevant_documents = {}
        
        for token in query_tokens:
            if token in inverted_index:
                for doc in tqdm(inverted_index[token]):
                    if doc in relevant_documents:
                        relevant_documents[doc] += 1
                    else:
                        relevant_documents[doc] = 1
        
        # Calculate relevance score for each document
        total_query_tokens = len(query_tokens)
        for doc, count in relevant_documents.items():
            relevant_documents[doc] = count / total_query_tokens

        results = sorted([(document[0], "_", "_", document[1]) for document in relevant_documents.items()], key=lambda x: x[3], reverse=True)

        return results

# Define function for export of results to .tsv

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
                    title = result[1].replace('\n', '')
                    f.write(f"{rank_of_result}\t{result[0]}\t{title}\t{result[2]}\t{result[3]:.2f}\n")
                    rank_of_result += 1

        print(f"Results have been exported to {destination_path}")

# Query style definitions
def query_structured(location_inverted_index, metadata_df, user_query_param):
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
    if user_query_param[0] == "s":
        result = search_text(user_query_param[1], location_inverted_index)
        export_results(result, user_query_param[2])
