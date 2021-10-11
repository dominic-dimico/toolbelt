import toolbelt
import json;

#cc = toolbelt.sockets.ChatClient('dominic');

# def hello(s):
#     sock  = toolbelt.sockets.Socket('localhost', 50007, s);
#     data  = bytearray('ls', 'utf-8');
#     print((len(data), sock.name, data));
#     sock.write(data);
# 
# def hello1(args):
#     hello('death');
#     return args;
# 
# def hello2(args):
#     hello('maiden');
#     return args;


def docmd(name, cmd):
    sock = toolbelt.sockets.Socket('localhost', 50007, name);
    data = { "id": name, "cmd": cmd };
    print(sock.name, data);
    sock.write(data);

def ls(args):
    docmd('dat', 'date');
    return args;

def pwd(args):
    docmd('pwd', 'pwd');
    return args;

p = toolbelt.poller.Poller(
[
{
  'function' : ls,
  'naptime'  : 2,
},

{
  'function' : pwd,
  'naptime'  : 3,
}

]);
p.poll();
