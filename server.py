#!/usr/bin/env python3

from bottle import *
import db
from db import getMysqlBackend
import json
from text_processing import *
from filters import html2text
import pystache 
import logging
from cork import Cork
from bottle.ext import beaker
import bottle

rr = pystache.Renderer()

from gen_html_basic import html_code

logging.basicConfig(format='localhost - - [%(asctime)s] %(message)s', level=logging.DEBUG)
log = logging.getLogger(__name__)
bottle.debug(True)

aaa = Cork(backend=getMysqlBackend(), email_sender='federico.ceratto@gmail.com', smtp_url='smtp://smtp.magnet.ie')

app = bottle.app()
session_opts = {
    'session.cookie_expires': True,
    'session.encrypt_key': 'It was an honor to host you, @narendramodi. ',
    'session.httponly': True,
    'session.timeout': 3600 * 24,  # 1 day
    'session.type': 'cookie',
    'session.validate_key': True,
}
app = beaker.middleware.SessionMiddleware(bottle.app(), session_opts)# #  Bottle methods  # #

def postd():
    return bottle.request.forms


def post_get(name, default=''):
    return bottle.request.POST.get(name, default).strip()


if __name__ == '__main__':
   root = "/"
else:
   root = "/langcon/"



def wrap_in_div(div_class, inside_text):
   res='<div class=%s> %s </div>' % (div_class, inside_text)
   return res

menu_array=[{"name": "About the project", "url": root+"about.html"}, {"name": "Texts", "url": root+"texts.html"}]

def page_template (menu_array, template, locations): 
   menu_links = ''#make a separate function for menu
   for i in menu_array:
     menu_links = menu_links+'<a class="menu_item" href="%s">%s</a>&nbsp&nbsp&nbsp'%(i['url'], i['name'])
   menu_links_in_div = wrap_in_div("menu", menu_links)
   navigator_links = navigator(locations)
   hor_line = '<div class="hor_line"></div>'
   template = menu_links_in_div +  navigator_links + template
   return hor_line+wrap_in_div ("container", template)
#make current link of a diff colour


def new_fragment_form(lang_keys):#insert into template
  textarea_fragments=''
  for lang in lang_keys:
    new_fragment='<p> %s:  <br> <textarea cols="50", rows="10", name="text_%s"></textarea></p>' % (lang['caption'], lang['key'])
    textarea_fragments=textarea_fragments+new_fragment
  return (textarea_fragments)

def edit_fragment_form(lang_keys, fragment_variants):#insert into template
  textarea_fragments=''
  for lang in lang_keys:
    fragment_var_text = output_fragment_as_plain_text (fragment_variants[lang['key']])
    new_fragment='<p> %s:  <br> <textarea cols="50", rows="10", name="text_%s">%s</textarea></p>' % (lang['caption'], lang['key'], fragment_var_text)
    textarea_fragments=textarea_fragments+new_fragment
  return (textarea_fragments)


def move_fragment_to_trash (id):
  row=db.Fragment.get(db.Fragment.id==int(id))
  try:
     trash = db.Text.get( db.Text.name_in_url == 'trash' )
  except db.Text.DoesNotExist:
     abort(404,"File not Found")     

  row.text=trash
  row.save()

def navigator (locations):

  navigator_tpl=pystache.parse('''<div class="navigator">
      
      {{#locations}}
        {{#url}}
           <a class="navigator_link" href="{{{url}}}">{{title}}</a> <img class="arrow" src="{{root}}icons/triangle.png" width="20px" height="20px" />
        {{/url}}

        {{^url}}
          {{title}} <img class="arrow" src="{{root}}icons/triangle.png" width="20px" height="20px" />
        {{/url}}
     {{/locations}}
     </div>
  ''')
  navigator_rendered=rr.render(navigator_tpl, {'locations':locations, 'root':root})
  return navigator_rendered
 

