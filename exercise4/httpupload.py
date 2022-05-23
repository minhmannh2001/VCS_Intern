import socket
import argparse
from random import randint
import urllib.parse
import re
from os.path import exists

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

def handle_login_response(response):
    response = response.decode()
    # print(response)
    cookie = ''
    for s in response.split('\r\n'):
        if 'Set-Cookie:' in s:
            cookie += s.split(' ')[1]
    # print(cookie)
    if "HTTP/1.1 302 Found" in response and "is incorrect" not in response and "is not registered on this site" not in response:
        if log == 'on':
            print(f"[INFORM] User {username} đăng nhập thành công")
        else:
            print(f"User {username} đăng nhập thành công")
        return cookie
    else:
        if log == 'on':
            print(f"[INFORM] User {username} đăng nhập thất bại")
            print(f'[LOG]    Program exit')
            exit(1)
        else:
            print(f"User {username} đăng nhập thất bại")
            exit(1)

def handle_upload_response(response):
    response = response.decode()
    if "HTTP/1.1 200 OK" in response and '"success":true' in response:
        if log == 'on':
            print('[INFORM] Upload success.')
        else:
            print('Upload success.')
        index = response.find('"url"') + 7
        link = response[index:].split('"')[0]
        link = link.replace('\\', '')
        if log == 'on':
            print('[INFORM] File upload url: ' + link)
        else:
            print('File upload url: ' + link)

    else:
        if log == 'on':
            print('[INFORM] Upload fail.')
        else:
            print('Upload fail.')

def get_wpnonce(response):
    response = response.decode()
    idx = response.find('name="_wpnonce" value')
    return response[idx + 23:].split('"')[0]

# Initialize parser instance
parser = argparse.ArgumentParser()
parser.add_argument('--log', help='enable/disable log', default='on')
parser.add_argument('--url', help='web address')
parser.add_argument('--user', help='username')
parser.add_argument('--password', help="user's password")
parser.add_argument('--localfile', help="file's local path")
args = parser.parse_args()
log = args.log
url = args.url
username = args.user
password = args.password
localfile = args.localfile

# check if user provide enough arguments
if not url:
    if log == 'on':
        print('[LOG]    Program end.')
        print('[LOG]    You need to specify the url of website.')
        print('[LOG]    Using -h argument for more information')
    else:
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

random_user_agent = getRandomUserAgent()

# Prepare request header
req_header_msg = 'POST /wp-login.php HTTP/1.1\r\n'
req_header_msg += 'Host: ' + url + '\r\n'
req_header_msg += f'Content-Length: {len(req_body_msg)}\r\n'
req_header_msg += 'Origin: http://blogtest.vnprogramming.com\r\n'
req_header_msg += 'Content-Type: application/x-www-form-urlencoded\r\n'
req_header_msg += 'User-Agent: ' + random_user_agent + '\r\n' 
req_header_msg += 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n'
req_header_msg += 'Accept-Language: en-US,en;q=0.9\r\n'
req_header_msg += 'Cookie: wp-settings-time-2=1653110778; wordpress_test_cookie=WP%20Cookie%20check\r\n'
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
        print(f'[LOG]    Logging to {server_address[0]}...')
    if log == 'on':
        print('[LOG]    Sending request...')
    sock.send(req_msg.encode())
    if log == 'on':
        print('[LOG]    Receiving response...')
    response = recvall(sock)
    if log == 'on':
        print('[LOG]    Handling response...')
    cookie = handle_login_response(response)

# Reinitialize TCP socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    if log == 'on':
        print(f'[LOG]    Reconnecting to {server_address[0]}...')
    sock.connect(server_address)

    # Make request to get _wpnonce value

    req_msg = 'GET /wp-admin/media-new.php HTTP/1.1\r\n'
    req_msg += 'Host: ' + url + '\r\n'
    req_msg += 'User-Agent: ' + random_user_agent + '\r\n' 
    req_msg += 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n'
    req_msg += 'Accept-Language: en-US,en;q=0.9\r\n'
    req_msg += f'Cookie: {cookie}\r\n'
    req_msg += 'Connection: close\r\n\r\n'

    # print(req_msg)

    if log == 'on':
        print(f'[LOG]    Getting _wpnonce from {server_address[0]}...')
    if log == 'on':
        print('[LOG]    Sending request...')
    sock.send(req_msg.encode())
    if log == 'on':
        print('[LOG]    Receiving response...')
    response = recvall(sock)
    # print(response.decode())
    _wpnonce = get_wpnonce(response)
    if log == 'on':
        print(f'[INFORM] _wpnonce value: {_wpnonce}')

# Upload image using post method

# Reinitialize TCP socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    if log == 'on':
        print(f'[LOG]    Reconnecting to {server_address[0]}...')
    sock.connect(server_address)

    if not exists(localfile):
        if log == 'on':
            print('[LOG]    File không tồn tại.')
            print('[LOG]    Upload failed.')
            exit(1)
        else:
            print('Upload failed.')
            exit(1)

    # load image in localfile path
    with open(localfile, 'rb') as f:
        image_content = f.read()

    filename = localfile.split('/')[-1]
    fileext = localfile.split('.')[-1]
    
    # Make request to upload image

    req_body_msg = '------WebKitFormBoundary\r\n'
    req_body_msg += 'Content-Disposition: form-data; name="name"\r\n\r\n'
    req_body_msg += f'{filename}\r\n'
    req_body_msg += '------WebKitFormBoundary\r\n'
    req_body_msg += 'Content-Disposition: form-data; name="action"\r\n\r\n'
    req_body_msg += 'upload-attachment\r\n'
    req_body_msg += '------WebKitFormBoundary\r\n'
    req_body_msg += 'Content-Disposition: form-data; name="_wpnonce"\r\n\r\n'
    req_body_msg += f'{_wpnonce}\r\n'
    req_body_msg += '------WebKitFormBoundary\r\n'
    req_body_msg += f'Content-Disposition: form-data; name="async-upload"; filename="{filename}"\r\n'
    req_body_msg += f'Content-Type: image/{fileext}\r\n\r\n'
    req_body_msg = req_body_msg.encode() + image_content + '\r\n------WebKitFormBoundary\r\n'.encode()

    req_header_msg = 'POST /wp-admin/async-upload.php HTTP/1.1\r\n'
    req_header_msg += 'Host: ' + url + '\r\n'
    req_header_msg += f'Content-Length: {len(req_body_msg)}\r\n'
    req_header_msg += 'User-Agent: ' + random_user_agent + '\r\n' 
    req_header_msg += 'Content-Type: multipart/form-data; boundary=----WebKitFormBoundary\r\n'
    req_header_msg += 'Accept: */*\r\n'
    req_header_msg += 'Accept-Language: en-US,en;q=0.9\r\n'
    req_header_msg += f'Cookie: {cookie}\r\n'
    req_header_msg += 'Connection: close\r\n\r\n'

    req_msg = req_header_msg.encode() + req_body_msg

    # print(req_msg)

    if log == 'on':
        print(f'[LOG]    Uploading image to {server_address[0]}...')
    if log == 'on':
        print('[LOG]    Sending request...')
    sock.send(req_msg)
    if log == 'on':
        print('[LOG]    Receiving response...')
    response = recvall(sock)

    # print(response.decode())

    handle_upload_response(response)
    