from SimpleXMLRPCServer import *
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

server = MyServer(("localhost", 3001), requestHandler=RequestHandler)

def decir(x):
    return {
    	'Que tal': 'Todo bien',
    	'Ok': 'Adios'
    }[x]

server.register_function(decir)

def talk():
	global stub
	stub = xmlrpclib.ServerProxy('http://localhost:3000/SOII')
	print 'Dije: Hola'
	print 'B dijo: ' + stub.decir('Hola')
	print 'Dije: Todo bien'
	print 'B dijo: ' + stub.decir('Todo bien')
	print 'Dije: Adios'
	print 'B dijo: ' + stub.decir('Adios')

def close():
	stub.close()
	server.quit = 1
	return 1

server.register_function(close)

service = threading.Thread(target=server.serve_forever, name='Server')
service.setDaemon(True)

conversation = threading.Timer(0, talk)

service.start()
conversation.start()

service.join()
conversation.join()