# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import base64
import sky_api.skysmart_api as skysmart_api
import aiohttp

def remove2linebreak(x:str) -> str:
    while '\n\n' in x:
        x = x.replace('\n\n', '\n')
    return x.strip()

class SkyAnswers:

    def __init__(self, task_hash: str):
        self.task_hash = task_hash

    async def get_answers(self):
        answers_array = []

        async with aiohttp.ClientSession() as session:
            try:
                tasks_uuids = await skysmart_api.get_room(self.task_hash, session)

                for idx, uuid in enumerate(tasks_uuids):
                    soup = await skysmart_api.get_task_html(uuid, session)
                    if soup:
                        parsed_soup = BeautifulSoup(soup, 'html.parser')
                        answers_array.append(self.get_task_answer(parsed_soup, idx + 1))
            except Exception as e:
                print(f"Error in get_answers: {e}")

        return answers_array
    
    async def get_room_info(self):
        async with aiohttp.ClientSession() as session:
            try:
                room_info = await skysmart_api.get_room_info(session, self.task_hash)

                return room_info
            except Exception as e:
                print(f"Error: {e}")


    def get_task_question(self, soup):
        return soup.find("vim-instruction").text.strip()

    def get_task_full_question(self, soup):
        vim_elements = soup.find_all(['vim-instruction', 'vim-groups','vim-test-item','vim-order-sentence-verify-item','vim-input-answers','vim-select-item','vim-test-image-item','math-input-answer','vim-dnd-text-drop','vim-dnd-group-drag','vim-groups-row','vim-strike-out-item','vim-dnd-image-set-drag','vim-dnd-image-drag','edu-open-answer'])
        for element in vim_elements:
            element.extract()
        return remove2linebreak(soup.text)

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
            'full_q' : self.get_task_full_question(soup),
            'answer' : answers,
            'task_number' : tasks_count,
        }

