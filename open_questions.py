import os
import re
from dotenv import load_dotenv


load_dotenv()


def load_questions():
    file_path = os.path.join('questions', os.getenv('QUESTIONS_FILES', 'anime10.txt'))

    with open(file_path, 'r', encoding='KOI8-R') as questions_file:
        file_contents = questions_file.read()
        
    questions = re.split(r'Вопрос \d+:', file_contents)[1:]

    questions_answers = {}

    for question in questions:
        parts = re.split(r'Ответ:', question, maxsplit=1)
            
        question, answer = parts
        
        question = question.strip()
        
        answer = re.split(r'[.\n]', answer.strip())[0].strip()
        questions_answers[question] = answer
        
    return questions_answers