texts_list_tpl = pystache.parse(page_template(menu_array, \
 '''
    <div class="texts">
      <div class=newtext>
       <a href="%snew_text.html">
         <div class="header" >Add New Text</div>
       </a>
      </div>
    {{#text}}
      <div class=text>
       
         <div  class="header">
           <a class="link_to_text" href="{{root}}edit/{{name_in_url}}.html" >{{name}} </a>
           <div class="buttons">
             <a id='del_text_button_{{id}}' class="del_text_button" href='%sdelete_text/{{id}}' onclick="return confirm('Are you sure you want to delete the text?')"> Delete Text </a>
           </div>

         </div>
         <div class="description">{{description}}</div>
       
      </div>
    {{/text}}
    </div>
'''%(root, root), [{'title':'Texts', 'url':''}])
 )

about_tpl = pystache.parse(page_template(menu_array,\
 '''
<div class="about">
<p>Language Connector is the editor that allows connecting words in parallel texts.</p> 

<p>When you have a text and its translation, very often the difference in the languages is such that it is not obvious which word is the translation of which. The editor allows the translator to connect manually every word or expression from the text in one language to its counterpart in the text in the other language.</p> 

<p>In the resultant text the connections allow the reader, whithout a deep knowledge or even without any knowledge of the original language, read the translation as if he is reading the original text.<p>  

</div>
''',[{'title':'About', 'url':''}])
 )

@bottle.post('/login')
def login():
    """Authenticate users"""
    username = post_get('username')
    password = post_get('password')
    aaa.login(username, password, success_redirect='/', fail_redirect='/login')

@bottle.route('/user_is_anonymous')
def user_is_anonymous():
    if aaa.user_is_anonymous:
        return 'True'

    return 'False'

@bottle.route('/logout')
def logout():
    aaa.logout(success_redirect='/login')


@hook('before_request')
def _connect_db():
    db.db.connect()

@hook('after_request')
def _close_db():
    if not db.db.is_closed():
        db.db.close() 

@route(root)
def main ():
  return texts()


@route(root+'about.html')
def about():
  tpl=about_tpl
  return html_code (rr.render(tpl, {"root":root}),head_code='<title>About the project</title>',css_files=[root+'css/global.css',root+'css/about.css'])


@route(root+'texts.html')
def texts ():
  
  tpl= texts_list_tpl
  rows=db.Text.select().where((db.Text.name_in_url != 'trash') and (db.Text.visible == 1)).order_by(db.Text.order)
  
  return html_code (rr.render(tpl,{"text": rows, "root": root}), head_code='<title>Texts</title>',css_files=[root+'css/global.css',root+'css/text_list.css'])

text_template=\
'''
    {{#mode_switchers}}
     {{^read_only}}
     <a class="text_mode_link" href="{{root}}read/{{name_in_url}}.html"> Read Only Mode </a>
     {{/read_only}}
     {{#read_only}}
     <a class="text_mode_link" href="{{root}}edit/{{name_in_url}}.html"> Edit Text </a>
     {{/read_only}}
    {{/mode_switchers}}
 
    {{^read_only}}
    <a class="add_fragment_link" href="{{root}}{{name_in_url}}/new_fragment.html">Add New Fragment</a>
    {{/read_only}}

    <div class="fragments{{#read_only}} read_mode{{/read_only}}">
      {{#fragment}}
         <div class="fragment" id="fragment_{{id}}"> 
           {{#variant}}<div class="{{class_name}}" id="{{var_id}}">{{{content}}}</div>{{/variant}} 
            <div class="comment"></div>
            {{^read_only}}
            <div class="buttons">
              <a class="edit_fragment_link" href="{{root}}edit_fragment/{{id}}/">Edit Fragment</a>
              <a class="delete_fragment_link" onclick="return confirm('Are you sure you want to delete the fragment?')" href="{{root}}delete/{{id}}/">Delete Fragment</a> 
            </div>
            {{/read_only}}
         </div>
      {{/fragment}}
    </div>
   '''


text_with_edit_tpl = pystache.parse(page_template(menu_array, text_template, [{'title':'Texts', 'url': root+'texts.html'}, {'title':'{{text_title}}', 'url':''}]))

text_with_static_tpl = pystache.parse(text_template)

