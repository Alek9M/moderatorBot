# This is a sample Python script.
import logging
import os

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, CommandHandler
from telegram import Update

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
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Registered")


async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    member = Member.derive(update.message)
    firebase.subscribe(member)

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
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Do you agree to T&C's? If yes reply /subscribe")

async def set_moderators(update: Update, context: ContextTypes.DEFAULT_TYPE):
    firebase.set_group_notification(Group.derive(update.message), " ".join(context.args))


registration_handler = CommandHandler('start', register, SupergroupFilter() & UnregisteredGroup())
terms_handler = CommandHandler('start', terms, PrivateFilter())
moderator_notification_handler = CommandHandler('notify', set_moderators, Admin())
userlist_handler = MessageHandler(SupergroupFilter() & RegisteredGroup() & UnregisteredMember(), register_member)
subscriber_handler = CommandHandler("subscribe", subscribe, PrivateFilter())
meta_handler = MessageHandler(filters.TEXT & SupergroupFilter() & RegisteredGroup() & Subscribed(), meta_watch)
language_handler = MessageHandler(filters.TEXT & SupergroupFilter() & RegisteredGroup(), ananlyse)

if __name__ == '__main__':
    application = ApplicationBuilder().token(os.getenv('TBOT_KEY')).build()

    application.add_handler(moderator_notification_handler)
    application.add_handler(registration_handler)
    application.add_handler(terms_handler)
    application.add_handler(subscriber_handler)
    application.add_handler(userlist_handler)
    application.add_handler(meta_handler)
    application.add_handler(language_handler)

    application.run_polling()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
