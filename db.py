from peewee import *
import json
import config


db = MySQLDatabase(config.mysql_db_name, config.mysql_host, user=config.mysql_user, password=config.mysql_password)


class Text(Model):

    name=CharField()
    name_in_url=CharField()
    description=TextField()
    lang_keys=TextField()
    order = IntegerField()
    visible = IntegerField () # to do convert to boolean 
    class Meta:
          database = db 
          db_table = 'texts' 


class Fragment (Model):
     
    content=TextField()
    connections=CharField()
    number_in_text = IntegerField()
    lang_keys=TextField() 
    text=ForeignKeyField(Text, related_name='fragments')
    #helps to retrieve by text_number all the fields of Paragraphs related to this number as objects, later I can make a loop and get the field I want
    class Meta:
          database = db 
          db_table = 'fragments' 




def create_tables():
    db.create_tables([Text, Fragment])