def detect_hebrew(txt):
  return any("\u0590" <= char <= "\u05EA" for char in txt)#any takes as a parameter the list of booleans,here it takes an element from the first iterator and it orders the element from the second iterator

import copy

def accents(split_text):

  new_split_text = []

  for token in split_text:
     newtoken = copy.deepcopy(token)
     newtoken["content"] = token["content"].replace('\\=','<span class="accent">').replace('=\\','</span>')
     new_split_text.append(newtoken)#append adds elements to list

  return new_split_text


@route(root+'edit/<name_in_url:re:[0-9A-Za-z_]+>.html')
def text_with_edit (name_in_url):
	aaa.require(fail_redirect='/login')
	text_with_edit_tpl
	return show_text (name_in_url, read_only = False, template = text_with_edit_tpl, mode_switchers = True)  

@route(root+'read/<name_in_url:re:[0-9A-Za-z_]+>.html')
def text_with_read (name_in_url):
  return show_text (name_in_url, read_only = True, template = text_with_edit_tpl, mode_switchers = True)  

@route(root+'static/<name_in_url:re:[0-9A-Za-z_]+>.html')
def text_with_static (name_in_url):
  return show_text (name_in_url, read_only = True, template = text_with_static_tpl, mode_switchers = False)  


def show_text (name_in_url, read_only = False, template = text_with_edit_tpl, mode_switchers = True):
 
  try:
     text = db.Text.get( db.Text.name_in_url == name_in_url )#foreign key refers to the whole row in peewee
  except db.Text.DoesNotExist:
     abort(404,"File not Found")     

  fragments = []
  for row in db.Fragment.select().where( db.Fragment.text==text ).order_by(db.Fragment.number_in_text):
     frag_vars = json.loads(row.content)
     lang_keys = json.loads(row.lang_keys)
     fragment = {}
  
     variants = []
     for k in [lang['key'] for lang in lang_keys]:#list comprehension, 
       variant = {}
     
       variant['content'] = output_fragment (k+str(row.id),accents(frag_vars[k]))
       if detect_hebrew(variant['content']):
          variant['class_name'] = k + ' hebrew'
       else:
          variant['class_name'] = k

       variant['var_id'] = k+str(row.id)
       variants = variants + [variant]

     fragment['variant'] = variants
     fragment['id'] = row.id
     fragments = fragments + [fragment]

  html = rr.render(template,{'root': root, 'name_in_url': name_in_url, 'fragment': fragments, 'read_only': read_only , 'text_title': text.name, 'mode_switchers': mode_switchers})

  return html_code (html, css_files=[root+'css/global.css',root+'css/phrases.css'], 
     js_files=[root+'jquery-1.11.3.min.js',root+'%s/text_name.js' % name_in_url, root+'phrases.js']) 


@route(root+'<name_in_url:re:[0-9A-Za-z_]+>/text_name.js')
def set_name_js(name_in_url):
  response.headers['Content-Type']='application/javascript'
  return 'text_name = "%s"; root = "%s";' % (name_in_url, root) 


@route(root+'phrases.js')
def js_file ():
   return static_file('phrases.js', root='./')


@route(root+'icons/<name>.png')
def icon(name):
   if name in ['connections','connections-50','connections-col','connections-col2','triangle','add','del']:     
      return static_file(name+'.png', root='./icons')
   else:
      abort(404,'File Not Found')


@route(root+'css/<name>.css')
def css_file (name):
   if name in ['global','phrases','text_list','editor','about','new_fragment']:
      return static_file(name+'.css', root='./')
   else:
      abort(404,'File Not Found')


@route(root+'jquery-1.11.3.min.js')
def jquery ():
   return static_file('jquery-1.11.3.min.js', root='./')

@route(root+'<name_in_url:re:[0-9A-Za-z_]+>/get_fragments_and_connections.json')
def get_fragments_and_connections(name_in_url):

   try:
     text = db.Text.get( db.Text.name_in_url == name_in_url )
   except db.Text.DoesNotExist:
     abort(404,"File not Found")     

   res = []
   for row in db.Fragment.select().where( db.Fragment.text == text ).order_by( db.Fragment.number_in_text ):
     lang_keys = json.loads(row.lang_keys)
     fragments = {}
     lang_keys_list=[lang['key'] for lang in lang_keys]#list comprehension(a list of lang keys)
     for k in lang_keys_list:
       fragments[k] = k+str(row.id)
     connections = json.loads(row.connections)
     res = res + [{"fragments":fragments, "connections":connections, "lang_keys":lang_keys_list, "fragment_id":"fragment_"+str(row.id)}]
   
   return json.dumps(res)  

