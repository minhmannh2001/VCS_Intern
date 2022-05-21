import socket
import argparse
from random import randint
from html import unescape

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

def get_web_title(response):
    response = response.decode()
    start_pos = response.find('<title>') + 7
    end_pos = response.find('</title>')
    return unescape(response[start_pos:end_pos])

# initialize parser instance
parser = argparse.ArgumentParser(description='You need to provide correct arguments for program to retrieve information from website')
parser.add_argument('-u', '--url', default=None, help='the web address')
parser.add_argument('-l', '--log', default='on', help='turn on/off the log | LOG = ["on", "off"]')
args = parser.parse_args()
url = args.url
log = args.log

# check if user provide enough arguments
if not url:
    print('Program end.')
    print('You need to specify the url of website.')
    print('Using -h argument for more information')
    exit(1)

# get only domain name from url
url = url.replace('http://', '')
url = url.replace('https://', '')

if url[-1] == '/':
    url = url[:-1]

if log == 'on':
    print(f"[INFORM] You've entered the web address: {url}")

# Request's content, which is intercepted by Burp Suite:
# GET / HTTP/1.1
# Host: blogtest.vnprogramming.com
# Upgrade-Insecure-Requests: 1
# User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36
# Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
# Accept-Encoding: gzip, deflate
# Accept-Language: en-US,en;q=0.9
# Connection: close

# Prepare packet header
get_request_msg = 'GET / HTTP/1.1\r\n'
get_request_msg += 'Host: ' + url + '\r\n'
get_request_msg += 'User-Agent: ' + getRandomUserAgent() + '\r\n' 
get_request_msg += 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n'
# get_request_msg += 'Accept-Encoding: gzip, deflate\r\n'
get_request_msg += 'Accept-Language: en-US,en;q=0.9\r\n'
get_request_msg += 'Connection: close\r\n\r\n'

# print(get_request_msg)

server_address = (url, 80)

# Initialize TCP socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    if log == 'on':
        print(f'[LOG]    Connecting to {server_address[0]}...')
    sock.connect(server_address)
    if log == 'on':
        print('[LOG]    Sending request...')
    sock.send(get_request_msg.encode())
    if log == 'on':
        print('[LOG]    Receiving response...')
    response = recvall(sock)
    if log == 'on':
        print("[LOG]    Extracting web's title...")
    title = get_web_title(response)
    if log == 'on':
        print(f"[INFORM] The web's title: {title}")
    else:
        print(f"The web's title: {title}")
    if log == 'on':
        print('[LOG]    Done')
