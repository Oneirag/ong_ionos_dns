from ong_ionos_dns import storage

public_preffix = input("Insert API_KEY public preffix:")
secret = input("Insert API_KEY secret:")
api_key = f"{public_preffix}.{secret}"
storage.store_value("API_KEY", api_key)
