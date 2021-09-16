import smartlog
import toolbelt
import sys


class Interpreter:

  auto     = toolbelt.keybindings.AutoCompleter();
  log      = smartlog.Smartlog();
  commands = {}


  def help(self):
      maxlength = max([len(key) for key in self.commands.keys()]);
      for key in self.commands:
          description = ""
          if 'opts' in self.commands[key]:
             if 'help' in self.commands[key]['opts']:
                description = self.commands[key]['opts']['help'];
          spaces = ' ' * (maxlength - len(key));
          self.log.info("%s%s : %s" % (key, spaces, description));


  def quit(self):
      sys.exit(0);


  def __init__(self, commands=None):
      self.commands = {
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
         }
      if commands:
         self.commands.update(commands);


  # Handle command 
  def handle(self, command):
      if command['cmd'] not in self.commands: 
         self.log.warn("Command not found: %s" % (command['cmd']));
         self.help();
         return;
      command_name = command['cmd'];
      action = self.commands[command_name];
      args = None;
      if action['args']:
         args = self.log.gather(
                  action['args'].keys(), 
                  command['xs'],
                  opts={'overwrite': False}
                );
      return self.log.exlog(action['func'], args, action['opts']);


  def run(self, xs=None):
      command = self.log.gatherwords(['cmd'], xs);
      self.handle(command);
