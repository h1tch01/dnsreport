#!/usr/bin/env python3
# 
# dnsreport.py
# Brian Hitchcock (h1tch)
# 2020/09/15
# Python3 DNS lookup - Formats in CSV for 10-D Reports
#EXAMPLE
#python3 dnsreport.py --domain google.com --subdomain subdomains-100.txt
#
import dns.resolver
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--domain',default="google.com", help="domain name to test example bank.com")
parser.add_argument('--subdomain',default="subdomains-100.txt", help="subdomain wordlist to brute")
args = parser.parse_args()

domain = args.domain
SubDomain = args.subdomain


# does the actual lookups and returns results
def dns_lookup(record,Rtype):
        try:
            result = dns.resolver.resolve(record, Rtype)
        except:
        	#print (result)
        	# ignore errors aka record doesnt exsist
        	return []

        return result 



# NS Lookup
resultN = dns_lookup(domain,'NS')
for ipval in resultN:
	print(domain +",NS," + ipval.to_text())

# MX Lookup
resultM = dns_lookup(domain,'MX')
for ipval in resultM:
	print(domain +",MX," + ipval.to_text())

# TXT Lookup
resultT = dns_lookup(domain,'TXT')
for ipval in resultT:
	print(domain +",TXT," + ipval.to_text())

# domain only A Lookup
resultA = dns_lookup(domain,'A')
for ipval in resultA:
	print(domain +",A," + ipval.to_text())

# domain only CNAME Lookup
resultC = dns_lookup(domain,'CNAME')
for ipval in resultC:
	print(domain +",CNAME," + ipval.to_text())

# Wildcard Check
Wdomain = "klsdfioer893jskdf89IDf893skd." + domain
resultW = dns_lookup(Wdomain,'A')
if resultW:
	for ipval in resultW:
		WildCardIP = ipval.to_text()
		print ("*." + domain + ",A," + WildCardIP)


with open(SubDomain) as fp:
	for cnt, line in enumerate(fp):
		Trecord = line.strip() + "." + domain


# A  from subdomain list Record brute
		resultA = dns_lookup(Trecord,'A')
		for ipval in resultA:
			if ipval.to_text() != WildCardIP:
				print(line.strip() + "." + domain +",A," + ipval.to_text())
# Cname from subdomain list record brute
		resultC = dns_lookup(Trecord,'CNAME')
		for ipval in resultC:
			if ipval.to_text() != WildCardIP:
				print(line.strip() + "." + domain +",CNAME," + ipval.to_text())


