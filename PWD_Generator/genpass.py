#
# Python password generator which produces all potential combinations based on length and charset
# Takes user input as to which list to generate
#
#
def makepwdlist(charset, pwd_length):
  import itertools, string
  all=[]
  alpha=[]
  alphanum=[]
  retlist=[]
  # make upper charlist
  number=map(chr, range(48,58))
  upper=map(chr, range(65, 91))
  lower=map(chr, range(97, 123))
  special=map(chr, range(32,47))
  for xspec1 in map(chr, range(58,64)):
    special.append(xspec1)
  for xspec2 in map(chr, range(91,96)):
    special.append(xspec2)
  for xspec3 in map(chr, range(123,126)):
    special.append(xspec3)
  # make all charset
  for n in number:
    all.append(n)
    alphanum.append(n)
  for u in upper:
    all.append(u)
    alpha.append(u)
    alphanum.append(u)
  for l in lower:
    all.append(l)
    alpha.append(l)
    alphanum.append(l)
  # make special charset
  for s in special:
    all.append(s)
  if charset == "all":
    cset=all
  if charset == "number":
    cset=number
  if charset == "special":
    cset=special
  if charset == "upper":
    cset=upper 
  if charset == "lower":
    cset=lower  
  if charset == "alpha":
    cset=alpha 
  if charset == "alphanum":
    cset=alphanum
  for xlen in xrange(pwd_length+1):
    keywords = [''.join(i) for i in itertools.product(cset, repeat = xlen)]
    retlist.append(keywords)
  return retlist

makepwdlist("number",4)
