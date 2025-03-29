from flask import Flask, request, jsonify
from flask_cors import CORS
from llm_engineering.app.actions import PabloAI  #causing errors?
#likely the poetry as he mentioned earlier, ask futurther

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

@app.route('/')
def homepage():
    return '<h1>hello</h1>'
           
@app.route('/api/new_questions',methods=['POST'])
def new_questions():
    incoming_data = request.json
    '''
    incoming_data = 
    { 
    "keyword": "",
    "summary": "",
    "wrong_a": ""    
    }
    '''
    #confirm with pablo what this function returns. 
    return pablo_ai.makeNewQ(incoming_data["keywords"], incoming_data["summary"], incoming_data["wrong_a"])

@app.route ('/api/make_summary', methods=['POST'])
def make_summary():
    incoming_data = request.json
    '''
    incoming_data = 
    { 
    "keyword": "",
    "summary": "",
    "wrong_a": ""    
    }
    '''
    #confirm with pablo what this function returns. 
    return pablo_ai.makeSummary(incoming_data["keywords"], incoming_data["summary"], incoming_data["wrong_a"])

@app.route('/api/make_summary', methods=['POST'])
def make_summary():
    incoming_data = request.json
    '''
    {
    "keywords":"",
    "data":""
    }
    '''
    #confirm with pablo what this function returns. Might need to reformat
    return pablo_ai.makeSum(incoming_data["keywords"], incoming_data["data"])

@app.rout('/api/make_questions', methods=['POST'])
def make_questios():
    incoming_data = request.json
    '''
    { 
    "keyword": "",
    "summary": "",
    "wrong_a": ""    
    }
    '''
    
    return pablo_ai.makeQ(incoming_data["keywords"], incoming_data["summary"], incoming_data["wrong_a"])


# when you make for multiple users fix this implementation for 
# Pablo AI
pablo_ai = PabloAI()

'''
@app.route('/initial_summary', methods=['POST'])
def initial_summary():
    # chrome extension needs: summary
    # we need context (dom body) and topic
    
    response = request.json # type is dict, stuff from chrome extension scope 
    
    try:    
        assert(document_text in response and topic in response)
    except Exception as e:
        print(e)
        return jsonify({"status" : "FAILED, please attatch correct parameters"}), 500
    
    summary = grab_init_summary(response.get(document_text, ""), response.get(topic, ""))
    
    return jsonify({
        "summary" : summary,
        "status" : "clear"
    }), 200 

@app.route("/initial_questions", methods=['POST'])
def initial_questions():
    response = request.json

    try:
        assert(document_text in response and topic in response)
    except:
        return jsonify({"status" : "FAILED, please attatch correct parameters"}), 500
    
    questions = grab_init_questions(response.get(document_text, ""), response.get(topic, ""))
    return questions
 # no longer needed
#gets topic and document_text, use it for pablo get request later
@app.route('/base_data', methods=['POST'])
def base_data():
    # DOM and TOPIC OF PAGE
    response = request.json
    try:    
        assert(document_text in response and topic in response)
    except Exception as e:
        return jsonify({"status" : "FAILED, please attatch correct parameters"}), 500
    return response

@app.route("/start", methods=['POST'])
def start_quiz():
    response = request.json
    try:    
        assert(document_text in response and topic in response)
    except Exception as e:
        return jsonify({"status": "FAILED, please attach correct parameters"}), 500
    
    # Call start function from llm_engineering
    result = pablo_ai.start(response["document_text"], response["topic"])
    return jsonify(result), 200

@app.route("/wrong_question", methods=['POST'])
def handle_wrong_question():
    # Dom and Topic
    response = request.json
    try:
        assert(document_text in response and topic in response)
    except Exception as e:
        return jsonify({"status": "FAILED, please attach correct parameters"}), 500
    
    # Call runQuiz with the wrong question data
    result = pablo_ai.runQuiz(response["document_text"], response["topic"])
    return jsonify(result), 200

 No longer needed? function above replaces it
@app.route("/recursive_question", methods=['GET'])
def recusive_question():
    response = request.json
    try:
        assert(document_text in response and topic in response)
    except:
        return jsonify({"status" : "FAILED, please attatch correct parameters"}), 500
'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)