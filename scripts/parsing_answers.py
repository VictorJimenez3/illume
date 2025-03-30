from llm_engineering.models.operations import create_answers, create_questions, create_word_explanation
from llm_engineering.infrastructure import clean_wiki_content
import json


def test_create_answers_euler():
    keyword = "Euler's number"

    text = clean_wiki_content("message.txt")
    explanation = create_word_explanation(keyword, text)
    questions = create_questions(keyword, explanation)
    answer_text = create_answers(questions)
    
    # Split each answer-explanation pair
    question_parts = questions.split("\n\n")
    answer_parts = answer_text.split("\n\n")  # Assuming answers are separated by blank lines

    return question_parts, answer_parts


def parse_answers(answer_parts: list) -> list:
    parsed_answers = []
    parsed_explanations = []
    for part in answer_parts:
        answer_part, explanation_part = part.split("\nExplanation: ")
        parsed_answers.append(answer_part)
        parsed_explanations.append(explanation_part)
    return parsed_answers, parsed_explanations


def parse_multiple_choice_question(question_text):
    # Split into question and options
    lines = question_text.strip().split('\n')
    
    # Get question (removing the number prefix "2. ")
    question = lines[0].split('. ', 1)[1]
    
    # Get options (removing the leading spaces and "a. ", "b. " etc.)
    options = [line.strip()[3:] for line in lines[1:]]
    
    return {
        'question': question,
        'options': {
            'a': options[0],
            'b': options[1],
            'c': options[2],
            'd': options[3]
        }
    }


if __name__ == "__main__":
    question_parts, answer_parts = test_create_answers_euler()
    parsed_answers, parsed_explanations = parse_answers(answer_parts)
 

    results = []

    for i in range(4):
        print(question_parts[i])
        print(parsed_answers[i])
        print(parsed_explanations[i])

        if i < 2:
            multiple_choice_question = parse_multiple_choice_question(question_parts[i])
                    
            json_data = {
                "questions" : [{
                    "question": multiple_choice_question['question'],
                    "type": "mc",

                    "options": [{
                        "text": multiple_choice_question['options']['a'],
                        "correct": multiple_choice_question['options']['a'] in parsed_answers[i],
                        "explanation": parsed_explanations[i] if multiple_choice_question['options']['a'] in parsed_answers[i] else None
                    },
                    {
                        "text": multiple_choice_question['options']['b'],
                        "correct": multiple_choice_question['options']['b'] in parsed_answers[i],
                        "explanation": parsed_explanations[i] if multiple_choice_question['options']['b'] in parsed_answers[i] else None
                    },
                    {
                        "text": multiple_choice_question['options']['c'],
                        "correct": multiple_choice_question['options']['c'] in parsed_answers[i],
                        "explanation": parsed_explanations[i] if multiple_choice_question['options']['c'] in parsed_answers[i] else None
                    },
                    {
                        "text": multiple_choice_question['options']['d'],
                        "correct": multiple_choice_question['options']['d'] in parsed_answers[i],
                        "explanation": parsed_explanations[i] if multiple_choice_question['options']['d'] in parsed_answers[i] else None
                    }
                    ] # options will be of length one if O-E
                }],

                "questions_raw" : question_parts,
                "answers_raw" : answer_parts
            }
        else:
            
            json_data = {
                "questions" : [{
                    "question": question_parts[i],
                    "type": "oe",

                    "options": [{
                        "text": parsed_answers[i],
                        "correct": True,
                        "explanation": parsed_explanations[i]
                    }] # options will be of length one if O-E
                }],

                "questions_raw" : question_parts,
                "answers_raw" : answer_parts
            }

        results.append(json_data)

    

    with open("answers.json", "w") as f:
        print(json.dumps(results, indent=4))
        json.dump(results, f)