@route(root+'editor.js')
def editor_js ():
   return static_file('editor.js', root='./')


#@route(root+'cleditor/images/<name>.gif')
#def images(name):
#   if name in ['toolbar','buttons']:     
#      return static_file(name+'.gif', root='./images')
#   else:
#      abort(404,'File Not Found')

@route(root+'cleditor/<fname:re:(images/)?[0-9A-Za-z._]+>')
def cleditor_files(fname):
   return static_file(fname, root='cleditor')


#@route(root+'cleditor/jquery.cleditor.js')
#def jquery_cleditor ():
#   return static_file('cleditor/jquery.cleditor.js', root='./')


@route(root+'edit_fragment/<id:re:[0-9]+>/')#change into template
def editor (id):
   html =''
   row=db.Fragment.get(db.Fragment.id==id)
   frag_vars = json.loads(row.content)
   lang_keys = json.loads(row.lang_keys)
   html = html + "\n".join ( [("<div class=\"%s\" id=\"%s\" >" % (k,k+str(row.id)))+output_fragment (k+str(row.id),accents(frag_vars[k]))+"</div>" for k in [lang['key'] for lang in lang_keys] ] )
   html='<div class="button" id="edit_button"> Edit group </div> <div class="button" id="save_button"> Save group </div> <div class="button" id="new_button"> New group </div> <div class="button" id="read_mode"> Read mode </div> <div class="button" id="edit_text"> Edit text </div>'+wrap_in_div('text',html)+'<div class="comment"></div><div id="comments"></div>'
   html=wrap_in_div('main', html)
   html=page_template(menu_array, html, [{'title':'Texts', 'url': root+'texts.html'}, {'title':row.text.name, 'url':root+'edit/%s.html#fragment_%s'%(row.text.name_in_url,id)}, {'title':'Edit fragment', 'url':''}])
   return html_code (html, css_files=[root+'css/editor.css', root+'css/global.css', root+'cleditor/jquery.cleditor.css'], 
     js_files=[root+'jquery-1.11.3.min.js', root+'editor.js', root+'cleditor/jquery.cleditor.js'], head_code='<title>Connections Editor</title>')

@route(root+'edit_fragment/<id:re:[0-9]+>/edit_fragment_text.html')
def edit_fragment_text (id):
  try:
   row=db.Fragment.get(db.Fragment.id==id)
  except db.Fragment.DoesNotExist:
    abort(404,"File not Found")

  frag_vars = json.loads(row.content)
  lang_keys = json.loads(row.lang_keys)
  form_html=rr.render(form_tpl_edit_fragment, {'id':id, 'edit_fragment_form':edit_fragment_form(lang_keys, frag_vars), 'text_title': row.text.name, 'name_in_url': row.text.name_in_url, 'confirm_block':(len(json.loads(row.connections))!=0)})
  return html_code (form_html, head_code='<title>Edit fragment</title>',css_files=\
    [root+'css/global.css'])


@route(root+'delete/<id:re:[0-9]+>/')
def delete_fragment (id):
   aaa.require(fail_redirect='/login')
   try:
     fragment=db.Fragment.select().where(db.Fragment.id==id).get()
   except db.Fragment.DoesNotExist:
     abort(404,"File not Found")
   name_in_url=fragment.text.name_in_url
   move_fragment_to_trash(id)   
   redirect (root+"edit/%s.html"%(name_in_url))
   


