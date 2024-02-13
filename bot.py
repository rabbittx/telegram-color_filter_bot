from PIL import Image
import os ,logging , glob
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
from telegram import Update
import logging
from dotenv import load_dotenv



class ColorFilterBot:
    def __init__(self, token):
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                           level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.updater = Updater(token, use_context=True)
        self.dp = self.updater.dispatcher
        self.setup_handlers()
        self.logger.info('[+]  Bot started')
      

    def setup_handlers(self):
        self.logger.info('[+] setup handler ... ')
        self.dp.add_handler(CommandHandler("start", self.start_command))
        self.dp.add_handler(CommandHandler("help", self.help_command))
        conversation_handler = ConversationHandler(
            entry_points=[
                CommandHandler("black_white", self.get_black_white),
                CommandHandler("blue", self.get_blue),
                CommandHandler("red", self.get_red),
                CommandHandler("3d", self.get_3d),
            ],
            states={
                "black_white": [MessageHandler(Filters.photo, self.black_white_filter)],
                "blue": [MessageHandler(Filters.photo, self.blue_filter)],
                "red": [MessageHandler(Filters.photo, self.red_filter)],
                "3d": [MessageHandler(Filters.photo, self.red_blue_3d_filter)],
            },
            fallbacks=[],
            allow_reentry=True
        )
        self.dp.add_handler(conversation_handler)
        self.logger.info('[+] command handler ready')

    def start(self):
        self.logger.info('[+] starting to get command')
        self.dp.add_error_handler(self.error)        
        self.updater.start_polling()
        self.updater.idle()

    def get_black_white(self, update: Update, context: CallbackContext) -> str:
        self.logger.info('[+] geting image for the black and white filter')
        chat_id = update.effective_chat.id
        context.bot.send_message(chat_id=chat_id, text="send me your image !")
        return "black_white"

    def get_blue(self,update: Update, context: CallbackContext) -> str:
        self.logger.info('[+] geting image for the blue filter')
        chat_id = update.effective_chat.id
        context.bot.send_message(chat_id=chat_id, text="send me your image !")
        return "blue"

    def get_red(self,update: Update, context: CallbackContext) -> str:
        self.logger.info('[+]  geting image for the red filter')
        chat_id = update.effective_chat.id
        context.bot.send_message(chat_id=chat_id, text="send me your image !")
        return "red"

    def get_3d(self,update: Update, context: CallbackContext) -> str:
        self.logger.info('[+]  geting image for red and blue filter')
        chat_id = update.effective_chat.id
        context.bot.send_message(chat_id=chat_id, text="send me your image !")
        return "3d"  

    def black_white_filter(self, update: Update, context: CallbackContext):
        self.logger.info('[+] start to apply black and white filter to image')
        try:
            chat_id = update.effective_chat.id
            file = context.bot.getFile(update.message.photo[-1].file_id)
            file.download('originalPic.jpg')
            Image.open('originalPic.jpg').convert("L").save("BW.jpg")
            context.bot.send_message(chat_id=chat_id, text="you image is black and white now !")
            context.bot.send_photo(chat_id=chat_id, photo=open('BW.jpg', 'rb'))
            self.remove_image()
        except Exception as get_image_error:
            chat_id = update.effective_chat.id
            context.bot.send_message(chat_id=chat_id, text=f"something is wrong try one more time {get_image_error}")

    def blue_filter(self,update: Update, context: CallbackContext):
        self.logger.info('[+] start to apply blue filter to image')       
        try:
            chat_id = update.effective_chat.id
            file = context.bot.getFile(update.message.photo[-1].file_id)
            file.download('originalPic.jpg')
            img = self.change_pixels('originalPic.jpg', -30, -30, 100)  
            img.save("BlueFiltered.jpg")
            context.bot.send_photo(chat_id=chat_id, photo=open('BlueFiltered.jpg', 'rb'))
            self.remove_image()
        except Exception as get_image_error:
            context.bot.send_message(chat_id=chat_id, text=f"Error: {get_image_error}")

    def red_filter(self,update: Update, context: CallbackContext):
        self.logger.info('[+] start to apply red filter to image')       
        try:
            chat_id = update.effective_chat.id
            file = context.bot.getFile(update.message.photo[-1].file_id)
            file.download('originalPic.jpg')
            img = self.change_pixels('originalPic.jpg', 100, -30, -30)  
            img.save("RedFiltered.jpg")
            context.bot.send_photo(chat_id=chat_id, photo=open('RedFiltered.jpg', 'rb'))
            self.remove_image()
        except Exception as get_image_error:
            context.bot.send_message(chat_id=chat_id, text=f"Error: {get_image_error}")


    def red_blue_3d_filter(self,update: Update, context: CallbackContext):
        self.logger.info('[+] start to apply 3d filter to image')       
        try:
            chat_id = update.effective_chat.id
            file = context.bot.getFile(update.message.photo[-1].file_id)
            file.download('originalPic.jpg')
            img = self.change_pixels('originalPic.jpg', 50, -50, 50)  
            img.save("RedBlue3DFiltered.jpg")
            context.bot.send_photo(chat_id=chat_id, photo=open('RedBlue3DFiltered.jpg', 'rb'))
            self.remove_image()
        except Exception as get_image_error:
            context.bot.send_message(chat_id=chat_id, text=f"Error: {get_image_error}")


    def remove_image(self,):
        self.logger.info('[+] start to remove image')       

        try:
            for i in glob.glob("*.jpg"):
                os.remove(i)
        except Exception as delete_error:
            self.logger.error("something is wrong file not removed")

    def color_filter(self,pixel, color):
        return tuple(max(0, min(255, pixel[i] + color[i])) for i in range(3))

    def change_pixels(self,image_path, red, green, blue):
        self.logger.info('apply filter to image pixels')
        img = Image.open(image_path)
        pixels = img.load()
        for i in range(img.size[0]):
            for j in range(img.size[1]):
                if pixels[i, j] > (230, 230, 230):
                    continue
                else:
                    pixels[i, j] = self.color_filter(pixels[i, j], (red, green, blue))
        return img

    def start_command(self, update: Update, context: CallbackContext):
        self.logger.info(f"User {update.effective_user.id} started the bot.", )
        update.message.reply_text(
            "سلام! من یک ربات تلگرام هستم که می‌توانم فیلترهای رنگی را به تصاویر شما اضافه کنم.\n"
            "برای استفاده از قابلیت‌های من، یکی از دستورات زیر را وارد کنید:\n"
            "/black_white - تبدیل تصویر به سیاه و سفید\n"
            "/blue - افزودن فیلتر آبی به تصویر\n"
            "/red - افزودن فیلتر قرمز به تصویر\n"
            "/3d - افزودن افکت سه بعدی قرمز و آبی به تصویر\n"
            "/help - نمایش این راهنما"
        )

    def help_command(self, update: Update, context: CallbackContext):
        self.logger.info(f"User {update.effective_user.id} asked for help.", ) 
        update.message.reply_text(
            "شما می‌توانید با ارسال تصویر و انتخاب یکی از دستورات زیر، فیلتر مورد نظر خود را اعمال کنید:\n"
            "/black_white - برای تبدیل تصویر به سیاه و سفید\n"
            "/blue - برای افزودن فیلتر آبی به تصویر\n"
            "/red - برای افزودن فیلتر قرمز به تصویر\n"
            "/3d - برای افزودن افکت سه بعدی قرمز و آبی\n"
            "برای شروع، فقط تصویری را ارسال کنید و دستور مربوطه را انتخاب نمایید."
        )

    def error(self, update, context):
        """Log Errors caused by Updates."""
        self.logger.warning(f'Update "{update}" caused error "{context.error}"',  )


if __name__ == '__main__':
    load_dotenv()  
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    color_filter_bot = ColorFilterBot(TOKEN)
    color_filter_bot.start()
