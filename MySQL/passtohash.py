import glob
import re
import base64
import hashlib
import binascii
import passlib.hash
from sys import argv as sa
d = glob.glob(sa[1])

try:
 def ntlmhash(passwd):
  hash=hashlib.new('md4', passwd.encode('utf-16le')).digest()
  return binascii.hexlify(hash)

 def lmhash(passwd):
  return passlib.hash.lmhash.encrypt(passwd)

 def md5hash(passwd):
  return hashlib.md5(passwd).hexdigest()

 def sha1hash(passwd):
  return hashlib.sha1(passwd).hexdigest()

 def sha224hash(passwd):
  return hashlib.sha224(passwd).hexdigest()

 def sha256hash(passwd):
  return hashlib.sha256(passwd).hexdigest()

 def sha384hash(passwd):
  return hashlib.sha384(passwd).hexdigest()

 def sha512hash(passwd):
  return hashlib.sha512(passwd).hexdigest()
except Exception as e:
 pass

for i in d:
 with open(i, "r") as f:
  for x in f:
   x = x.strip()
   try:
    print("%s,%s,%s,%s,%s,%s,%s,%s,%s") % (x,md5hash(x),sha1hash(x),sha224hash(x),sha256hash(x),sha384hash(x), sha512hash(x), lmhash(x), ntlmhash(x))
   except Exception as e:
    #print e
    pass
