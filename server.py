import toolbelt
import smartlog;
import queue;

# sock = toolbelt.sockets.Socket('localhost', 50007);
# print(sock.read())
#       def __init__(self, port, host):
#           super().__init__(port, host);


#server = SmartlogServer('localhost', 50007);
#server.read();

server = toolbelt.sockets.DispatchServer('localhost', 50007);
server.read();


# def server_read(args):
#     server.read();
#     return args;

# def server_print(args):
#     server.print();
#     return args;

# p = toolbelt.poller.Poller(
# [
# {
#   'function' : server_read,
#   'naptime'  : 10,
# },
# {
#   'function' : server_print,
#   'naptime'  : 5,
# }
# ]);
# p.poll();
