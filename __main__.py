import os
import random
import datetime
import string
from logging import getLogger
from subprocess import Popen
from subprocess import PIPE

from telegram import Bot
from telegram import Update
from telegram import ParseMode
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram import ReplyKeyboardRemove
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram.ext import CallbackQueryHandler

from echo.buttons import BUTTON_IMG, BUTTON_GIF, BUTTON_HELP
from echo.buttons import get_base_reply_keyboard
from echo.config import load_config
from settings.config import TG_TOKEN

# config = load_config()
# logger = getLogger(__name__)


# def debug_requests(f):
#     def inner(*args, **kwargs):
#         try:
#             logger.info("Обращение в функцию {}".format(f.__name__))
#             return f(*args, **kwargs)
#         except Exception:
#             logger.exception("Ошибка в обработчике {}".format(f.__name__))
#
#     return inner


path = os.path.dirname(os.path.abspath(__file__))
picfolder = os.path.join(path, "photo")
giffolder = os.path.join(path, "gif")

MAIN_LEFT = "main_left"
MAIN_RIGHT = "main_right"
MAIN_BOTTOM = "main_bottom"

TITLES = {
    MAIN_LEFT: "Гг 😆",
    MAIN_RIGHT: "Боян 🎹",
    MAIN_BOTTOM: "Ват? 🙃"
}


# Положення кнопок
def base_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(TITLES[MAIN_LEFT], callback_data=MAIN_LEFT),
            InlineKeyboardButton(TITLES[MAIN_RIGHT], callback_data=MAIN_RIGHT),
        ],
        [
            InlineKeyboardButton(TITLES[MAIN_BOTTOM], callback_data=MAIN_BOTTOM)
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


# Дії для кнопок
# @debug_requests
def call_keyboard(bot: Bot, update: Update, **kwargs):
    if update.callback_query.data == MAIN_LEFT:
        bot.send_message(
            chat_id=update.effective_message.chat_id,
            text="Чьотко 😎",
            reply_markup=get_base_reply_keyboard(), )
    elif update.callback_query.data == MAIN_RIGHT:
        bot.send_message(chat_id=update.effective_message.chat_id,
                         text='Сам боян 😒',
                         reply_markup=get_base_reply_keyboard(), )
    elif update.callback_query.data == MAIN_BOTTOM:
        bot.send_message(
            chat_id=update.effective_message.chat_id,
            reply_markup=get_base_reply_keyboard(),
            text=(random.choice(["Телепо джубі окоптору?",
                                 "Бако бако пакупако!!!",
                                 "Кококо купокупо!",
                                 "Лапанеро кубакупу...",
                                 "Арарака купанака :)"])) + "\n(говорить по марсіанські)")


# Початкове меню
# @debug_requests
def do_start(bot: Bot, update: Update):
    bot.send_photo(chat_id=update.message.chat_id, photo=open(path + '/start.jpg', 'rb'))
    bot.send_message(chat_id=update.message.chat_id,
                     text='Слава Нібіру! Рептилоідам Слава!\n'
                          'Юзай менюшку Homosapien...',
                     reply_markup=get_base_reply_keyboard(), )


# @debug_requests
def do_echo(bot: Bot, update: Update):
    chat_id = update.message.chat_id
    text = update.message.text
    if text == BUTTON_GIF:
        return do_random_gif(bot=bot, update=update)
    elif text == BUTTON_IMG:
        return do_random_image(bot=bot, update=update)
    elif text == BUTTON_HELP:
        return do_help(bot=bot, update=update)
    else:
        bot.send_message(
            chat_id=chat_id,
            reply_markup=get_base_reply_keyboard(),
            text=(random.choice(["Телепо джубі окоптору? 👽",
                                 "Бако бако пакупако!!! 👽",
                                 "Кококо купокупо! 👽",
                                 "Лапанеро кубакупу... 👽",
                                 "Арарака купанака :) 👽"])) + "\n(говорить по марсіанські) "
                                                               "\n\nВалєрка не розуміє..."
                                                               "\nВведи / або юзай менюшку👇"
        )


# Меню виклику допомоги
# @debug_requests
def do_help(bot: Bot, update: Update):
    bot.send_photo(chat_id=update.message.chat_id, photo=open(path + '/help.jpg', 'rb'))
    bot.send_message(chat_id=update.message.chat_id,
                     text='Що не справився? 😨\n\n'
                          'ну дивись що можна:\n'
                          '/start - привітаю\n'
                          '/help - ти вже і так тут\n'
                     # '/poshuti - текстовочки з Нібіру\n'
                          '/poshutipic - Космопікча\n'
                          '/poshutigif - Анімайка\n\n',
                     # 'Або юзай менюшку Homosapien...',
                     reply_markup=get_base_reply_keyboard(), )


# Рандомна шутка картинка
# @debug_requests
def do_random_image(bot: Bot, update: Update):
    files = os.listdir(picfolder)
    mem = str(random.choice(list(files)))

    bot.send_photo(chat_id=update.message.chat_id, photo=open(picfolder + '/' + mem, 'rb'),
                   reply_markup=base_keyboard(), )


# @debug_requests
def do_random_gif(bot: Bot, update: Update):
    files = os.listdir(giffolder)
    mem = str(random.choice(list(files)))

    bot.send_animation(chat_id=update.message.chat_id, animation=open(giffolder + '/' + mem, 'rb'),
                       reply_markup=base_keyboard(), )


# @debug_requests
def main():
    bot = Bot(
        token=TG_TOKEN,
    )
    updater = Updater(
        bot=bot,
    )

    start_handler = CommandHandler("start", do_start)
    echo_handler = MessageHandler(Filters.text, do_echo)
    help_handler = CommandHandler("help", do_help)
    random_image = CommandHandler("poshutipic", do_random_image)
    random_gif = CommandHandler("poshutigif", do_random_gif)
    buttons_handler = CallbackQueryHandler(callback=call_keyboard, pass_chat_data=True)

    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(echo_handler)
    updater.dispatcher.add_handler(help_handler)
    updater.dispatcher.add_handler(random_image)
    updater.dispatcher.add_handler(random_gif)
    updater.dispatcher.add_handler(buttons_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
