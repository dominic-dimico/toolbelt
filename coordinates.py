class Coordinates():


      xmin =  0;
      ymin =  0;
      xmax = 10;
      ymax = 10;
      x    =  0;
      y    =  0;

      xwrap = False;
      ywrap = False;


      def __init__(self, args=None):
          if args: self.resize(args);


      def violation(self, dx, dy):
          if ((self.xwrap or (self.x+dx < self.xmax and self.x+dx > self.xmin)) and
              (self.ywrap or (self.y+dy < self.ymax and self.y+dy > self.ymin))):
                return True;
          else: return False;


      def adjust(self, what, howmuch):
          if what=='xmin': self.xmin += howmuch;
          elif what=='ymin': self.ymin += howmuch;
          elif what=='xmax': self.xmax += howmuch;
          elif what=='ymax': self.ymax += howmuch;


      def getpos(self):
          return (self.x, self.y);


      def setpos(self, x, y):
          if not self.violation(x-self.x, y-self.y):
             self.x = x;
             self.y = y;


      def move(self, dx, dy):
          if not self.violation(dx, dy):
             self.x += dx;
             self.y += dy;


      def resize(self, args): 
          try:
              self.x    = args['x'];
              self.y    = args['y'];
              self.xmax = args['xmax'];
              self.ymax = args['ymax'];
              self.xmin = args['xmin'];
              self.ymin = args['ymin'];
          except KeyError:
              pass;


      def up(self):
          if self.ywrap:
             self.y = (((self.y + 1) % (self.ymax-self.ymin+1)) + self.ymin);
          elif self.y > self.ymin:
             self.y -= 1;
      

      def down(self):
          if self.ywrap:
              self.y = (
                    ((self.y + (self.ymax-self.ymin)) % 
                    (self.ymax-self.ymin+1)) + self.ymin
              );
          elif self.y < self.ymax:
             self.y += 1;


      def left(self):
          if self.xwrap:
             self.x = (
                ((self.x + (self.xmax-self.xmin)) % 
                (self.xmax-self.xmin+1)) + self.xmin
             );
          elif self.x > self.xmin:
             self.x -= 1;


      def right(self):
          if self.xwrap:
             self.x = ((self.x + 1) % (self.xmax-self.xmin+1)) + self.xmin;
          elif self.x < self.xmax:
             self.x += 1;


class Cursor(Coordinates):

     def __init__(self, args={}):

         super().__init__(args);

         from smartlog import Smartlog;
         self.log = Smartlog();

         args = self.log.argcheck(args, {
            'kb'     : {'default' :  None},
            'extend' : {'default' :  False},
         });

         if args['kb']: 
            self.kb = args['kb'];
         else:
           from toolbelt.keybindings import KeyBindings;
           self.kb = KeyBindings({
              'h'  : (self.up,    None),
              'l'  : (self.down,  None),
              'k'  : (self.left,  None),
              'j'  : (self.right, None),
              '\n' : (self.getpos, None),
           });
           if args['extend']:
               self.kb.bindings.update({
                  'L' : (self.adjust,  ('xmax',  1)),
                  'H' : (self.adjust,  ('xmax', -1)),
                  'K' : (self.adjust,  ('ymax', -1)),
                  'J' : (self.adjust,  ('ymax',  1)),
               });



