#!/usr/bin/env python
# parse the mysql db the DB should exist prior to use
#
# Takes user input on shell interface useful for queries to file
#
import MySQLdb # mysql driver
from sys import argv as sa # takes user agruments
import __builtin__ as bi
'''takes initial argument from end user'''

bi.dbname=sa[1] # the db name
dbname = bi.dbname
bi.project=sa[2] # the project name
project = bi.project
#
#
#class dbfun():
# def __init__(self):
#  pass
def connup():
 '''connect to the sql db, change connection string as needed'''
 bi.db = MySQLdb.connect(host="localhost", user="root") #,"password")
 db=bi.db
 bi.cur = db.cursor()
 cur=bi.cur
def conndown():
 '''close the sql connection'''
 cur.close()
def selectdb():
 '''select the datastore to use for the query'''
 try:
  cur.execute('use ' + str(dbname))
 except Exception as e:
  pass
def docommit():
 '''commit the query'''
 db.commit()
def makedb():
 '''select the datastore to use for the query'''
 try:
  cur.execute('create database '+str(dbname)+';')
 except Exception as e:
  pass
def maketable():
 '''create table for db'''
 try:
  query=tables()
  cur.execute(query)
 except Exception as e:
  pass
def quickup():
 connup()
 selectdb()


'''Main functionality of the script'''
#
#
#class actions():
# def __init__(self):
#  pass
def dumppwds():
 '''dumps the passwords from the given db and tablename to unique'''
 try:
  print "dumppasswords attempting"
  query=pwddump()
  cur.execute(query)
  print "executed password dump"
 except Exception as e:
  print e
def dumpusers():
 '''dumps the passwords from the given db and tablename to unique'''
 try:
  query=userdump()
  cur.execute(query)
 except Exception as e:
  print e
def dumpdomains():
 '''dumps the passwords from the given db and tablename to unique'''
 try:
  query=domaindump()
  cur.execute(query)
 except Exception as e:
  print e
def dumpemails():
 '''dumps the passwords from the given db and tablename to unique'''
 try:
  query=emaildump()
  cur.execute(query)
 except Exception as e:
  print e
def dumpall():
 '''dumps the passwords from the given db and tablename to unique'''
 try:
  query=alldump()
  cur.execute(query)
 except Exception as e:
  pass
#
#
#class sqlcmds():
# def __init___(self):
#  pass
def fileup():
 query='LOAD DATA LOCAL INFILE "'+str(infile)+'" INTO TABLE '+str(project)+' FIELDS TERMINATED BY ":" (email,user,domain,password);'
 return query
def alldump():
 query='SELECT email, user, domain, password INTO OUTFILE '+str(project)+'_all_data.txt FROM '+str(project)+';'
 return query
def pwddump():
 query='SELECT password INTO OUTFILE "'+str(project)+'_password_data.txt" FROM (SELECT * FROM '+str(project)+' ORDER BY password DESC) AS t1 GROUP BY password;'
 print query
 return query
def userdump():
 query='SELECT user INTO OUTFILE "'+str(project)+'_user_data.txt" FROM (SELECT * FROM '+str(project)+' ORDER BY user DESC) AS t1 GROUP BY user;'
 return query
def domaindump():
 query='SELECT domain INTO OUTFILE "'+str(project)+'_domain_data.txt" FROM (SELECT * FROM '+str(project)+' ORDER BY domain DESC) AS t1 GROUP BY domain;'
 return query
def emaildump():
 query='SELECT email INTO OUTFILE "'+str(project)+'_email_data.txt" FROM (SELECT * FROM '+str(project)+' ORDER BY email DESC) AS t1 GROUP BY email;'
 return query
def tables():
 query='CREATE TABLE '+str(project)+' (id INT NOT NULL AUTO_INCREMENT,email VARCHAR(255) NOT NULL,user VARCHAR(255) NOT NULL,domain VARCHAR(255) NOT NULL,password VARCHAR(255) NOT NULL,PRIMARY KEY (id));'
 return query
def importfile():
 try:
  changedb=raw_input("[?] Do you want to change the DB: (y/n) ?")
  if changedb.lower() == "y":
   dbname=raw_input("\t[!] Enter the new dbname now: ")
   makedb()
   project=raw_input("\t[!] Enter the new project name now: ")
   selectdb()
  bi.infile=raw_input("[!] Enter a filename for importing: ")
  infile=bi.infile
  query=fileup()
  cur.execute(query)
  docommit()
 except Exception as e:
  print e
#
# end user console interface
#
#
def interface():
 quickup()
 print "\n[?] What do you want to do ?\n"
 print "\t* Dumpemails"
 print "\t* Dumpusers"
 print "\t* Dumpdomains"
 print "\t* Dumppasswords"
 print "\t* Dumpall"
 print "\t* Importfile"
 print "\t* Exit"
 ui=raw_input("\nEnter your choice now: ")
 if ui.lower() == "dumpemails":
  dumpemails()
  interface()
  print "ran dumpemails"
 if ui.lower() == "dumpusers":
  dumpusers()
  interface()
  print "dumpusers"
 if ui.lower() == "dumpdomains":
  dumpdomains()
  interface()
 if ui.lower() == "dumppasswords":
  dumppwds()
  interface()
  print "ran dumppasswords"
 if ui.lower() == "dumpall":
  dumpall()
  interface()
 if ui.lower() == "importfile":
  importfile()
  interface()
 if ui.lower == "exit":
  exit()

interface()
