
import telebot
import validators
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

import publishReel
import donwload
import publishVideo

# Tu token de Telegram
TOKEN = '6777968775:AAGgGcfLXRNYLB2oWjNIpF1bZv0pG7T21tA'

bot = telebot.TeleBot(TOKEN)

# Opciones de menú disponibles
menu_options = ["perexa", "yuls","frank","shinchan"]

# Diccionario para almacenar temporalmente los enlaces recibidos
user_links = {}


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Send me a link to publish.")


@bot.message_handler(func=lambda message: True)
def receive_link(message):
    link = message.text
    if validate_link(link):
        user_links[message.chat.id] = link
        bot.send_message(message.chat.id, "Please select a menu to publish the link:",
                         reply_markup=generate_menu_markup())
    else:
        bot.reply_to(message, "Invalid link. Please provide a valid link.")


def validate_link(link):
    return validators.url(link)


def generate_menu_markup():
    markup = InlineKeyboardMarkup()
    for index, option in enumerate(menu_options):
        markup.add(InlineKeyboardButton(option, callback_data=str(index)))
    return markup


@bot.callback_query_handler(func=lambda call: True)
def handle_menu_selection(call):
    link = user_links.get(call.message.chat.id)
    if link:
        menu_option = int(call.data)
        publish_link(call.message, menu_options[menu_option], link)
    else:
        bot.send_message(call.message.chat.id, "Error: No link found.")
    # bot.answer_callback_query(call.id)


def publish_link(message, menu_option, link):
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                          text=f"Publishing link to {menu_option}...")
    print(f"Publishing link '{link}' to {menu_option}...")
    # Aquí agregar la lógica para publicar el enlace en el menú seleccionado
    donwload.execute(link)
    if menu_option == "frank" or menu_option == "shinchan":
        publishVideo.main(menu_option)
    else:
        publishReel.main(menu_option)
    bot.send_message(message.chat.id, f"Link published to {menu_option} successfully.")


def main():
    bot.polling()


if __name__ == '__main__':
    main()
