from llm_engineering.models.operations import create_questions
from llm_engineering.infrastructure import clean_wiki_content

def test_question_format_euler():
    # Sample test input
    keyword = "Euler's number"
    text = clean_wiki_content("message.txt")
    
    # Get questions
    questions = create_questions(keyword, text)
    split_questions = questions.split("\n\n")
   
    assert (len(split_questions) == 4)
    assert (len(split_questions[0]) > 0)
    assert (len(split_questions[1]) > 0)
    assert (len(split_questions[2]) > 0)
    assert (len(split_questions[3]) > 0)


def test_question_format_transcendental():
    keyword = "Transcendental"
    text = clean_wiki_content("message.txt")
    
    questions = create_questions(keyword, text)
    split_questions = questions.split("\n\n")

    assert (len(split_questions) == 4)
    assert (len(split_questions[0]) > 0)
    assert (len(split_questions[1]) > 0)
    assert (len(split_questions[2]) > 0)
    assert (len(split_questions[3]) > 0)
    
    