#1.1) Given an IP Address, WAP to find out its class network id and host id
def ipv4_info(ip_address):
    octets = ip_address.split('.')
    octets = [int(octet) for octet in octets]
    if octets[0] >= 1 and octets[0] <= 126:
        ip_class = 'A'
        network_id = octets[:1]
        host_id = octets[1:]
    elif octets[0] >= 128 and octets[0] <= 191:
        ip_class = 'B'
        network_id = octets[:2]
        host_id = octets[2:]
    elif octets[0] >= 192 and octets[0] <= 223:
        ip_class = 'C'
        network_id = octets[:3]
        host_id = octets[3:]
    elif octets[0] >= 224 and octets[0] <= 239:
        ip_class = 'D'
        network_id = None
        host_id = None
    else:
        ip_class = 'Unknown'
        network_id = None
        host_id = None

    return ip_class, network_id, host_id
ip_address = str(input("Enter the IPv4 address :- "))#(e.g., 192.168.1.10)
ip_class, network_id, host_id = ipv4_info(ip_address)
print("IPv4 Class:", ip_class)
print("Network ID:", '.'.join(str(octet) for octet in network_id))
print("Host ID:", '.'.join(str(octet) for octet in host_id))


#1.b) Given an IP Address and the required subnet. WAP to Find out the subnet mask and subnetwork address of each subnet
import ipaddress
def ipv4_subnet(ip_address, subnet):
    try:
        network = ipaddress.ip_interface(f"{ip_address}/{subnet}")
    except (ValueError,ipaddress.AddressValueError) as e:
        raise ValueError(f"Invalid Ip address or subnet: {e}")
    subnet_mask = str(network.netmask)
    subnetwork_address = str(network.network)
    return subnet_mask,subnetwork_address
ip_address = str(input("Enter the IPv4 address :- "))#(e.g., 192.168.1.0)
subnet = int(input("Enter the required subnet :- "))#(e.g., 24)
try:
    subnet_mask, subnetwork_address = ipv4_subnet(ip_address, subnet)
    print(f"Subnet Mask : {subnet_mask}")
    print(f"Subnetwork Address : {subnetwork_address}")
except ValueError as e:
    print(f"Error : {e}")


#---------------------------------------------------------------------------------------------------------------------------#

#2) Given an IP address /n notation (classless addressing). WAP in python to Find out the network ID and host ID

import ipaddress

