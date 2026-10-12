# Deel 2.2 - Werkt Netmiko? (zoals LAB 2)
from netmiko import ConnectHandler

r1 = {"device_type": "cisco_ios", "host": "172.16.16.2", "username": "student", "password": "pxl"}

with ConnectHandler(**r1) as conn:
    print(conn.find_prompt())
    print(conn.send_command("show ip interface brief"))
