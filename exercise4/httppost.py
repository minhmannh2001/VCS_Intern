import socket
import argparse
from random import randint
from html import unescape
import urllib.parse

def getRandomUserAgent():
    user_agents = ["Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:38.0) Gecko/20100101 Firefox/38.0",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
                   "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36",
                   "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9",
                   "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36",
                   "Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0",
                   "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)",
                   "Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1)",
                   "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0",
                   "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36",
                   "Opera/9.80 (Windows NT 6.2; Win64; x64) Presto/2.12.388 Version/12.17",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0"]
    return user_agents[randint(0, len(user_agents) - 1)] 

# function for receiving all response's content 
def recvall(sock):
    response = b''
    buffer = sock.recv(4096)
    while buffer:
        response += buffer
        buffer = sock.recv(4096)
    return response

def handle_response(response):
    response = response.decode()
    # print(response)
    if "HTTP/1.1 302 Found" in response and "is incorrect" not in response and "is not registered on this site" not in response:
        if log == 'on':
            print(f"[INFORM] User {username} đăng nhập thành công")
        else:
            print(f"User {username} đăng nhập thành công")
    else:
        if log == 'on':
            print(f"[INFORM] User {username} đăng nhập thất bại")
        else:
            print(f"User {username} đăng nhập thất bại")

# Initialize parser instance
parser = argparse.ArgumentParser()
parser.add_argument('--log', help='enable/disable log', default='on')
parser.add_argument('--url', help='web address')
parser.add_argument('--user', help='username')
parser.add_argument('--password', help="user's password")
args = parser.parse_args()
log = args.log
url = args.url
username = args.user
password = args.password

# check if user provide enough arguments
if not url:
    print('Program end.')
    print('You need to specify the url of website.')
    print('Using -h argument for more information')
    exit(1)

url = url.replace('http://', '')
url = url.replace('https://', '')

if url[-1] == '/':
    url = url[:-1]

server_address = (url, 80)

if log == 'on':
    print(f"[INFORM] You've entered the web address: {url}")

# Prepare request body

params = {'log': username, 'pwd': password}
req_body_msg = urllib.parse.urlencode(params) + '&wp-submit=Log+In'

# Prepare request header
req_header_msg = 'POST /wp-login.php HTTP/1.1\r\n'
req_header_msg += 'Host: ' + url + '\r\n'
req_header_msg += f'Content-Length: {len(req_body_msg)}\r\n'
req_header_msg += 'Content-Type: application/x-www-form-urlencoded\r\n'
req_header_msg += 'User-Agent: ' + getRandomUserAgent() + '\r\n' 
req_header_msg += 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n'
req_header_msg += 'Accept-Language: en-US,en;q=0.9\r\n'
req_header_msg += 'Connection: close\r\n\r\n'

# Request message
req_msg = req_header_msg + req_body_msg

# print(req_msg)

# Initialize TCP socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    if log == 'on':
        print(f'[LOG]    Connecting to {server_address[0]}...')
    sock.connect(server_address)
    if log == 'on':
        print('[LOG]    Sending request...')
    sock.send(req_msg.encode())
    if log == 'on':
        print('[LOG]    Receiving response...')
    response = recvall(sock)
    if log == 'on':
        print('[LOG]    Handling response...')
    handle_response(response)