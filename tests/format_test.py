import json

with open("tests/message.txt", "r", encoding="utf-8") as f:
    text = f.read().replace("\"", "'").split("\n")

with open("tests/formatted.txt", "w", encoding="utf-8") as f:
    formatted_request_body = {
        "keyword" : "euler's constant",
        "data" : "\\n".join(text)
    }
    
    f.write(json.dumps(formatted_request_body))