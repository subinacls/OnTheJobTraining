#!/usr/bin/env python
# parse the mysql db
# the DB should exist prior to use
#
# Takes user input on shell interface
# useful for queries to file
#

import MySQLdb # mysql driver
from sys import argv as sa # takes user agruments

'''takes initial argument from end user'''
dbname=sa[1] # the db name
project=sa[2] # the project name
outfile=sa[3] # the outfile to disk

def dbconnect():
 '''connect to the sql db'''
 db = MySQLdb.connect(host="localhost", user="root")
 cur = db.cursor()

def dbteardown():
 '''close the sql connection'''
 cur.close()

def dbcommit():
 '''commit the query'''
 db.commit()

def selectdb():
 '''select the datastore to use for the query'''
 try:
  createdb()
  settable()
 except Exception as e:
  pass
 try:
  cur.execute("use " + str(dbname))
 except Exception as e:
  pass

def createdb():
 '''select the datastore to use for the query'''
 try:
  cur.execute("create database" + str(dbname) + ";")
 except Exception as e:
  pass

def settable():
 '''create table for db'''
 try:
  query=sqlquery().tables()
  cur.execute(query)
 except Exception as e:
  pass

'''build the connection up'''
dbconnect()
selectdb()

'''Main functionality of the script'''

def dumppwds():
 '''dumps the passwords from the given db and tablename to unique'''
 try:
  query=sqlquery().pwddump()
  cur.execute(query)
 except Exception as e:
  pass

def dumpusers():
 '''dumps the passwords from the given db and tablename to unique'''
 try:
  query=sqlquery().userdump()
  cur.execute(query)
 except Exception as e:
  pass

def dumpdomains():
 '''dumps the passwords from the given db and tablename to unique'''
 try:
  query=sqlquery().domaindump()
  cur.execute(query)
 except Exception as e:
  pass

def dumpemails():
 '''dumps the passwords from the given db and tablename to unique'''
 try:
  query=sqlquery().emaildump()
  cur.execute(query)
 except Exception as e:
  pass

def dumpall():
 '''dumps the passwords from the given db and tablename to unique'''
 try:
  query=sqlquery().alldump()
  cur.execute(query)
 except Exception as e:
  pass
'''
def importfile():
 try:
  print("[?] Do you want to change the DB: %s (y/n) ?") % dbname
  read changedb
  if changedb.lower() == "y":
   read dbname "\t[!] Enter the new dbname now:"
   read project "\t[!] Enter the new project name now:"
   selectdb()
  print("[?] Enter a filename for importing: %s ?")
  read infile "[!] Enter a filename for importing:"
  query=sqlquery().fileup()
  cur.execute(query)
 except Exception as e:
  pass
'''

class sqlquery():
 def __init__(self):
  pass
 def fileup(self):
  query="LOAD DATA " \
    "LOCAL INFILE '" \
    +str(infile)+ \
    "' INTO TABLE "\
    +str(project)+ \
    " FIELDS TERMINATED BY ':' " \
    "(email," \
    "user," \
    "domain," \
    "password);"
  return query
 def alldump(self):
  query="SELECT " \
    "email, user, domain, password " \
    "INTO OUTFILE '"+str(project)+"_all_data.txt"'" \
    "FROM "+str(project)+";"
  return query
 def pwddump(self):
  query="SELECT " \
    "password " \
    "INTO OUTFILE '"+str(project)+"_password_data.txt"'" \
    "FROM " \
    "(SELECT " \
    "* " \
    "FROM "
    +str(project)+ \
    " ORDER BY " \
    "password "\
    "DESC) " \
    "AS t1 " \
    "GROUP BY "\
    "password);"
  return query
 def userdump(self):
  query="SELECT " \
    "user " \
    'INTO OUTFILE "'+str(project)+'"_user_data.txt"' \
    "FROM " \
    "(SELECT " \
    "* " \
    "FROM "
    +str(project)+ \
    " ORDER BY " \
    "user "\
    "DESC) " \
    "AS t1 " \
    "GROUP BY "\
    "user);"
  return query
 def domaindump(self):
  query="SELECT " \
    "domain " \
    'INTO OUTFILE "'+str(project)+'"_domain_data.txt"' \
    "FROM (SELECT " \
    "* " \
    "FROM "
    +str(project)+ \
    " ORDER BY " \
    "domain "\
    "DESC) " \
    "AS t1 " \
    "GROUP BY "\
    "domain);"
  return domain
 def emaildump(self):
  query="SELECT " \
    "email " \
    'INTO OUTFILE "'+str(project)+'"_email_data.txt"' \
    "FROM (SELECT " \
    "* " \
    "FROM "
    +str(project)+ \
    " ORDER BY " \
    "email "\
    "DESC) " \
    "AS t1 " \
    "GROUP BY "\
    "email);"
  return query
 def tables(self):
  query="CREATE TABLE " \
    +str(project)+ \
    " (" \
    "id INT NOT NULL AUTO_INCREMENT," \
    "email VARCHAR(255) NOT NULL," \
    "user VARCHAR(255) NOT NULL," \
    "domain VARCHAR(255) NOT NULL," \
    "password VARCHAR(255) NOT NULL," \
    "PRIMARY KEY (id)" \
    ");"
  return query

# end user console interface
def interface()
 print "What do you want to do ?"
 print "\t* Dumpemails"
 print "\t* Dumpusers"
 print "\t* Dumpdomains"
 print "\t* Dumppasswords"
 print "\t* Dumpall"
 print "\t* Importfile"
 print "\t* Exit"
 read ui "\nEnter your choice now:"
 if ui.lower == "dumpemails"
  dumpemails()
 if ui.lower == "dumpusers"
  dumpusers()
 if ui.lower == "dumpdomains"
  dumpdomains()
 if ui.lower == "dumppasswords"
  dumppwds()
 if ui.lower == "dumpall"
  dumpall()
 if ui.lower == "importfile"
  importfile()
 if ui.lower == "exit"
  exit()
