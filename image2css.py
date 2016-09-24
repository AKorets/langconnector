#!/usr/bin/python3

import base64
import sys

if len(sys.argv)>1:
  fname = sys.argv[1]

  with open(fname, "rb") as image_file:
     data = base64.b64encode(image_file.read())


  print ('background-image: url("data:image/png;base64,%s");' % data.decode("utf-8") )

else:
  print ("Usage: image2css img.png")
