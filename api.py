from flask import Flask, request, jsonify
from flask_cors import CORS
from llm_engineering.app.actions import PabloAI  #causing errors?

import json

app = Flask(__name__)
CORS(app)

#  placeholder functions to abstract
grab_init_summary = lambda x, y: [None,] 
grab_init_questions = lambda x, y: [None,]
grab_init_recursive_question = lambda : [None,]
grab_init_recursive_summary = lambda : [None,]

# temporary pablo ai call, implement custom dictionary to have multiple users after 
# I finish the basic data pipelines
pablo_ai = PabloAI()
# .start() makes initial question
#.runQuiz() is the recursive quiz
#matt needs to give the questions in order

#keyword it the topic
#summary 
#wrong answer
#data is dom body
#

# @app.route('/')
# def homepage():
#     return '<h1>hello</h1>'

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
    #confirm with pablo what this function returns. 
    json_output = pablo_ai.makeSummary(response["keyword"], response["data"])
    json_output.update({"status" : "success"})
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
    with open("tests/q1.txt", "w") as f:
        y = [x.strip() for x in questions.split("\n")]
        questions_formatted = []
        current_question_buffer = []
        for sentence in y:
            if not sentence: #double newline
                questions_formatted.append(current_question_buffer)
                current_question_buffer = []
            else:
                current_question_buffer.append(sentence)
        #QUESTIONS FORMATTED STARTS WITH QUESTION, FOLLOWED WITH MC OPTIONS IF EXISTS
        print(questions_formatted)
        f.write(json.dumps(questions_formatted))

    with open("tests/a1.txt", "w") as f:
        y = [x.strip() for x in answers.split("\n") if x]
        answers_formatted = []
        for i in range(len(y) - 1):
            answers_formatted.append((y[i], y[i + 1])) 
        
        #ANSWERS FORMATTED is [(answer, explanation), ...]
        f.write(json.dumps(answers_formatted))

    # final = {
    #     "questions" : [
    #         x for x in question_bodies
    #     ]
    # }
    
    return jsonify(json_output), 200
           

@app.route ('/api/makeSummaryAdjustment', methods=['POST']) #DONE
def makeSummaryAdjustment():
    """
    will create summary ADDITIONS (not rephrase) summaries.
    Must be passed the new questions and answers from the makeNewQuestions endpoint call,
    Can be passed parsed and formatted or jsonified and parsed on this side, TODO define implementation
    """
    response = request.json
    
    try:
        assert("keyword" in response and "explanation" in response)
    except:
        return jsonify({"status" : "failure, incorrect parameters for endpoint"}), 500

    '''
    body: { 
        "keyword" : #the specific topic of discussion / hightlighted terms,
        "new_questions" : questions (ambiguous type TODO communicate with Matt to format to string)
        "new_answers" : questions (ambiguous type TODO communicate with Matt to format to string)
    }
    '''

    json_output = pablo_ai.makeSummaryAdjustment(response["keyword"], response["new_questions"], response["new_answers"])
    json_output.update({"status" : "success"})

    return jsonify(json_output), 200

@app.route('/api/makeNewQuestions', methods=['POST']) #DONE
def makeNewQuestions():
    response = request.json
    
    try:
        assert("keyword" in response and "data" in response and "wrong_questions" in response)
    except:
        return jsonify({"status" : "failure, incorrect parameters for endpoint"}), 500


    ''' 
    body: {
        "keyword" : #the specific topic of discussion / hightlighted terms,
        "data": #entire text from dom body,
        "wrong_questions" : "list or ideally text of the incorrect questions ONLY"
    }
    '''
    #confirm with pablo what this function returns. Might need to reformat
    json_output = pablo_ai.makeSum(response["keyword"], response["data"], response["wrong_questions"])
    json_output.update({"status" : "success"})
    return jsonify(json_output), 200

pablo_ai = PabloAI()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)