from main import bot

def start(message):
    bot.send_message(message.chat.id, "Здравствуйте, бот готов к работе!")

def info(message):
    bot.send_message(message.chat.id, "Информация о боте")

def help(message):
    bot.send_message(message.chat.id, "Помощь в пользовании ботом")

def usr_msg(message):
    print("[log] Текстовое сообщение")
