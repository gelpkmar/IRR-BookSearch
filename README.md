# IRR Assignment01 - Book Search Engine

|| |
|-----------|--------------|
|**Author:**| Marlon Gelpke|
|**Matriculation Number:**|15-532-849|
|**Date of Submission:**| 09.04.2024|

The submission to this project contains the following files:
```
.
└── IRR_assignment01_Marlon_Gelpke
    ├── code.zip
    ├── query_results/
    │   ├── query_1.tsv
    │   ├── query_2.tsv
    │   ├── query_2_title.tsv
    │   ├── query_3.tsv
    │   ├── query_4.tsv
    │   ├── query_5.tsv
    │   ├── query_6.tsv
    └── IRR_assignment01_approach.pdf
````

## 1. Introduction
This document describes the approach and setup of the book search engine that was developed in scope of assignment 01 of the University of Zurich Computer Science course "Introduction to Retrieval and Recommendation".

The exact requirements for this task can be accessed for authorized user at the following link: [Exercise 1 Book Search Engine.pdf](https://lms.uzh.ch/auth/1%3A1%3A1122002015%3A2%3A0%3Aserv%3Ax%3A_csrf%3Aa0a3187d-686d-4721-a917-7d3dc4c59e6d/Exercise%201%20Book%20Search%20Engine.pdf).

The following materials were supplied to us:
- A `.zip` file with roughly 70'000 public domain books in `.txt` format.
- A `metadata.csv` file containing metadata on the above-mentioned books, namely (following the column names of the `.csv` file): `gutenberg_id`, `title`, `author`, `gutenberg_author_id`, `language`, `gutenberg_bookshelf`, `rights`, `has_text`.

A search engine should be developed which can receive search queries from a user with a specific information need and return results in a `.tsv` format.
To showcase the search engine functionality, the following search queries should be executed:
1. to be, or not to be
2. English Grammar
3. Philip K Dick
4. Jabberwocky
5. Gutenberg
6. Dornröschen

## 2. Approach
The search engine follows the conceptual view below as presented in IRR-class (example).



![Overview IR-System](data/concept_IR_System.png)

In this document I follow the "Test Collection Approach" as outlines in IRR-class:

1. **Document collection:** The document collection has been provided by the teaching team and consists of the 70'000 `.txt`files.
2. **Information need and Queries:** Have been also provided by the teaching team and consists of the 6 search queries listed above.
3. **Relevance judgement:** Document relevance will be calculated using calculated similary. More on that below.

### 2.1 Conceptual
The below describes the technical approach and outlines the design decisions taken to solve this project.

#### 2.1.1 User Interface and Query Types
The user interface of this search engine is a traditional terminal window application. The user is provided with different types of queries that can be performed (see example output of selecting an author-search below):
```
THIS IS THE IRR SIMPLE BOOK SEARCH ENGINE. PLEASE FOLLOW THE INSTRUCTIONS BELOW
Which type of query do you want to execute?
a - author
t - title
c - category
s - simple full-text search
Your choice (a/t/c/s): a
```

**The different query types:**
Fifferent query types were chosen as querying with the help of descriptive metadata is easy and fast. Lastly, a simple full-text search is still available for general querying.
- **a - author:** The user is looking for a book or books by a specific author and provides the name in text format.
- **t - title:** The user is looking for a book or books with a specific title and provides the title in text format.
- **c - category:** The user is looking for a book or books from a specific genre and provides the genre name in text format.
- **s - simple full-text search:** The user is either looking for a specific text passage in a book or just wants to do a simple full-text query. 

### 2.1.2 Difference in Query Type Execution
The above described query types of this search engine can be best mapped to the two categories as explained in IRR-class as follows:
- **Structured Data Search:** a - author, t - title, c - category
- **Simple Full-Text Search:** s - simple full-text search

The supplied `metadata.csv` file can be used to solve the three Strictured Data Search queries. As the columns of the `.csv` file map to the respective book ID's, queries can be performed reliably and without any prior offline preprocessing.

The Simple Full-Text Search works differently. As we don't know what we are looking for in this case (i.e. does the query refer to an author name, a text section or something else?), we must perform an offline preprocessing step to create an inverse document index (tokens mapped to documents).

### 2.2 Technical Implementation
The technical execution of this project relies heavily on the following third party libraries:
- pandas - reading of the `metadata.csv` file 
- json - writing and reading of the inverse document index
- NLTK - all natural language processing (e.g., tokenization, lemmatization, calculation of similarity, etc.)

The project is spread over four different Python files. A quick overview and explanation of the different files:
- `main.py`: Definition of global variables and main file to import all others.
- `user_input_funcs.py`: Used for function definitions for anything that must be provided by the user through the terminal. E.g., query type and query text.
- `query_funcs.py`: The main file for all query function defintions and supporting functionality, such as preprocessing (i.e. tokenization, lemmatization, etc.), computing of similarity value and result parsing.
- `offline_preprocessing.py`: Script used to run the preprocessing functions to create the inverse document index to facilitate the simple full-text-search.

#### 2.2.1 Query Process
Below the overview of a query process can be seen in a flow diagram. The steps highlighted in orange are explained in more detail beneath the flow diagram incl. important technical design decisions.

![Overview IR-System](data/IRR_Search_UML.png)

1. "Offline preprocessing of book data"
    - The book data collection contains some 70'000 books and is of a size of about 10GB. This is too large to process in memory. Therefore in order to do a free-text search, one must preprocess the data ahead of time.
    - Preprocessing is done with the `offline_preprocessing.py` script by iterating through each of the book files and creating one JSON-file as an inverted document index.
2. "Preprocessing of query text"
    - The query text provided by the user is always preprocessed.
    - Preprocessing includes tokenization, checking for english stop words and, lemmatization through NLTK.
3. "Load inverted document index as JSON object"
    - As the inverted document index of all 70'000 books is still to large to test the free-text search on a normal laptop, ***it was decided, that a document index covering 20'000 books (this is the amount my 16GB RAM laptop could handle) would be sufficient for testing.***
4. "Search inverted document index for matches in query tokens"
    - Relevance of a search result for the free-text search is calculated by dividing the count of occurence of query text tokens by the total query text token count.
    - The most relevant search result will have all query text tokens associated to it in the inverted document index.
5. "Calculate similarity value for each row"
    - The relevance of a search result in the `metadata.csv` is done by caluculating the jaccard similarity between the query text and the text found in the `metadata.csv`.
    - ***For this project it has been chosen that a jaccard similarity of 0.25 is relevant enough to return it as a search result.*** This could be further optimized.

## 3. Example Query Results
Below it is shown how the respective queries (provided by the teaching team) were performed and in which `.tsv` file the result can be found incl. a short description of the findings:

1. to be, or not to be ==> s - simple full-text search (query_1.tsv)
    - This doesn't return any valid results. Aparently Shakespeares Hamlet is not in the 20'000 reversed indexed books. I cannot verify this as my laptop crashes everytime I try to open the large JSON file manually. 
2. English Grammar ==> c - category (query_2.tsv)
    - Category search ("gutenberg_bookshelf" column in `metadata.csv`) doesn't return any results. A manual search with Excel confirms this.
    - Title search ("title" column in `metadata.csv`) returns multiple valid results. This is saved in query_2_title.tsv
3. Philip K Dick ==> a - author (query_3.tsv)
    - Search returns multiple valid results. Max score is only 0.6, this could be optimized.
4. Jabberwocky ==> t - title (query_4.tsv)
    - Search correctly returns the only valid search result. This was verified with manual search in `metadata.csv`.
5. Gutenberg ==> s - simple full-text search (query_5.tsv)
    - The full-text search returns every book in the inverse document index (20'000 books) as all of them have a header stating "Gutenberg".
6. Dornröschen ==> t - title (query_6.tsv)
    - Title search ("title" column in `metadata.csv`) returns no relevant search results. This can be verified with a manual search in `metadata.csv``
    - The full-text search returns 17 relevant search results. This is saved in query_6_full.tsv

Some results to the queries provided by the teaching team may not include any relevant results. This could be due to the fact that the size of the inverted document index had to be limited in order to be able to perform the testing.