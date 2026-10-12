# Deel 4 - Verificatie: config van R1 opvragen en zelf nakijken
from netmiko import ConnectHandler

r1 = {"device_type": "cisco_ios", "host": "172.16.16.2", "username": "student", "password": "pxl"}

with ConnectHandler(**r1) as conn:
    for cmd in ["show running-config", "show ip interface brief", "show ip route",
                "show ip ospf neighbor", "show access-lists"]:
        print(f"\n===== {cmd} =====")
        print(conn.send_command(cmd))
