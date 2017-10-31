# Web server to Carambola

#

import cgi
import serial

from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

# The web server.
class MyHandler(SimpleHTTPRequestHandler):
  def do_POST(self):        
     if self.path == '/gpio':	
       form = cgi.FieldStorage(fp=self.rfile, headers=self.headers,
        environ={'REQUEST_METHOD':'POST'})
       code = form['code'].value
       print 'Sent:', code
       pin14 = open("/sys/class/gpio/gpio14/value","w")
       pin14.write(str(code))
       pin14.close()
       #arduino.write(code)
       self.send_response(200)
       self.send_header('Content-type', 'text/html')
       return
     return self.do_GET()

# You may need something other than /dev/ttyUSB0
export = open("/sys/class/gpio/export","w")
export.write(str(14))
export.close()
gpio = open("/sys/class/gpio/gpio14/direction","w")
gpio.write("out")
gpio.close()

server = HTTPServer(('', 8080), MyHandler).serve_forever()
