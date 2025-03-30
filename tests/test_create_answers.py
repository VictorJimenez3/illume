from llm_engineering.models.operations import create_answers, create_questions, create_word_explanation
from llm_engineering.infrastructure import clean_wiki_content

def test_create_answers_euler():
    keyword = "Euler's number"

    text = clean_wiki_content("message.txt")
    explanation = create_word_explanation(keyword, text)
    questions = create_questions(keyword, explanation)
    answer_text = create_answers(questions)
    
    # Split each answer-explanation pair
    answer_parts = answer_text.split("\n\n")  # Assuming answers are separated by blank lines
    
    for part in answer_parts:
        # Split answer and explanation
        answer_part, explanation_part = part.split("\nExplanation: ")
        
        # Verify format
        assert answer_part.startswith("Answer "), "Answer should start with 'Answer '"
        assert explanation_part.strip(), "Explanation should not be empty"




