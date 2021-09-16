class Cursor():


      xmin =  0;
      ymin =  0;
      xmax = 10;
      ymax = 10;
      x    =  0;
      y    =  0;


      def __init__(self, args=None):
          if args: self.resize(args);


      def violation(self, dx, dy):
          if (self.x+dx > self.xmax or self.x+dx < self.xmin or 
              self.y+dy > self.ymax or self.y+dy < self.ymin):
                return True;
          else: return False;


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
          if self.y > self.ymin:
             self.y -= 1;
      

      def down(self):
          if self.y < self.ymax-1:
             self.y += 1;


      def left(self):
          if self.x > self.xmin:
             self.x -= 1;


      def right(self):
          if self.x < self.xmax-1:
             self.x += 1;

