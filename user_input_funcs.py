
# This function asks the user to provide a choice in query style.
#   general: The user doesn't posess any information about the book to search other than a simple query string (no information is available whether this string is a passage in the book, the author, the genre or the title, etc.) 
#   detailed: The user possesses information about the book (e.g., author, title, category, etc.).
def user_query_choice():
    print("THIS IS THE IRR SIMPLE BOOK SEARCH ENGINE. PLEASE FOLLOW THE INSTRUCTIONS BELOW")
    user_query_choice = input("Do you have information about the book you are looking for (e.g., author, title, category, etc.)? (y/n): ")
    if user_query_choice == "y":
        return "structured"
    elif user_query_choice == "n":
        print("This isn't working yet..")
        return "simple"
    else:
        print("Please type either 'y' or 'n'.")
        return False

def query_structured_params(legal_query_params):
    print("Which of the below information do you possess about the book in question:")
    for param in legal_query_params.items():
        print(f"{param[0]} - {param[1]}")
    user_param_choice = input("Your choice (a/t/p/c): ")

    if user_param_choice not in legal_query_params:
        return False
    
    user_query_text = input("Your query: ")
    user_destination_file = input("Destination file name (incl. absolute path): ")

    return (user_param_choice, user_query_text, user_destination_file)