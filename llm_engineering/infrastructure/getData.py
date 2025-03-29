from . import cleanData

def get_data():
    file_path = "llm_engineering/infrastructure/data/test_1.txt"
    
    # Read the file contents first
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Clean the actual content
    data = cleanData.clean_wiki_content(content)
    return data




