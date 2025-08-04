import os
import re

file_path = os.path.join('questions', '6pers15.txt')

with open(file_path, 'r', encoding='KOI8-R') as questions_file:
      file_contents = questions_file.read()
      
questions = re.split(r'Вопрос \d+:', file_contents)[1:]

questions_answer = {}

for question in questions:
    parts = re.split(r'Ответ:', question, maxsplit=1)
        
    question, answer = parts
    
    question = question.strip()
    
    answer = re.split(r'[.\n]', answer.strip())[0].strip()
    questions_answer[question] = answer

for question, answer in questions_answer.items():
    print(f'Q: {question}\nA: {answer}\n{" "*50}')
