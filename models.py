#!/usr/bin/env python
# coding=utf-8
from peewee import *

botdb = SqliteDatabase('bastard.sqlite', threadlocals=True, check_same_thread=False)

class BaseModel(Model):
    class Meta:
        database = botdb

class User(BaseModel):
    display_name = CharField()
    alias = CharField(unique=True)
    gaia_id = CharField(unique=True)

class Conversation(BaseModel):
    name = CharField()
    conv_id = CharField(unique=True)
    private = BooleanField(default=True)

class MessageType(BaseModel):
    name = CharField(unique=True)

class Tag(BaseModel):
    name = CharField(unique=True)
    author = ForeignKeyField(User, related_name="tags")

class Message(BaseModel):
    content = TextField()
    conversation = ForeignKeyField(Conversation, related_name="messages")
    author = ForeignKeyField(User, related_name="messages")
    message_type = ForeignKeyField(MessageType, related_name="messages")
    date_created = DateField()
