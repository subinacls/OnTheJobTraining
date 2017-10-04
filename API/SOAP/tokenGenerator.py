#!/usr/bin/env python
##### Used to generate Session Tokens against SOAP Service <REDACTED>.asmx?WSDL
##### Replace <REDACTED> with your asmx and ensure the body aligns with your request 
##### Otherwise replace it with the appropiate body 
# Imports
import os, re, sys, requests
#
# User arguments
target=sys.argv[1]
uname=sys.argv[2]
pword=sys.argv[3]
dir=sys.argv[4]
# Static vars
gmt="-7"
services="/<REDACTED>.asmx"
url="http://"+target+services
# performs nonGMTauth to SOAP interface, choose this if your are not supplying GMT informaiton
def nonGMTauth(uname,pword,dir):
	body = """<?xml version="1.0" encoding="UTF-8"?>
	<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope"> 
		<soap12:Body>
			<Authenticate xmlns="http://<REDACTED>.com/OG">
				<userName>"""+uname+"""</userName>
				<password>"""+pword+"""</password>
				<directoryId>"""+str(dir)+"""</directoryId>
			</Authenticate>
		</soap12:Body>
	</soap12:Envelope>
	"""
	return body
# perfoms GMTauth to SOAP interface, choose this if you are suppling GMT information
def GMTauth(uname,pword,dir,gmt):
	body="""<?xml version="1.0" encoding="utf-8"?>
	<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
		<soap12:Body>
			<AuthenticateWithGMTOffset xmlns="http://<REDACTED>.com/OG">
				<userName>"""+uname+"""</userName>
				<password>"""+pword+"""</password>
				<directoryId>"""+str(dir)+"""</directoryId>
				<gmtOffset>"""+str(gmt)+"""</gmtOffset>
			</AuthenticateWithGMTOffset>
		</soap12:Body>
	</soap12:Envelope>"""
	return body
# performs the actual request && captures request, returns results
def doauth(target,authfunction):
	headers = {'content-type': 'application/soap+xml; charset=utf-8', 'Host': target, 'Content-Length': str(len(authfunction))}
	response = requests.post(url,data=authfunction,headers=headers)
	return response.content
# For loop 10 iterations, to produce session token from legit user:pass pair
def tokenGenerator(count):
 for x in range(0,count):
   results=doauth(target,GMTauth(uname,pword,dir,gmt))
   searchToken=re.search('<authResultns:Token>(.*)<\/authResultns:Token>',results)
   token=searchToken.groups(1)[0]
   print token
# main function
tokenGenerator(10)
