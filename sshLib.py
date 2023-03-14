import paramiko
import time

class SSHController:
    def __init__(self, ip="", user="1", password="p"):
      self.ip = ip
      self.user = user
      self.password = password  
    def setConfig(self, ip, user, password):
      self.ip = ip
      self.user = user
      self.password = password

    def startConection(self):
      try:
        self.ssh.connect(self.ip, 
                    username=self.user, 
                    password=self.password,
                    look_for_keys=True )
        self.remote_conn = self.ssh.invoke_shell()
      except Exception as e:
        print("Error en connection")
        print(e)
        return 1
      return 0

    def sendCommand(self, command, timeout=1):
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
        print(temp_output, end="")
      return output