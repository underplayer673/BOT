import os
from threading import Thread

from flask import Flask
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters


web_app = Flask(__name__)

HELLO_TEXT = "\U0001f44b \u041f\u0440\u0438\u0432\u0435\u0442"
BYE_TEXT = "\U0001f44b \u041f\u043e\u043a\u0430"
START_MESSAGE = "\U0001f44b \u041f\u0440\u0438\u0432\u0435\u0442! \u0427\u0442\u043e \u0445\u043e\u0442\u0438\u0442\u0435?"

START_KEYBOARD = ReplyKeyboardMarkup(
    [[HELLO_TEXT, BYE_TEXT]],
    resize_keyboard=True,
    is_persistent=True,
)

HELLO_ONLY_KEYBOARD = ReplyKeyboardMarkup(
    [[HELLO_TEXT]],
    resize_keyboard=True,
    is_persistent=True,
)


@web_app.get("/")
def health_check() -> str:
    return "Bot is running"


def start_web_server() -> None:
    port = int(os.environ.get("PORT", "10000"))
    web_app.run(host="0.0.0.0", port=port)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        START_MESSAGE,
        reply_markup=START_KEYBOARD,
    )


async def answer_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text.lower()

    if "\u043f\u0440\u0438\u0432\u0435\u0442" in text:
        await update.message.reply_text(
            START_MESSAGE,
            reply_markup=START_KEYBOARD,
        )
        return

    if "\u043f\u043e\u043a\u0430" in text:
        await update.message.reply_text(
            "\U0001f44b \u041f\u043e\u043a\u0430!",
            reply_markup=HELLO_ONLY_KEYBOARD,
        )
        return

    await update.message.reply_text(
        "\U0001f642 \u041d\u0430\u0436\u043c\u0438\u0442\u0435 \u043a\u043d\u043e\u043f\u043a\u0443 \u043d\u0438\u0436\u0435.",
        reply_markup=START_KEYBOARD,
    )


def main() -> None:
    token = os.environ.get("BOT_TOKEN")

    if not token:
        raise RuntimeError(
            "\u0414\u043e\u0431\u0430\u0432\u044c\u0442\u0435 \u0442\u043e\u043a\u0435\u043d "
            "\u0431\u043e\u0442\u0430 \u0432 \u043f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u0443\u044e "
            "\u043e\u043a\u0440\u0443\u0436\u0435\u043d\u0438\u044f BOT_TOKEN."
        )

    Thread(target=start_web_server, daemon=True).start()

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, answer_buttons))

    print(
        "\u0411\u043e\u0442 \u0437\u0430\u043f\u0443\u0449\u0435\u043d. "
        "\u041d\u0430\u0436\u043c\u0438\u0442\u0435 Ctrl+C, \u0447\u0442\u043e\u0431\u044b "
        "\u043e\u0441\u0442\u0430\u043d\u043e\u0432\u0438\u0442\u044c."
    )
    app.run_polling()


if __name__ == "__main__":
    main()
