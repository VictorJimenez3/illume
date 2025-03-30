from llm_engineering.models import GeminiClient, create_word_explanation, create_questions, create_answers, create_new_questions, create_summary_adjustment
# from llm_engineering.models.comfyui_client import ComfyUIClient
from llm_engineering.infrastructure import clean_wiki_content



class PabloAI:
    def __init__(self):
        # Starting PabloAI'
        # self.comfyui_client = ComfyUIClient()
        pass

    def makeSummary(self, keyword: str, data: str) -> dict:
        print("Making Initial Explanation ...")
        
        # Test GeminiClient import
        gemini_client = GeminiClient()
        print("✓ GeminiClient imported successfully")
        
        # Test get_data and create_initial_summary
        cleaned_data = clean_wiki_content(data)
        print("✓ data imported and cleaned successfully")   
        
        # Test create_word_explanation
        explanation = create_word_explanation(keyword, cleaned_data)

        print("✓ create_word_explanation imported and called successfully")
        print("\nExplanation:")
        print(explanation)
        
        split_explanation = explanation.split("\n")   
        print("SPLIT EXPANSION", split_explanation)      
       
        gemini_client.close()

        results = {
            "cleaned_data": cleaned_data,
            "general_explanation": split_explanation[0],
            "detailed_explanation": split_explanation[2]
        }
        
        return results

    def makeQuestions(self, keyword: str, explanation: str) -> dict:
        print("Making Initial Questions ...")

        gemini_client = GeminiClient()
        print("✓ GeminiClient imported successfully")

        questions = create_questions(keyword, explanation)
        print("✓ create_questions imported and called successfully")
        print("\nQuestions:")
        print(questions)

        split_questions = questions.split("\n\n")

        answers = create_answers(questions)
        print("✓ create_answers imported and called successfully")
        print("\nAnswers:")
        print(answers)

        split_answers = answers.split("\n\n")

        gemini_client.close()

        results = {
            "questions_raw": split_questions,
            "answers_raw": split_answers
        }

        return results

    def makeNewQuestions(self, keyword: str, data: str, wrong_questions: str) -> dict:
        print("Making New Questions ...")

        gemini_client = GeminiClient()
        print("✓ GeminiClient imported successfully")

        cleaned_data = clean_wiki_content(data)
        print("✓ data imported and cleaned successfully")

        new_questions = create_new_questions(keyword, cleaned_data, wrong_questions)
        print("✓ create_new_questions imported and called successfully")
        print("\nNew Questions:")
        print(new_questions)

        new_questions_split = new_questions.split("\n\n")
        
        new_answers = create_answers(new_questions)
        print("✓ create_answers imported and called successfully")
        print("\nAnswers:")
        print(new_answers)

        new_answers_split = new_answers.split("\n\n")

        gemini_client.close()

        results = {
            "questions_raw": new_questions_split,
            "answers_raw": new_answers_split
        }

        return results
    
    def makeSummaryAdjustment(self, keyword: str, new_questions: str, new_answers: str) -> dict:
        print("Making Summary Adjustment ...")

        GeminiClient()
        print("✓ GeminiClient imported successfully")  

        summary_adjustment = create_summary_adjustment(keyword, new_questions, new_answers)
        print("✓ create_summary_adjustment imported and called successfully")
        print("\nSummary Adjustment:")
        print(summary_adjustment)

        results = {
            "summary_adjustment": summary_adjustment
        }

        return results    


    # def generate_video(self, keyword: str, explanation: str) -> dict:
    #     """
    #     Generate a video visualization for the keyword and its explanation.
        
    #     Args:
    #         keyword (str): The keyword to visualize
    #         explanation (str): The explanation of the keyword
            
    #     Returns:
    #         dict: Dictionary containing the video path and metadata
    #     """
    #     print("Generating video visualization...")
        
    #     # Create a prompt that combines the keyword and explanation
    #     prompt = f"Create a visual representation of {keyword}: {explanation}"
        
    #     try:
    #         video_path = self.comfyui_client.generate_video(prompt)
    #         print("✓ Video generated successfully")
            
    #         results = {
    #             "video_path": video_path,
    #             "keyword": keyword,
    #             "prompt": prompt
    #         }
            
    #     except Exception as e:
    #         print(f"✗ Error generating video: {str(e)}")
    #         results = {
    #             "error": str(e),
    #             "keyword": keyword,
    #             "prompt": prompt
    #         }
            
    #     return results
    