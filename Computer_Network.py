#1) Given an IP Address, WAP to find out its class network id and host id
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

#---------------------------------------------------------------------------------------------------------------------------#

#2) Given an IP address /n notation (classless addressing). WAP in python to Find out the network ID and host ID

from ipaddress import ip_interface

def get_network_host_id(ip_address):
  """
  This function takes an IP address in CIDR notation and returns the network ID and host ID.

  Args:
      ip_address: The IP address in CIDR notation (e.g., "192.168.1.0/24").

  Returns:
      A tuple containing the network ID and host ID (e.g., ("192.168.1.0", "255.255.255.0")).
  """
  try:
    # Use ipaddress module for safe and efficient IP address handling
    interface = ip_interface(ip_address)
    network_address = interface.network
    host_mask = int(~interface.netmask)  # Invert netmask to get host mask
    host_id = str(ip_interface(address=network_address, mask=host_mask))
    return str(network_address), host_id
  except ValueError:
    return "Invalid IP address or CIDR notation."

# Get user input
ip_address = input("Enter IP address in CIDR notation (e.g., 192.168.1.0/24): ")

# Call the function and print results
network_id, host_id = get_network_host_id(ip_address)
if network_id != "Invalid IP address or CIDR notation.":
  print("Network ID:", network_id)
  print("Host ID:", host_id)
else:
  print(network_id)

#---------------------------------------------------------------------------------------------------------------------------#

#3) WAP to find the subnet mask and subnetwork address for each subnet given an IP address and the desired number of subnets :- 
from ipaddress import ip_interface
import math
def get_subnet_info(ip_address, num_subnets):
  """
  This function takes an IP address and the desired number of subnets and returns the subnet mask and subnetwork address for each subnet.

  Args:
      ip_address: The IP address in dotted decimal notation (e.g., "192.168.1.0").
      num_subnets: The number of subnets to create.

  Returns:
      A list of dictionaries, where each dictionary contains the subnet mask and subnetwork address for a subnet.
  """
  try:
    # Convert IP address to object for manipulation
    ip_obj = ip_interface(ip_address)
    # Get number of bits needed for subnetting based on number of subnets
    cidr_prefix = 32 - int(round(math.log2(num_subnets + 2)))
    subnet_mask = ip_interface(address="255.255.255.255", mask=cidr_prefix)
    # Calculate usable bits for host addressing
    host_bits = 32 - cidr_prefix

    subnet_info = []
    # Iterate through each subnet address
    for i in range(num_subnets):
      subnet_address = ip_obj.network + (i << host_bits)
      subnet_info.append({"Subnet Mask": str(subnet_mask.netmask), "Subnetwork Address": str(subnet_address)})

    return subnet_info
  except ValueError:
    return "Invalid IP address."

# Get user input
ip_address = input("Enter IP address (e.g., 192.168.1.0): ")
num_subnets = int(input("Enter the number of subnets: "))

# Call the function and print results
subnet_info = get_subnet_info(ip_address, num_subnets)
if subnet_info != "Invalid IP address.":
  for subnet in subnet_info:
    print("Subnet Mask:", subnet["Subnet Mask"])
    print("Subnetwork Address:", subnet["Subnetwork Address"])
    print("---")
else:
  print(subnet_info)

#---------------------------------------------------------------------------------------------------------------------------#

#4) Find the IP address of a local machine or any other machine on the network
import socket

def get_ip_address(hostname):
  try:
    ip=socket.gethostbyname(hostname)
    return ip
  except socket.gaierror as e:
     print(f"Error: Cannot resolve hostname'{hostname}'.")
local_ip=get_ip_address('localhost')
print(f"Local IP Address : {local_ip}")
website_ip=get_ip_address('www.google.com')
print(f"IP Address of website : {website_ip}")