from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup

BUTTON_IMG = "Комсопікча 🚀"
BUTTON_GIF = "Анімайка 👻"
BUTTON_TALK = "Аааа❔"
BUTTON_JOKE = "Щутка 👌"
BUTTON_HELP = "Памагітє❕"


def get_base_reply_keyboard():
    keyboard = [
        [
            KeyboardButton(BUTTON_GIF),
            KeyboardButton(BUTTON_IMG),
        ],
        [
            KeyboardButton(BUTTON_TALK),
            KeyboardButton(BUTTON_JOKE),
            KeyboardButton(BUTTON_HELP),
        ],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )
