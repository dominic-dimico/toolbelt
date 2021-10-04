import toolbelt
import queue;

# sock = toolbelt.sockets.Socket('localhost', 50007);
# print(sock.read())

server = toolbelt.sockets.Server('localhost', 50007);
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
