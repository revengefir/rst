from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import platform
import psutil
import json
import socket
import speedtest

with open("config.json", mode="r") as config_file:
    config = json.load(config_file)



TOKEN = config["token"]
BOT_USERNAME = config["username"]

print ("Получение сетевой и прочей информации о системе.")

s = speedtest.Speedtest()
s.get_best_server()

sdownload = (s.download() / 1000000)
udownload = (s.upload() / 1000000)
sping = s.results.ping

hostname = socket.gethostname()
IP = socket.gethostbyname(hostname) 

systeminfo = platform.freedesktop_os_release()
systemname = systeminfo["NAME"]
systemver =  systeminfo ["VERSION"]

print ("Готово.")

# Переменные для команд


# Info
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Добро пожаловать в RST! - пропишите /help.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Добро пожаловать в справку о боте RST \n Тут имеется несколько команд \n /cpuc - Процент загрузки CPU \n /ram, /usedram, /availableram - информация об оперативной памяти \n /linver - название и версия операционной системы \n /sent, /recv - информация по отправленным/полученным сетевым пакетам \n /cpu - время работы процессора \n /temp температуры системы \n Скорость интернета Download/Upload - /download, /upload. Пинг - /ping. IP машины - /ip")

# Baza
async def cpuc_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Загружено: " + str(psutil.cpu_percent())+ " %")
    
async def ram_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Всего: " + str(round(psutil.virtual_memory().total / (1024.00 **3)))+" GB")

async def usedram_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Занято: " + str(psutil.virtual_memory().percent) + " % оперативной памяти")
    
async def availableram_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Доступно: " + str(psutil.virtual_memory().available / (1024 **3)) + " GB")
    
async def linuxversion_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Информация о системе: " + "Система: " + systemname + " Версия: " + systemver)
    
    
#Network Features

async def download_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(str(sdownload) + "Mbps")

async def upload_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(str(udownload) + "Mbps")

async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(str(sping) + "MS")

async def ip_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ваш IP адрес: " + IP)
    
async def sent_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Отправленные пакеты: " + str((psutil.net_io_counters(pernic=False, nowrap=True).packets_sent)))
    
async def recv_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Полученные пакеты: " + str(psutil.net_io_counters(pernic=False, nowrap=True).packets_recv))
    
    
#SysMonitor
async def temp_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Температуры " + str(psutil.sensors_temperatures()) + "C")
async def cpu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Частоты " + str(psutil.cpu_times(percpu=False)))
    
    

# Define message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Your message handling logic goes here
    pass

# Define error handler
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Обновление {update} произошла ошибка {context.error}")

if __name__ == '__main__':
    print('Запуск ...')
    app = Application.builder().token(TOKEN).build()

    # Register command handlers
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('cpu', cpu_command))
    app.add_handler(CommandHandler('cpuc', cpuc_command))
    app.add_handler(CommandHandler('ram', ram_command))
    app.add_handler(CommandHandler('usedram', usedram_command))
    app.add_handler(CommandHandler('availableram', availableram_command))
    app.add_handler(CommandHandler('linver', linuxversion_command))
    app.add_handler(CommandHandler('sent', sent_command))
    app.add_handler(CommandHandler('recv', recv_command))
    app.add_handler(CommandHandler('temp', temp_command))
    app.add_handler(CommandHandler('ip', ip_command))
    app.add_handler(CommandHandler('download', download_command))
    app.add_handler(CommandHandler('upload', upload_command))
    app.add_handler(CommandHandler('ping', ping_command))
    # Register message handler
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Register error handler
    app.add_error_handler(error)

    # Start polling
    print("Опрос...")
    app.run_polling(poll_interval=3)
