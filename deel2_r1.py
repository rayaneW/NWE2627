# Deel 2.3 - Configuratie van R1 via Netmiko (tafel 16)
from netmiko import ConnectHandler

r1 = {"device_type": "cisco_ios", "host": "172.16.16.2", "username": "student", "password": "pxl"}

commands = [
    "hostname R1",

    # Subinterfaces per VLAN
    "interface g0/0/0.116",
    " encapsulation dot1Q 116",
    " ip address 172.16.16.2 255.255.255.192",
    "interface g0/0/0.216",
    " encapsulation dot1Q 216",
    " ip address 172.16.16.66 255.255.255.192",
    "interface g0/0/0.316",
    " encapsulation dot1Q 316",
    " ip address 172.16.16.130 255.255.255.192",
    "interface g0/0/0.416",
    " encapsulation dot1Q 416",
    " ip address 172.16.16.194 255.255.255.192",
    "interface g0/0/0.99",
    " encapsulation dot1Q 99 native",

    # Buiten-interface + default route
    "interface g0/0/1",
    " ip address 10.199.66.216 255.255.255.224",
    " no shutdown",
    "ip route 0.0.0.0 0.0.0.0 g0/0/1 10.199.66.200",

    # OSPF
    "router ospf 10",
    " router-id 16.16.16.16",
    " network 10.199.66.192 0.0.0.31 area 0",    # buitennet, nodig voor neighbors
    " network 172.16.16.192 0.0.0.63 area 0",    # VLAN 416
    " passive-interface g0/0/0.416",
    " default-information originate",

    # ACL's: VLAN 116 (management) mag niet naar buiten en buiten niet naar VLAN 116.
    # Uitzondering: SSH naar de andere routers voor Deel 6.
    "no ip access-list extended OUTSIDE-IN",   # eerst wissen zodat je het script opnieuw kan draaien
    "no ip access-list extended INSIDE-OUT",
    "ip access-list extended OUTSIDE-IN",
    " permit tcp any eq 22 172.16.16.0 0.0.0.63 established",
    " deny ip any 172.16.16.0 0.0.0.63",
    " permit ip any any",
    "ip access-list extended INSIDE-OUT",
    " permit tcp 172.16.16.0 0.0.0.63 any eq 22",
    " deny ip 172.16.16.0 0.0.0.63 any",
    " permit ip any any",
    "interface g0/0/1",
    " ip access-group OUTSIDE-IN in",
    " ip access-group INSIDE-OUT out",
]

with ConnectHandler(**r1) as conn:
    print(conn.send_config_set(commands))
    conn.save_config()
