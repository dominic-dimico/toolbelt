
class ArgumentError(Exception):

      def introspect(self):
          message = "";
          alert   = "";
          self.errors = 0;
          self.alerts = [];
          for key in self.default.keys():
            if isinstance(self.default[key], dict):
              if 'error' in self.default[key]:
                 message      += '\nError: '     + key + ' '   + self.default[key]['error'];
                 alert        +=                   key + ' '   + self.default[key]['error'];
                 if 'log'     in self.default[key]:
                     message  += '\n  name:    ' + key + ' - ' + self.default[key]['log'];
                 if 'default' in self.default[key]:
                     message  += '\n  default: '               + str(self.default[key]['default']);
                 if 'type'    in self.default[key]:
                     message  += '\n  type:    '               + str(self.default[key]['type'])
                 if 'actions' in self.default[key]:
                     message  += '\n  actions: ' + ",".join(     self.default[key]['actions'])
                 self.errors  = self.errors + 1;
                 self.alerts += [alert];
          self.message = message;
          return message;

      def __init__(self, default):
          self.default = default; 
          self.introspect();




# TODO: Put into different class
def argcheck(user, default, log=None):
    """ Process arguments
    """

    if not log:
       from smartlog import Smartlog;
       log = Smartlog();

    def add_error(default, key, error):
        if 'error' not in default[key]: 
                          default[key]['error']  =        error;
        else:             default[key]['error'] += '; ' + error;
        return            default;


    from copy import copy
    def backup(user, key, ext='.1'):
        if ext != '.1':
           user[key+ext] = copy(user[key]);
           return user;
        index = 1;
        backup_key = key + ext;
        while backup_key in user:
              backup_key = key + "." + str(index);
              index      = index + 1;
        user[backup_key] = copy(user[key]);
        return user;


    def restore(user, key, ext='.1'):
        if ext != '.1':
            user[key] = user[key+ext];
            user.pop(backup_key)
            return user;
        index = 1;
        next_backup_key = key + ext;
        last_backup_key = key;
        while next_backup_key in user:
              index           = index + 1;
              last_backup_key = next_backup_key;
              next_backup_key = key + "." + str(index);
        if last_backup_key in user and last_backup_key != key:
            user[key] = copy(user[last_backup_key]);
            user.pop(last_backup_key)
        else: return None;
        return user;


    def default_actions(user, default, key):

        if 'actions' not in default[key]:
           default[key]['actions'] = [];

        actions = [
           'log',
           'restore', 'backup',  
           'default', 'overwrite', 
           'clear',   'delete', 
           'gather',  
           'type',    
           'require', 
        ];

        for action in actions:
            if (((action in default and key in default[action])
              or (action in default[key])) 
             and (action not in default[key]['actions'])):
                     default[key]['actions'] += [action];

        if 'all' in default:
           default[key]['actions'] = default['all'] + default[key]['actions'];

        return (user, default);


    def do_gather(log, user, default, key):
        t = str;
        if 'gather' not in default[key]:
              default[key]['gather'] ='maybe';
        if    default[key]['gather']=="never": return (user, default);
        elif (default[key]['gather']=="always" or
             (default[key]['gather']=="maybe"  and 
               key not in user 
             )):
             if 'type' in default[key]:
                 t = default[key]['type'];
             args = log.gather({
                       'method': 'linear',
                       'keys'  : [key],
                       'data'  : {},
                       'types' : {key:str(t)},
             });
             try:    user[key] = (t)(args['data'][key]);
             except: user[key] = '';
        return (user, default)


    def do_actions(log, user, default, key):
        (user, default) = default_actions(user, default, key);
        for action in default[key]['actions']:
            if action == "require":
               log.log("Requiring %s" % (key));
               if key not in user:
                    log.fail("not found");
                    default = add_error(default, key, "required");
                    break;
               else: log.ok();
            elif action == "gather":
                 (user, default) = do_gather(log, user, default, key);
            elif action == "overwrite":
                     log.log("Overwriting %s" % (key));
                     user[key] = default[key]['overwrite'];
                     log.ok();
            elif action == "default":
                 if key not in user: 
                     log.log("Defaulting %s" % (key));
                     if 'default' in default[key]:
                        user[key] = default[key]['default'];
                        log.ok(str(default[key]['default']));
                     else: log.fail("no default field supplied");
            elif action == "restore":
                    log.log("Restoring %s" % (key));
                    if 'restore' in default[key]:
                          restored = restore(user, key, default[key]['restore']);
                    else: restored = restore(user, key);
                    if not restored: log.fail("no backup");
                    else: 
                      user = restored;
                      log.ok(str(user[key]));
            elif action == "clear":
                    log.log("Clearing %s" % (key));
                    if isinstance(user[key], str):
                       user[key] = '';
                    elif isinstance(user[key], dict):
                       user[key] = {}; 
                    elif isinstance(user[key], list):
                       user[key] = []; 
                    elif isinstance(user[key], tuple):
                       user[key] = tuple(); 
                    elif isinstance(user[key], int):
                       user[key] = 0; 
                    elif isinstance(user[key], float):
                       user[key] = 0.0; 
                    else: 
                       user[key] = None;
                    log.ok();
            elif action == "delete":
                 log.log("Deleting %s" % (key));
                 if key in user: 
                    user.pop(key);
                    log.ok();
                 else: log.fail("no key to delete")
            elif action == "log":
                 if 'log' in default[key]:
                    log.info(key+": "+default[key]['log']);
            elif action == "backup":
                 log.log("Backing up %s" % (key));
                 if key in user: 
                    if 'backup' in default[key]:
                          user = backup(user, key, default[key]['backup']);
                    else: user = backup(user, key);
                    log.ok();
                 else: log.fail();
            elif action == "type":
                 log.log("Type-checking %s" % (key));
                 if 'type' in default[key]: 
                     if key in user:
                        if not isinstance(user[key], default[key]['type']):
                           try:   
                               user[key] = (default[key]['type'])(user[key]);
                               log.ok("converted");
                           except Exception: 
                               default = add_error(default, key, "type");
                               log.fail("exception occured");
                               break;
                        else: log.ok("ok");
                     else: log.fail('key not found');
                 else: log.fail('type not set');
        return (user, default);


    def extract_keys(log, user, default):
        keys = list(default.keys());
        morekeys = [];
        for key in keys:
            if isinstance(default[key], list):
               for akey in default[key]:
                   if akey not in morekeys:
                      morekeys += [akey];
        for key in morekeys:
            if key not in default:
               default[key] = {};
        return (user, default);


    def process(log, user, default):
        keys = list(default.keys());
        for key in keys:
            if isinstance(default[key], dict):
               (user, default) = do_actions(log, user, default, key);
        return (user, default);


    def check_errors(log, user, default):
        ae = ArgumentError(default);
        for i in range(ae.errors):
            log.alert(ae.alerts[i]);
        return ae;


    if not isinstance(user, dict):
       raise ArgumentError({'args':{'error':'type'}});

    if not isinstance(default, dict):
       raise ArgumentError({'default':{'error':'type'}});


    quiet = log.quiet;
    log.quiet = True;
    if 'quiet' in default and not default['quiet']:
       log.quiet = False;

    (user, default) = extract_keys(log, user, default);
    (user, default) =      process(log, user, default);
    ae              = check_errors(log, user, default);

    log.quiet = False;
    if ae.errors>0: 
       raise ae;

    return user;


def funcheck(log, args, preproc, function, postproc):
    """ Do argcheck before/after a function call """
    args = log.argcheck(args, preproc);
    args = function(args);
    args = log.argcheck(args, postproc);
    return args;


def copyback(log, args, keys, function):
    """ Call a *function* that accepts dict *args*, but 
        backup *args* before calling it, and restore *args*
        after
    """
    return log.funcheck(
         args,
        {'backup' : keys},
         function,
        {'restore' : keys}
    );