def find_network_host(ip_address):
    ip,subnet_mask =  ip_address.split('/')
    subnet_mask = int(subnet_mask)
    ip_parts = ip.split('.')
    network_id_parts = ip_parts[:4]
    for i in range(subnet_mask//8):
        network_id_parts[i] = str(int(ip_parts[i]) & 255)
    for i in range(subnet_mask // 8, 4):
        network_id_parts[i] = '0'
    network_id = '.'.join(network_id_parts)
    host_id_parts = ip_parts[:4]
    for i in range(subnet_mask // 8, 4):
        host_id_parts[i] = str(int(ip_parts[i]) & 255)
    host_id = '.'.join(host_id_parts)
    return network_id,host_id
ip_address = str(input("Enter the IPv4 address :- "))#(e.g., 192.168.1.100/24)
network_id,host_id = find_network_host(ip_address)
print("Network ID : " , network_id)
print("Host ID : ",host_id)

#---------------------------------------------------------------------------------------------------------------------------#

#3) WAP in Python to find out the ip address of a local machine or any other machine

import socket

def get_local_ip():
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except socket.error as e:
        return "Error: {}".format(e)

def get_ip_address(domain):
    try:
        ip_address = socket.gethostbyname(domain)
        return ip_address
    except socket.error as e:
        return "Error: {}".format(e)

local_ip = get_local_ip()
print("Local IP Address:", local_ip)

domain = input("Enter the domain name (e.g., www.google.com): ")

domain_ip = get_ip_address(domain)
print("IP Address of", domain + ":", domain_ip)

#---------------------------------------------------------------------------------------------------------------------------#

# 4.a ) WAP In python showing socket creation at both the client and server side.

#Server Side

import socket

server_ip = '127.0.0.1'
server_port = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((server_ip, server_port))

server_socket.listen()

print("Server is listening on", server_ip, "port", server_port)

client_socket, client_address = server_socket.accept()

print("Client connected from", client_address)

data = client_socket.recv(1024)

print("Received:", data.decode())

client_socket.close()

server_socket.close()

#Client Side

import socket

server_ip = '127.0.0.1'
server_port = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((server_ip, server_port))

message = "Hello, server!"
client_socket.send(message.encode())

client_socket.close()


# 4.b) WAP in Python to create a client side socket and use it to send a request to access current date and time

# Server side
import socket
import datetime

server_ip = '127.0.0.1'
server_port = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((server_ip, server_port))

server_socket.listen()

print("Server is listening on", server_ip, "port", server_port)

while True:
    client_socket, client_address = server_socket.accept()

    print("Client connected from", client_address)

    request = client_socket.recv(1024).decode()

    if request.startswith("GET /date-time"):
        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n{}\r\n".format(current_datetime)
        client_socket.sendall(response.encode())

    client_socket.close()

# Client Side

import socket

server_ip = '127.0.0.1'
server_port = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((server_ip, server_port))

request = "GET /date-time HTTP/1.1\r\nHost: {}\r\n\r\n".format(server_ip)
client_socket.sendall(request.encode())

response = client_socket.recv(1024)

print("Current Date and Time:", response.decode())

client_socket.close()

# 4.c ) Write a server program in python to create server side socket and use it to receive a client side request, process it to generate response in form of current date and time where server program should be running and sent response back to the client

#Server Side

import socket
import datetime

server_ip = '127.0.0.1'
server_port = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((server_ip, server_port))

server_socket.listen()

print("Server is listening on", server_ip, "port", server_port)

while True:
    client_socket, client_address = server_socket.accept()

    print("Client connected from", client_address)
    request = client_socket.recv(1024).decode()

    if request == "GET /date-time":
        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        response = current_datetime.encode()
        client_socket.sendall(response)

    client_socket.close()

# Client Side 

import socket
server_ip = '127.0.0.1'
server_port = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((server_ip, server_port))

request = "GET /date-time"
client_socket.sendall(request.encode())

response = client_socket.recv(1024)

print("Current Date and Time:", response.decode())

client_socket.close()

#---------------------------------------------------------------------------------------------------------------------------#

# 5) Write a program to create client & Server Side Sockets & use them to implement Echo Server

#Server Side

import socket

server_ip = '127.0.0.1'
server_port = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((server_ip, server_port))

server_socket.listen()

print("Echo Server is listening on", server_ip, "port", server_port)

while True:
    client_socket, client_address = server_socket.accept()

    print("Client connected from", client_address)

    message = client_socket.recv(1024).decode()

    client_socket.sendall(message.encode())

    client_socket.close()

# Client Side 

import socket

server_ip = '127.0.0.1'
server_port = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((server_ip, server_port))

message = "Hello, Echo Server!"
client_socket.sendall(message.encode())

response = client_socket.recv(1024).decode()

print("Server Response:", response)

client_socket.close()

#---------------------------------------------------------------------------------------------------------------------------#

# 6) Write client-server interaction programs to implement multicasting

#Server Side

import socket
import struct
import time

multicast_group = '224.3.29.71'
server_port = 10000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

ttl = struct.pack('b', 1)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

message = "Hello, multicast world!"

try:
    print("Sending message:", message)
    sent = sock.sendto(message.encode(), (multicast_group, server_port))
    
finally:
    sock.close()

# Client Side 

import socket
import struct

multicast_group = '224.3.29.71'
server_port = 10000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind(('', server_port))

group = socket.inet_aton(multicast_group)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

while True:
    print("\nWaiting to receive message...")
    data, address = sock.recvfrom(1024)
    
    print("Received", len(data), "bytes from", address)
    print("Message:", data.decode())


#---------------------------------------------------------------------------------------------------------------------------#

# 7) Write a program to create client and server side sockets and use them to send a string in lowercase from client to the server, the server then converts the string to uppercase and return back to client.

#Server Side

import socket

server_ip = '127.0.0.1'
server_port = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((server_ip, server_port))

server_socket.listen()

print("Server is listening on", server_ip, "port", server_port)

while True:
    client_socket, client_address = server_socket.accept()

    print("Client connected from", client_address)

    lowercase_string = client_socket.recv(1024).decode()

    uppercase_string = lowercase_string.upper()

    client_socket.sendall(uppercase_string.encode())

    client_socket.close()

# Client Side 

import socket

server_ip = '127.0.0.1'
server_port = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((server_ip, server_port))

lowercase_string = str(input("Enter a String :- "))
lowercase_string = lowercase_string.lower()
client_socket.sendall(lowercase_string.encode())

uppercase_string = client_socket.recv(1024).decode()

print("Uppercase String from Server:", uppercase_string)

client_socket.close()

#---------------------------------------------------------------------------------------------------------------------------#

# 8) Possible Question

"""Write a program to simulate the Sliding Window Protocol in a network transmission. Implement the following features:
1. Prompt the user to enter the window size.
2. Prompt the user to enter the number of frames to transmit.
3. Allow the user to enter the frames.
4. Simulate the sending of frames in windows, where the sender sends a window of frames and waits for an acknowledgment before sending the next window of frames.
5. Print the frames being sent and when the acknowledgment for those frames is received.
"""

def main():
    w = int(input("Enter window size: "))
    
    f = int(input("Enter number of frames to transmit: "))
    
    frames = []
    print(f"Enter {f} frames: ")
    for i in range(f):
        frames.append(int(input()))
    
    print("\nWith sliding window protocol, the frames will be sent in the following way (assuming no corruption of frames):")
    
    i = 0
    while i < f:
        print(f"\nSending frames: {frames[i:i+w]}")
        if (i + w) <= f:
            print("Acknowledgement of above frames sent is received by sender\n")
        else:
            print("Acknowledgement of above frames sent is received by sender\n")
        
        i += w

if __name__ == "__main__":
    main()

#---------------------------------------------------------------------------------------------------------------------------#

# 9) Write a program to implement error detection at Datalink layer using CRC

def xor(a, b):
    result = []
    for i in range(1, len(b)):
        if a[i] == b[i]:
            result.append('0')
        else:
            result.append('1')
    return ''.join(result)

def mod2div(dividend, divisor):
    pick = len(divisor)
    tmp = dividend[0 : pick]

    while pick < len(dividend):
        if tmp[0] == '1':
            tmp = xor(divisor, tmp) + dividend[pick]
        else:
            tmp = xor('0'*pick, tmp) + dividend[pick]
        pick += 1

    if tmp[0] == '1':
        tmp = xor(divisor, tmp)
    else:
        tmp = xor('0'*pick, tmp)

    return tmp

def encodeData(data, key):
    l_key = len(key)
    appended_data = data + '0'*(l_key-1)
    remainder = mod2div(appended_data, key)
    codeword = data + remainder
    return codeword

def decodeData(data, key):
    remainder = mod2div(data, key)
    return remainder

data = '11010011101100'
key = '1011'

print("Data:", data)
print("Key:", key)

encoded_data = encodeData(data, key)
print("Encoded Data:", encoded_data)

remainder = decodeData(encoded_data, key)
print("Remainder after decoding:", remainder)

if '1' in remainder:
    print("Error detected in the received data")
else:
    print("No error detected in the received data")

#---------------------------------------------------------------------------------------------------------------------------#

# 10.a) Implement Error Control Mechanism in DataLink Layer Using Go Back-N Protocols

import random
import time

class Frame:
    def __init__(self, seq_num, data):
        self.seq_num = seq_num
        self.data = data

class Sender:
    def __init__(self, window_size, timeout):
        self.window_size = window_size
        self.timeout = timeout
        self.next_seq_num = 0
        self.base = 0
        self.buffer = []
        self.timer = None

    def send_frame(self, frame):
        print(f"Sending frame: {frame.seq_num}")
        self.buffer.append(frame)

    def start_timer(self):
        if self.timer is None:
            self.timer = time.time()

    def stop_timer(self):
        self.timer = None

    def timeout_occurred(self):
        return self.timer is not None and time.time() - self.timer > self.timeout

    def receive_ack(self, ack_num):
        print(f"Received ACK: {ack_num}")
        if ack_num >= self.base:
            self.base = ack_num + 1
            self.stop_timer()

    def send_window(self):
        while self.next_seq_num < self.base + self.window_size:
            frame = Frame(self.next_seq_num, f"Data{self.next_seq_num}")
            self.send_frame(frame)
            self.start_timer()
            self.next_seq_num += 1

    def handle_timeout(self):
        if self.timeout_occurred():
            print("Timeout occurred, resending window...")
            self.timer = None  # Stop the current timer
            for seq in range(self.base, self.next_seq_num):
                frame = Frame(seq, f"Data{seq}")
                self.send_frame(frame)
            self.start_timer()

class Receiver:
    def __init__(self, expected_seq_num=0):
        self.expected_seq_num = expected_seq_num

    def receive_frame(self, frame):
        if frame.seq_num == self.expected_seq_num:
            print(f"Received frame: {frame.seq_num}")
            self.expected_seq_num += 1
            return frame.seq_num
        else:
            print(f"Discarded frame: {frame.seq_num}")
            return self.expected_seq_num - 1

window_size = 4
timeout = 3  # seconds

sender = Sender(window_size, timeout)
receiver = Receiver()

sender.send_window()

for i in range(10):
    if random.random() > 0.1:
        ack = receiver.receive_frame(Frame(i, f"Data{i}"))
        sender.receive_ack(ack)
    else:
        print(f"Frame {i} lost")

    sender.handle_timeout()
    sender.send_window()
    time.sleep(1)

#---------------------------------------------------------------------------------------------------------------------------#
