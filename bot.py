import asyncio
import logging
import os

from dotenv import load_dotenv
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
    WebAppInfo,
)
from telegram.constants import ChatMemberStatus
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

load_dotenv()

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHANNEL = os.getenv("CHANNEL", "@Taiman")
CHANNEL_URL = os.getenv("CHANNEL_URL", "https://t.me/Taiman")

NFS_URL = "https://taimandevloper12.github.io/Need-for-speed/"
GTA_URL = "https://world-virtual.taimandev.workers.dev/"

logging.basicConfig(level=logging.INFO)

ALLOWED = (
    ChatMemberStatus.MEMBER,
    ChatMemberStatus.ADMINISTRATOR,
    ChatMemberStatus.OWNER,
)


async def is_subscribed(bot, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(CHANNEL, user_id)
        return member.status in ALLOWED
    except Exception as e:
        logging.warning("Obuna tekshirishda xato: %s", e)
        return False


def sub_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Taiman kanaliga obuna bo'lish", url=CHANNEL_URL)],
            [InlineKeyboardButton("Obunani tekshirish", callback_data="check")],
        ]
    )


def games_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("GTA", web_app=WebAppInfo(url=GTA_URL))],
            [InlineKeyboardButton("NFS", web_app=WebAppInfo(url=NFS_URL))],
        ]
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if await is_subscribed(context.bot, user.id):
        await show_games(update.message, context)
        return
    await update.message.reply_text(
        f"Salom, {user.first_name}!\n\n"
        "Botdan foydalanish uchun avval <b>Taiman</b> kanaliga obuna bo'ling, "
        "so'ng «Obunani tekshirish» tugmasini bosing.",
        parse_mode="HTML",
        reply_markup=sub_keyboard(),
    )


async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if await is_subscribed(context.bot, query.from_user.id):
        await query.answer("Obuna tasdiqlandi!")
        await query.message.delete()
        await show_games(query.message, context)
    else:
        await query.answer("Siz hali obuna bo'lmagansiz!", show_alert=True)


async def show_games(message, context: ContextTypes.DEFAULT_TYPE):
    msg = await message.chat.send_message("Yuklanmoqda")
    for text in ["Yuklanmoqda.", "Yuklanmoqda..", "Yuklanmoqda..."]:
        await asyncio.sleep(0.4)
        try:
            await msg.edit_text(text)
        except Exception:
            pass
    await msg.edit_text("O'yinni tanlang:", reply_markup=games_keyboard())


def main():
    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .connect_timeout(30)
        .read_timeout(30)
        .write_timeout(30)
        .pool_timeout(30)
        .get_updates_read_timeout(30)
        .build()
    )
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check, pattern="^check$"))
    app.run_polling()


if __name__ == "__main__":
    main()
