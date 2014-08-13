import peewee
import json

class Entry(peewee.Model):
	uid = peewee.TextField(primary_key=True)
	title = peewee.TextField()
	contents = peewee.TextField()
	timestamp = peewee.DateTimeField(index=True)
	extra = peewee.TextField()

