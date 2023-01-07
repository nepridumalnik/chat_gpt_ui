from .open_ai_core import oaiCore

from telebot import TeleBot
from os import environ


class GPTDudeBot():
    def __init__(self) -> None:
        pass

    def Run(self) -> None:
        bot.infinity_polling()


gptDudeBot: GPTDudeBot = GPTDudeBot()

TELEGRAM_API_TOKEN: str = environ['TELEGRAM_API_TOKEN']
bot: TeleBot = TeleBot(token=TELEGRAM_API_TOKEN)

HELP: str = '''
Введите /help или /start для получения этой строки
Введите /text с каким-то текстом для обработки сообщения
'''


@bot.message_handler(commands=['start', 'help'])
def __start(message) -> None:
    bot.reply_to(message.chat.id, HELP)


@bot.message_handler(commands=['text'])
def __text(message) -> None:
    try:
        if '/text' == message.text:
            bot.reply_to(message, 'Нужен текст')
            return

        text: str = message.text.split(' ', 1)[1]
        bot.reply_to(message, 'Ожидайте ответ...')

        completion: str = oaiCore.makeCompletion(text)
        bot.reply_to(message, f'Ответ:\n{completion}')
    finally:
        pass
