from flask import Flask, request, jsonify
from flask_cors import CORS
from llm_engineering.app.actions import start, runQuiz


app = Flask(__name__)
CORS(app)

# placeholder functions to abstract
grab_init_summary = lambda x, y: [None,] 
grab_init_questions = lambda x, y: [None,]
grab_init_recursive_question = lambda : [None,]
grab_init_recursive_summary = lambda : [None,]

# .start() makes initial question
#.runQuiz() is the recursive quiz
#matt needs to give the questions in order

@app.route('/')
def homepage():
    return '<h1>hello</h1>'
           


# request headers
document_text, topic = "document_text", "topic"




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

#gets topic and document_text, use it for pablo get request later
@app.route('/base_data', methods=['POST'])
def base_data():
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
    result = start(response["document_text"], response["topic"])
    return jsonify(result), 200

@app.route("/wrong_question", methods=['POST'])
def handle_wrong_question():
    response = request.json
    try:
        assert(document_text in response and topic in response)
    except Exception as e:
        return jsonify({"status": "FAILED, please attach correct parameters"}), 500
    
    # Call runQuiz with the wrong question data
    result = runQuiz(response["document_text"], response["topic"])
    return jsonify(result), 200

@app.route("/recursive_question", methods=['GET'])
def recusive_question():
    response = request.json
    try:
        assert(document_text in response and topic in response)
    except:
        return jsonify({"status" : "FAILED, please attatch correct parameters"}), 500
    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)