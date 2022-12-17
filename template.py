from answer_module import SkyAnswers
import asyncio


async def main():

    answers_module = SkyAnswers('paganemare')
    answers = await answers_module.get_answers()

    for solution in answers:
        print(f"Задание #{solution['task_number']} - {solution['question']}")
        for answer in solution['answer']:
            print(f'   Ответ: {answer}')
        print('')

asyncio.run(main())
