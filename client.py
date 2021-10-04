import toolbelt


def hello(s):
    sock  = toolbelt.sockets.Socket('localhost', 50007, s);
    data  = bytearray('hello', 'utf-8');
    print((len(data), sock.name, data));
    sock.write(data);

def hello1(args):
    hello('death');
    return args;

def hello2(args):
    hello('maiden');
    return args;


p = toolbelt.poller.Poller(
[
{
  'function' : hello1,
  'naptime'  : 2,
},

{
  'function' : hello2,
  'naptime'  : 3,
}

]);
p.poll();
