from peewee import MySQLDatabase, Model, CharField, TextField, IntegerField, ForeignKeyField
import json
from cork.backends import SqlAlchemyBackend
import logging

try:
    import config
except ImportError:
    import config_default as config

db = MySQLDatabase(config.mysql_db_name, config.mysql_host, user=config.mysql_user, password=config.mysql_password)

logger = logging.getLogger('peewee')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

def getMysqlBackend():
    connectionString = config.generateConnectioString()
    sqlBackend = SqlAlchemyBackend(db_full_url = connectionString)
    return sqlBackend

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

