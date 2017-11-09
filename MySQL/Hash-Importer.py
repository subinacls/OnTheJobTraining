import MySQLdb
from sys import argv as sa

dbname="HashPass"
project=sa[1]
infile=sa[2]

db = MySQLdb.connect(host="localhost", user="root")
cur = db.cursor()
try:
 cur.execute("create database " + str(dbname))
except Exception as e:
 #print e
 cur.execute("use " + str(dbname))
try:
 cur.execute("CREATE TABLE "+str(project)+" (" \
   "id INT NOT NULL AUTO_INCREMENT," \
   "password VARCHAR(255) NOT NULL," \
   "md5sum VARCHAR(255) NOT NULL," \
   "sha1sum VARCHAR(255) NOT NULL," \
   "sha224sum VARCHAR(255) NOT NULL," \
   "sha256sum VARCHAR(255) NOT NULL," \
   "sha384sum VARCHAR(255) NOT NULL," \
   "sha512sum VARCHAR(255) NOT NULL," \
   "lmhash VARCHAR(255) NOT NULL," \
   "ntlmhash VARCHAR(255) NOT NULL," \
   "PRIMARY KEY (id));")
except Exception as e:
 #print e
 pass
try:
 cur.execute("ALTER TABLE "+str(project)+" AUTO_INCREMENT = 1;")
except Exception as e:
 #print e
 pass
db.commit()
cur.close()
db = MySQLdb.connect(host="localhost", user="root")
cur = db.cursor()
try:
 cur.execute("use " + str(dbname))
 query="LOAD DATA LOCAL INFILE '"+infile+"' " \
    "INTO TABLE "+str(project)+" " \
    "FIELDS TERMINATED BY ',' (" \
        "password, " \
        "md5sum, " \
        "sha1sum," \
        "sha224sum," \
        "sha256sum," \
        "sha384sum," \
        "sha512sum," \
        "lmhash," \
        "ntlmhash);"
 cur.execute(query)
except Exception as e:
 print e
 pass
db.commit()
cur.close()
print "Finished"
