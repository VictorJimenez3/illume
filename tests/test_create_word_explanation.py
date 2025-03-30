from llm_engineering.models.operations import create_word_explanation, create_questions
from llm_engineering.infrastructure import clean_wiki_content

def test_create_word_explanation_euler():
    keyword = "Euler's number"
    text = clean_wiki_content("message.txt")

    explanation = create_word_explanation(keyword, text)
    split_explanation = explanation.split("\n")
    print(split_explanation)
    assert (len(split_explanation) == 4)

def test_create_word_explanation_transcendental():
    keyword = "Transcendental"
    text = clean_wiki_content("message.txt")
    
    explanation = create_word_explanation(keyword, text)
    split_explanation = explanation.split("\n")
    print(split_explanation)
    assert (len(split_explanation) == 4)



def test_create_questions_euler():
    keyword = "Euler's number"
    text = clean_wiki_content("message.txt")
    
    questions = create_questions(keyword, text)
    split_questions = questions.split("\n")
    print(split_questions)