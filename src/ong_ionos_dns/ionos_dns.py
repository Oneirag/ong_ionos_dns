import httpx
import time
from ong_utils import InternalStorage

storage = InternalStorage("ong_ionos_dns")
api_key = storage.get_value("API_KEY")
if not api_key:
    api_key = input("Insert API_KEY:")
    storage.store_value("API_KEY", api_key)
    exit(0)

domains = [
    "neirapinuela.es",
    "bau360.es",
]

class DnsManager:
    BASE_URL = "https://api.hosting.ionos.com/dns"

    def __init__(self):
        self.ionos_client = httpx.Client(headers={"X-API-Key": api_key})
        # self.current_ip = self.client.get(protocols[proto]['api'], params={'format': 'json'})
        self.current_ip = httpx.get('https://api.ipify.org', params={'format': 'json'}).json()['ip']
        print("My IP: ", self.current_ip)
        self.zones = self.ionos_client.get(self.BASE_URL + "/v1/zones").json()
        print(self.zones)

    def update(self):
        for zone in self.zones:
            zone_id = zone['id']
            records = self.ionos_client.get(self.BASE_URL + f"/v1/zones/{zone_id}").json()['records']
            for record in records:
                if record['type'] == "A":
                    record_id = record['id']
                    print("name: ", record['name'])
                    A = record['content']
                    print("A: ", A)
                    if A != self.current_ip:
                        print("Record must be updated")
                        record['content'] = self.current_ip
                        resp = self.ionos_client.put(self.BASE_URL + f"/v1/zones/{zone_id}/records/{record_id}",
                                                     json=record)
                        print("update result:  ", resp.json())
                    else:
                        print("record OK")



if __name__ == '__main__':
    dns = DnsManager()
    while True:
        dns.update()
        time.sleep(5 * 60)


