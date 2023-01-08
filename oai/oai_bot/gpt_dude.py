from ..oai_core.open_ai_core import oaiCore

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

PROCESSING: str = 'Обработка запроса...'
NEEDS_DESCRIPTION: str = 'Нужно описание'
INTERNAL_ERROR: str = 'Произошла внутренняя ошибка: {}'

HELP: str = '''
Введите /help или /start для получения этой строки
Введите /text с каким-то текстом для обработки сообщения
Введите /image с каким-то текстом для генерации изображения
'''


def __handleCompletionRequest(message) -> None:
    try:
        if '/text' == message.text:
            bot.send_message(message.chat.id, NEEDS_DESCRIPTION)
            return

        prompts: str = message.text.split(' ', 1)[1]
        bot.send_message(message.chat.id, PROCESSING)

        completion: str = oaiCore.makeCompletion(prompts)
        bot.reply_to(message, f'Ответ:\n{completion}')
    except Exception as e:
        bot.reply_to(message, INTERNAL_ERROR.format(e))


def __handleImageRequest(message) -> None:
    try:
        if '/image' == message.text:
            bot.send_message(
                message.chat.id, NEEDS_DESCRIPTION)
            return

        prompts: str = message.text.split(' ', 1)[1]
        bot.send_message(message.chat.id, PROCESSING)

        response = oaiCore.makeImage(prompts)
        uri: str = response['data'][0]['url']

        bot.send_photo(message.chat.id, photo=uri, caption=prompts)
    except Exception as e:
        bot.reply_to(message, INTERNAL_ERROR.format(e))


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
