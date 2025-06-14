# Install instructions
1. Get api key from https://developer.hosting.ionos.es/keys
2. Execute `python -m ong_ionos_dns.config_api_key` for first time to setup api key
2. Run directly:
   1. Execute `python -m ong_ionos_dns.ionos_dns` to run program
3. Setup supervisor 
   1. Execute `python -m ong_ionos_dns.generate_supervisor_conf` to create a script for supervisor
   2. Add generated `ionos_dns.conf` to `/etc/supervisor/conf.d` folder and restart supervisor with `sudo service supervisor restart`
   3. Check logs for errors: `tail /var/log/ong_ionos_dns.err.log`
