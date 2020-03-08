#!/usr/bin/env python

#################################################
#												#
#	VUT FIT Brno								#
#	Počítačové komunikace a sítě				#
#	Projekt 1: HTTP resolver doménových mien	#
#	Autor: Daniel Miloslav Ocenas (xocena06)	#
#	Datum: 3.2020								#
#	Popis: Server komunikujuci s protokolom 	#
#	HTTP, zaistujuci preklad domenovych mien	#
#												#
#################################################

import os, sys, re, socket, signal, datetime

BAD_REQ = { 'code':'400', 'msg': 'Bad Request' }
NOT_FOUND = { 'code':'404', 'msg': 'Not Found' }
METHOD_NOT_ALLOWED = { 'code':'405', 'msg':'Method Not Allowed' }

def signal_handler(sig, frame):
	sys.exit(0)

def formatLine(s):
	return ''.join((line + '\n') for line in s.splitlines())

def recvAll(sock):
	prev_timeout = sock.gettimeout()
	try:
		sock.settimeout(0.01)
		rdata = None
		while True:
			try:
				rdata = sock.recv(4096).decode()
			except socket.timeout:
				return ''.join(rdata)
	finally:
		sock.settimeout(prev_timeout)

def sendResponse(conn, params):
	if 'code' not in params or 'msg' not in params:
		params['code'] = '400'
		params['msg'] = 'Bad Request'

	responseCodeHeader = 'HTTP/1.1 ' + params['code'] + ' ' + params['msg'] + '\r\n'
	conn.send(responseCodeHeader.encode())

	if 'text' not in params:
		params['text'] = ''


	headers = {
		'Content-Type': 'text/html',
		'Content-Length': len(params['text']),
		'Connection': 'close',
		'Date': str(datetime.datetime.now())
	}
	response_headers = ''.join('%s: %s\r\n' % (k, v) for k, v in headers.items())

	data = response_headers + '\r\n' + params['text'] + '\n'
	conn.send(data.encode())


def chceckUrl(url):
	regex = re.compile('^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$')
	if regex.match(url) != None:
		return True
	else:
		return False

def chechIpAdress(ip):
	try: 
		socket.inet_aton(ip)
		return True
	except:
		return False

def parseData(params):
	if 'type' not in params or 'name' not in params:
		return BAD_REQ

	if params['type'] == 'A' and chceckUrl(params['name']):			
		try:
			remote_ip = socket.gethostbyname( params['name'] )
		except socket.gaierror:
			return NOT_FOUND

		response = params['name'] + ':' + params['type'] + '=' + remote_ip 
		return {'code':'200', 'msg': 'OK', 'text':response }
		
	elif params['type'] == 'PTR' and chechIpAdress(params['name']):
		try:
			remote_addr = socket.gethostbyaddr( params['name'] )[0]
		except socket.herror:
			return NOT_FOUND

		response = params['name'] + ':' + params['type'] + '=' + remote_addr 
		return {'code':'200', 'msg': 'OK', 'text':response }
		
	else:
		return BAD_REQ

def main():
	signal.signal(signal.SIGINT, signal_handler)
	
	try:
		port = int(sys.argv[1])
		if not ((port >= 2**10) and (port < 2**16-1)):
			print('Port must have unsigned 16bit integer value\n')
			sys.exit(1)
	except ValueError as err:
		print('Selected port does not have integer value\nPlease change port value and start server again')
		sys.exit(1)

	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #help for debugging
	serversocket.bind(('',port ))	#binds everything
	print('Server is now listening on port:',port)
	serversocket.listen(10)	#stores 10 incoming requests

	while True:	#server listens untill manually interrupted

		(conn, address) = serversocket.accept()

		request = formatLine(recvAll(conn))
		head, body = request.split('\n\n', 1)
		head = head.splitlines()
		body = body.splitlines()

		dataStr = head[0].rsplit('HTTP/1.1',1)[0]
		if dataStr.startswith('GET'):
			if dataStr.startswith('GET /resolve?'):						
				dataStr = dataStr.replace('GET /resolve?','').split('&')
				if len(dataStr) == 2:
					params = dict(x.split('=') for x in dataStr)
					params = {x: v.replace(' ', '') for x, v in params.items()}
					sendResponse(conn,parseData(params))
				else:
					sendResponse(conn,BAD_REQ)
			else:
				sendResponse(conn,BAD_REQ)
		

		elif dataStr.startswith('POST'):
			if dataStr.startswith('POST /dns-query'):
				postResponseBody = []
				for x in body:
					param = x.split(':')
					if len(param) != 2:
						continue
					param = {'name':param[0],'type':param[1]} 
					postResponseBody.append(parseData(param))

				validResponse = False
				for x in postResponseBody:
					if x['code'] == '200':
						validResponse = True
						break;

				if validResponse:
					validResponse = []
					for x in postResponseBody:
						if 'text' in x:
							validResponse.append(x['text'])

					validResponse = ''.join((line + '\n') for line in validResponse)
					response = {'code':'200', 'msg':'OK','text':validResponse}
				else:
					if len(postResponseBody) == 0:
						response = { 'code': '200', 'msg': 'OK', 'text': ''}
					else:
						response = { 'code' : postResponseBody[0]['code'] , 'msg': postResponseBody[0]['msg'] }

				sendResponse(conn,response)
			else:
				sendResponse(conn,BAD_REQ)
		else:
			sendResponse(conn,METHOD_NOT_ALLOWED)

		conn.close()

main()