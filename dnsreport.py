#!/usr/bin/env python3
#
# dnsreport.py
# Brian Hitchcock (h1tch)
# 2020/09/15 - Initial
# 2024/02/16 - Modernize and add threading
# Python3 DNS lookup - Formats in CSV for Reports
#EXAMPLE
#python3 dnsreport.py google.com subdomains-100.txt
# requirements
# pip3 install dnspython

import threading
import dns.resolver
import argparse

def resolve_subdomain(subdomain, domain, Output):
  try:
    answers = dns.resolver.resolve(subdomain + "." + domain)
    answers.timeout = 2
    answers.lifetime = 2
    for answer in answers:
      print(f"{subdomain}.{domain},A,{answer.to_text() }")
      with open(Output, 'a') as file:
        file.write(f"{subdomain}.{domain},A,{answer.to_text() }")
        file.write("\n")
  except dns.resolver.NXDOMAIN:
    pass  # Subdomain not found
  except dns.resolver.NoAnswer:
    pass  # No answer for the query
  return

def main():
  parser = argparse.ArgumentParser(description="Perform DNS queries using a text file of subdomains")
  parser.add_argument("domain", help="The target domain")
  parser.add_argument("subdomains_file",default="subdomains-100.txt", help="The file containing subdomains")
  args = parser.parse_args()
  Output = "DNS-" + args.domain + ".csv"
      
  print ("\n***-=Writing output to file=-***   " + Output + "\n")
  # NS Lookup
  resultN = dns.resolver.resolve(args.domain, 'NS')
  for ipval in resultN:
          print(args.domain +",NS," + ipval.to_text())
          with open(Output, 'w') as file:
              file.write(args.domain +",NS," + ipval.to_text() + "\n")

  # MX Lookup
  resultM = dns.resolver.resolve(args.domain,'MX')
  for ipval in resultM:
          print(args.domain +",MX," + ipval.to_text())
          with open(Output, 'a') as file:
            file.write(args.domain +",MX," + ipval.to_text() + "\n")

  # TXT Lookup
  resultT = dns.resolver.resolve(args.domain,'TXT')
  for ipval in resultT:
          print(args.domain +",TXT," + ipval.to_text())
          with open(Output, 'a') as file:
            file.write(args.domain +",TXT," + ipval.to_text() + "\n")

  # domain only A Lookup
  resultA = dns.resolver.resolve(args.domain,'A')
  for ipval in resultA:
          print(args.domain +",A," + ipval.to_text())
          with open(Output, 'a') as file:
            file.write(args.domain +",A," + ipval.to_text() + "\n")

  # domain only CNAME Lookup
  try:
    resultC = dns.resolver.resolve(args.domain,'CNAME')
    for ipval in resultC:
            print(args.domain +",CNAME," + ipval.to_text())
            with open(Output, 'a') as file:
                file.write(args.domain +",CNAME," + ipval.to_text() + "\n")
  except dns.resolver.NXDOMAIN:
    pass  # Subdomain not found
  except dns.resolver.NoAnswer:
    pass

  WildCardIP = "999.999.999.999"
  WildCardTrue = "0"
  # Wildcard Check
  Wdomain = "klsdfioer893jskdf89IDf893skd." + args.domain
  try:
    resultW = dns.resolver.resolve(Wdomain,'A')
    if resultW:
           for ipval in resultW:
                   WildCardIP = ipval.to_text()
                   print ("*." + args.domain + ",A," + WildCardIP)
                   WildCardTrue = "1"
                   with open(Output, 'a') as file:
                     file.write("*." + args.domain + ",A," + WildCardIP  + "\n")
  except dns.resolver.NXDOMAIN:
    pass  # Subdomain not found
  except dns.resolver.NoAnswer:
    pass

    # open subdomains file passed as an arg
  with open(args.subdomains_file, "r") as file:
    subdomains = file.read().splitlines()
    # brute force A record lookup if Wildcard is not in use
  if WildCardTrue == "0":
    threads = []
    for subdomain in subdomains:
     thread = threading.Thread(target=resolve_subdomain, args=(subdomain, args.domain, Output))
     threads.append(thread)
     thread.start()

    for thread in threads:
     thread.join()

if __name__ == "__main__":
  main()
