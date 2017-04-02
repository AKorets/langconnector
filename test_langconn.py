import unittest 
import code

from webtest import TestApp
from server import app

class TestCat(unittest.TestCase):
  def setUp(self):
     self.app = TestApp(app)

  def test_main(self):
     resp = self.app.get('/langcon/')
     #code.interact (local=locals())
     self.assertEqual (resp.status,'200 OK')
     
     self.assertIn ('Hatikva',resp.html)
       