#this is for ajax
@route(root+'edit_fragment/<id:re:[0-9]+>/data.json')
def get_fragment_json (id):
   aaa.require(fail_redirect='/login')
   row=db.Fragment.get(db.Fragment.id==int(id))
   lang_keys = json.loads(row.lang_keys)
   fragments = {}
   lang_keys_list = [lang['key'] for lang in lang_keys]
   for k in lang_keys_list:
     fragments[k] = k+str(row.id)
   #print (row.content)
   #print (row.connections)
   connections = json.loads(row.connections)
   res={"fragments":fragments, "connections":connections, "lang_keys": lang_keys_list}
   return json.dumps(res)

form_tpl_edit_fragment = pystache.parse (page_template(menu_array,
 '''
 <div class="edit_fragment_form">
 <form action="%sedit_fragment/{{id}}/edit_fragment_text.html/save_edited_fragment" method="post" >
 <p>Edit fragment </p> {{{edit_fragment_form}}}
 <input type="submit" value="Save changes" {{#confirm_block}}onclick="return confirm ('All the existing connections will be lost')"{{/confirm_block}}')>
 </form>
 </div>
 '''%(root), [{'title':'Texts', 'url': root+'texts.html'}, {'title':'{{text_title}}', 'url':root+'edit/{{name_in_url}}.html'}, {'title':'Edit fragment', 'url': root+'edit_fragment/{{id}}/'}, {'title':'Edit fragment text', 'url': ''}]))


form_tpl_new_fragment = pystache.parse (page_template(menu_array,
 '''
 <div class="new_fragment_form">
 <form action="{{url}}/save_new_fragment" method="post" >
 <p>New fragment: </p> {{{new_fragment_form}}}
 <input type="submit" value="Save fragment">
 </form>
 </div>
 ''', [{'title':'Texts', 'url':root+'texts.html'}, {'title':'{{text_title}}', 'url':root+'edit/{{name_in_url}}.html'}, {'title':'New fragment', 'url':''}]))

new_text_form = page_template(menu_array,
 '''
 <form id='add_new_text_form' action="%ssave_new_text.html" method="post" >
 <div>
   <p>Text Details:</p>
   Text title: <input type="text" name="new_text"><br>
   Text name in url: <input type="text" name="name_in_url"><br>
   Text description: <input type="text" name="description"><br>
 </div>
 <div>
   <p>Number of Languages:</p>
   <input type="radio" name="lang_keys" value='[{"key":"orig","caption":"Original"},{"key":"trans","caption":"Translation"}]'> Original and Translation<br>
   <input type="radio" checked="checked" name="lang_keys" value='[{"key":"orig","caption":"Original"},{"key":"phonetic","caption":"Phonetic"},{"key":"trans","caption":"Translation"}]'> Original, Phonetic and Translation<br>
   <p><input type="submit" value="Save new text"></p>
 </div>
 </form>
 '''%(root), [{'title':'Texts', 'url':root+'texts.html'}, {'title':'Add new text', 'url':''}])
#make advanced options for choosing languages

@route(root+'<name_in_url:re:[0-9A-Za-z_]+>/new_fragment.html')
def new_fragment(name_in_url):
  try:
    text=db.Text.select().where(db.Text.name_in_url==name_in_url).get()   
  except db.Text.DoesNotExist:
    abort(404,"File not Found")

  lang_keys = json.loads(text.lang_keys)
  form_html=rr.render(form_tpl_new_fragment, {'url':root+name_in_url, 'new_fragment_form':new_fragment_form(lang_keys), 'text_title': text.name, 'name_in_url': name_in_url})
  return html_code (form_html, head_code='<title>Add new fragment</title>',css_files=\
    [root+'css/global.css',root+'css/new_fragment.css'])



#@route(root+'<name_in_url:re:[0-9A-Za-z_]+>/save_new_fragment', method="POST") #he cannot output the num spl ws array, needs a string in main

@route(root+'new_text.html')
def new_text():
  return html_code (new_text_form, head_code='<title>Add new text</title>',css_files=[root+'css/global.css'])

