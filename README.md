# Install instructions
1. Get api key from https://developer.hosting.ionos.es/keys
2. Execute `ong_ionos_dns.ionos_dns` for first time to setup api key
3. Execute `ong_ionos_dns.generate_supervisor_conf` to create a script for supervisor
4. Add generated `ionos_dns.conf` to `/etc/supervisor/conf.d` folder and restart supervisor with `sudo service supervisor restart`
5. Check logs for errors: `tail /var/log/ong_ionos_dns.err.log`
