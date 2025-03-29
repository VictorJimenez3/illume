from .gemini_client import GeminiClient


# This function creates an initial summary of the specific keyword in context of the data
def create_initial_summary(data):
    client = GeminiClient()
    prompt = f"Please provide a summary of the following data: {data}"
    return client.generate_text(prompt)


# This function creates a list of questions based on the initial summary relevant to the keyword
def create_questions(keyword: str, text: str):
    client = GeminiClient()
    prompt = f"""Please provide 4 questions that test a very basic understanding of the keyword '{keyword}'. 
    Use the text provided to create the questions. Ensure that the questions are relevant to the text and specifically test the understanding of the keyword '{keyword}'.

    The questions should be in the following format:
    1. Multiple choice question
    2. Multiple choice question
    3. True or false question
    4. Fill in the blank question(Should be a single word or short expression which should be easy to fill in and should be derived from the text)
    
    Styling: DO NOT USE ANY MARKDOWN OR ANY OTHER FORMATTING. JUST THE PLAIN TEXT.

    Text: {text}"""

    return client.generate_text(prompt)


# This function creates a list of answers to the questions
def create_answers(questions):
    client = GeminiClient()
    prompt = f"""Please provide the answers to the following questions: {questions}
    
    Ensure that the answers are correct and relevant to the questions.
    Ensure that the answers are concise and to the point.
    Ensure that the answers are in the same order as the questions.

    Output:
    - DO NOT START WITH 'Here are the answers to the questions' or anything similar.
    - DO NOT START WITH 'Here are the answers to the questions' or anything similar.
    - DO NOT START WITH 'Here are the answers to the questions' or anything similar.

    Example:
    Question 1: What is the capital of France?
    Answer 1: Paris
    Explanation:
    Explain the answer in a way that is easy to understand. Ensure you add why the answer is correct. Short and concise.

    Question 2: What is the slope?
    Answer 2: The slope is the rise over run.
    Explanation:
    Explain the answer in a way that is easy to understand. Ensure you add why the answer is correct. Short and concise.
    
    Styling: DO NOT USE ANY MARKDOWN OR ANY OTHER FORMATTING. JUST THE PLAIN TEXT.
    """
    return client.generate_text(prompt)


def create_new_questions(wrong_questions: str, keyword: str, text: str):
    client = GeminiClient()
    prompt = f"""Please provide 4 questions that test a very basic understanding of the keyword '{keyword}'. 
    Use the questions that were wrong to create the new questions. The focus should be on the questions that were wrong, with the aim of reinforcing the understanding of the keyword '{keyword}' in the context of the text but more importantly the questions should be different from the questions that were wrong.
    The questions should be relevant to the text and specifically test the understanding of the keyword '{keyword}'.
    The questions should be different, but focused on reinforcing the understanding of the keyword '{keyword}' from the following questions: {wrong_questions}
    The questions should be relevant to the text.

    The questions should be in the following format:
    
    1. Multiple choice question
    2. Multiple choice question
    3. True or false question
    4. Fill in the blank question(Should be a single word or short expression which should be easy to fill in and should be derived from the text, no symbols or special characters)

    Styling: DO NOT USE ANY MARKDOWN OR ANY OTHER FORMATTING. JUST THE PLAIN TEXT.

    Text: {text}
    """
    return client.generate_text(prompt)


def create_word_explanation(keyword: str, data: str) -> str:
    """
    Creates a detailed explanation of a keyword in the context of the provided article.
    
    Args:
        keyword (str): The word to explain
        data (str): The full article context
        
    Returns:
        str: A detailed explanation of the keyword in context
    """
    client = GeminiClient()
    prompt = f"""Please provide a detailed explanation of the word '{keyword}' in the context of the following article. 
    Focus on how this word is used and its significance within the article's context. 
    Provide a clear, concise paragraph that helps readers understand the word's meaning and importance in this specific context. You will do this by starting with WHAT THE WORD MEANS in the simplest terms possible and what it is used for, ensure to provdide a good defpth explanation of the word. Afterwards finish the explanation by providing an explanation of the word in context referringto the article. Ensure that there is a clear transition between the two parts. Do not finish with 'In conclusion' or anything similar.
    
    Article context:
    {data}


    Output:
    - DO NOT START WITH 'Here is the explanation for the word' or anything similar.
    - DO NOT START WITH 'Here is the explanation for the word' or anything similar.
    - DO NOT START WITH 'Here is the explanation for the word' or anything similar.
    - DO NOT START WITH 'Here is the explanation for the word' or anything similar.
    - DO NOT START WITH 'Here is the explanation for the word' or anything similar.
    - DO NOT START WITH 'Here is the explanation for the word' or anything similar.

    Styling: DO NOT USE ANY MARKDOWN OR ANY OTHER FORMATTING. JUST THE PLAIN TEXT.

    """
    
    return client.generate_text(prompt)


def create_summary_adjustment(keyword: str, new_questions: str, new_answers: str) -> str:
    client = GeminiClient()
    prompt = f"""
    Please create a small explanation of the keyword '{keyword}' in the context of the following questions and answers.
    The new questions are: {new_questions}
    The new answers are: {new_answers}
    The keyword is: {keyword}

    Ensure that the explanation is concise and to the point. The explanation should allow the user to understand the keyword '{keyword}' in the context of the questions and answers.
    
    Styling: DO NOT USE ANY MARKDOWN OR ANY OTHER FORMATTING. JUST THE PLAIN TEXT.

    """
    return client.generate_text(prompt)



