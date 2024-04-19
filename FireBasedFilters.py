from telegram.ext.filters import MessageFilter

from firebase import Firebase
from firebase_types import Group, Member


class SupergroupFilter(MessageFilter):
    def filter(self, message):
        return message.chat.type == 'supergroup'

class PrivateFilter(MessageFilter):
    def filter(self, message):
        return message.chat.type == 'private'

class UnregisteredMember(MessageFilter):
    def filter(self, message):
        group = Group(message.chat.id, message.chat.title)
        member = Member(message.from_user.id, message.from_user.username)
        exists = Firebase().member_exists(group, member)
        return not exists


class UnregisteredGroup(MessageFilter):
    def filter(self, message):
        group = Group(message.chat.id, message.chat.title)
        return not Firebase().group_exists(group)


class RegisteredGroup(MessageFilter):
    def filter(self, message):
        group = Group(message.chat.id, message.chat.title)
        return Firebase().group_exists(group)

class Subscribed(MessageFilter):
    def filter(self, message):
        member = Member(message.from_user.id, message.from_user.username)
        group = Group(message.chat.id, message.chat.title)
        return Firebase().subscriber_exists(member, soft_search=True)


class Admin(MessageFilter):
    def filter(self, message):
        member = Member(message.from_user.id, message.from_user.username)
        group = Group(message.chat.id, message.chat.title)
        return Firebase().is_admin(group, member)

class SomeoneLeft(MessageFilter):
    def filter(self, message):
        return hasattr(message, "left_chat_member") and (message.left_chat_member is not None)


class SomeoneJoined(MessageFilter):
    def filter(self, message):
        return hasattr(message, "new_chat_members") and (message.new_chat_members is not None) and len(message.new_chat_members) > 0
