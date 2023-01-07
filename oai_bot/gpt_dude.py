from .open_ai_core import oaiCore

from telebot import TeleBot
from threading import Thread
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
Введите /image с каким-то текстом для генерации изображения
'''


def __handleCompletionRequest(message) -> None:
    try:
        if '/text' == message.text:
            bot.send_message(message.chat.id, 'Требуется текст для обработки')
            return

        prompts: str = message.text.split(' ', 1)[1]
        bot.send_message(message.chat.id, 'Ожидайте ответ...')

        completion: str = oaiCore.makeCompletion(prompts)
        bot.reply_to(message, f'Ответ:\n{completion}')
    except Exception as e:
        bot.reply_to(message, f'Произошла внутренняя ошибка: {e}')


def __handleImageRequest(message) -> None:
    try:
        if '/image' == message.text:
            bot.send_message(
                message.chat.id, 'Требуется описание для обработки')
            return

        prompts: str = message.text.split(' ', 1)[1]
        bot.send_message(message.chat.id, 'Ожидайте ответ...')

        response = oaiCore.makeImage(prompts)
        uri: str = response['data'][0]['url']

        bot.send_photo(message.chat.id, photo=uri, caption=prompts)
    except Exception as e:
        bot.reply_to(message, f'Произошла внутренняя ошибка: {e}')


@bot.message_handler(commands=['image'])
def __image(message) -> None:
    t = Thread(target=__handleImageRequest,
               kwargs={'message': message})

    t.daemon = True
    t.start()


@bot.message_handler(commands=['text'])
def __text(message) -> None:
    t = Thread(target=__handleCompletionRequest,
               kwargs={'message': message})

    t.daemon = True
    t.start()


@bot.message_handler(commands=['start', 'help'])
def __start(message) -> None:
    bot.send_message(message.chat.id, HELP)
