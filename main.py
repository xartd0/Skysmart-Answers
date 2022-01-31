import requests
from bs4 import BeautifulSoup
import base64
from  more_itertools import unique_everseen
from colorama import init, Fore
init(autoreset=True,convert=True)

#auth_token аккаунта буду менять,но он может перестать работать,поэтому лучше используйте свой
# еще один токен Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE2NDM2NTE3NDksImV4cCI6MTY0NjI0Mzc0OSwicm9sZXMiOlsiUk9MRV9FRFVfU0tZU01BUlRfU1RVREVOVF9VU0FHRSJdLCJ1c2VySWQiOjQ4OTg1Mzg1LCJlbWFpbCI6ImdkZmtqbmdrc2hqZG1mbmdraGpzbkBnbWFpbC5jb20iLCJuYW1lIjoi0JLQsNC90Y8iLCJzdXJuYW1lIjoi0JLQsNC90Y8iLCJpZGVudGl0eSI6Im11YmluaW5vZ2kifQ.CDpO-n7febtcZErWOFmK9R6WmJc7a2uNXDYBRbOvJetVdMlhXAGaj3nb3yS6rUMxRnEZcBuNcFeroI5F9yUAMk5uMIGEaTlECiMIxWLE4VUZ2TRkHK_w6jNlRZC3RBHBJjISWdFpA3i37pMarpij7tHnNNzN2DSvjzL3KNLe_Hy1mliN_LFZGRg2UNwRvc77u71zxI7ExIZ2-MwVjY53OoHxiqVZr-59y3rhnMLtREQGsCBmHZXkuf9rlv9wZxsipF9y_w03SMFGZjhXvchIVuGiJbDD11bVPA1LXHO5w2H71WXTn05ZV3Z6YG11s8Dn-AaPx2uKCW4QYsQDwpxGZ-fNRxP36Qb1vgQpMoCKcSpjV3bH7hPyzTgxqWNCBX7oYv2OTvCU9GMiN1T7nGc6kLI5SF-C_PvpMu1LkKwK35MgaLRVt4Ffjvh9ujKTzVHzEJuBzak9R-8MWTC8Sq-Olr3Hmb7KWnT9-egTsgLs6kXURqCfaFAupOAdd5ABhaK9KwsfAvp5zpNeP-f_oG59iH5d7atUKtC5I4hgtchXyvqet88b6Gu0ZO49akXteVSI0yReA_kQUlx0hEcQQx1tDM9lF2DM3pexDLE1ZGBm8b2O7-cWl7GSIpaM-zPXVz16NMNrgqoperSLmEEBWtE3cNhvbJJMEu0esu5JhNYTE_g
auth_token = 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE2NDM2NTEzNjAsImV4cCI6MTY0NjI0MzM2MCwicm9sZXMiOlsiUk9MRV9FRFVfU0tZU01BUlRfU1RVREVOVF9VU0FHRSJdLCJ1c2VySWQiOjQ4OTgzMzU3LCJlbWFpbCI6Im9hZGptZmdram5hZGZrbWdqQGdtYWlsLmNvbSIsIm5hbWUiOiLQktC70LDQtCDQktC70LDQtCIsInN1cm5hbWUiOiLQktC70LDQtCIsImlkZW50aXR5IjoieGl6dXJldGlkdSJ9.E3wX-TAtl05HshNr-DS2ktcpYsie_Stv_zkxeY2oPzU98kF146N2p5ubRbyL87Qn53eIBu-VFBDxIK3aqI52nD2gZtigG5eU58svtbDBDSiWtHT0wNclFhtxAhZtXF6tP7TJXZ53O-vhAiZTyRwA4yODGUiIeQ7Fdv3oluvDzg1YQO4ctJBXrQSffJ_P9eEQW_4X7y5ccn3BMD52iA6tgj86mAcrw87iWRC1WSxkpCk03L8Hpary7Lqs7etFt0Hc7nPrdbra0czeT1d6SZaxtFA_6e0Eci0qT8CGBQ_kkyLU8K8oxdrd1BL5VLteH41Znsa_tsHEifIwUoCSwp_Qc6dkDNZXmPqWzWadaz6LeZJRxu81V4Y-N8rNMP5-XnC6BkRp5EaBDAnlcF9OyjjdgSLqMyO8BDEzdN4Aqg6gwyQ5N002EBpxlUmaBBPwrwBp4_b1TZFPGzbPamnt_JCM4-muylWln55Rud13yjRINPz8RO-zvbv4XFRpfGA-ffhVQec8GyvIVNQJahEDl8jVnLRJxgImb8lobH6eNC4bNbqzuSbkH3qSyVbeXUa2XZEyp2CMJ9mA6I041uONiOCjhvGy7dUq61lc3zwhIm0bS7AND2-6M8wvdGXowGgIynBAGnWuLWrOpEVWit5ygC-JOy6E9H2cC8CBd4YrViUDmlM'
results =[]

