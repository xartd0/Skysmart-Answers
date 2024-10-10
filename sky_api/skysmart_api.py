import aiohttp
from user_agent import generate_user_agent
from utils import api_variables as api


class SkysmartAPIClient:
    """
    Client for interacting with the Skysmart API.

    This class handles authentication, session management, and provides methods to fetch data from the Skysmart API.
    """

    def __init__(self):
        """
        Initialize the SkysmartAPIClient with a new aiohttp session and user agent.
        """
        self.session = aiohttp.ClientSession()
        self.token = ''
        self.user_agent = generate_user_agent()

    async def close(self):
        """
        Close the aiohttp session.
        """
        await self.session.close()

    async def _authenticate(self):
        """
        Authenticate with the Skysmart API to obtain a JWT token.
        """
        headers = {
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'User-Agent': self.user_agent
        }
        async with self.session.post(api.url_auth2, headers=headers) as resp:
            if resp.status == 200:
                json_resp = await resp.json()
                self.token = json_resp["jwtToken"]
            else:
                raise Exception(f"Authentication failed with status: {resp.status}")

    async def _get_headers(self):
        """
        Get request headers with the JWT token.

        Returns:
            dict: A dictionary of headers including the JWT token.
        """
        if not self.token:
            await self._authenticate()
        return {
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'User-Agent': self.user_agent,
            'Accept': 'application/json, text/plain, */*',
            'Authorization': f'Bearer {self.token}'
        }

    async def get_room(self, task_hash):
        """
        Get UUIDs for all tasks in a test.

        Args:
            task_hash (str): The task hash identifier.

        Returns:
            list: A list of task UUIDs.
        """
        payload = {"taskHash": task_hash}
        headers = await self._get_headers()
        async with self.session.post(api.url_room, headers=headers, json=payload) as resp:
            if resp.status == 200:
                json_resp = await resp.json()
                return json_resp['meta']['stepUuids']
            else:
                raise Exception(f"get_room failed with status: {resp.status}")

    async def get_meta(self, task_hash):
        """
        Get metadata for a task.

        Args:
            task_hash (str): The task hash identifier.

        Returns:
            tuple: A tuple containing the title and module title.
        """
        payload = {"taskHash": task_hash}
        headers = await self._get_headers()
        async with self.session.post(api.url_room, headers=headers, json=payload) as resp:
            if resp.status == 200:
                json_resp = await resp.json()
                title = json_resp["title"]
                module_title = json_resp["meta"]["path"]["module"]["title"]
                return title, module_title
            else:
                raise Exception(f"get_meta failed with status: {resp.status}")

    async def get_task_html(self, uuid):
        """
        Get HTML content for a task by UUID.

        Args:
            uuid (str): The UUID of the task.

        Returns:
            str: The HTML content of the task.
        """
        headers = await self._get_headers()
        async with self.session.get(f"{api.url_steps}{uuid}", headers=headers) as resp:
            if resp.status == 200:
                json_resp = await resp.json()
                return json_resp['content']
            else:
                raise Exception(f"get_task_html failed with status: {resp.status}")

    async def get_room_info(self, task_hash):
        """
        Get information about a Skysmart room test.

        Args:
            task_hash (str): The task hash identifier.

        Returns:
            dict: The JSON response containing room information.
        """
        payload = {"taskHash": task_hash}
        headers = await self._get_headers()
        async with self.session.post(api.url_room_preview, headers=headers, json=payload) as resp:
            if resp.status == 200:
                json_resp = await resp.json()
                return json_resp
            else:
                raise Exception(f"get_room_info failed with status: {resp.status}")
