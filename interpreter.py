import smartlog
from toolbelt import keybindings
import sys


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
      if self.commands:
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
      self.auto.words += list(self.commands.keys());


  # Handle command 
  def handle(self, args):
      command_name = args['data']['cmd'];
      if command_name not in self.commands: 
         self.log.warn("Command not found: %s" % (command_name));
         self.help();
         return;
      action = self.commands[command_name];
      if action['args']:
         args['keys']      = action['args'].keys();
         args['overwrite'] = False;
         args['words']     = False;
         args = self.log.gather(args);
      args = self.preprocess({
           'data' : args['data'],
           'auto' : args['auto'],
           'xs'   : args['xs']
      });
      if 'args' in action:
         if not action['args']:
            args = None;
      args = self.log.exlog(
        callback = action['func'], 
        args     = args,
        opts     = action['opts']
      );
      return args;


  def preprocess(self, args):
      pass


  def run(self, xs=None):
      while True:
          args = self.log.gather({
            'keys'      : ['cmd'], 
            'xs'        : xs, 
            'auto'      : self.auto,
            'words'     : True
          });
          self.handle(args);
          xs = [];
