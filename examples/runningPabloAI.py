from llm_engineering.app.actions import PabloAI

def main():
    # Example usage
    pablo_ai = PabloAI()
    
    # Example keyword and data
    keyword = "Python programming"
    data = "Python is a high-level, interpreted programming language known for its simplicity and readability."
    
    # Run the initial learning session
    results = pablo_ai.start(keyword, data)
    
    # Example of running a quiz with wrong questions
    wrong_questions = "What is Python? A: A snake"
    quiz_results = pablo_ai.runQuiz(keyword, data, wrong_questions)
    
    return results, quiz_results

if __name__ == "__main__":
    main()