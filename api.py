from flask import Flask, request, jsonify
from flask_cors import CORS

from llm_engineering.app.actions import PabloAI  #causing errors?
from youtube import youtubeSearch

from pprint import pprint
import json

app = Flask(__name__)
CORS(app)

pablo_ai = PabloAI()

"""
Calls should procede as:

1) Init Summary
2) Init Questions
3) make new questions
4) make summary additions
5) repeat 3-5 again until user stops
"""

@app.route('/api/makeSummary', methods=['POST']) #DONE
def makeSummary():
    """
    Init summary, should be called first for creating first quiz
    """
    response = request.json
    
    try:
        assert("keyword" in response and "data" in response)
    except:
        return jsonify({"status" : "failure, incorrect parameters for endpoint"}), 500

    '''
    body: { 
        "keyword": highlighted phrase,
        "data": entire text from dom body
    }
    '''

    json_output = pablo_ai.makeSummary(response["keyword"], response["data"])
    json_output.update({"status" : "success"})

    with open("tests/parsing/makeSummary/output.txt", "w") as f:
        f.write("***json_output***\n" + json.dumps(json_output))
        
    return jsonify(json_output), 200

@app.route('/api/makeQuestions', methods=['POST']) #DONE 
def makeQuestions():
    """
    Creates initial questions for quiz, init summary must be called prior 
    and included within body

    {
        questions : [{
            question: "how are you?",
            type: mc / oe

            options: [{
                text: "option 1",
                correct: true / false
                explanation: "explanation for 1" / NULL
            }] # options will be of length one if O-E
        }]

        questions_raw : "",

        answers_raw : ""
    }
    """
    response = request.json

    try:
        assert("keyword" in response and "explanation" in response)
    except:
        return jsonify({"status" : "failure, incorrect parameters for endpoint"}), 500

    '''
    body: { 
        "keyword" : #the specific topic of discussion / hightlighted terms,
        "explanation" : #current summary of topic called from other API endpoint
    }
    '''
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

    json_output = pablo_ai.makeQuestions(response["keyword"], response["explanation"])
    
    question_parts, answer_parts = json_output["questions_raw"], json_output["answers_raw"]

    parsed_answers, parsed_explanations = parse_answers(answer_parts)

    json_data = {
        "questions" : [],
        "questions_raw" : question_parts,
        "answers_raw" : answer_parts
    }

    assert(min(len(question_parts), len(answer_parts)) == 4)
    for i in range(min(len(question_parts), len(answer_parts))):
        # print(question_parts[i])
        # print(parsed_answers[i])
        # print(parsed_explanations[i])

        if i < 2:
            multiple_choice_question = parse_multiple_choice_question(question_parts[i])
                    
            json_data["questions"].append({
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
                })

            
        else:
            json_data["questions"].append({
                    "question": question_parts[i],
                    "type": "oe",

                    "options": [{
                        "text": parsed_answers[i],
                        "correct": True,
                        "explanation": parsed_explanations[i]
                    }] # options will be of length one if O-E
            })

    # print("FLAG", type(json_data), len(json_data))
    # pprint(json_data)
    return jsonify(json_data), 200

@app.route ('/api/makeSummaryAdjustment', methods=['POST']) #DONE
def makeSummaryAdjustment():
    """
    will create summary ADDITIONS (not rephrase) summaries.
    Must be passed the new questions and answers from the makeNewQuestions endpoint call,
    Can be passed parsed and formatted or jsonified and parsed on this side, TODO define implementation
    """
    response = request.json
    
    try:
        assert("keyword" in response and "new_questions" in response and "new_answers" in response)
    except:
        return jsonify({"status" : "failure, incorrect parameters for endpoint"}), 500

    '''
    body: { 
        "keyword" : #the specific topic of discussion / hightlighted terms,
        "new_questions" : questions_raw from original call
        "new_answers" : answers_raw from original call
    }
    '''

    json_output = pablo_ai.makeSummaryAdjustment(response["keyword"], response["new_questions"], response["new_answers"])
    json_output.update({"status" : "success"})

    with open("tests/parsing/makeSummaryAdjustment/in-out-put.txt", "w") as f:
        f.write("***json_output***\n" + json.dumps(json_output))

    return jsonify(json_output), 200

@app.route('/api/makeNewQuestions', methods=['POST']) #DONE
def makeNewQuestions():
    """
    {
        questions : [{
            question: "how are you?",
            type: mc / oe

            options: [{
                text: "option 1",
                correct: true / false
                explanation: "explanation for 1" / NULL
            }] # options will be of length one if O-E
        }]

        questions_raw : "",

        answers_raw : ""
    }
    """
    response = request.json
    
    print("response")
    pprint(response)

    try:
        assert("keyword" in response and "data" in response and "wrong_questions" in response)
    except:
        return jsonify({"status" : "failure, incorrect parameters for endpoint"}), 500

    '''
    body: { 
        "keyword" : #the specific topic of discussion / hightlighted terms,
        "data" : str,
        "wrong_questions": ["", ""]
    }
    '''
    json_output = pablo_ai.makeNewQuestions(response["keyword"], response["data"], response["wrong_questions"])
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
    
    question_parts, answer_parts = json_output["questions_raw"], json_output["answers_raw"]
    # try:
    parsed_answers, parsed_explanations = parse_answers(answer_parts)
    # except:
    #     print(answer_parts)

    json_data = {
        "questions" : [],
        "questions_raw" : question_parts,
        "answers_raw" : answer_parts
    }

    assert(min(len(question_parts), len(answer_parts)) == 4)
    for i in range(min(len(question_parts), len(answer_parts))):
        # print(question_parts[i])
        # print(parsed_answers[i])
        # print(parsed_explanations[i])

        if i < 2:
            multiple_choice_question = parse_multiple_choice_question(question_parts[i])
                    
            json_data["questions"].append({
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
                })
        # elif "true" in question_parts[i].lower() or "false" in question_parts[i].lower():
        #     json_data["questions"].append({
        #             "question": multiple_choice_question['question'],
        #             "type": "mc",

        #             "options": [{
        #                 "text": True,
        #                 "correct": multiple_choice_question['options']['a'] in parsed_answers[i],
        #                 "explanation": parsed_explanations[i] if multiple_choice_question['options']['a'] in parsed_answers[i] else None
        #             },
        #             {
        #                 "text": False,
        #                 "correct": multiple_choice_question['options']['b'] in parsed_answers[i],
        #                 "explanation": parsed_explanations[i] if multiple_choice_question['options']['b'] in parsed_answers[i] else None
        #             },
        #             ] # options will be of length one if O-E
        #         })
        
        else:
            json_data["questions"].append({
                    "question": question_parts[i],
                    "type": "oe",

                    "options": [{
                        "text": parsed_answers[i],
                        "correct": True,
                        "explanation": parsed_explanations[i]
                    }] # options will be of length one if O-E
            })

    return jsonify(json_data), 200
        
        
@app.route('/api/youtubeVideoFinder', methods=['POST'])
def youtubeVideoFinder():
    response = request.json

    try:
        assert("topic" in response)
    except:
        return jsonify({"status" : "Incorrect parameters, missing topic!"}), 500

    topic = response['topic']
    '''
    {
    topic:"whatever the user highlighted"
    } 34.139.24.227:5000
    '''
    
    return {
        "media_link" : youtubeSearch(topic),
        "status" : "success"
    }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)