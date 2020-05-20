from PIL import Image
from telegram.ext import Updater,\
                         CommandHandler,\
                         MessageHandler,\
                         Filters,\
                         ConversationHandler

# want make color filter for image
# get image from user
# find out pixels
# add filter
# send it back to user


def get_black_white(bot, update):
    # get ready to receive image
    return "black-white"


def black_white_filter(bot, update):
    try:
        # receive image from user
        # add filter
        # send it back to user
        pass
    except Exception as get_image_error:
        # if something was wrong get error!
        pass


def main():
    updater = Updater('token here ! ')
    db = updater.dispatcher
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("black-white", get_black_white)],

        states={"black-white": [MessageHandler(Filters.photo, black_white_filter)]},
        fallbacks=[MessageHandler(Filters.photo, black_white_filter),
                   CommandHandler("black-white", get_black_white),],
        allow_reentry=True,
        per_user=True,
        conversation_timeout=3600,
        name="test"
    )
    db.add_handler(conversation_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()