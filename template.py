from parser.answer_module import SkyAnswers  
import asyncio


async def main():

    task_hash = input('Укажите название комнаты: ')

    answers_module = SkyAnswers(task_hash)
    answers = await answers_module.get_answers()

    for solution in answers:
        print(f"Задание #{solution['task_number']} - {solution['question']}")
        for answer in solution['answers']:
            print(f'   Ответ: {answer}')
        print('')

asyncio.run(main())
