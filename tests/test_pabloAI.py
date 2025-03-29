from llm_engineering.app import PabloAI
from llm_engineering.infrastructure import get_data

pablo = PabloAI()

data = get_data()

initial_summary = pablo.makeSummary("Eulers Number", data)

questions = pablo.makeQuestions("Eulers Number", initial_summary["general_explanation"])

print(questions)

wrong_questions = input("Enter the wrong questions: ")

new_questions = pablo.makeNewQuestions("Eulers Number", data, wrong_questions)

summary_adjustment = pablo.makeSummaryAdjustment("Eulers Number", questions["questions"], questions["answers"])

print(summary_adjustment["summary_adjustment"])
print(new_questions["new_questions"])
