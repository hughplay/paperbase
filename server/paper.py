from datetime import datetime

import mongoengine.fields as field


class Link(field.Document):
    name = field.StringField()
    url = field.URLField()


class Paper(field.Document):
    index = field.IntField(primary_key=True)
    title = field.StringField(required=True)
    abbr = field.StringField(default='')
    url = field.URLField(default='')
    year = field.IntField()
    venue = field.StringField(default='')
    bibtex = field.StringField(default='')
    authors = field.ListField(field.StringField())
    organizations = field.ListField(field.StringField())
    links = field.ListField(field.ReferenceField(Link))

    tags = field.ListField(field.StringField())
    note = field.StringField(default='')
    topic = field.StringField(default='')

    date_add = field.DateTimeField(default=datetime.utcnow)
    date_update = field.DateTimeField(default=datetime.utcnow)

    removed = field.BooleanField(default=False)
