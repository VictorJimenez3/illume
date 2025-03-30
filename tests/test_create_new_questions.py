from llm_engineering.models.operations import create_new_questions, create_questions
from llm_engineering.infrastructure import clean_wiki_content

def test_create_new_questions_euler():
    keyword = "Euler's number"
    text = clean_wiki_content("message.txt")
    questions = create_questions(keyword, text)
    split_questions = questions.split("\n\n")
    # for s in split_questions:
    #     print("original question")
    #     print(s)
    #     print("\n\n")
    wrong_questions = split_questions[0] + split_questions[3]

    new_questions = create_new_questions(keyword, text, wrong_questions)
    split_new_questions = new_questions.split("\n\n")
    # for s in split_new_questions:
    #     print("new question")
    #     print(s)
    #     print("\n\n")

    assert (len(split_new_questions) == 4)
    assert (split_new_questions[0].startswith("1."))
    assert (split_new_questions[1].startswith("2."))
    assert (split_new_questions[2].startswith("3."))
    assert (split_new_questions[3].startswith("4."))





def test_create_new_questions_transcendental():
    keyword = "Transcendental"
    text = clean_wiki_content("message.txt")
    questions = create_questions(keyword, text)
    split_questions = questions.split("\n\n")
    # for s in split_questions:
    #     print("original question")
    #     print(s)
    #     print("\n\n")
    wrong_questions = split_questions[0] + split_questions[3]

    new_questions = create_new_questions(keyword, text, wrong_questions)
    split_new_questions = new_questions.split("\n\n")
    # for s in split_new_questions:
    #     print("new question")
    #     print(s)
    #     print("\n\n")

    assert (len(split_new_questions) == 4)
    assert (split_new_questions[0].startswith("1."))
    assert (split_new_questions[1].startswith("2."))
    assert (split_new_questions[2].startswith("3."))
    assert (split_new_questions[3].startswith("4."))
