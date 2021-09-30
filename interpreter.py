import smartlog
from toolbelt import keybindings
import sys
import re;


class Interpreter:

  auto     = keybindings.AutoCompleter();
  log      = smartlog.Smartlog();
  commands = {}


  def help(self):
      description = {};
      for key in self.commands:
          if 'opts' in self.commands[key]:
             if 'help' in self.commands[key]['opts']:
                description[key] = self.commands[key]['opts']['help'];
      self.log.logdata({'data': description});


  def quit(self):
      sys.exit(0);


  def __init__(self, commands=None):
      if not self.commands:
         self.commands = {};
      self.commands.update({
           'help' : {
              'func' :  self.help,
              'args' :  None,
              'opts' :  { 'help' : 'print this info' }
           }, 
           'quit' : {
              'func' :  self.quit,
              'args' :  None,
              'opts' :  { 
                'log'  : 'Quitting program',
                'help' : 'quit program' 
              }
           }
         })
      if commands:
         self.commands.update(commands);


  # Handle command 
  def handle(self, args):

      adf = args['argspec'];

      import pandas
      try:
         cn = adf.loc[adf['key']=='cmd'].iloc[0]['data'];
         action = self.commands[cn];
         dogather = False;
         if action['args']:
              for arg in action['args']:
                  idx = adf[adf['key']==arg].index.to_list()
                  adf.optional.loc[idx] = False
                  if pandas.isnull(adf.data.loc[idx]).any():
                     dogather = True;
              args['argspec'] = adf;
         if dogather: args = self.log.gather(args);
         #self.log.print(args);
             
         args = self.preprocess({
            'argspec' : args['argspec'],
               'data' : args['data'],
               'auto' : args['auto'],
                 'xs' : args['xs']
         });
         if 'args' in action:
             if not action['args']:
                args = None;
      except KeyError: 
         self.log.warn("Command not found: %s" % (cn));
         return args;
      except Exception:
         import traceback; traceback.print_exc();
         import code; code.interact(local=locals()); 

      args = self.log.exlog(
        callback = action['func'], 
        args     = args,
        opts     = action['opts']
      );
      args = self.log.exlog(
        callback = self.postprocess,
        args     = args
      );
      return args;


  def preprocess(self, args):
      return args;

  def postprocess(self, args):
      return args;


  def run(self, xs=None):
      while True:
            args = self.log.gather({
                'argspec'   : self.argspec,
                'keys'      : ['cmd'], 
                'xs'        : xs, 
                'auto'      : self.auto,
                'words'     : True
            });
            args = self.handle(args);
            xs = [];
