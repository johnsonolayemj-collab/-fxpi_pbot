# Text Diff Checker Telegram Bot

A simple Telegram bot that highlights differences between two paragraphs.

## Features
- Compare two texts and see added/removed lines
- Simple two-step input: send first text, then second text
- `/reset` command to start over
- In-memory storage (no database needed)

## Deploy on Railway

1. Push this repo to GitHub
2. Go to [Railway](https://railway.app) → New Project → Deploy from GitHub
3. Add environment variable: `TELEGRAM_BOT_TOKEN` = your BotFather token
4. Deploy — Railway will auto-detect the Procfile and run the bot

## Usage
- `/start` — Begin
- `/help` — Show instructions
- `/reset` — Clear and start over
