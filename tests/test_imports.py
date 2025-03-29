from llm_engineering.models import GeminiClient, create_initial_summary, create_word_explanation, create_questions, create_answers, create_new_questions
from llm_engineering.infrastructure import get_data

def main():
    print("Testing imports...")
    
    # Test GeminiClient import
    try:
        client = GeminiClient()
        print("✓ GeminiClient imported successfully")
    except Exception as e:
        print(f"✗ GeminiClient error: {str(e)}")
    
    # Test get_data and create_initial_summary
    try:
        data = get_data()
        print("✓ get_data imported and called successfully")    
        summary = create_initial_summary(data)
        print("✓ create_initial_summary imported and called successfully")

        

        # Test create_word_explanation
        keyword = "Euler's constant"
        explanation = create_word_explanation(keyword, data)

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

        # Test create_new_questions
        wrong_questions = """
        2. Euler's constant is defined as the limiting difference between which two mathematical concepts?
a) Sine and Cosine b) Exponential and Logarithmic functions c) Harmonic series and Natural logarithm d) Factorial and Gamma functions
        3. True or False: It is currently known whether Euler's constant is rational or irrational. 
        """
        keyword = "Euler's constant"
        new_questions = create_new_questions(wrong_questions, keyword, data)
        print("✓ create_new_questions imported and called successfully")
        print("\nNew Questions:")
        print(new_questions)
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")

if __name__ == "__main__":
    main() 