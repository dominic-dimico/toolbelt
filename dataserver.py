import smartlog
import hashtag
import json


# Let's assume a DataServer base class is a list of dictionaries.
# Then we can convert any type to and from it
class DataServer:


      pk      = 'id';
      config  = None; # for accessing SQL tables, decrypting ht databases
      name    = '';   # SQL table, ht database, dict var name
      types   = {};   # key->type dictionary
      log     = None; # A smartlog
      data    = [];   # SQL table, list of dictionaries, hashtag db
      format  = {};   # how to join other dataservers
      friends = [];   # references to other dataservers


      def __init__(self, name='dataserver'):
          self.name   = name;
          self.log    = smartlog.Smartlog();


      open_ = open
      def open(self, arg):
          if os.path.exists(arg):
             f = open_(arg, 'r')
             self.data = data;


      #############
      #! Sets types
      #############
      def describe(self):
          if self.types: 
             return self.types;
          for i in len(self.data):
              for k in self.data[i]:
                  if k not in self.types:
                     self.types[k] = type(self.data[i][k]);
          return self.types;



      ######################
      #! #! Gets first value
      ######################
      def first(self):
          if self.data:
             if len(self.data) > 0:
                return self.data[0];
          return None;


      ######################################
      #!   Searches, returns list of indices
      ######################################
      def search(self, query):
          import re;
          locs = [];
          if '=' in query: 
             parts = query.split("=");
             field = parts[0];
             value = parts[1];
             f = re.compile(field);
          else: f = re.compile('.');
          v = re.compile(value);
          for i in range(len(self.data)):
              for k in self.data[i]:
                  if f.match(k):
                     if v.match(str(self.data[i][k])):
                        locs.append(i);
          return locs;



      ####################################
      #!   Creates a new entry
      ####################################
      def insert(self, data):
          if isinstance(data, dict):
             self.data += [data];
          elif isinstance(data, list):
             self.data += data;
          elif isinstance(data, tuple):
             self.data += list(data); 


      ####################
      #! Deletes by id
      ####################
      def delete(self, id):
          ds = [d for d in self.data if d[self.pk]==id]
          for d in ds:
              self.data.pop(d);


      #######################
      #! Updates by data/id 
      #######################
      def update(self, d):
          ds = [x for x in self.data if d[self.pk]==x[self.pk]]
          for x in ds:
              x.update(d);
          if not ds: self.data += [d];



if '__name__' == '__main__':
   ds = DataServer('people');
   ds.update();
