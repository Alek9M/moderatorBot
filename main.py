# This is a sample Python script.
import os

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, CommandHandler
from telegram import Update

from FireBasedFilters import SupergroupFilter, UnregisteredMember, UnregisteredGroup, PrivateFilter, RegisteredGroup
from firebase import Firebase
from firebase_types import Group, Member

load_dotenv()

firebase = Firebase()

async def register_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    group = Group(update.message.chat.id, update.message.chat.title, update.message.from_user.id)
    member = Member(update.message.from_user.id, update.message.from_user.username)
    firebase.add_member(member, group)


async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if (password := context.args[0]) and len(context.args) == 1:
        if password == os.getenv('PASSWORD'):
            group = Group(update.message.chat.id, update.message.chat.title, update.message.from_user.id)
            member = Member(update.message.from_user.id, update.message.from_user.username)
            firebase.register(group, member)
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Registered")


async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    member = Member(update.message.from_user.id, update.message.from_user.username)
    firebase.subscribe(member)

registration_handler = CommandHandler('start', register, UnregisteredGroup())
userlist_handler = MessageHandler(SupergroupFilter() & RegisteredGroup() & UnregisteredMember(), register_member)
subscriber_handler = MessageHandler(PrivateFilter(), subscribe)


if __name__ == '__main__':
    application = ApplicationBuilder().token(os.getenv('TBOT_KEY')).build()

    application.add_handler(registration_handler)
    application.add_handler(subscriber_handler)
    application.add_handler(userlist_handler)

    application.run_polling()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
