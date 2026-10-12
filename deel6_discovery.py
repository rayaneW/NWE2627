# Deel 6 - Network Discovery: routers van klasgenoten ontdekken
from netmiko import ConnectHandler

gezochte_route = "172.16.16.192/26"   # route die we bij iedereen controleren

print("===== NETWORK DISCOVERY =====")

for tafel in range(1, 24):
    ip = f"10.199.66.{200 + tafel}"   # tafel 16 -> 10.199.66.216
    try:
        conn = ConnectHandler(device_type="cisco_ios", host=ip, username="student",
                              password="pxl", conn_timeout=3)
    except Exception:
        continue   # router niet bereikbaar -> volgende

    hostname = conn.find_prompt().strip("#>")
    brief = conn.send_command("show ip interface brief")
    route = conn.send_command("show ip route")
    neighbors = conn.send_command("show ip ospf neighbor")
    conn.disconnect()

    # neighbor-lijnen bevatten "FULL", het eerste woord is de router-ID van de buur
    buren = [l.split()[0] for l in neighbors.splitlines() if "FULL" in l]
    # OSPF-routes beginnen met een "O"
    ospf_routes = [l for l in route.splitlines() if l.startswith("O")]

    print(f"\n{hostname}  {ip}")
    print(f"   OSPF neighbors: {', '.join(buren)}")
    print(f"   OSPF routes:    {len(ospf_routes)}")
    for l in ospf_routes:
        print("      " + l.strip())
    print(f"   Route {gezochte_route} aanwezig: {gezochte_route in route}")
