!#/usr/bin/python
import json, sys, urllib2, urllib, re
import socket, time
from urllib2 import HTTPError, URLError
from httplib import BadStatusLine
from socket import timeout as SocketTimeout
from socket import error as SocketError

def elastick_parse(address, port):
	url = "http://"+ str(address) +":"+ str(port) +"/"
	url = urllib2.Request(url)
	try:
		data = urllib2.urlopen(url, timeout=2)
		print " "+ address
		for key, value in json.load(data).items():
			if( key == "cluster_name" ):
				sys.stdout.write(" Cluster name \t\t-> "+ value +"\n")
			if( key == "name" ):
				sys.stdout.write(" Sever name \t\t-> "+ value +"\n")
			continue
		
		indexes = urllib2.urlopen("http://"+ str(address) +":"+ str(port)+"/_cat/indices?v")
		matches = re.compile(u"\s+")
		datakeys = matches.split(indexes.readline())
		dataline = indexes.read()
		stack = {}
		stack['values'] = []
		stack['keys'] = {}

		for x in range(len(datakeys)):
			if( datakeys[x] == "" or len(datakeys[x]) < 2 ):
				continue
			stack['keys'][x] = datakeys[x]
			for i in range(len(dataline.split("\n"))):
				if( dataline.split("\n")[i] == "" or len(dataline.split("\n")[i]) < 2 ):
					continue
				stack['values'].append(matches.split(dataline.split("\n")[i]))
		
		sys.stdout.write(" Indexes in the stack \t-> "+ str(len(stack['values'])) +"\n")
		sys.stdout.write(" - - - - - - - - - \n")
		return json.dumps(stack)
						
	except (ValueError, IndexError):
		sys.stdout.write(" any string for source request\n - - - - - \n\r")
	except KeyboardInterrupt:
		sys.exit("Cancel\n\n\r")
	except BadStatusLine:
		pass
	except (SocketError, HTTPError):
		pass
	except (SocketTimeout, URLError):
		pass
		
with open(sys.argv[2], "r+") as filerd:	
	for line in filerd:
	
		if( sys.argv[1] == "-e" or sys.argv[1] == "--elasctick" ):
			result = elastick_parse(line.split(":")[1].replace("\n", ""), line.split(":")[0])
			if( result != None):
				with open("./result/"+ str(line.split(":")[1].replace("\n", "")) +".json", "a+") as newfile:
					newfile.write(result)
					newfile.close()
