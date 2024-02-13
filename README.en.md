[read in persian](README.fa.md)

# Telegram Color Filter Bot

The Telegram Color Filter Bot is a bot that allows you to apply various color filters to your images. This bot can convert your images to black and white, add color filters like blue or red, and even create a red and blue 3D effect.

## How to Use

To use this bot, first search for it in Telegram and then start chatting. After starting the chat, you can use the following commands:

- `/start`: Begin interacting with the bot and receive initial instructions.
- `/help`: Get guidance on how to use the bot.
- `/black_white`: Convert the sent image to black and white.
- `/blue`: Add a blue filter to the image.
- `/red`: Add a red filter to the image.
- `/3d`: Apply a red and blue 3D effect.

## Installation and Setup

To set up this bot on your server or development environment, follow the steps below:

1. Ensure `python3` and `pip` are installed on your system.
2. Install the required libraries using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```
3. Create a `.env` file at the root of the project and add your Telegram bot token like so:

```bash
TELEGRAM_TOKEN=your_telegram_bot_token_here
```
4. Run the bot script with the following command:

```bash 
python bot.py
```

## Contributing

Contributions to improve this bot are welcome. Please create an issue first to discuss proposed changes or improvements.
