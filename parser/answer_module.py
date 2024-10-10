# -*- coding: utf-8 -*-
"""
Module for extracting answers from Skysmart tasks.
"""

import asyncio
import base64
import re

from bs4 import BeautifulSoup
from sky_api.skysmart_api import SkysmartAPIClient


def remove_extra_newlines(text: str) -> str:
    """
    Remove extra newline characters from the text.

    Args:
        text (str): The input text.

    Returns:
        str: The text with extra newlines removed.
    """
    return re.sub(r'\n+', '\n', text.strip())


class SkyAnswers:
    """
    Class to fetch and parse answers from Skysmart tasks.

    Attributes:
        task_hash (str): The hash of the task to fetch.
    """

    def __init__(self, task_hash: str):
        """
        Initialize the SkyAnswers instance.

        Args:
            task_hash (str): The hash of the task to fetch.
        """
        self.task_hash = task_hash

    async def get_answers(self):
        """
        Fetch answers for all tasks associated with the task hash.

        Returns:
            list: A list of dictionaries containing question, full question, answers, and task number.
        """
        answers_list = []
        client = SkysmartAPIClient()

        try:
            tasks_uuids = await client.get_room(self.task_hash)

            # Fetch task HTMLs concurrently
            tasks_html_coroutines = [client.get_task_html(uuid) for uuid in tasks_uuids]
            tasks_html_list = await asyncio.gather(*tasks_html_coroutines, return_exceptions=True)

            for idx, task_html in enumerate(tasks_html_list):
                if isinstance(task_html, Exception):
                    print(f"Error fetching task HTML for UUID {tasks_uuids[idx]}: {task_html}")
                    continue
                soup = BeautifulSoup(task_html, 'html.parser')
                task_answer = self._get_task_answer(soup, idx + 1)
                answers_list.append(task_answer)
        except Exception as e:
            print(f"Error in get_answers: {e}")
        finally:
            await client.close()

        return answers_list

    async def get_room_info(self):
        """
        Fetch information about the room associated with the task hash.

        Returns:
            dict: The JSON response containing room information.
        """
        client = SkysmartAPIClient()
        try:
            room_info = await client.get_room_info(self.task_hash)
            return room_info
        except Exception as e:
            print(f"Error in get_room_info: {e}")
            return None
        finally:
            await client.close()

    @staticmethod
    def _extract_task_question(soup):
        """
        Extract the question text from the task soup.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object of the task HTML.

        Returns:
            str: The extracted question text.
        """
        instruction = soup.find("vim-instruction")
        return instruction.text.strip() if instruction else ""

    @staticmethod
    def _extract_task_full_question(soup):
        """
        Extract the full text of the task, excluding certain elements.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object of the task HTML.

        Returns:
            str: The extracted full question text.
        """
        elements_to_exclude = [
            'vim-instruction', 'vim-groups', 'vim-test-item',
            'vim-order-sentence-verify-item', 'vim-input-answers',
            'vim-select-item', 'vim-test-image-item', 'math-input-answer',
            'vim-dnd-text-drop', 'vim-dnd-group-drag', 'vim-groups-row',
            'vim-strike-out-item', 'vim-dnd-image-set-drag',
            'vim-dnd-image-drag', 'edu-open-answer'
        ]
        for element in soup.find_all(elements_to_exclude):
            element.decompose()
        return remove_extra_newlines(soup.get_text())

    def _get_task_answer(self, soup, task_number):
        """
        Parse the task soup to extract answers.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object of the task HTML.
            task_number (int): The number of the task.

        Returns:
            dict: A dictionary containing question, full question, answers, and task number.
        """
        answers = []

        # Multiple choice questions with correct answers marked
        for item in soup.find_all('vim-test-item', attrs={'correct': 'true'}):
            answers.append(item.get_text())

        # Order sentences
        for item in soup.find_all('vim-order-sentence-verify-item'):
            answers.append(item.get_text())

        # Input answers
        for input_answer in soup.find_all('vim-input-answers'):
            input_item = input_answer.find('vim-input-item')
            if input_item:
                answers.append(input_item.get_text())

        # Select items with correct answers
        for select_item in soup.find_all('vim-select-item', attrs={'correct': 'true'}):
            answers.append(select_item.get_text())

        # Test image items with correct answers
        for image_item in soup.find_all('vim-test-image-item', attrs={'correct': 'true'}):
            answers.append(f"{image_item.get_text()} - Correct")

        # Math input answers
        for math_answer in soup.find_all('math-input-answer'):
            answers.append(math_answer.get_text())

        # Drag and drop text
        for drop in soup.find_all('vim-dnd-text-drop'):
            drag_ids = drop.get('drag-ids', '').split(',')
            for drag_id in drag_ids:
                drag = soup.find('vim-dnd-text-drag', attrs={'answer-id': drag_id})
                if drag:
                    answers.append(drag.get_text())

        # Drag and drop groups
        for drag_group in soup.find_all('vim-dnd-group-drag'):
            answer_id = drag_group.get('answer-id')
            for group_item in soup.find_all('vim-dnd-group-item'):
                drag_ids = group_item.get('drag-ids', '').split(',')
                if answer_id in drag_ids:
                    answers.append(f"{group_item.get_text()} - {drag_group.get_text()}")

        # Group rows
        for group_row in soup.find_all('vim-groups-row'):
            for group_item in group_row.find_all('vim-groups-item'):
                encoded_text = group_item.get('text')
                if encoded_text:
                    try:
                        decoded_text = base64.b64decode(encoded_text).decode('utf-8')
                        answers.append(decoded_text)
                    except Exception as e:
                        print(f"Error decoding base64 text: {e}")

        # Strike out items
        for striked_item in soup.find_all('vim-strike-out-item', attrs={'striked': 'true'}):
            answers.append(striked_item.get_text())

        # Drag and drop image set
        for image_drag in soup.find_all('vim-dnd-image-set-drag'):
            answer_id = image_drag.get('answer-id')
            for image_drop in soup.find_all('vim-dnd-image-set-drop'):
                drag_ids = image_drop.get('drag-ids', '').split(',')
                if answer_id in drag_ids:
                    answers.append(f"{image_drop.get('image')} - {image_drag.get_text()}")

        # Drag and drop images
        for image_drag in soup.find_all('vim-dnd-image-drag'):
            answer_id = image_drag.get('answer-id')
            for image_drop in soup.find_all('vim-dnd-image-drop'):
                drag_ids = image_drop.get('drag-ids', '').split(',')
                if answer_id in drag_ids:
                    answers.append(f"{image_drop.get_text()} - {image_drag.get_text()}")

        # Open answer requiring file upload
        if soup.find('edu-open-answer', attrs={'id': 'OA1'}):
            answers.append('File upload required')

        return {
            'question': self._extract_task_question(soup),
            'full_question': self._extract_task_full_question(soup),
            'answers': answers,
            'task_number': task_number,
        }
