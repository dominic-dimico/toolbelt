import toolbelt
import smartlog

log = smartlog.Smartlog();

#q = toolbelt.quickdate.QuickDate('one hour');
#log.logn("Time is %s" % q.lex);
#q.random('now', 'september 10');
#log.logn("Random day: %s" % q.lex);

#a = toolbelt.keybindings.AutoCompleter([
#    'new', 'edit', 'view', 'client', 'object'
#]);
#a.prompt = "cmd> "
#a.run();


def current_date(args):
    q = toolbelt.quickdate.QuickDate('now');
    args['queue'].put(q.lex);
    return args;
    
def output(args):
    x = args['queue'].get();
    log.logn(x);
    return args;


import queue;
q = queue.Queue();
p = toolbelt.poller.Poller(
[
{
  'function' : current_date,
  'naptime'  : 1,
  'until'    : '10 seconds',
  'queue'    : q,
},
{
  'function' : output,
  'naptime'  : 1,
  'until'    : '10 seconds',
  'queue'    : q,
}
]);
p.poll();
