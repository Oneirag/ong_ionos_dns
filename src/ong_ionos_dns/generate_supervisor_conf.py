import os
import sys
from pathlib import Path
code_path = Path(__file__).parent
python_executable = sys.executable
venv_path = Path(python_executable).parent.parent
python_path = os.environ.get("PYTHONPATH")
script_path = code_path / 'ionos_dns.py'
user = os.environ.get("USER")
assert script_path.exists()
print(f"{code_path=} {python_executable=} {venv_path=} {python_path=} {script_path=} {user=}")

template = f"""\
[program:ong_ionos_dns]
directory={code_path}
environment=PATH={code_path};PYTHONPATH={python_path}
command={python_executable} {script_path}
autostart=true
autorestart=true
user={user}
stderr_logfile=/var/log/ong_ionos_dns.err.log
stderr_logfile_backups=0        # No backups
stderr_capture_maxbytes=10      # 10Mb maximum
stdout_logfile=/var/log/ong_ionos_dns.out.log
stdout_logfile_backups=0        # No backups
stdout_capture_maxbytes=10      # 10mb maximum
"""
print(template)
Path(__file__).with_name("ionos_dns.conf").write_text(template)