@route(root+'save_new_text.html', method="POST")
def save_new_text():
  '''
to do:
 check name_in_url
  only allowed symbols
  unique
 check lang_keys
  proper json

  '''
  text_data = {}
  text_data['title'] = request.forms.getunicode ('new_text')
  text_data['name_in_url'] = request.forms.getunicode ('name_in_url')
  text_data['description'] = request.forms.getunicode ('description')
  text_data['lang_keys'] =request.forms.getunicode ('lang_keys')#make json.loads
  #lang_keys_dict = json.loads ("{\"hh\":\"mm\"}")#json.loads (text_data['lang_keys'])
  #lang_keys_dict = json.loads (text_data['lang_keys'])
  new_text = db.Text(name = text_data['title'], name_in_url=text_data['name_in_url'], description=text_data['description'], lang_keys=text_data['lang_keys'], order = 5, visible = 1)
  new_text.save() 

  redirect (root)

@route(root+'delete_text/<id:re:[0-9]+>')
def delete_text (id):
   try:
    text=db.Text.select().where(db.Text.id==id).get()
   except db.Text.DoesNotExist:
    abort(404,"File not Found")
   text.delete_instance(recursive=True)
   redirect (root+'texts.html')


@route(root+'<name_in_url:re:[0-9A-Za-z_]+>/save_new_fragment', method="POST")
def save_new_fragment(name_in_url):

  fragment_text = {}

  rows=db.Text.select().where(db.Text.name_in_url==name_in_url)
  ids = [row.id for row in rows]
#for row in rows: this is the same as the line above
# ids = ids + [row.id]

  if len(ids) == 0:
     abort(404,"File not Found")
  
  text_id = ids[0]
  text_row = rows[0]
  
  lang_keys = json.loads(text_row.lang_keys)


  for key in [lang['key'] for lang in lang_keys]:
    text = request.forms.getunicode ('text_%s' %(key))
    text = html2text(text) #this is for safety and for future editor
    split_text = words_split(text)
    numbered_split_text = words_numbering (split_text)
    fragment_text['%s'%(key)] = numbered_split_text

  max_number = db.Fragment.select(db.fn.Max(db.Fragment.number_in_text)).scalar()
  #text_row=db.Text.get(db.Text.id==text_id)#I am getting a row, then it gets id by itself for it is a for.key
#we have to deal with exclusions in case the id is not correct
  fragment = db.Fragment(content= json.dumps(fragment_text,ensure_ascii=False), connections="[]", number_in_text=max_number+1, text=text_row, lang_keys=text_row.lang_keys)#then make it in a separate function.it is creating a new line, it is constructor
  fragment.save()
  redirect (root+"edit/%s.html"%(name_in_url))


@route(root+'edit_fragment/<id:re:[0-9]+>/edit_fragment_text.html/save_edited_fragment', method="POST")
def save_edited_fragment(id):
  id_number = int(id)#do this everywhere with id
  try:
   row=db.Fragment.get(db.Fragment.id==id_number)
  except db.Fragment.DoesNotExist:
    abort(404,"File not Found")
  
  fragment_text = {}
  lang_keys = json.loads(row.lang_keys)

  for key in [lang['key'] for lang in lang_keys]:
     fragment_var_text = request.forms.getunicode ('text_%s' %(key))
     text = html2text(fragment_var_text) #this is for safety and for future editor
     split_text = words_split(text)
     numbered_split_text = words_numbering (split_text)
     fragment_text['%s'%(key)] = numbered_split_text

  row.content = json.dumps(fragment_text,ensure_ascii=False)
  row.connections = "[]"
  row.save()
  redirect (root+"edit_fragment/%d/"%(id_number))

@route(root+'edit_fragment/<id:re:[0-9]+>/save_connections', method="POST")
def save_connections(id):
  conn = request.forms.getunicode ('connections')
  #print (conn) 
  row = db.Fragment.get(db.Fragment.id==id)
  row.connections = conn
  row.save()   
  return "Ok"

# Static pages

@bottle.route('/login')
@bottle.view('login_form')
def login_form():
    """Serve login form"""
    return {}


@bottle.route('/sorry_page')
def sorry_page():
    """Serve sorry page"""
    return '<p>Sorry, you are not authorized to perform this action</p>'

if __name__ == '__main__':
  run(app=app, host='0.0.0.0', port=8080)
else:
  app = application = default_app()






