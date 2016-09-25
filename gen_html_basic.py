#!/usr/bin/env python
# -*- coding: utf-8 -*-


def html_tag(tag_name, attr={}, tag_type='closed'):#parameters with '=' are optional and the right parts of exps are default values
  attrs_str = " ".join(["%s=\"%s\""  % (a, attr[a])  for a in attr])
  if tag_type == "closed":
      return "<%s %s />" % (tag_name, attrs_str)
  if tag_type == "open":
      return attrs_str and "<%s %s>" % (tag_name, attrs_str) or "<%s>" % tag_name
   
  if tag_type == "close":
      return "</%s>" % tag_name 

  raise ValueError("tag_type should be 'open', 'close' or 'closed'")#give errors in case the second and first parameters are wrong


def img(src,attr={}):
  attr['src']=src
  return html_tag(tag_name='img',attr=attr,tag_type='closed')


def html_node(tag_name,content,class_name=False, attr={}):
  if class_name:
    attr['class'] = class_name
  return html_tag(tag_name=tag_name,attr=attr,tag_type='open') + content + html_tag(tag_name=tag_name,attr=attr,tag_type='close')
 

def div(class_name,content,**attr):#**before argument mean that this fn may have many parameters and they will all be put into this dict.you will write key=value and then comma, if * then the array will be a list
  attr['class']=class_name
  return html_tag(tag_name='div',attr=attr,tag_type='open') + content + html_tag(tag_name='div',attr=attr,tag_type='close')
 

def html_code(body_code, head_code='', css_files=[], js_files=[]):

  main_t = \
'''<!DOCTYPE HTML>
<html>
<head>
<meta charset="UTF-8">
%s
</head>
<body>
%s
</body>
''' 

  css_t ='<link rel="stylesheet" type="text/css" href="%s">'
  js_t = '<script src="%s"></script>'

  css_str = "\n".join([css_t % css_file for css_file in css_files])
  js_str = "\n".join([js_t % js_file for js_file in js_files])
  head_code = head_code + css_str + "\n" + js_str

  return main_t % (head_code,body_code)

#print(html_code(div('main','aav ffd'),css_files=['my.css','1.css'],js_files=['23.js']))
 

def table(cols_list, rows, cols_titles=False, class_name=False, attr={}):
  if class_name:
    attr['class'] = class_name

  if cols_titles:
    html = html_node ('tr',''.join([ html_node('th',cols_titles[col], class_name='head_cell_'+col) for col in cols_titles ]),class_name='head_row')
  else:
    html = '' 
  
  for row_values in rows:
    html = html + html_node ('tr',''.join(
       [ html_node('td',row_values[col] or "&nbsp;", class_name='cell_'+col) for col in row_values ]
       ))
  return html_node (tag_name='table',attr=attr,content=html)  

#table(cols_list=['id','name'],rows=[{'id':'1','name':'John'},{'id':'3','name':'Anna'}],cols_titles={'id':'id','name':"Имя"},class_name='users_tbl')

#table(cols_list=['id','name'],rows=[{'id':'1','name':'John'},{'id':'3','name':'Anna'}],class_name='users_tbl')

