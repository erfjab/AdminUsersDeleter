import httpx
import logging
import asyncio
from typing import Dict, List, Optional
from collections import defaultdict

# Configuration
PANEL_USERNAME = 'sudo_username'
PANEL_PASSWORD = 'sudo_password'
ADMIN_USERNAME = ''  # Set to '' if you want to list all admins
PANEL_HOST = 'https://sub.domain.com:port'
DELETE_USERS = False  # Set this to True to enable user deletion

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def create_access_token(username: str, password: str, host: str) -> Optional[Dict[str, str]]:
    data = {"username": username, "password": password}
    url = f'{host}/api/admin/token'
    headers = {'Accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, data=data, headers=headers)
            response.raise_for_status()
            token = response.json().get('access_token')
            if not token:
                raise ValueError("Access token not found in response")
            
            logger.info("Token created successfully")
            return {
                'accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': f"Bearer {token}"
            }
    except (httpx.HTTPStatusError, httpx.RequestError, ValueError) as e:
        logger.error(f"Failed to create token: {str(e)}")
        return None

async def get_users_list(headers: Dict[str, str], host: str) -> Optional[List[Dict]]:
    url = f'{host}/api/users'
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            users = response.json().get('users')
            if not users:
                raise ValueError("Users list not found in response")
            
            logger.info(f"Retrieved {len(users)} users")
            return users
    except (httpx.HTTPStatusError, httpx.RequestError, ValueError) as e:
        logger.error(f"Failed to get users list: {str(e)}")
        return None

def process_users(users: List[Dict], admin_username: str) -> None:
    if not admin_username:
        admin_count = defaultdict(int)
        for user in users:
            admin = user['admin']['username'] if user['admin'] else 'None'
            admin_count[admin] += 1
        
        for admin, count in admin_count.items():
            logger.info(f"Admin '{admin}': {count} users")
    else:
        filtered_users = [
            user['username'] for user in users
            if (admin_username == 'None' and user['admin'] is None) or
               (user['admin'] and user['admin']['username'] == admin_username)
        ]
        logger.info(f"Users for admin '{admin_username}': {', '.join(filtered_users)}")
        print(filtered_users)
        return filtered_users

async def delete_user(username: str, headers: Dict[str, str], host: str) -> bool:
    url = f'{host}/api/user/{username}'
    try:
        async with httpx.AsyncClient() as client:
            response = await client.delete(url, headers=headers)
            response.raise_for_status()
            logger.info(f"Successfully deleted user: {username}")
            return True
    except (httpx.HTTPStatusError, httpx.RequestError) as e:
        logger.error(f"Failed to delete user {username}: {str(e)}")
        return False

async def main():
    headers = await create_access_token(PANEL_USERNAME, PANEL_PASSWORD, PANEL_HOST)
    if not headers:
        logger.error("Failed to create access token. Exiting.")
        return

    users = await get_users_list(headers, PANEL_HOST)
    if not users:
        logger.error("Failed to retrieve users list. Exiting.")
        return

    users = process_users(users, ADMIN_USERNAME)

    if DELETE_USERS:
        logger.warning("User deletion mode is enabled! Proceeding with caution.")
        deletion_tasks = [delete_user(user, headers, PANEL_HOST) for user in users]
        deletion_results = await asyncio.gather(*deletion_tasks)
        successful_deletions = sum(deletion_results)
        logger.info(f"Deleted {successful_deletions} out of {len(users)} users.")
    else:
        logger.info("User deletion mode is disabled. No users will be deleted.")

if __name__ == '__main__':
    asyncio.run(main())