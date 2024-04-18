import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin.auth import Client

from firebase_types import Member, Group, Metage

cred = credentials.Certificate("firebase-serviceAccountKey.json")
app = firebase_admin.initialize_app(cred)

class Firebase:
    store: Client
    def __init__(self):
        self.store = firestore.client(app=app)


    def group_reference(self, group):
        return self.store.collection(Group.FirestoreCollection).document(group.id)
    def get_group(self, group: Group):
        doc = self.group_reference(group).get()
        if not doc.exists:
            return None

        return doc

    def group_exists(self, group: Group):
        doc = self.group_reference(group).get()
        exists = doc.exists
        return exists

    def member_exists(self, group: Group, member: Member):
        doc = self.member_reference(group, member).get()
        return doc.exists

    def subscriber_exists(self,member: Member):
        doc = self.store.collection(Member.FirestoreCollection).document(member.id).get()
        return doc.exists

    def member_reference(self, group: Group, member: Member):
        return self.group_reference(group).collection(Member.FirestoreCollection).document(member.id)
    def register(self, group: Group, by: Member):
        if self.group_exists(group): return

        self.group_reference(group).set(group.fire())
        self.member_reference(group, by).set(by.fire())

    def add_member(self, member: Member, group: Group):
        self.member_reference(group, member).set(member.fire())

    def subscribe(self, member: Member):
        self.store.collection(Member.FirestoreCollection).document(member.id).set(member.fire())


    def set_meta(self, member: Member, metage: Metage, group: Group):
        self.member_reference(group, member).collection(Metage.FirestoreCollection).document(str(metage.date)).set(
            metage.fire())

    def get_admin_username(self, group: Group) -> str:
        doc = self.group_reference(group).get()
        group_admin = doc.to_dict()['admin_id']
        admin = self.member_reference(group, Member(group_admin, "")).get()
        return admin.to_dict()['username']