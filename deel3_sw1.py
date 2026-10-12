# Deel 3 - Configuratie van SW1 via Netmiko (tafel 16)
from netmiko import ConnectHandler

sw1 = {"device_type": "cisco_ios", "host": "172.16.16.4", "username": "student", "password": "pxl"}

# VLAN -> (naam, poorten)
# Poort 22 laat ik in VLAN 116, want daar hangt je VM (Deel 1). Anders valt je SSH weg.
vlans = {
    116: ("Management", "g1/0/1 - 2 , g1/0/22"),
    216: ("VM-Hosts", "g1/0/3 - 6"),
    316: ("Appliance-Servers", "g1/0/7 - 10"),
    416: ("Data-Users", "g1/0/11 - 21"),
}

commands = ["hostname SW1", "vlan 99", " name Native-Vlan"]

for vlan, (naam, poorten) in vlans.items():
    commands += [
        f"vlan {vlan}",
        f" name {naam}",
        f"interface range {poorten}",
        " switchport mode access",
        f" switchport access vlan {vlan}",
    ]

commands += [
    "interface range g1/0/23 - 24",
    " switchport mode trunk",
    " switchport trunk native vlan 99",
]

with ConnectHandler(**sw1) as conn:
    print(conn.send_config_set(commands))
    conn.save_config()
