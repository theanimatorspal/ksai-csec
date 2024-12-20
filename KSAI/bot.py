import telebot
import subprocess
import time

BOT_TOKEN = "8128117790:AAHhKWnFTuk4DIeFsl1xyBiUsYxovpzm-_w"
PARSE_MODE = "Markdown"
bot = telebot.TeleBot(BOT_TOKEN)
user_modes = {}
active_processes = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    print(f"Chat ID: {message.chat.id}, Command: /start")
    bot.reply_to(message, "Welcome! Use /mode to switch between WSL and CMD, send commands to execute them, and use /stop to terminate the current command.")

@bot.message_handler(commands=['mode'])
def set_mode(message):
    chat_id = message.chat.id
    current_mode = user_modes.get(chat_id, "CMD")
    new_mode = "WSL" if current_mode == "CMD" else "CMD"
    user_modes[chat_id] = new_mode
    print(f"Chat ID: {chat_id}, Mode switched to: {new_mode}")
    bot.reply_to(message, f"Mode switched to {new_mode}.")

@bot.message_handler(commands=['stop'])
def stop_command(message):
    chat_id = message.chat.id
    process = active_processes.get(chat_id)
    if process and process.poll() is None:
        process.terminate()
        active_processes.pop(chat_id, None)
        print(f"Chat ID: {chat_id}, Command terminated")
        bot.reply_to(message, "The command was terminated.")
    else:
        print(f"Chat ID: {chat_id}, No active command to terminate")
        bot.reply_to(message, "No active command to terminate.")

@bot.message_handler(commands=['hello'])
def toggle_code_block(message):
    global PARSE_MODE
    PARSE_MODE = None if PARSE_MODE == "Markdown" else "Markdown"
    print(f"Chat ID: {message.chat.id}, Parse mode toggled to: {PARSE_MODE}")

@bot.message_handler(func=lambda message: True)
def execute_command(message):
    chat_id = message.chat.id
    mode = user_modes.get(chat_id, "CMD")
    shell = "bash" if mode == "WSL" else None
    command = message.text
    print(f"Chat ID: {chat_id}, Mode: {mode}, Command: {command}")

    try:
        status_message = bot.send_message(chat_id, "Executing...\n")
        process = subprocess.Popen(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, executable=shell
        )
        active_processes[chat_id] = process
        output = ""
        last_update_time = time.time()

        for line in iter(process.stdout.readline, ""):
            if chat_id not in active_processes:
                break
            output += line
            current_time = time.time()
            if current_time - last_update_time >= 0.5:
                bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=status_message.message_id,
                    text=f"```\n{output}\n```",
                    parse_mode="Markdown"
                )
                last_update_time = current_time

        process.wait()
        active_processes.pop(chat_id, None)
        if process.returncode != 0:
            output += f"\nCommand failed with return code {process.returncode}."
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=status_message.message_id,
            text=f"```\n{output.strip()}\n```",
            parse_mode=PARSE_MODE
        )
        print(f"Chat ID: {chat_id}, Command output: {output.strip()}, Return code: {process.returncode}")
    except Exception as e:
        print(f"Chat ID: {chat_id}, Error: {e}")
        bot.send_message(chat_id, f"Failed to execute command: {e}")
    finally:
        active_processes.pop(chat_id, None)

bot.polling()
