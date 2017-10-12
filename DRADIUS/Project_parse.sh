
projectMatrix() {
  appname=$(cat $1| head -n1 | tr -s "\t" "," | tr -s " " "_" | tr -s "\n" " "| sed -r "s/^\,(.*)/\1/g")
  proto=$(cat $1 | tail -n+2| tr -s "\t" "," | cut -d "," -f1 | sed -r s"/( |\/)/_/g")
  matrix=$(cat $1 | tail -n+2| tr -s "\t" "," | sed -r s"/( |\/)/_/g")         
  count=0;
  for x in $(echo $appname | tr -s " " "_" | tr -s "," " ");
    do
      count=$((count+1));
      echo -e "[*] $x";
      for p in $(echo $proto | tr -s " " "\n");
        do
          for z in $(echo $matrix | tr -s " " "\n"| grep $p | cut -d "," -f2-);
            do
              if [ "`echo $z | cut -d"," -f$count`" == "x" ]; then
                echo -e "\t[-] Requires: $p testing";
              fi;
          done | \
          sort -u;
      done;
  echo;
  done;
  count=0;
}

