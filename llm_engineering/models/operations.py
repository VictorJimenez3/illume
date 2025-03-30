from .gemini_client import GeminiClient

# This function creates a detailed explanation of a keyword in the context of the provided article.
def create_word_explanation(keyword: str, text: str) -> str:
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
    Focus on how this word is used and its significance within the article's context. There will be two parts to the explanation. The first paragraph will be a detailed explanation of the word and what it means. Provide a clear, concise paragraph that helps readers understand the word's meaning. You will do this by starting with WHAT THE WORD MEANS in the simplest terms possible and what it is used for, ensure to provide a good depth explanation of the word.
    
    The second paragraph will be an explanation of the word in context referring to the article. This should be a concise paragraph that helps readers understand the word's meaning in the context of the article. The reader should understand how the word plays a role in the article. Do not finish with 'In conclusion' or anything similar. 
    
    Article context:
    {text}

    Formatted Output:
    - Between Paragraph 1 and Paragraph 2, there should be a line break \n 
    - Between Paragraph 1 and Paragraph 2, there should be a line break \n
    - Between Paragraph 1 and Paragraph 2, there should be a line break \n


    Styling: DO NOT USE ANY MARKDOWN OR ANY OTHER FORMATTING. JUST THE PLAIN TEXT.
    NOTICE: DO NOT START WITH 'Here is the explanation for the word' or anything similar.
    """
    
    return client.generate_text(prompt)

# This function creates a list of questions based on the initial summary relevant to the keyword
def create_questions(keyword: str, explanation: str):
    client = GeminiClient()
    prompt = f"""Please provide 4 questions that test a very basic understanding of the keyword '{keyword}'. 
    Use the text provided to create the questions. Ensure that the questions are relevant to the text and specifically test the understanding of the keyword '{keyword}'.

    The questions should be in the following format. Ensure there is a double line break between each question (use \n\n). Finally ONLY RETURN THE QUESTIONS, NO OTHER TEXT. ONLY RETURN THE QUESTIONS:
    1. Multiple choice question
    a. Option 1
    b. Option 2
    c. Option 3
    d. Option 4
    
    2. Multiple choice question
    a. Option 1
    b. Option 2
    c. Option 3
    d. Option 4
    
    3. True or false question
    
    4. Fill in the blank question(Should be a single word or short expression which should be easy to fill in and should be derived from the text)
    
    Styling: DO NOT USE ANY MARKDOWN OR ANY OTHER FORMATTING. JUST THE PLAIN TEXT.

    Explanation: {explanation}"""

    return client.generate_text(prompt)

# This function creates a list of answers to the questions
def create_answers(questions):
    client = GeminiClient()
    prompt = f"""Please provide the answers to the following questions: {questions}
    
    Ensure that the answers are correct and relevant to the questions.
    Ensure that the answers are concise and to the point.
    Ensure that the answers are in the same order as the questions.
    Explain the answer in a way that is easy to understand. Ensure you add why the answer is correct. Short and concise.
    The expalantions should be easy to understand. The explanation should add A LOT of value to the user.s
    

    Output:
    - DO NOT START WITH 'Here are the answers to the questions' or anything similar.
    - After each answer, there should be a double line break (use \n\n)
    - Follow the examples below to format the answers. Follow them EXACTLY. NO EXCEPTIONS. NO ADDITIONAL TEXT.
    - DO NOT RESTATE THE QUESTION, JUST THE ANSWER.

    Example:
    Question 1: What is the capital of France? ( DO NOT RESTATE THE QUESTION, JUST THE ANSWER)
    Answer 1: Paris
    Explanation: Paris became the capital of France because of its strategic location on the Seine, early political importance under the Capetians, central role in French governance, and lasting influence as a cultural and intellectual center.
 
        
    Question 2: What is the slope? ( DO NOT RESTATE THE QUESTION, JUST THE ANSWER)
    Answer 2: The slope is the rise over run.
    Explanation: The slope is a measure of a line's steepness, calculated as the change in y divided by the change in x between two points, indicating whether the line rises, falls, stays flat, or is vertical.

    
    Styling: DO NOT USE ANY MARKDOWN OR ANY OTHER FORMATTING. JUST THE PLAIN TEXT.
    """
    return client.generate_text(prompt)

# This function creates new questions based on the wrong questions
def create_new_questions(wrong_questions: str, keyword: str, text: str):
    client = GeminiClient()
    prompt = f"""Please provide 4 questions that test a very basic understanding of the keyword '{keyword}'. 
    Use the questions that were wrong to create the new questions. The focus should be on the questions that were wrong, with the aim of reinforcing the understanding of the keyword '{keyword}' in the context of the text but more importantly the questions should be different from the questions that were wrong.
    The questions should be relevant to the text and specifically test the understanding of the keyword '{keyword}'.
    The questions should be different, but focused on reinforcing the understanding of the keyword '{keyword}' from the following questions: {wrong_questions}
    The questions should be relevant to the text.

    The questions should be in the following format:
    
    1. Multiple choice question
        a. Option 1
        b. Option 2
        c. Option 3
        d. Option 4
    2. Multiple choice question
        a. Option 1
        b. Option 2
        c. Option 3
        d. Option 4
    3. True or false question
    4. Fill in the blank question(Should be a single word or short expression which should be easy to fill in and should be derived from the text, no symbols or special characters)

    Styling: DO NOT USE ANY MARKDOWN OR ANY OTHER FORMATTING. JUST THE PLAIN TEXT.

    Text: {text}
    """
    return client.generate_text(prompt)

# This function creates a small explanation of the keyword in the context of the questions and answers.
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



