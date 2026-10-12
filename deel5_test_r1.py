# Deel 5 - Automated testing van R1 met unittest
import unittest
from netmiko import ConnectHandler

r1 = {"device_type": "cisco_ios", "host": "172.16.16.2", "username": "student", "password": "pxl"}


class TestR1(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # 1x verbinden en alle output opslaan
        with ConnectHandler(**r1) as conn:
            cls.config = conn.send_command("show running-config")
            cls.brief = conn.send_command("show ip interface brief")
            cls.route = conn.send_command("show ip route")
            cls.ospf = conn.send_command("show ip ospf neighbor")
            cls.g001 = conn.send_command("show ip interface g0/0/1")

    def check(self, naam, ok):
        print(f"    {naam:<30} [{'PASS' if ok else 'FAIL'}]")
        with self.subTest(naam):      # subTest: bij een FAIL gaan de andere checks gewoon door
            self.assertTrue(ok)

    def test_1_hostname(self):
        print("Hostname:")
        self.check("R1", "hostname R1" in self.config)

    def test_2_interfaces(self):
        print("Interfaces:")
        interfaces = {
            "GigabitEthernet0/0/0.116": "172.16.16.2",
            "GigabitEthernet0/0/0.216": "172.16.16.66",
            "GigabitEthernet0/0/0.316": "172.16.16.130",
            "GigabitEthernet0/0/0.416": "172.16.16.194",
            "GigabitEthernet0/0/1": "10.199.66.216",
        }
        for interface, ip in interfaces.items():
            # zoek de lijn van deze interface in 'show ip interface brief'
            lijn = ""
            for l in self.brief.splitlines():
                if l.startswith(interface + " "):
                    lijn = l
            ok = ip in lijn and lijn.endswith("up") and "down" not in lijn
            self.check(f"{interface} {ip}", ok)

    def test_3_ospf(self):
        print("OSPF:")
        self.check("Proces 10", "router ospf 10" in self.config)
        self.check("VLAN 416 in area 0", "network 172.16.16.192 0.0.0.63 area 0" in self.config)
        self.check("Default route opgenomen", "default-information originate" in self.config)
        self.check("Neighbor gevonden", "FULL" in self.ospf)

    def test_4_routing(self):
        print("Routing:")
        self.check("Default route", "Gateway of last resort is 10.199.66.200" in self.route)
        for net in ["172.16.16.0/26", "172.16.16.64/26", "172.16.16.128/26", "172.16.16.192/26"]:
            self.check(f"Connected {net}", net in self.route)

    def test_5_beveiliging(self):
        print("Beveiliging:")
        self.check("SSH only", "transport input ssh" in self.config)
        self.check("ACL configured", "ip access-list extended OUTSIDE-IN" in self.config)
        self.check("Buiten -> VLAN 116 deny", "deny   ip any 172.16.16.0 0.0.0.63" in self.config)
        self.check("VLAN 116 -> buiten deny", "deny   ip 172.16.16.0 0.0.0.63 any" in self.config)
        self.check("ACL in op g0/0/1", "Inbound  access list is OUTSIDE-IN" in self.g001)
        self.check("ACL out op g0/0/1", "Outgoing access list is INSIDE-OUT" in self.g001)


if __name__ == "__main__":
    print("===== R1 CONFIGURATION TEST =====")
    unittest.main(verbosity=0)
