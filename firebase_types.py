import datetime
from abc import abstractmethod
from typing import Protocol

from telegram import Message


class FireType(Protocol):
    FirestoreCollection: str

    @abstractmethod
    def fire(self) -> dict:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def derive(message: Message) -> "FireType":
        raise NotImplementedError


class Member(FireType):
    FirestoreCollection = "members"

    id: str
    username: str

    def __init__(self, id: int, username: str):
        self.id = str(id)
        self.username = username

    def fire(self):
        return {"username": self.username}

    @staticmethod
    def derive(message: Message) -> "Member":
        return Member(message.from_user.id, message.from_user.username)


class Metage(FireType):

    FirestoreCollection = "metages"

    date: datetime
    length: int
    thread: int | None

    def __init__(self, date: datetime, length: int, thread: int | None = None):
        self.date = date
        self.length = length
        self.thread = thread

    @staticmethod
    def derive(message: Message) -> "Metage":
        return  Metage(message.date, len(message.text), message.message_thread_id)

    def fire(self):
        if self.thread is None:
            return {"date": self.date, "length": self.length}
        else:
            return {"date": self.date, "length": self.length, "thread": self.thread}


class Group(FireType):
    FirestoreCollection = "groups"

    id: str
    title: str
    admin_id: str
    admin: Member

    notifying: str = None

    members: [Member] = []

    def __init__(self, id: int, title: str, admin_id: int = None, admin: Member = None):
        self.id = str(id)
        self.title = title
        if admin_id is not None:
            self.admin_id = str(admin_id)
        if admin is not None:
            # TODO: save admin username
            self.admin = admin


    @staticmethod
    def derive(message: Message) -> "Group":
        return Group(message.chat.id, message.chat.title)

    def fire(self):
        if self.admin_id is None:
            return {"id": self.id, "title": self.title}
        else:
            return {"id": self.id, "title": self.title, "admin_id": self.admin_id}
