from llm_engineering.models import GeminiClient, create_word_explanation, create_questions, create_answers, create_new_questions
from llm_engineering.infrastructure import clean_wiki_content



class PabloAI:
    def __init__(self):
        self.client

    def start(self, keyword: str, data: str) -> dict:
        print("Starting RAG ...")
        
        # Test GeminiClient import
        try:
            gemini_client = GeminiClient()
            print("✓ GeminiClient imported successfully")
        except Exception as e:
            print(f"✗ GeminiClient error: {str(e)}")
        
        # Test get_data and create_initial_summary
        try: 
            cleaned_data = clean_wiki_content(data)
            print("✓ data imported and cleaned successfully")   
            
            # Test create_word_explanation
            explanation = create_word_explanation(keyword, cleaned_data)

            print("✓ create_word_explanation imported and called successfully")
            print("\nExplanation:")
            print(explanation)
            
            split_explanation = explanation.split("\n")

            general_explanation = split_explanation[0]
            
            # Test create_questions
            questions = create_questions(keyword, general_explanation)
            print("✓ create_questions imported and called successfully")
            print("\nQuestions:")
            print(questions)

            # Test create_answers
            answers = create_answers(questions)
            print("✓ create_answers imported and called successfully")
            print("\nAnswers:")
            print(answers)
            

        except Exception as e:
            print(f"✗ Processing Error: {str(e)}")

        finally:
            gemini_client.close()

            results = {
                "explanation": general_explanation,
                "questions": questions,
                "answers": answers
            }
            
            return results


    def runQuiz(self, keyword: str, data: str, wrong_questions: str) -> dict:
        print("Starting Quiz ...")

        try:
            gemini_client = GeminiClient()
            print("✓ GeminiClient imported successfully")
        except Exception as e:
            print(f"✗ GeminiClient error: {str(e)}")


        try:
            cleaned_data = clean_wiki_content(data)
            print("✓ data imported and cleaned successfully")

            new_questions = create_new_questions(keyword, cleaned_data, wrong_questions)
            print("✓ create_new_questions imported and called successfully")
            print("\nNew Questions:")
            print(new_questions)

            answers = create_answers(new_questions)
            print("✓ create_answers imported and called successfully")
            print("\nAnswers:")
            print(answers)

        except Exception as e:
            print(f"✗ Processing Error: {str(e)}")

        finally:
            gemini_client.close()

            results = {
                "new_questions": new_questions,
                "answers": answers
            }

            return results

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
