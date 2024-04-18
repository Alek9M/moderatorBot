import datetime


class Member:

    FirestoreCollection = "members"

    id: str
    username: str

    def __init__(self, id: int, username: str):
        self.id = str(id)
        self.username = username

    def fire(self):
        return {"username": self.username}


class Metage:
    FirestoreCollection = "metages"

    date: datetime
    length: int

    def __init__(self, date: datetime, length: int):
        self.date = date
        self.length = length

    def fire(self):
        return {"date": self.date, "length": self.length}


class Group:

    FirestoreCollection = "groups"

    id: str
    title: str
    admin_id: str

    def __init__(self, id: int, title: str, admin_id: int = None):
        self.id = str(id)
        self.title = title
        if admin_id is not None:
            self.admin_id = str(admin_id)
        else:
            self.admin_id = None


    def fire(self):
        if self.admin_id is None:
            return {"id": self.id, "title": self.title}
        else:
            return {"id": self.id, "title": self.title, "admin_id": self.admin_id}
