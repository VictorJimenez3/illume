from llm_engineering.app.actions import PabloAI

def main():
    # Example usage
    pablo_ai = PabloAI()
    
    # Example keyword and data
    keyword = "Python programming"
    data = "Python is a high-level, interpreted programming language known for its simplicity and readability."
    
    # Run the initial learning session
    results = pablo_ai.makeSummary(keyword, data)
  
    quiz_results = pablo_ai.makeQuestions(keyword, results["general_explanation"])
    
    # Generate video visualization
    video_results = pablo_ai.generate_video(keyword, results["general_explanation"])
    
    return results, quiz_results, video_results

if __name__ == "__main__":
    main()
    