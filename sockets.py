import socket
import json
import smartlog
import select
import binascii
import threading
import os, sys
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
   plug = None;


   def __init__(self, host, port, lhost='localhost', lport=0, name="", init=True):
       self.config(host, port, lhost, lport, name);
       if init: self.reset();


   def __str__(self):
       s = str((self.fileno(), self.name, self.host, self.port, self.listening, self.connected));
       if self.plug: s += ":=:" + self.plug.__str__();
       return s


   def config(self, host, port, lhost='localhost', lport=0, name=""):
      if name == "":
            self.name     = binascii.b2a_hex(os.urandom(4)).decode();
      else: self.name     = name;
      self.host           = host;
      self.port           = port;
      self.lhost          = lhost;
      self.lport          = lport;
      self.listening      = False;
      self.connected      = False;
      self.reset_server   = False;
      self.reset_on_write = False;
      self.reset_on_read  = False;


   def _select(self, rx, wx, xx):
         rx  = [r for r in rx if r.fileno() > 0];
         wx  = [w for w in wx if w.fileno() > 0];
         xx  = [x for x in xx if x.fileno() > 0];
         rxx = [r.sock for r in rx]; 
         wxx = [w.sock for w in wx]; 
         xxx = [x.sock for x in xx]; 
         rxx, wxx, xxx = select.select(rxx, wxx, xxx);
         rx = [r for r in rx if r.sock in rxx]
         wx = [w for w in wx if w.sock in wxx]
         xx = [x for x in xx if x.sock in xxx]
         return rx, wx, xx;


   def fileno(self):
       return self.sock.fileno();




   def reset(self):
      self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
      return self.sock;



   def listen(self):
       import math; import random;
       if not self.listening:
          print((self.lhost, self.lport));
          while True:
             port = (math.floor(random.random()*10000+50000) 
                     if (self.lport == 0) else self.lport);
             try:
                self.sock.bind((self.lhost, port));
                self.sock.listen(5);
             except Exception as e: 
                  import traceback;
                  traceback.print_exc();
                  print(port);
                  input();
             else: break;
          lhost, lport   = self.sock.getsockname();
          self.lport     = lport;
          conn, addr     = self.sock.accept();
          host, port     = addr;
          self.plug      = Socket(host, port, name='?', init=False);
          self.plug.sock = conn;
          self.listening = True;


   def read(self):
       if self.reset_server:
          self.reset();
          self.listening = False;
       self.listen();
       data = bytearray();
       while 1:
          recvdata = self.plug.sock.recv(1024)
          if not recvdata: break;
          else: data += recvdata;
       data = self.decode(data);
       self.plug.name = data['id'];
       if self.reset_on_read:
          self.plug.sock.close();
          self.listening = False;
       return data;


   def decode(self, data):
       try:    data = json.loads(data);
       except: print(('error decoding: ', data));
       return  data;


   def encode(self, data):
       if isinstance(data, dict):
          if 'id' not in data:
             data['id'] = self.name;
          try:    data = json.dumps(data);
          except: data = str(data);
       return bytearray(data, 'utf-8');


   def write(self, data):
      try:
         data = self.encode(data);
         if self.reset_on_write: 
            self.reset();
         while True:
            rx, wx, xx = self._select([], [self], []);
            for ww in wx:
               w = ww.sock;
               if not ww.connected:
                  try: 
                     w.connect((self.host, self.port));
                     ww.connected = True;
                  except BlockingIOError: 
                     ww.connected = False;
                     continue;
               w.sendall(data);
               if ww.reset_on_write:
                  w.close();
                  ww.connected = False;
               return;
      except Exception as e: 
           import traceback;
           traceback.print_exc();



class Server(Socket):


     data = {};


     def __init__(self, host, port):
        super().__init__(host, port, host, port);
     

     #####################################
     #! load all data from queue into dict
     #####################################
     def _load(self, q):
         data = bytearray();
         while not q.empty():
            data += q.get();
         data = self.decode(data);
         self.data[data['id']] = data;
         return data['id'];


     def postproc(self, args):
         print(('postproc: ', args));
         return args;


     def reset(self):
         super().reset()
         if not self.listening:
            self.sock.bind((self.lhost,self.lport));
            self.sock.listen(5);
            self.listening = True;


     def read(self):
        qs = {}
        rx = [self];
        while True:
           serversock = self.sock;
           if self not in rx:
              rx += [self];
              if self.reset_server:
                 self.reset();
           rx, wx, xx = self._select(rx, rx, []);
           self.rx = rx;
           self.wx = wx;
           for ss in rx:
              try:
                 s = ss.sock;
                 if s == serversock:
                   #print((ss, s));
                   conn, addr = s.accept();
                   host, port = addr;
                   if conn:
                      conn.setblocking(0);
                      plug = Socket(host, port, name='', init=False);
                      plug.sock = conn;
                      rx.append(plug); 
                      qs[conn] = queue.Queue();
                 else:
                   data = s.recv(1024);
                   if not data: 
                       if not qs[s].empty():
                          id = self._load(qs[s]);
                          self.postproc({'socket': ss, 'id': id});
                       if ss.reset_on_read:
                          s.close()
                   else: 
                      qs[s].put(data);
              except Exception as e: 
                  import traceback;
                  traceback.print_exc();
                  sys.exit(1);



class ChatClient(Socket):

      log = smartlog.Smartlog();

      def __init__(self, name):
          super().__init__('box.local', 50007, name=name);
          self.log.printname=True;
          self.run();

      def listener(self):
          while True:
            x = self.read(); 
            self.log.name = x['from']
            self.log.logn(x['date'] + ': ' + x['content']);

      def talker(self):
          while True:
             x = self.log.prompt('msg');
             self.write({
                'from': self.name, 
                'content': x,
                'date': quickdate('now')
             });

      def run(self):
          self.write({
             'from': self.name, 
             'content': 'logged in',
             'date': quickdate('now')
          });
          listener = threading.Thread(target=self.listener, args=());
          listener.run();
          self.talker();
          
          


class ChatServer(Server):

      log = smartlog.Smartlog();

      def __init__(self):
          super().__init__('box.local', 50007);

      def postproc(self, args):
         msg = self.data[args['id']];
         for w in self.wx:
             if w != self:
                w.write(msg);
                print(msg);
         sock = args['socket'];
         return args;



class SmartlogServer(Server):

      log = smartlog.Smartlog();

      def postproc(self, args):
         self.log.printname = True
         for k in self.data[args['id']]:
             self.log.name = k;
             self.log.info("%s" % (
                  self.data[args['id']][k]
             ));
         return args;



class DispatchServer(Server):

      #ts = []
      def runcmd(self, sock, key, data):
          cmd = data['cmd'];
          import subprocess
          p = subprocess.Popen(
                cmd.split(" "), 
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
          );
          log = smartlog.Smartlog();
          log.name      = key;
          log.printname = True
          stdout, stderr = p.communicate();
          for line in stdout.decode().split('\n')[:-1]:
              log.logok(line);

      def postproc(self, args):
          for k in self.data:
              t = threading.Thread(target=self.runcmd, args=(args['socket'], k, self.data[k]));
              t.start();
          self.data = {};
          return args;
