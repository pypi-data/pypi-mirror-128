import os
import sys
import subprocess
import FamcyTools

LOCAL_USER = "/home/%U/.local/share/famcy"

def main(args):
	try:
		socket_port = args[1]
	except:
		print("[ERROR] Please provide port number. e.g. famcy deploy pms 9090")
		return

	# Write famcy.ini
	content = """[uwsgi]
module = wsgi:app
master = true
processes = 1
http-socket = :%s
chmod-socket = 660
vacuum = true
die-on-term = true
enable-threads = true
single-interpreter = true
http-websockets = true
logto = %s
log-maxsize = 2048000""" % (args[1], LOCAL_USER + "/" + args[0] + "/logs" + """/famcy.log""")

	f = open(FamcyTools.FAMCY_DIR % (FamcyTools.USERNAME, args[0]) + "/famcy.ini", "w")
	f.write(content)
	f.close()
	
	# Write wsgi.py
	content = """from Famcy import create_app

app = create_app('%s',True)

if __name__ == "__main__":
    app.run()"""% (args[0])

	f = open(FamcyTools.FAMCY_DIR % (FamcyTools.USERNAME, args[0]) + "/wsgi.py", "w")
	f.write(content)
	f.close()

	print()
	print("== Copy the following part and setup system service == (Need to change path if necessary)")
	print("""
[Unit]
Description=uWSGI instance to serve famcy
After=network.target

[Service]
User=%s
Group=www-data
WorkingDirectory=/home/%s/.local/share/famcy/%s/venv/lib/python3.7/site-packages/Famcy
Environment="PATH=/home/%s/.local/share/famcy/%s/venv/bin"
ExecStart=/home/%s/.local/share/famcy/%s/venv/bin/uwsgi --ini famcy.ini --lazy

[Install]
WantedBy=multi-user.target
""" % (FamcyTools.USERNAME, FamcyTools.USERNAME, args[0], FamcyTools.USERNAME, args[0], FamcyTools.USERNAME, args[0]))

	print()
	print("== Copy the following part to nginx configurations == (Need to change alias path if necessary)")
	print("""
location / {
    proxy_set_header X-Forward-For $proxy_add_x_forwarded_for;
    proxy_set_header Host $http_host;
    proxy_redirect off;
    uwsgi_max_temp_file_size 20480m;
    proxy_pass http://127.0.0.1:%s;
}

location /static  {
    alias /home/%s/.local/share/famcy/%s/venv/lib/python3.7/site-packages/Famcy/static;
}
""" % (args[1], FamcyTools.USERNAME, args[0]))
	print("Deployed to wsgi")