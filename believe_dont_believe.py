import logging
import sqlite3
from random import randint

from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Updater, ConversationHandler, CallbackQueryHandler, MessageHandler, Filters

from facts import *

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)
logger = logging.getLogger(__name__)
TOKEN = '5346789615:AAGsYMrZrCudqdfLQSkMZXtbrEHItVJEg7M'

keyboard = [
    [InlineKeyboardButton("Верю", callback_data='1'),
     InlineKeyboardButton("Не верю", callback_data='0')],
]
reply_markup = InlineKeyboardMarkup(keyboard)

key_for_new_fact = [
    [InlineKeyboardButton("Правда", callback_data='True'),
     InlineKeyboardButton("Ложь", callback_data='False')],
]
new_fact_markup = InlineKeyboardMarkup(key_for_new_fact)

used_answers = []
answer = ()
for i in range(1, 35):
    used_answers.append(i)

reply_keyboard = [['Правда'],
                  ['Ложь']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


def poisk():
    global answer, used_answers
    con = sqlite3.connect("project")
    cur = con.cursor()
    number = randint(1, 34)
    while number not in used_answers:
        number = randint(1, 34)
    result = cur.execute("""SELECT * FROM FACT
              WHERE id= ?""", (number,)).fetchall()

    answer = result[0]
    del used_answers[used_answers.index(answer[0])]
    con.close()
    print(used_answers)
    return answer


def start(update, context):
    update.message.reply_text(
        'Привет 👋. Я прелагаю тебе сыграть со мной в игру "Верю не верю!" 😄\n'
        'Используй 👇👇👇\n'
        '/play — Чтобы начать играть🧩\n'
        '/add — Если хочешь добавить свое интересное высказывание 🧨'
    )


def play(update, context):  # начало игры
    fact = poisk()
    print(fact)
    update.message.reply_text("Чтобы перейти к следующему высказыванию воспользуйтесь /fact\n"
                              "Начали🧭", reply_markup=ReplyKeyboardRemove())
    update.message.reply_text(fact[1], reply_markup=reply_markup)
    return next


def fact(update, context):
    fact = poisk()
    update.message.reply_text(fact[1], reply_markup=reply_markup)


def check_answer(update, context):  # фукция обрабатывает нажатие кнопок "верю не верю"
    query = update.callback_query
    variant = query.data
    query.answer()

    ID, key, pic = answer[0], answer[2], answer[3]
    if pic == 1:
        photo = f"images/{ID}.jpg"
        chat_id = update.effective_chat.id
        context.bot.send_photo(chat_id=chat_id, photo=open(photo, 'rb'))

    if str(variant) == str(key):
        # создать список, кторый рандомно будет выбирать что ответить
        query.edit_message_text(text=f"{true_answer[randint(0, 3)]}\n"
                                     f"{facts[ID]}")
    else:
        query.edit_message_text(text=f"{false_answer[randint(0, 2)]}\n"
                                     f"{facts[ID]}")


def add(name1, key1):  # добавить новый факт
    con = sqlite3.connect("new_fact")
    cur = con.cursor()

    cur.execute(f"INSERT INTO fact(name, key) VALUES(?, ?)", (name1, key1)).fetchall()
    con.commit()


def add_fact(update, context):
    update.message.reply_text("Интересный факт! ❓\n"
                              "Сейчас ты помогаешь сделать игру в разы интереснее 🌈\n"
                              "Чтобы продолжить, введи высказывание, которое ты хочешь добавить 🌝\n"
                              "Если ты уже передумал, введи команду /stop")
    return "fact"


def new_fact(update, context):
    context.user_data['fact'] = update.message.text
    update.message.reply_text("Отлично, теперь мне надо знать, является ли твое высказывание фактом"
                              " или убедительной ложью", reply_markup=markup)
    return "key"


def new_key(update, context):
    key = update.message.text
    context.user_data['key'] = key
    if str(key) == "Правда":
        context.user_data['key'] = 1

    elif str(key) == "Ложь":
        context.user_data['key'] = 0
    add(context.user_data['fact'], context.user_data['key'])

    update.message.reply_text("Спасибо за помощь!", reply_markup=ReplyKeyboardRemove())
    update.message.reply_text("Твое высказывание добавлено в список на рассмотрение.")
    return ConversationHandler.END


def stop(update, context):
    update.message.reply_text("Всего доброго!")
    return ConversationHandler.END


def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))

    dp.add_handler(CommandHandler("play", play))
    dp.add_handler(CallbackQueryHandler(check_answer))
    dp.add_handler(CommandHandler("fact", fact))

    add_handler = ConversationHandler(
        entry_points=[CommandHandler('add', add_fact)],
        states={
            "fact": [MessageHandler(Filters.text & ~Filters.command, new_fact)],
            "key": [MessageHandler(Filters.text & ~Filters.command, new_key)]
        },

        fallbacks=[CommandHandler('stop', stop)]
    )
    dp.add_handler(add_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
