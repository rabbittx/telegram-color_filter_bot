from PIL import Image
import glob
import os
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


def remove_image():
    try:
        for i in glob.glob("*.jpg"):
            os.remove(i)
    except Exception as delete_error:
        print("something is wrong file not removed")

def get_black_white(bot, update):
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text="send me your image !")
    return "black_white"


def black_white_filter(bot, update):
    # is there any way to didn't download image ?and add filter on it ?
    try:
        chat_id = update.message.chat_id
        file = bot.getFile(update.message.photo[-1].file_id)
        file.download('originalPic.jpg')
        Image.open('originalPic.jpg').convert("L").save("BW.jpg")
        bot.send_message(chat_id=chat_id, text="you image is black and white now !")
        bot.send_photo(chat_id=chat_id, photo=open('BW.jpg', 'rb'))
        remove_image()
    except Exception as get_image_error:
        chat_id = update.message.chat_id
        bot.send_message(chat_id=chat_id, text=f"something is wrong try one more time {get_image_error}")


def main():
    updater = Updater('token is here ! ')
    db = updater.dispatcher
    conversation_handler = ConversationHandler(
        entry_points=[
            CommandHandler("black_white", get_black_white),

        ],

        states={
            "black_white": [MessageHandler(Filters.photo, black_white_filter)],
        },
        fallbacks=[
            MessageHandler(Filters.photo, black_white_filter),
            CommandHandler("black_white", get_black_white),
        ],
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