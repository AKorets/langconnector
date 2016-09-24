import lxml.html
import lxml.etree as el
from lxml.html.clean import Cleaner


def html_basic_cleaning(html):
  cleaner = Cleaner()
  cleaner.javascript = True 
  cleaner.style = True   
  return lxml.html.tostring(cleaner.clean_html(lxml.html.fromstring(html)),encoding='unicode')


def html_strict_cleaning(html,allow_tags=['p','br','a','img','div']):
  cleaner = Cleaner()
  cleaner.javascript = True 
  cleaner.style = True   
  cleaner.allow_tags = allow_tags
  cleaner.remove_unknown_tags = False
  return lxml.html.tostring(cleaner.clean_html(lxml.html.fromstring(html)),encoding='unicode')


def html2text(html):
  cleaner = Cleaner()
  cleaner.javascript = True 
  cleaner.style = True   
  html_tree = cleaner.clean_html(lxml.html.fromstring(html))
  el.strip_tags(html_tree,'*')
  return html_tree.text


