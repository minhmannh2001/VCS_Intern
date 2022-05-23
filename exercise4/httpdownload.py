import socket
import argparse
from random import randint
import datetime
import os

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
    response = response.decode('iso-8859-1')

    # print(response)

    if "The requested URL was not found on this server" in response and "HTTP/1.1 200 OK" not in response:
        if log == 'on':
            print('[LOG]    Không tồn tại file ảnh.')
            exit(1)
        else:
            print('Không tồn tại file ảnh.')
            exit(1)
    else:
        index = response.find('Content-Length: ')
        image_len = response[index + 16:].split('\r\n')[0]
        image_len = int(image_len)
        image_name = remotefile.split('/')[-1]
        if log == 'on':
            print(f'[INFORM] Image: {image_name}')
            print(f'[INFORM] Kích thước file ảnh: {image_len} bytes')
            print(f'[LOG]    Downloading image {image_name}...')
        else:
            print(f'Kích thước file ảnh: {image_len} bytes')
        
        image_content = response.split('\r\n\r\n')[-1].encode('iso-8859-1')

        saved_image = image_name.split('.')[0] + '-' + str(datetime.datetime.now()).split(' ')[0] + '-' + str(datetime.datetime.now()).split(' ')[1] + '.' + image_name.split('.')[-1]
        if log == 'on':
            print(f'[LOG]    Saving image as {saved_image}...')
        with open(saved_image, 'wb') as file_handler:
            result = file_handler.write(image_content)
            if log == 'on':
                location = os.getcwd() + '/' + saved_image
                print(f'[INFORM] Saving image successfully at {location}.')

# initialize parser instance
parser = argparse.ArgumentParser(description='You need to provide correct arguments for program to retrieve information from website')
parser.add_argument('--url', default=None, help='the web address')
parser.add_argument('--log', default='on', help='turn on/off the log | LOG = ["on", "off"]')
parser.add_argument('--remotefile', default=None, help="file's remote path")

args = parser.parse_args()
url = args.url
log = args.log
remotefile = args.remotefile

# check if user provide enough arguments
if not url:
    print('Program end.')
    print('You need to specify the url of website.')
    print('Using -h argument for more information.')
    exit(1)

# get only domain name from url
url = url.replace('http://', '')
url = url.replace('https://', '')

if url[-1] == '/':
    url = url[:-1]

server_address = (url, 80)

if log == 'on':
    print(f"[INFORM] You've entered the web address: {url}")

# Prepare request
request_msg = f'GET {remotefile} HTTP/1.1\r\n'
request_msg += 'Host: ' + url + '\r\n'
request_msg += 'User-Agent: ' + getRandomUserAgent() + '\r\n' 
request_msg += 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n'
request_msg += 'Accept-Language: en-US,en;q=0.9\r\n'
request_msg += 'Connection: close\r\n\r\n'

# print(request_msg)

# Initialize TCP socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    if log == 'on':
        print(f'[LOG]    Connecting to {server_address[0]}...')
    sock.connect(server_address)
    if log == 'on':
        print('[LOG]    Downloading image...')
    if log == 'on':
        print('[LOG]    Sending request...')
    sock.send(request_msg.encode())
    if log == 'on':
        print('[LOG]    Receiving response...')
    response = recvall(sock)

    handle_response(response)

    if log == 'on':
        print('[LOG]    Done.')