def answerparse(taskHash):
    # ---- получение uuid заданий в тесте ----#
    url = f"https://api-edu.skysmart.ru/api/v1/task/start"
    payload = "{\"taskHash\":\"" + taskHash + "\"}"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': auth_token

    }
    response = requests.request("POST", url, headers=headers, data=payload)
    roomhashjson = response.json() 
    roomHash = roomhashjson['roomHash'] # код рума 
    
    # ---- тут получаем html в json ----#
    url = "https://api-edu.skysmart.ru/api/v1/lesson/join"
    payload = "{\"roomHash\":\"" + roomHash + "\"}"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': auth_token
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    steps_raw = response.json()
    
    
    checkradom = steps_raw['taskStudentMeta']['steps'] # все uuid заданий
    random = False # проверка на рандомные задания
    for uuid in checkradom:
        url = "https://api-edu.skysmart.ru/api/v1/content/step/load?stepUuid=" + uuid['stepUuid']
        headers = {
        'Authorization': auth_token
        }
        response = requests.request("GET", url, headers=headers)
        answer_row = response.json()
        soup = BeautifulSoup(answer_row['content'], 'html.parser')
        anstitle = soup.find('vim-instruction')
        try:
            anstitlerow = '📝Вопрос:' + (anstitle.text.replace('\n', ' ')).replace('\r',' ')
            results.append(anstitlerow)
        except:
            pass
        
        # а тут много циклов,каждый цикл это разные типы заданий,знаю стремно,но мне лень переделывать
        for i in soup.find_all('vim-test-item', attrs={'correct': 'true'}):
            results.append(i.text)
        for i in soup.find_all('vim-input-answers'):
            j = i.find('vim-input-item')
            results.append(j.text)
        for i in soup.find_all('vim-select-item', attrs={'correct': 'true'}):
            results.append(i.text)
        for i in soup.find_all('vim-test-image-item', attrs={'correct': 'true'}):
            results.append(f'{i.text} - Верный')
        for i in soup.find_all('math-input'):
            j = i.find('math-input-answer')
            results.append(j.text)
        for i in soup.find_all('vim-dnd-text-drop'):
            for f in soup.find_all('vim-dnd-text-drag'):
                if i['drag-ids'] == f['answer-id']:
                    results.append(f'{f.text}')
        for i in soup.find_all('vim-dnd-group-drag'):
            for f in soup.find_all('vim-dnd-group-item'):
                if i['answer-id'] in f['drag-ids']:
                    results.append(f'{f.text} - {i.text}')
        for i in soup.find_all('vim-groups-item'):
            arow = i['text']
            a = base64.b64decode(arow) 
            results.append(f"{a.decode('utf-8')}")   
        for i in soup.find_all('vim-strike-out-item', attrs={'striked': 'true'}):
            results.append(i.text)
        for i in soup.find_all('vim-dnd-image-set-drag'):
            for f in soup.find_all('vim-dnd-image-set-drop'):
                if i['answer-id'] in f['drag-ids']:
                    results.append(f'{f["image"]} - {i.text}')
        for i in soup.find_all('vim-dnd-image-drag'):
            for f in soup.find_all('vim-dnd-image-drop'):
                if i['answer-id'] in f['drag-ids']:
                    results.append(f'{f.text} - {i.text}')
        if uuid['isRandom']:
            random = True
            return random
    if random:
        print('В тесте есть рандомные задания!')

                
print("Введите комнату")
taskHash = input()
answerparse(taskHash)
i = 0
for item in results:
    if 'Вопрос' in item:
        i = i + 1
        print(Fore.CYAN + str(i),Fore.MAGENTA + str(item))
    else:
        print(Fore.GREEN + str(item))



