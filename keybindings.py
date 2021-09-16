import getch
import sys
import smartlog


class KeyBindings():

    log = smartlog.Smartlog();

    def __init__(self, bindings=None):
        if bindings == None:
              self.bindings = {
                'q' : (sys.exit, None),
              };
        else: self.bindings = bindings;

    # Add a keybinding by supplying key, callback, arg
    def add(self, key, callback, args):
        self.bindings[key] = (callback, args);

    # Allow multiple iterations of key command; supports numbers
    def accumulate(self, key):
        num = "";
        while key.isdigit():
              num += key;
              key = getch.getch();
        for i in range(int(num)):
            self.handle(key);

    # Handle keybinding
    def handle(self, key):
        if key.isdigit():
           self.accumulate(key);
        if key not in self.bindings: return True;
        (callback, args) = self.bindings[key];
        if args == None: return callback();
        else:            return callback(args);

    # Show key and function name
    def legend(self):
        str = "";
        for key in self.bindings:
            str += "   " + key + ": " + self.bindings[key][0].__name__ + '\n';
        return str;

    # Wait for keypress, and handle
    def wait(self):
        key = getch.getch();
        self.handle(key);


class AutoCompleter():

    words      = [];
    suggestion = "";
    input      = "";
    finished   = False;
    prompt     = "";

    log = smartlog.Smartlog();


    def __init__(self, words=[]):
        self.words += words;


    def consume(self, key):
        if ord(key) == 127:
           self.input = self.input[:-1];
        elif key == "\x17":
           parts = self.input.split(" ");
           self.input = " ".join(parts[:-1]);
        elif key in "=-';:.,<>/?][{}\|)(!@#$%^&*~_`":
           if self.suggestion:
              self.input += self.suggestion + key;
           else: self.input += key;
        elif key == '\t':
           if self.suggestion:
              self.input += ' ';
        elif key == '\n':
           if self.suggestion:
              self.input += self.suggestion;
           self.finished = True;
        elif key == ' ':
           if self.suggestion:
              self.input += self.suggestion + ' ';
           else: self.input += key;
        elif key.isalnum(): 
           self.input += key;
        else: pass
        self.log.reprint(self.prompt + self.input);


    def autocomplete(self):
        lastword = self.input.split(" ")[-1];
        lastword = ''.join(e for e in lastword if e.isalnum())
        if lastword != "":
            for word in self.words:
                if word.startswith(lastword):
                   self.suggestion = word[len(lastword):];
                   return;
        self.suggestion = None;
               

    def dosuggestion(self):
        if self.suggestion:
           self.log.reprint(
             self.prompt +
             self.input + 
             self.log.t.italic(self.suggestion)
           );


    def handle(self,key):
        self.consume(key);
        self.autocomplete();
        self.dosuggestion();
      

    def run(self):
        self.finished = False;
        self.input = "";
        self.log.outfile.write(self.prompt);
        self.log.outfile.flush();
        while not self.finished:
            key = getch.getch();
            self.handle(key);
        self.log.outfile.write('\n');
        return self.input;
