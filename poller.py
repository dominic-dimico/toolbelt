import time
import threading
import queue
import smartlog
import toolbelt



# Extend into SQL poller
#   - has Squid
#   - polls datetime in database

class Poller:


    log = smartlog.Smartlog();


    def __init__(self, args=None):
        q = queue.Queue();
        self.args = [
        {
            'queue'    : q,
            'naptime'  : '3 seconds',
            'count'    : 6,
            'function' : self.testproducer,
        },
        {
            'queue'    : q,
            'naptime'  : '2 seconds',
            'count'    : 10,
            'function' : self.testproducer,
        },
        {
            'queue'    : q,
            'naptime'  : '1 seconds',
            'until'    : '25 seconds',
            'function' : self.testconsumer,
        }
        ];
        if args:
           self.args = args;
           


    def testproducer(self, args):
        args['queue'].put("%s %s" % (args['threadnum'], args['counter']));
        return args;



    def testconsumer(self, args):
        msg = args['queue'].get();
        self.log.print(msg);
        return args;



    def execute(self, args):
        args = args['function'](args);
        time.sleep(args['naptime']);
        args['counter'] += 1;
        return args;
        

    def pollthread(self, args):
        self.finished = False;
        if 'naptime' not in args:
            args['naptime'] = 1;
        args['counter']=0;
        if 'count' in args: 
            while args['counter']<args['count']:
                  args = self.execute(args);
        elif 'until' in args:
            now   = toolbelt.quickdate.QuickDate();
            until = toolbelt.quickdate.QuickDate(args['until']);
            while now.before(until):
                  args = self.execute(args);
                  now.set();
        else:
            while True:
                  args = self.execute(args);
        args['queue'].task_done();



    def poll(self, args=None):

        if not args: 
               args = self.args;

        ts       = [];
        qs       = []
        threadno = 1;
        for arg in args:
            arg['threadnum'] = threadno;
            t = threading.Thread(target=self.pollthread, args=(arg,));
            ts.append(t);
            if 'queue' in arg:
               if arg['queue'] not in qs:
                  qs.append(arg['queue']);
            threadno += 1;

        for t in ts:
            t.start();

        for q in qs:
            q.join();
