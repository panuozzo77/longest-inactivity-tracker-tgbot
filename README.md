# Telegram Inactivity Tracker Bot

This is a Python-based Telegram bot that tracks and reports the longest period of inactivity between messages in a group.

## Features

*   **Monitors Inactivity:** Tracks the time between messages in any group it's a part of.
*   **Per-Group Records:** Each group has its own separate inactivity record.
*   **New Record Announcements:** Optionally announces when a new longest period of inactivity is achieved.
*   **Simple Commands:** Easy-to-use commands to check the record or configure the bot.

## Architecture

The bot is built using clean architecture principles to ensure it is maintainable, scalable, and testable.

*   **SOLID Principles:** The codebase is designed following SOLID principles.
*   **Dependency Injection:** Components are decoupled using dependency injection.
*   **Pluggable Storage:** The storage mechanism is abstracted, starting with a simple JSON file (`db.json`) but easily replaceable with a database.

## Installation

Follow these steps to set up and run the bot locally.

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd longest-inactivity-tracker
```

### 2. Create a Virtual Environment

It is highly recommended to use a Python virtual environment to manage dependencies.

```bash
python3 -m venv venv
```

### 3. Install Dependencies

Activate the virtual environment and install the required packages from `requirements.txt`.

**On macOS and Linux:**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

**On Windows:**
```bash
.\venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Configure the Bot Token

You need to provide a Telegram Bot Token for the bot to work.

1.  Make a copy of the `.env.example` file and name it `.env`.
2.  Open the new `.env` file and replace `your_token_here` with your actual token from BotFather.

```
TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
```

## How to Run

Once the dependencies are installed and the configuration is set, you can run the bot.

```bash
python src/main.py
```

The bot will start polling for updates from Telegram. You can add it to your groups and start using its commands.

## Bot Commands

*   `/start` or `/help` - Shows the help message with all available commands.
*   `/record` - Displays the current longest inactivity record for the group.
*   `/toggle_announcements` - Enables or disables the announcement of new records in the group.
*   `/seed` - Sets an initial inactivity record of 10 minutes to prevent spam on first use.

## Development (VS Code)

This project includes a launch configuration for Visual Studio Code. To run or debug the bot within VS Code:

1.  Make sure you have selected the Python interpreter from the `venv` directory.
2.  Go to the **Run and Debug** view (Ctrl+Shift+D).
3.  Select the **"Python: Run Bot"** configuration from the dropdown and press F5.