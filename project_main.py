import logging

from telegram.ext import CommandHandler, Updater, Filters, MessageHandler, ConversationHandler

from project.constanta import *

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)
logger = logging.getLogger(__name__)
TOKEN = '5346789615:AAGsYMrZrCudqdfLQSkMZXtbrEHItVJEg7M'


class learning_AND_decision:
    def __init__(self):
        pass

    def choice(self, update, context):
        print(56676764)
        context.user_data['next_decision'] = update.message.text
        print(context.user_data)

        update.message.reply_text(
            "Выберите тему или начните изучение с самого начала\n"
            "---> Механика\n"
            "---> Молекулярная физика\n"
            "---> Атомная физика\n"
            "---> Я хочу начать узучение с самого начала)"
        )


def start(update, context):
    update.message.reply_text(
        "Привет. Я бот, готовый поомочь тебе с подготовкой к ЕГЭ по физике!\n"
        "Вы можете прервать наш диалог, послав команду /stop.\n"
        "Выберите то, что вам подходит!\n"
        "--> Хочу приступить к изучению темы и решению задач\n"
        "--> Хочу начать решать задачи!\n"
        "--> Блиц тест!")

    return 1


def decision_response(update, context):
    # Сохраняем ответ в словаре.
    context.user_data['decision'] = update.message.text
    print(context.user_data, context.user_data['decision'] == decisions[0])
    update.message.reply_text(
        "Выберите тему или начните изучение с самого начала\n"
        "---> Механика\n"
        "---> Молекулярная физика\n"
        "---> Атомная физика\n"
        "---> Я хочу начать узучение с самого начала)"
    )
    return 2
    #     if context.user_data['decision'] == decisions[0]:
    #         print(23)
    #
    #     elif context.user_data['decision'] == decisions[1]:
    #         print(24)
    #     elif context.user_data['decision'] == decisions[2]:
    #         print(25)


def choice(update, context):
    context.user_data['next_decision'] = update.message.text

    update.message.reply_text(
        "Выберите тему или начните изучение с самого начала\n"
        "---> Механика\n"
        "---> Молекулярная физика\n"
        "---> Атомная физика\n"
        "---> Я хочу начать узучение с самого начала)"
    )
    return 3

# return ConversationHandler.END


def stop(update, context):
    update.message.reply_text("Всего доброго!")
    return ConversationHandler.END


def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            1: [MessageHandler(Filters.text & ~Filters.command, decision_response)],
            2: [MessageHandler(Filters.text & ~Filters.command, choice)]
        },

        fallbacks=[CommandHandler('stop', stop)]
    )
    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
