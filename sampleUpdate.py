#!/usr/bin/python

#import section
from pysnmp import hlapi
from pysnmp.hlapi import *
from ipaddress import *
import os, time, sys, argparse, math


#collect argument section

parser = argparse.ArgumentParser(description = 'The result of the output ')
parser.add_argument("ip",    help = 'Agent Ip')
parser.add_argument("port",    help = 'Port')
parser.add_argument("community",  help = 'community sting')
parser.add_argument("frequency", type=float ,   help = 'sample Frequency')
parser.add_argument("sample",  type=int,  help = 'Number of sample')
parser.add_argument("OID_list",    help = 'delimited list input',  nargs = '+',  type=str )

args = parser.parse_args()
oid_list = args.OID_list

oid_holder =[]
sample = args.sample

frequency = 1/args.frequency #requent time




if __name__ == '__main__' :
    

    def construct_object_types(oid_list):
        object_types = []
        for oid in oid_list:
            object_types.append(ObjectType(ObjectIdentity(oid)))
        
        return object_types

    
    def snmpQuery():
        global timeCount, startTime 
        startTime = time.time()
        
        iterator = getCmd(SnmpEngine( ),
                          CommunityData(args.community),
                          UdpTransportTarget((args.ip, args.port), 1, 1),
                          ContextData(),
                          *construct_object_types(oid_list),
                          lookupMib = True
                          )

        errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

        if errorIndication:  # SNMP engine errors
            print(errorIndication)
        else:
            if errorStatus:  # SNMP agent errors
                print('%s at %s' % (errorStatus.prettyPrint(), varBinds[int(errorIndex)-1] if errorIndex else '?'))
            else:
                for i in range(1, len(varBinds)):
                    if count !=0 and len(oid_list) > 0:
                          oidTimeRate = oid_list[i-1] 
                          oidTimeFetch = round(startTime - timeCount , 1)
                          obtainSampleRate = int( (oidTimeRate) / (oidFetchTime))

                          if rate_obtain_sample < 0 :
                              if varBinds[i].snmp_type == 'COUNTER32':
                                 oidTimeRate = oidTimeRate + 2**32
                                 print(str(startTime) , "|" , str(oidTimeRate / oidTimeFetch) , "|" )
                                       
                              elif varBinds[i].snmp_type == 'COUNTER64':
                                    oidTimeRate = oidTimeRate + 2**64
                                    print(str(startTime), "|" ,str(oidTimeRate / oidTimeFetch) , "|")                                       
                                       
                          else:
                               print (str(startTime) , "|" , str(obtainSampleRate) , "|")

        oid_holder = construct_object_types(oid_list)
        timecount = startTime
       
    if args.sample == -1:
       count = 0
       oid_holder 
       
       while(True):
           startTime = time.time()
           snmpQuery()
           time_respone = time.time()
           count +=1
           time.sleep(abs(frequency - time_response + startTime ))
    else:
        
        for count in range(0, args.sample + 1):
            startTime = time.time()
            snmpQuery()
            time_response = time.time()
            time.sleep(abs(frequency - time_response + startTime  ))
                     
            
             
                               
                  
                 
                
           
            
            
