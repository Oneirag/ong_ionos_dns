from datetime import datetime, timedelta

import httpx
import time
from ong_utils import InternalStorage

storage = InternalStorage("ong_ionos_dns")
api_key = storage.get_value("API_KEY")
if not api_key:
    api_key = input("Insert API_KEY:")
    storage.store_value("API_KEY", api_key)
    exit(0)

def get_current_ip() -> str | None:
    try:
        return httpx.get('https://api.ipify.org', params={'format': 'json'}).json()['ip']
    except Exception as e:
        print(e)
        return

class DnsManager:
    BASE_URL = "https://api.hosting.ionos.com/dns"

    def __init__(self):
        self.ionos_client = httpx.Client(headers={"X-API-Key": api_key})
        # self.current_ip = self.client.get(protocols[proto]['api'], params={'format': 'json'})
        self.current_ip = None      # Force update on first run
        self.zones = self.ionos_client.get(self.BASE_URL + "/v1/zones").json()
        print(self.zones)

    def update(self):
        new_ip = get_current_ip()
        if self.current_ip == new_ip:
            print(f"Current IP {self.current_ip} did not change")
            return
        elif not new_ip:
            print("There was a problem updating current IP")
            return
        self.current_ip = new_ip
        print(f"New IP is {self.current_ip}")
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


def main(update_interval_seconds: int = None):
    dns = DnsManager()
    while True:
        dns.update()
        if update_interval_seconds:
            print("Next execution at ", datetime.now() + timedelta(seconds=update_interval_seconds))
            time.sleep(update_interval_seconds)
        else:
            return



if __name__ == '__main__':
    # main()
    main(5 * 60)

