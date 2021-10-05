import socket
import smartlog
import select
import binascii
import threading
import os
import queue
from toolbelt.quickdate import quickdate

import smartlog
log = smartlog.Smartlog()


########################################
#! My Socket class for easier sockets
########################################
class Socket:


   name = ""
   sock = None;


   def __init__(self, host, port, name=""):
       self.config(host, port, name);
       self.refresh();
       self.keepalive = False;
       self.renew = True;



   def config(self, host, port, name):
      if name=="":
         self.name = binascii.b2a_hex(os.urandom(4));
      else:
         self.name = bytearray(name, 'utf-8');
      self.bytes = bytearray([len(self.name)]);
      self.host = host;
      self.port = port;


   def refresh(self):
      self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
      return self.sock;


   def read(self):
      sock = self.sock;
      sock.bind((self.host, self.port))
      sock.listen(1)
      conn, addr = sock.accept()
      data = bytearray();
      while 1:
           recvdata = conn.recv(1024)
           if not recvdata:
             break
           else: data += recvdata;
      conn.close()
      return data;


   def write(self, data):
      try:
         if isinstance(data, str):
            data = bytearray(data, 'utf-8');
         data = (self.bytes+self.name+data);
         if self.renew:
            self.refresh();
         rx, wx, xx = select.select([], [self.sock], []);
         for w in wx:
            try:
              w.connect((self.host, self.port));
            except BlockingIOError: 
              continue;
            bytes = w.send(data, 1024);
            if not self.keepalive:
               w.close();
      except Exception as e: 
           import traceback;
           traceback.print_exc();



class Server(Socket):


     data = {};


     def __init__(self, host, port):
        #super().__init__(host, port);
        self.host = host;
        self.port = port;
        pass
     

     #####################################
     #! load all data from queue into dict
     #####################################
     def _load(self, q):
         first = None;
         while not first or first=='':
            first = q.get(False);
         nameend = int(first[0]);
         sockname = first[1:nameend+1];
         if sockname not in self.data:
            self.data[sockname] = [];
         self.data[sockname]  = bytearray();
         self.data[sockname] += first[nameend+1:];
         while not q.empty():
            self.data[sockname] += q.get(False);


     def postproc(self):
        print(('postproc: ', self.data));


     def read(self):
        qs = {}
        rx = [];
        while True:
           sock = self.sock;
           if sock not in rx:
              sock = self.refresh()
              sock.bind((self.host,self.port));
              sock.listen(5);
              rx += [sock];
           rx = [r for r in rx if r.fileno() > 0];
           rx, wx, xx = select.select(rx, [], []);
           for s in rx:
              try:
                 x = str([r.fileno() for r in rx]);
                 if s == sock:
                   conn, addr = s.accept();
                   if conn:
                      conn.setblocking(0);
                      rx.append(conn); 
                      qs[conn] = queue.Queue();
                 else:
                   data = s.recv(1024);
                   if not data: 
                       if not qs[s].empty():
                          #log.write(quickdate('now')+':');
                          self._load(qs[s]);
                          self.postproc();
                       s.close()
                   else: 
                      qs[s].put(data);
                      x = str([r.fileno() for r in rx]);
              except Exception as e: 
                  import traceback;
                  traceback.print_exc();
                  break;


class SmartlogServer(Server):
      log = smartlog.Smartlog();
      def postproc(self):
         for k in self.data:
             self.log.info("%s: %s" % (
                  str(k, 'utf-8'),
                  str(self.data[k], 'utf-8')
             ));


class DispatchServer(Server):
      #ts = []
      def runcmd(self, k, cmd):
          import subprocess
          p = subprocess.Popen(
                str(cmd, 'utf-8').split(" "), 
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
          );
          log = smartlog.Smartlog();
          log.name = k.decode();
          log.printname = True
          stdout, stderr = p.communicate();
          for line in stdout.decode().split('\n')[:-1]:
              log.logok(line);
      def postproc(self):
         for k in self.data:
             t = threading.Thread(target=self.runcmd, args=(k, self.data[k]));
             t.start();
         self.data = {};
