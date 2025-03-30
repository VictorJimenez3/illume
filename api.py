from flask import Flask, request, jsonify
from flask_cors import CORS
from llm_engineering.app.actions import PabloAI  #causing errors?

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
    json_output = pablo_ai.makeQuestions(response["keyword"], response["explanation"])
    
    #parse JSON formatted questions and answers
    questions, answers = json_output["questions_raw"], json_output["answers_raw"]
    
    #QUESTIONS FORMATTED STARTS WITH QUESTION, FOLLOWED WITH MC OPTIONS IF EXISTS
    y = [x.strip() for x in questions.split("\n")]
    questions_formatted = []
    current_question_buffer = []
    for sentence in y:
        if not sentence: #double newline
            questions_formatted.append(current_question_buffer)
            current_question_buffer = []
        else:
            current_question_buffer.append(sentence)

    #ANSWERS FORMATTED is [(answer, explanation), ...]
    y = [x.strip() for x in answers.split("\n") if x]
    answers_formatted = []
    for i in range(0, len(y) - 1, 2):
        answers_formatted.append((y[i], y[i + 1])) 
        

    final = {
        "questions" : []
    }

    def isCorrect(choice, answer):
        # Fixed: Add error handling for when ")" isn't found
        choice_pos = choice.find(")")
        answer_pos = answer.find(")")
        
        if choice_pos < 1 or answer_pos < 1:
            return False  # Invalid format
            
        currentChoice = choice[choice_pos - 1]
        answerChoice = answer[answer_pos - 1]
        return currentChoice == answerChoice

    for i, q in enumerate(questions_formatted):
        if not len(q):
            continue

        # Fixed: Create a new question object for each iteration
        question = {}
        question["question"] = q[0]
        question["type"] = "mc" if len(q) > 1 or "true" in q[0].lower() or "false" in q[0].lower() else "oe"

        if question["type"] == "oe":
            question["options"] = [{
                "text": answers_formatted[i][0],
                "correct": True,
                "explanation": answers_formatted[i][1]
            }]
            question["oeActual"] = [*answers_formatted[i]]

        else:
            question["options"] = []
        
        # Fixed: Create a copy instead of a reference
        choices = q[1:]  # Using slicing to create a copy
        for choice in choices:  # all choices if mc
            question["oeActual"] = [*answers_formatted[i]]

            question["options"].append({
                "text": choice,
                "correct": isCorrect(choice, answers_formatted[i][0]),
                "explanation": None if not isCorrect(choice, answers_formatted[i][0]) else answers_formatted[i][1] 
            })

        if not len(question["options"]) and question["type"] == "mc": #t/f 
            question["options"].append({
                "text": "True",
                "correct": "true" in answers_formatted[i][0].lower(),
                "explanation": answers_formatted[i][1] if "true" in answers_formatted[i][0].lower() else None
            })
            question["options"].append({
                "text": "False",
                "correct": "false" in answers_formatted[i][0].lower(),
                "explanation": answers_formatted[i][1] if "false" in answers_formatted[i][0].lower() else None
            })
            question["tfActual"] = [*answers_formatted[i]]
        
        final["questions"].append(question)
    
    final.update(json_output)
    with open("tests/parsing/makeQuestions/input.txt", "w") as f:
        f.write("***json_output***\n" + json.dumps(json_output))

    with open("tests/parsing/makeNewQuestions/output.txt", "w") as f:
        f.write("***FINAL***\n" + json.dumps(final))

    return jsonify(final), 200

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
    
    #parse JSON formatted questions and answers
    questions, answers = json_output["questions_raw"], json_output["answers_raw"]
    
    #QUESTIONS FORMATTED STARTS WITH QUESTION, FOLLOWED WITH MC OPTIONS IF EXISTS
    y = [x.strip() for x in questions.split("\n")]
    questions_formatted = []
    current_question_buffer = []
    for sentence in y:
        if not sentence: #double newline
            questions_formatted.append(current_question_buffer)
            current_question_buffer = []
        else:
            current_question_buffer.append(sentence)

    #ANSWERS FORMATTED is [(answer, explanation), ...]
    y = [x.strip() for x in answers.split("\n") if x]
    answers_formatted = []
    for i in range(0, len(y) - 1, 2):
        answers_formatted.append((y[i], y[i + 1])) 
        

    final = {
        "questions" : []
    }

    def isCorrect(choice, answer):
        # Fixed: Add error handling for when ")" isn't found
        choice_pos = choice.find(")")
        answer_pos = answer.find(")")
        
        if choice_pos < 1 or answer_pos < 1:
            return False  # Invalid format
            
        currentChoice = choice[choice_pos - 1]
        answerChoice = answer[answer_pos - 1]
        return currentChoice == answerChoice

    for i, q in enumerate(questions_formatted):
        if not len(q):
            continue

        # Fixed: Create a new question object for each iteration
        question = {}
        question["question"] = q[0]
        question["type"] = "mc" if len(q) > 1 or "true" in q[0].lower() or "false" in q[0].lower() else "oe"

        if question["type"] == "oe":
            question["options"] = [{
                "text": answers_formatted[i][0],
                "correct": True,
                "explanation": answers_formatted[i][1]
            }]
            question["oeActual"] = [*answers_formatted[i]]

        else:
            question["options"] = []
        
        # Fixed: Create a copy instead of a reference
        choices = q[1:]  # Using slicing to create a copy
        for choice in choices:  # all choices if mc
            question["oeActual"] = [*answers_formatted[i]]

            question["options"].append({
                "text": choice,
                "correct": isCorrect(choice, answers_formatted[i][0]),
                "explanation": None if not isCorrect(choice, answers_formatted[i][0]) else answers_formatted[i][1] 
            })

        if not len(question["options"]) and question["type"] == "mc": #t/f 
            question["options"].append({
                "text": "True",
                "correct": "true" in answers_formatted[i][0].lower(),
                "explanation": answers_formatted[i][1] if "true" in answers_formatted[i][0].lower() else None
            })
            question["options"].append({
                "text": "False",
                "correct": "false" in answers_formatted[i][0].lower(),
                "explanation": answers_formatted[i][1] if "false" in answers_formatted[i][0].lower() else None
            })
            question["tfActual"] = [*answers_formatted[i]]
        
        final["questions"].append(question)
    
    with open("tests/parsing/makeNewQuestions/input.txt", "w") as f:
        f.write("***json_output***\n" + json.dumps(json_output))

    final.update(json_output)
    
    with open("tests/parsing/makeNewQuestions/output.txt", "w") as f:
        f.write("***FINAL***\n" + json.dumps(final))
    
    return jsonify(final), 200

@app.route('/api/youtubeVideoFinder', methods=['POST'])
def youtubeVideoFinder():
    response = request.json()
    topic = response['topic']
    '''
    {
    topic:"whatever the user highlighted"
    }
    '''
    #returns json of {title:"", link:""}
    return youtubeVideoFinder(topic)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)