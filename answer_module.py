# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import base64
import skysmart_api

class SkyAnswers:

    def __init__(self, task_hash: str):
        self.task_hash = task_hash

    async def get_answers(self):
        tasks_count = 0
        answers_array = []

        tasks_uuids = await skysmart_api.get_room(self.task_hash)
        
        for uuid in tasks_uuids: 
            tasks_count += 1

            soup = await skysmart_api.get_task_html(uuid)
            answers_array.append(self.get_task_answer(BeautifulSoup(soup, 'html.parser'), tasks_count)) 

        return answers_array

    def get_task_question(self, soup):
        return soup.find("vim-instruction").text

    def get_task_answer(self, soup, tasks_count): # Тут все перепишу, если руки дойдут
        answers = []

        if soup.find('vim-test-item', attrs={'correct': 'true'}):
            for i in soup.find_all('vim-test-item', attrs={'correct': 'true'}):
                answers.append(i.text)
        
        if soup.find('vim-order-sentence-verify-item'):
            for i in soup.find_all('vim-order-sentence-verify-item'):
                answers.append(i.text)
        
        if soup.find('vim-input-answers'):
            for i in soup.find_all('vim-input-answers'):            
                answers.append(i.find('vim-input-item').text)
        
        if soup.find('vim-select-item', attrs={'correct': 'true'}):
            for i in soup.find_all('vim-select-item', attrs={'correct': 'true'}):
                answers.append(i.text)
        
        if soup.find('vim-test-image-item', attrs={'correct': 'true'}):
            for i in soup.find_all('vim-test-image-item', attrs={'correct': 'true'}):
                answers.append(f'{i.text} - Верный')
        
        if soup.find('math-input-answer'):
            for i in soup.find_all('math-input-answer'):
                answers.append(i.text)
        
        if soup.find('vim-dnd-text-drop'):
            for i in soup.find_all('vim-dnd-text-drop'):
                for f in soup.find_all('vim-dnd-text-drag'):
                    if i['drag-ids'] == f['answer-id']:
                        answers.append(f'{f.text}')
        
        if soup.find('vim-dnd-group-drag'):
            for i in soup.find_all('vim-dnd-group-drag'):
                for f in soup.find_all('vim-dnd-group-item'):
                    if i['answer-id'] in f['drag-ids']:
                        answers.append(f'{f.text} - {i.text}')
        
        if soup.find('vim-groups-row'):
            for i in soup.find_all('vim-groups-row'):
                for l in i.find_all('vim-groups-item'):
                    try:
                        answers.append(f"{base64.b64decode(l['text']).decode('utf-8')}")   
                    except:
                        pass

        if soup.find('vim-strike-out-item'):
            for i in soup.find_all('vim-strike-out-item', attrs={'striked': 'true'}):
                answers.append(i.text)

        if soup.find('vim-dnd-image-set-drag'):
            for i in soup.find_all('vim-dnd-image-set-drag'):
                for f in soup.find_all('vim-dnd-image-set-drop'):
                    if i['answer-id'] in f['drag-ids']:
                        answers.append(f'{f["image"]} - {i.text}')

        if soup.find('vim-dnd-image-drag'):
            for i in soup.find_all('vim-dnd-image-drag'):
                for f in soup.find_all('vim-dnd-image-drop'):
                    if i['answer-id'] in f['drag-ids']:
                        answers.append(f'{f.text} - {i.text}')


        if soup.find('edu-open-answer', attrs={'id': 'OA1'}):
            answers.append('Необходимо загрузить файл')

        return {
            'question' : self.get_task_question(soup),
            'answer' : answers,
            'task_number' : tasks_count
        }

