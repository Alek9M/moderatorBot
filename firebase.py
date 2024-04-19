import logging

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin.auth import Client

from firebase_types import Member, Group, Metage

cred = credentials.Certificate("firebase-serviceAccountKey.json")
app = firebase_admin.initialize_app(cred)

groups_local_copy: [Group] = []
subscribers_local_copy: [Member] = []

class Firebase:
    store: Client
    def __init__(self):
        self.store = firestore.client(app=app)
        logging.info("Firebase initialized")
        if len(groups_local_copy) == 0 or len(subscribers_local_copy) == 0:
            self.download()


    def group_reference(self, group):
        return self.store.collection(Group.FirestoreCollection).document(group.id)
    def get_group(self, group: Group):
        doc = self.group_reference(group).get()
        logging.warning("Got group")
        if not doc.exists:
            return None

        return doc

    def group_exists(self, group: Group) -> bool:
        if any(saved.id == group.id for saved in groups_local_copy):
            return True

        doc = self.group_reference(group).get()
        logging.warning("Got group for exist")
        exists = doc.exists
        return exists

    def member_exists(self, group: Group, member: Member) -> bool:
        for saved_group in [saved for saved in groups_local_copy if saved.id == group.id]:
            if any(saved.id == member.id for saved in saved_group.members):
                return True

        doc = self.member_reference(group, member).get()
        logging.warning("Got member for exist")
        return doc.exists

    def subscriber_exists(self,member: Member):
        if any(saved.id == member.id for saved in subscribers_local_copy):
            return True
        doc = self.store.collection(Member.FirestoreCollection).document(member.id).get()
        logging.warning("Got subscriber for exist")
        return doc.exists

    def member_reference(self, group: Group, member: Member):
        return self.group_reference(group).collection(Member.FirestoreCollection).document(member.id)
    def register(self, group: Group, by: Member):
        if self.group_exists(group): return

        self._register_local(group, by)

        self.group_reference(group).set(group.fire())
        logging.warning("Set group")
        self.member_reference(group, by).set(by.fire())
        logging.warning("Set member")

    def _register_local(self, group: Group, by: Member):
        local_group = Group(int(group.id), group.title, int(group.admin.id), by, memberable=True)
        local_group.members.append(by)
        groups_local_copy.append(group)

    def add_member(self, member: Member, group: Group):
        groups_filtered = [item for item in groups_local_copy if item.id == group.id]
        for group in groups_filtered:
            group.members.append(member)

        self.member_reference(group, member).set(member.fire())
        logging.warning("Set member")

    def subscribe(self, member: Member):
        if any(saved.id == member.id for saved in subscribers_local_copy):
            return

        subscribers_local_copy.append(member)

        self.store.collection(Member.FirestoreCollection).document(member.id).set(member.fire())
        logging.warning("Set subscriber")


    def set_meta(self, member: Member, metage: Metage, group: Group):
        self.member_reference(group, member).collection(Metage.FirestoreCollection).document(str(metage.date)).set(
            metage.fire())
        logging.warning("Set metage")

    def get_admin_username(self, group: Group) -> str:
        doc = self.group_reference(group).get()
        logging.warning("Got group for admin username")
        group_admin = doc.to_dict()['admin_id']
        admin = self.member_reference(group, Member(group_admin, "")).get()
        logging.warning("Got admin username")
        return admin.to_dict()['username']

    def download(self):
        groups_raw = self.store.collection(Group.FirestoreCollection).get()
        groups_filtered = [item for item in groups_raw if item.id != 'Group']
        for raw_group in groups_filtered:
            group = Group(raw_group.id, raw_group._data['title'], raw_group._data['admin_id'], memberable=True)
            members_raw = raw_group.reference.collection(Member.FirestoreCollection).get()
            for raw_member in members_raw:
                member = Member(raw_member.id, raw_member._data['username'])
                group.members.append(member)
        groups_local_copy.append(group)

        subscribers_raw = self.store.collection(Member.FirestoreCollection).get()
        subscribers_filtered = [item for item in subscribers_raw if item.id != 'Member']
        for raw_subscriber in subscribers_filtered:
            subscriber = Member(raw_subscriber.id, raw_subscriber._data['username'])
            subscribers_local_copy.append(subscriber)