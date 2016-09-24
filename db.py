from peewee import *
import json

#db = SqliteDatabase('paragraphs.db')
db = MySQLDatabase('langconnector',host='localhost',user='root',password='pwdycotangdb' )


class Text(Model):
    name=CharField()
    name_in_url=CharField()
    description=TextField()
    lang_keys=TextField()
    order = IntegerField()
    visible = IntegerField () # to do convert to boolean 
    class Meta:
          database = db # This model uses the "paragraphs.db" database.
          db_table = 'texts' 


class Fragment (Model):#***
     
    content=TextField()
    connections=CharField()
    number_in_text = IntegerField()
    lang_keys=TextField() 
    text=ForeignKeyField(Text, related_name='fragments')#helps to retrieve by text_number all the fields of Paragraphs related to this number as objects, later I can make a loop and get the field I want
    class Meta:
          database = db 
          db_table = 'fragments' 


#db.connect()


text2= {"orig": [{"type": "word", "content": "Had", "word_id": 1}, {"type": "space", "content": " "}, {"type": "word", "content": "I", "word_id": 2}, {"type": "space", "content": " "}, {"type": "word", "content": "not", "word_id": 3}, {"type": "space", "content": " "}, {"type": "word", "content": "heard", "word_id": 4}, {"type": "space", "content": " "}, {"type": "word", "content": "it", "word_id": 5}, {"type": "space", "content": " "}, {"type": "word", "content": "with", "word_id": 6}, {"type": "space", "content": " "}, {"type": "word", "content": "my", "word_id": 7}, {"type": "space", "content": " "}, {"type": "word", "content": "own", "word_id": 8}, {"type": "space", "content": " "}, {"type": "word", "content": "ears", "word_id": 9}, {"type": "space", "content": ", "}, {"type": "word", "content": "I", "word_id": 10}, {"type": "space", "content": " "}, {"type": "word", "content": "would", "word_id": 11}, {"type": "space", "content": " "}, {"type": "word", "content": "never", "word_id": 12}, {"type": "space", "content": " "}, {"type": "word", "content": "have", "word_id": 13}, {"type": "space", "content": " "}, {"type": "word", "content": "believed", "word_id": 14}, {"type": "space", "content": " "}, {"type": "word", "content": "a", "word_id": 15}, {"type": "space", "content": " "}, {"type": "word", "content": "word", "word_id": 16}, {"type": "space", "content": " "}, {"type": "word", "content": "of", "word_id": 17}, {"type": "space", "content": " "}, {"type": "word", "content": "it", "word_id": 18}], "trans": [{"type": "word", "content": "Я", "word_id": 1}, {"type": "space", "content": " "}, {"type": "word", "content": "бы", "word_id": 2}, {"type": "space", "content": " "}, {"type": "word", "content": "ни", "word_id": 3}, {"type": "space", "content": " "}, {"type": "word", "content": "слову", "word_id": 4}, {"type": "space", "content": " "}, {"type": "word", "content": "из", "word_id": 5}, {"type": "space", "content": " "}, {"type": "word", "content": "этого", "word_id": 6}, {"type": "space", "content": " "}, {"type": "word", "content": "не", "word_id": 7}, {"type": "space", "content": " "}, {"type": "word", "content": "поверил", "word_id": 8}, {"type": "space", "content": ", "}, {"type": "word", "content": "если", "word_id": 9}, {"type": "space", "content": " "}, {"type": "word", "content": "бы", "word_id": 10}, {"type": "space", "content": " "}, {"type": "word", "content": "не", "word_id": 11}, {"type": "space", "content": " "}, {"type": "word", "content": "слышал", "word_id": 12}, {"type": "space", "content": " "}, {"type": "word", "content": "это", "word_id": 13}, {"type": "space", "content": " "}, {"type": "word", "content": "собственными", "word_id": 14}, {"type": "space", "content": " "}, {"type": "word", "content": "ушами", "word_id": 15}]}

connections2='''[
             {"orig": [2, 4], "trans": [12]},
             {"orig": [5], "trans": [6]},
             {"orig": [7, 8], "trans": [14]},
             {"orig": [15,16], "trans": [4]},
             {"orig": [13,14], "trans": [8]}
             ]''' 


text1 = {"orig": [{"type": "word", "content": "Melkiy", "word_id": 1}, {"type": "space", "content": " "}, {"type": "word", "content": "needs", "word_id": 2}, {"type": "space", "content": " "}, {"type": "word", "content": "to", "word_id": 3}, {"type": "space", "content": " "}, {"type": "word", "content": "learn", "word_id": 4}, {"type": "space", "content": " "}, {"type": "word", "content": "to", "word_id": 5}, {"type": "space", "content": " "}, {"type": "word", "content": "control", "word_id": 6}, {"type": "space", "content": " "}, {"type": "word", "content": "his", "word_id": 7}, {"type": "space", "content": " "}, {"type": "word", "content": "temper", "word_id": 8}], "trans": [{"type": "word", "content": "Мелкий", "word_id": 1}, {"type": "space", "content": " "}, {"type": "word", "content": "должен", "word_id": 2}, {"type": "space", "content": " "}, {"type": "word", "content": "научиться", "word_id": 3}, {"type": "space", "content": " "}, {"type": "word", "content": "управлять", "word_id": 4}, {"type": "space", "content": " "}, {"type": "word", "content": "своим", "word_id": 5}, {"type": "space", "content": " "}, {"type": "word", "content": "характером", "word_id": 6}]}


connections1 = '''
 [{"orig":[1],"trans":[1]},{"orig":[2],"trans":[2]},{"orig":[3,4],"trans":[3]}]
'''
#second_paragraph=Paragraph.create (par_text=text_of_second_paragraph, connections=connections)

#json_connections=Paragraph.select.where (Paragraph.id==3).get()
#print (json_connections)




#сделать общий id для перевода одного и того же параграфа? как строка таблицы будет превращаться в json

def create_and_fill_table():
    db.create_tables([Fragment])
    fragment1= Fragment (text= json.dumps(text1), connections=connections1, number_in_text=1)
    fragment1.save()

    fragment2=Fragment (text=json.dumps(text2), connections=connections2, number_in_text=2)
    fragment2.save()

