# This is a sample Python script.
import logging
import os

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, CommandHandler, CallbackQueryHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

from FireBasedFilters import SupergroupFilter, UnregisteredMember, UnregisteredGroup, PrivateFilter, RegisteredGroup, \
    Subscribed, Admin
from firebase import Firebase
from firebase_types import Group, Member, Metage
from moderator import Moderator

load_dotenv()
logging.basicConfig(level=logging.WARNING)

firebase = Firebase()

async def register_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    group = Group.derive(update.message)
    member = Member.derive(update.message)
    firebase.add_member(member, group)


async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if (password := context.args[0]) and len(context.args) == 1:
        if password == os.getenv('PASSWORD'):
            group = Group.derive(update.message)
            group.admin_id = update.message.from_user.id
            member = Member.derive(update.message)
            group.admin = member
            firebase.register(group, member)
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Registered✅\n⚠️Starting now all messages in this chat are being processed for moderation assessment")


async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    member = Member.derive(update.message)
    await _subscribe(member, context)
    # firebase.subscribe(member)
    # await context.bot.send_message(chat_id=update.effective_chat.id, text="Subscribed ✅")


async def _subscribe(member: Member, context):
    firebase.subscribe(member)
    await context.bot.send_message(chat_id=member.id, text="Subscribed ✅")


async def unsubscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    member = Member.derive(update.message)
    firebase.unsubscribe(member)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Unsubscribed :c")

async def meta_watch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    metage = Metage.derive(update.message)
    member = Member.derive(update.message)
    group = Group.derive(update.message)
    firebase.set_meta(member, metage, group)
    await ananlyse(update, context)

async def ananlyse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    group = Group.derive(update.message)
    if danger := Moderator.is_harmful(update.message.text):
        await context.bot.send_message(chat_id=update.effective_chat.id, text=Firebase().group_notification(group) + "\n" + danger, reply_to_message_id=update.message.message_id, message_thread_id=update.message.message_thread_id)


async def terms(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
            InlineKeyboardButton("Yes ✍️", callback_data="1"),
            InlineKeyboardButton("No 🙅‍️", callback_data="2"),
        ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="We are going to ananlyse how often + how much users text. And might shoot you a rare private message. *Is that ok?*\nYou can always /unsubscribe later", reply_markup=reply_markup)


async def private_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    if query.data == "1":
        member = Member(update.effective_user.id, update.effective_user.username)
        await _subscribe(member, context)
    elif query.data == "2":
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Sure 🤷🏼")
    await query.answer()

async def set_moderators(update: Update, context: ContextTypes.DEFAULT_TYPE):
    firebase.set_group_notification(Group.derive(update.message), " ".join(context.args))


registration_handler = CommandHandler('start', register, SupergroupFilter() & UnregisteredGroup())
terms_handler = CommandHandler('start', terms, PrivateFilter())
moderator_notification_handler = CommandHandler('notify', set_moderators, Admin())
userlist_handler = MessageHandler(SupergroupFilter() & RegisteredGroup() & UnregisteredMember(), register_member)
subscriber_handler = CommandHandler("subscribe", subscribe, PrivateFilter())
unsubscriber_handler = CommandHandler("unsubscribe", unsubscribe, PrivateFilter())
meta_handler = MessageHandler(filters.TEXT & SupergroupFilter() & RegisteredGroup() & Subscribed(), meta_watch)
language_handler = MessageHandler(filters.TEXT & SupergroupFilter() & RegisteredGroup(), ananlyse)

if __name__ == '__main__':
    application = ApplicationBuilder().token(os.getenv('TBOT_KEY')).build()

    application.add_handler(moderator_notification_handler)
    application.add_handler(registration_handler)
    application.add_handler(terms_handler)
    application.add_handler(subscriber_handler)
    application.add_handler(unsubscriber_handler)
    application.add_handler(userlist_handler)
    application.add_handler(meta_handler)
    application.add_handler(language_handler)
    application.add_handler(CallbackQueryHandler(private_button))

    application.run_polling()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
