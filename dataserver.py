import smartlog
import hashtag
import json
import toolbelt


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


      def configure(self, format=None):
          if not format: format = self.format;
          commands = ['new', 'edit', 'view', 'list', 'search'];
          if 'fields' in format:
             for command in commands:
                 if command in format:
                    if 'fields' not in format[command]:
                        format[command]['fields'] = format['fields'];
                    if 'include' in format[command]:
                        format[command]['fields'] += format[command]['include'];
                    if 'exclude' in format[command]:
                        format[command]['fields'] = toolbelt.logic.difference(
                        format[command]['fields'], format[command]['exclude']);
                 else:  format[command] = {'fields': format['fields']};
          self.format = format;


      open_ = open
      def open(self, arg):
          """ Opens database from JSON file, or argument """
          if isinstance(arg, str) and os.path.exists(arg):
             f = open_(arg, 'r')
             self.data = json.loads(f.read());
          elif isinstance(arg, list):
             self.data = arg;

      def load(self,path):
          try:
             if path.endswith(".csv"):
                import csv
                with open(path, mode='r') as csvfile:
                   self.describe();
                   reader = csv.DictReader(csvfile, self.types.keys());
                   self.data = [];
                   for row in reader:
                       self.data  += [row];
             elif path.endswith(".tag"):
                  from hashtag.hashtag import HashTagger;
                  ht = HashTagger(path);
                  self.data = ht.db;
             elif path.endswith(".json"):
                  import json;
                  f = open(path, 'r');
                  self.data = json.loads(f.read());
                  close(f)
             else: 
                  from toolbelt.editors import vimdb
                  vimdb(self.data);
          except: 
            import traceback;
            traceback.print_exc();
            return False;
          else:   return True;


      def describe(self):
          """ Sets types"""
          for i in range(len(self.data)):
              for k in self.data[i]:
                  if k not in self.types:
                     self.types[k] = type(self.data[i][k]);
          return self.types;



      def first(self, data=None):
          """ Gets first value """
          if not data: data = self.data;
          if data:
             if len(data) > 0:
                return data[0];
          return None;


      def search(self, query):
          """ Searches, returns list of indices """
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



      def insert(self, data):
          """ Creates a new entry"""
          if isinstance(data, dict):
             self.data += [data];
          elif isinstance(data, list):
             self.data += data;
          elif isinstance(data, tuple):
             self.data += list(data); 



      def delete(self, ids):
         """ Deletes by id"""
         if not isinstance(ids, list):
            ids = [ids];
         for id in ids:
            ds = [d for d in self.data if d[self.pk]==id]
            for d in ds:
                self.data.remove(d);



      def update(self, uds):
          """ Updates by data/id """
          if not isinstance(uds, list):
             uds = [uds];
          for d in uds:
             ds = [x for x in self.data if d[self.pk]==x[self.pk]]
             for x in ds:
                 x.update(d);
             if not ds: 
                 self.data += [d];


      def save(self,path):
          try:
             if path.endswith(".csv"):
                import csv
                with open(path, mode='w') as csvfile:
                   self.describe();
                   writer = csv.DictWriter(csvfile, self.types.keys());
                   writer.writeheader();
                   for row in self.data:
                       writer.writerow(row);
             elif path.endswith(".tag"):
                  from hashtag.hashtag import HashTagger;
                  ht = HashTagger('');
                  ht.db = self.data;
                  ht.writeout(filename=path);
             elif path.endswith(".json"):
                  import json;
                  jstr = json.dumps(self.data);
                  f = open(path, 'w');
                  f.write(jstr);
             else: 
                  from toolbelt.editors import vimdb
                  vimdb(self.data);
          except: 
            import traceback;
            traceback.print_exc();
            return False;
          else:   return True;

