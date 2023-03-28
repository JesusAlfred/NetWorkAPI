import paramiko
import time
import socket

class SSHController:
    def __init__(self, ip="", user="1", password="p", local_address="localhost"):
      self.ip = ip
      self.user = user
      self.password = password  
      self.local_address = local_address
    def setConfig(self, ip, user, password):
      self.ip = ip
      self.user = user
      self.password = password

    def startConection(self):
      s = socket.socket()
      s.bind((self.local_address, 0))
      s.connect((self.ip, 22))
      self.ssh = paramiko.SSHClient()

      # Load SSH host keys.
      self.ssh.load_system_host_keys()
      # Add SSH host key automatically if needed.
      self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      # Connect to router using username/password authentication.
      try:
        self.ssh.connect(self.ip, 
                    username=self.user, 
                    password=self.password,
                    allow_agent=False,
                    look_for_keys=False,
                    sock=s )
        self.remote_conn = self.ssh.invoke_shell()
      except Exception as e:
        print("Error en connection")
        print(e)
        return 1
      return 0

    def sendCommand(self, command, timeout=0.5):
      self.remote_conn.settimeout(1)
      if self.remote_conn.recv_ready():
        while True:
          try:
            temp_output = str(self.remote_conn.recv(1024), "utf-8")
          except Exception as e:
            break
      self.remote_conn.settimeout(timeout)
      self.remote_conn.send(command)
      time.sleep(timeout)
      output = ""
      while True:
        try:
          temp_output = str(self.remote_conn.recv(1024), "utf-8")
        except Exception as e:
          #print("timeout")
          break
        output += temp_output
      print(output)
      return output
    
    def endConnection(self):
     self.ssh.close()