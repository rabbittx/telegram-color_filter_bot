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


def color_filter(pixel, color):
    return pixel[0]+color[0], pixel[1]+color[1], pixel[2]+color[2]


def change_pixels(image_path, red, green, blue):
    img = Image.open(image_path)
    pixels = img.load()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            # try to filter them better by find more rgb color
            if pixels[i, j] > (230, 230, 230):
                continue
            else:
                # (-150, -60, 160)
                pixels[i, j] = color_filter(pixels[i, j], (red, green, blue))
    return img

""" ************************************** Black-White start here !***************************************"""

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


""" ************************************** Black-White end here !***************************************"""

""" ************************************** blue start here !***************************************"""


def get_blue(bot, update):
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text="send me your image !")
    return "blue"


def blue_filter(bot, update):
    try:
        chat_id = update.message.chat_id
        file = bot.getFile(update.message.photo[-1].file_id)
        file.download('originalBluePic.jpg')
        # -150,-60,160
        img = change_pixels('originalBluePic.jpg', -150, -80, 130)
        img.save("blueImage.jpg")
        bot.send_message(chat_id=chat_id, text="blue filter is add to your image")
        bot.send_photo(chat_id=chat_id, photo=open('blueImage.jpg', 'rb'))
        remove_image()
    except Exception as get_image_error:
        chat_id = update.message.chat_id
        bot.send_message(chat_id=chat_id, text=f"something is wrong try one more time {get_image_error}")


""" *************************************** blue is end here***************************************"""


""" ***************************************red is start here***************************************"""


def get_red(bot, update):
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text="send me your image !")
    return "red"


def red_filter(bot, update):
    try:
        chat_id = update.message.chat_id
        file = bot.getFile(update.message.photo[-1].file_id)
        file.download('originalRedPic.jpg')
        # 75,-90,-110
        img = change_pixels('originalRedPic.jpg', 130, -90, -90)
        img.save("redImage.jpg")
        bot.send_message(chat_id=chat_id, text="red filter is add")
        bot.send_photo(chat_id=chat_id, photo=open('redImage.jpg', 'rb'))
        remove_image()
    except Exception as get_image_error:
        chat_id = update.message.chat_id
        bot.send_message(chat_id=chat_id, text=f"something is wrong try one more time {get_image_error}")


""" ***************************************red is end ***************************************"""

def main():
    updater = Updater('token is here !')
    db = updater.dispatcher
    conversation_handler = ConversationHandler(
        entry_points=[
            CommandHandler("black_white", get_black_white),
            CommandHandler("blue", get_blue),
            CommandHandler("red", get_red),

        ],

        states={
            "black_white": [MessageHandler(Filters.photo, black_white_filter)],
            "blue": [MessageHandler(Filters.photo, blue_filter)],
            "red": [MessageHandler(Filters.photo, red_filter)],
        },
        fallbacks=[
            MessageHandler(Filters.photo, black_white_filter),
            CommandHandler("black_white", get_black_white),
            MessageHandler(Filters.photo, blue_filter),
            CommandHandler("blue", get_blue),
            MessageHandler(Filters.photo, red_filter),
            CommandHandler("red", get_red),

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