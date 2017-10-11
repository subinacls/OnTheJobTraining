# parse copy and pasted output from IDA text view
# save local disk and use the following function to manipulate the data
#
## Example data (save as test.infile)
# nano ./test.infile
# """
# .rdata:004F3BFC aFfffffffffffff db '9999999999999999999999999999999999999999',0
# .rdata:004F3C25                 align 4
# .rdata:004F3C28 a1c97befc54bd7a db 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',0
# .rdata:004F3C51                 align 4
# .rdata:004F3C54 a01000000000000 db 'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',0
# .rdata:004F3C7F                 align 10h
# .rdata:004F3C80 a4a96b5688ef573 db 'CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC',0
# .rdata:004F3CA9                 align 4
# .rdata:004F3CAC a23a62855316894 db 'DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD',0
# """
## Function
#
parseida() { cat $1 | sed -r "s/(.*)('|\")([0-9A-Fa-f]{1,})('|\")(.*)/\3/g" | grep -vE "\t" | tr -d "\n" | xargs echo -e; }
#
## Example use
# parseida test.infile > test.outfile
#
## Example output
# cat ./test.outfile
# """
# 9999999999999999999999999999999999999999AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD
# """
#
