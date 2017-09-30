# find your node modules directory
# scrapes the project.json files for module information (_id)
# checks module against 3rd party site for known vulns
# dumps list of required modules and their locations/verision
# saves any output to evidence dir

getNodepackages() {
 rawprojects=`grep -i _id $(find . -maxdepth 10 -type f | grep -E "package\.json$")`
}
querymodule() {
 echo $modname
 checkmodule=`curl -k https://nodesecurity.io/advisories/?search=$modname 2>/dev/null`
}
getNodepackages
bulkprocess() {
 for xmodule in $(echo $rawprojects| sed -r "s/\, \./\,\n\./g" | tr -d " "); do
  echo $xmodule
  modver=`echo $xmodule | cut -d ':' -f3 | cut -d "@" -f2 | cut -d'"' -f1`
  modname=`echo $xmodule | cut -d ':' -f3 | cut -d "@" -f1 | cut -d'"' -f2`
  querymodule $modname
  isadvisory=`echo $checkmodule | sed -r "s/></>\n</g" | grep -A1 advisory-title | tail -n1`
  if [ "$isadvisory" != "" ]; then
   advisorydate=`echo $checkmodule | sed -r "s/></>\n</g" | grep -A1 advisory-date | tail -n1 | cut -d"<" -f2 | cut -d">" -f2`
   patched=`echo $checkmodule | sed -r "s/></>\n</g" | grep -A5 module-name | grep -i patched | cut -d"=" -f3 | cut -d "<" -f1 | tr -s " " "\n" | sort -u`
   version=`echo $checkmodule | sed -r "s/></>\n</g" | grep -A5 module-name | grep -i vulnerable | cut -d"=" -f3 | cut -d "<" -f1 | tr -s " " "\n" | sort -u`
   download=`echo $checkmodule | sed -r "s/></>\n</g" | grep -A5 module-name | grep href | cut -d '"' -f2 | tr -s " " "\n" | sort -u`
   effectedmod=`echo $checkmodule | sed -r "s/></>\n</g" | grep -A5 module-name | grep href | cut -d '>' -f2 | cut -d"<" -f1 | tr -s " " "\n" | sort -u`
   versort=`echo -e "$modver\n$version\n$patched" | sort -V`
   # sanitycheck
   patchline=`echo -e $(echo $versort) | tr -s " " "\n" | grep -n $(echo $patched) 2>/dev/null | cut -d":" -f1`
   modline=`echo -e $(echo $versort) | tr -s " " "\n" | grep -n $(echo $modver) 2>/dev/null | cut -d":" -f1`
   verline=`echo -e $(echo $versort) | tr -s " " "\n" | grep -n $(echo $version) 2>/dev/null | cut -d":" -f1`
   if [ "$patchline" != "" ]; then
    if [ "$verline" != "3" ]; then
     echo -e "\\------------------------------------\\"
     if [ "$effectedmod" != "" ]; then
      echo -e "\t[-] Impacted module: $effectedmod"
     fi
     if [ "$advisorydate" != "" ]; then
      echo -e "\t\t[!] Advisory date: $advisorydate"
     fi
     if [ "$modver" != "" ]; then
      echo -e "\t\t[!] Current Version $modver"
     fi
     if [ "$patched" != "" ]; then
      echo -e "\t\t[!] Patched version: $patched"
     fi
     if [ "$download" != "" ]; then
      echo -e "\t\t[!] Download URL: $download"
     fi
     echo -e "\\------------------------------------\\"
    fi
   fi
  fi
 done
}
