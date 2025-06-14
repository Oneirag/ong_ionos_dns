import sys
from datetime import datetime, timedelta
from pathlib import Path
import httpx
import time
from ong_ionos_dns import storage
import logging
import logging.handlers


def setup_logger(name='my_app', log_file='app.log'):
    """
    Configura un logger que escribe tanto en fichero como en consola

    Args:
        name (str): Nombre del logger
        log_file (str): Ruta del fichero de log

    Returns:
        logging.Logger: Logger configurado
    """
    # Crear el directorio de logs si no existe
    log_path = Path(log_file).parent
    log_path.mkdir(parents=True, exist_ok=True)

    # Crear y configurar el logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Formato del log
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(module)s:%(lineno)d - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Handler para escribir en fichero con rotación
    # 10MB = 10 * 1024 * 1024 bytes
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,  # Mantener 5 archivos de backup
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Handler para escribir en consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    # Añadir los handlers al logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


api_key = storage.get_value("API_KEY")
if not api_key:
    raise ValueError("No api key. Setup api key in https://developer.hosting.ionos.es/keys and run "
                     "ong_ionos_dns.config_api_key")

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
    logger = setup_logger(__name__, Path(__file__).with_name("app.log").as_posix())
    logger.info("starting process")
    dns = DnsManager()
    while True:
        logger.info("Starting DNS update")
        dns.update()
        if update_interval_seconds:
            next_time = datetime.now() + timedelta(seconds=update_interval_seconds)
            logger.info(f"Next execution at {next_time}")
            # print(f"Next execution at {next_time}")
            time.sleep(update_interval_seconds)
        else:
            return



if __name__ == '__main__':
    main(5 * 60)

