#!/usr/bin/python

import sys, time, pysnmp
import math
from math import *
import requests
from pysnmp import *


agent_details = sys.argv[1]
flag = agent_details.split(':')#split the ip:port:comm
agent_address = flag[0]
agent_port_details = flag[1]
agent_community = flag[2]
samplefrequency = float(sys.argv[2]) #frequency
sampletime = 1/samplefrequency #time
total_samples = int(sys.argv[3])#totalsamples
oids = []
oid_top = []
oid_stack = []


for i in range(4,len(sys.argv)): 
	oids.append(sys.argv[i])
oids.insert(0,'1.3.6.1.2.1.1.3.0')#SysUpTime oid

def snmpmetrics():
	global oid_top, time_counting 
	session=requests.Session(hostname=agent_address,remote_port=agent_port_details,community='public',version=2,timeout=1,retries=1)
	response_obtaining = session.get(oids)
	oid_stack=[]
	

	for j in range(1,len(response_obtaining)):
		if response_obtaining[j].value!='NOSUCHOBJECT' and response_obtaining[j].value!='NOSUCHINSTANCE':
			oid_stack.append(int(response_obtaining[j].value))
			
			if count!=0 and len(oid_top)>0:
				oid_time_rates = int(oid_stack[j-1]) - int(oid_top[j-1])
				oid_time_fetched = round(past_time-time_counting,1)#round to nearest 1 of decimal
				rate_obtained_samples = int(oid_time_rates / oid_time_fetched)
				if rate_obtained_samples < 0 :
					if response_obtaining[j].snmp_type == 'COUNTER32': 
						oid_time_rates = oid_time_rates + 2**32#32 bit counter
						print(str(past_time) +"|"+ str(oid_time_rates / oid_time_fetched) +"|")
					elif response_obtaining[j].snmp_type == 'COUNTER64':
						oid_time_rates = oid_time_rates + 2**64#64 bit counter
						print(str(past_time) +"|"+ str(oid_time_rates / oid_time_fetched) +"|")
				else:
					print(str(past_time) +"|"+ str(rate_obtained_samples) +"|")

	oid_top = oid_stack
	time_counting = past_time


if total_samples==-1:
	count=0
	oid_top=[]
	while True:
		past_time = (time.time())
		snmpmetrics()
		time_response = (time.time())
		count = count+1
		time.sleep(abs(sampletime - time_response + past_time))
else:
	oid_top = []
	for count in range(0,total_samples+1):
		past_time = (time.time())
		snmpmetrics()
		time_response = (time.time())
		time.sleep(abs(sampletime - time_response + past_time))
		
