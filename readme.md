# Admin Users Management Script

This script allows you to manage users on a panel, including listing users by admin and optionally deleting users.

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- Access to a Unix-like terminal (Linux, macOS, or Windows Subsystem for Linux)

## Installation and Setup

1. Install Python:
   - For Ubuntu/Debian: `sudo apt-get update && sudo apt-get install python3 python3-pip`
   - For macOS with Homebrew: `brew install python`
   - For other systems, download from [python.org](https://www.python.org/downloads/)

2. Clone the repository:
   ```
   git clone https://github.com/erfjab/AdminUsersDeleter.git
   cd AdminUsersDeleter
   ```

3. Install required libraries:
   ```
   pip3 install httpx
   ```

## Configuration

1. Open the script in a text editor:
   ```
   nano main.py
   ```

2. Modify the following variables at the top of the script:
   - `PANEL_USERNAME`: Your panel sudo username
   - `PANEL_PASSWORD`: Your panel sudo password
   - `ADMIN_USERNAME`: The admin username to filter by (or leave empty to list all admins. like: '')
   - `PANEL_HOST`: The URL of your panel without dashboard. like: 'https://sub.domain.com:port'
   - `DELETE_USERS`: Set to `True` if you want to enable user deletion (use with caution!)

3. Save the file:
   - In nano: Press `Ctrl + X`, then `Y`, then `Enter`

## Running the Script

1. Make the script executable:
   ```
   chmod +x main.py
   ```

2. Run the script:
   ```
   python3 main.py
   ```

## Caution

- If `DELETE_USERS` is set to `True`, the script will attempt to delete all users it retrieves. Use this feature with extreme caution.
- Always make sure you have proper backups before performing any deletion operations.


## Extra
### Contact with Me: [@ErfJab](https://t.me/ErfJab)
### My Telegram Channel: [@ErfJabs](https://t.me/ErfJabs)
### You can star ⭐ the project for support! 