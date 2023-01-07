from os import environ
from telebot import TeleBot


class GPTDudeBot():
    def __init__(self) -> None:
        pass

    def Run(self) -> None:
        bot.infinity_polling()


gptDudeBot: GPTDudeBot = GPTDudeBot()

TELEGRAM_API_TOKEN: str = environ['TELEGRAM_API_TOKEN']
bot: TeleBot = TeleBot(token=TELEGRAM_API_TOKEN)


@bot.message_handler(commands=['start'])
def __start(message) -> None:
    bot.send_message(message.chat.id, 'Привет!')
