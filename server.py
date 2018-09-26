from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
import threading
import xmlrpclib

stub = 0 #global stub variable

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/SOII',)

class MyServer(SimpleXMLRPCServer):
	def serve_forever(self):
		self.quit = 0
		while not self.quit:
			self.handle_request()

server = MyServer(("localhost", 3000), requestHandler=RequestHandler)

def decir(x):
    return {
    	'Hola': 'Que tal',
    	'Todo bien': 'Ok',
    	'Adios': 'Goodbye'
    }[x]
server.register_function(decir)

def talk():
	global stub
	stub = xmlrpclib.ServerProxy('http://localhost:3001/SOII')
	print 'Dije: Que tal'
	print 'A dijo: ' + stub.decir('Que tal')
	print 'Dije: Ok'
	print 'A dijo: ' + stub.decir('Ok')
	server.quit = stub.close()

def close():
	server.quit = 1
	return 1

server.register_function(close)

service = threading.Thread(target=server.serve_forever, name='Server')
service.setDaemon(True)

conversation = threading.Timer(5, talk)

service.start()
conversation.start()

service.join()
conversation.join()