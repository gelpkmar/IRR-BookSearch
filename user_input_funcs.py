
# This function asks the user to provide a choice in query style.

def query_structured_params(legal_query_params):
    print("THIS IS THE IRR SIMPLE BOOK SEARCH ENGINE. PLEASE FOLLOW THE INSTRUCTIONS BELOW")
    print("Which type of query do you want to execute?")
    for param in legal_query_params.items():
        print(f"{param[0]} - {param[1]}")
    user_param_choice = input("Your choice (a/t/c/s): ")

    if user_param_choice not in legal_query_params:
        return False
    
    user_query_text = input("Your query: ")
    user_destination_file = input("Destination file name (incl. absolute path): ")

    return (user_param_choice, user_query_text, user_destination_file)