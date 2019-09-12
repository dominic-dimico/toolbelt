import time
import re
import parsedatetime
from pytz import timezone

class TagException(Exception):
      pass;

cal = parsedatetime.Calendar();
def date(string):
      parsed = cal.parse(string)[0]
      dt = time.strftime('%Y-%m-%d %H:%M:%S', parsed)
      return dt;

def datedt(string):
     return cal.parseDT(datetimeString=string, tzinfo=timezone("America/New_York"))[0]

def datestr(dt):
     return time.strftime('%Y-%m-%dT%H:%M:%S-04:00', dt.timetuple())

# Var tags are of the form:
#     var1=val1,val2;var2=val3,val4
def tokenize_var_tags(string):
    assignments = string.split(';');
    tokens = {};
    for assignment in assignments:
        sides = assignment.split('=');
        if len(sides) != 2:
           raise TagException("%s has zero/multiple '='" % assignment);
        left = sides[0];
        right = sides[1];
        values = right.split(',');
        tokens[left] = right;
    return tokens;


def replace_vars(string, dictionary):
    vars = re.findall("\{(\w+)\}", string);
    #print vars;
    keys = dictionary.keys();
    for var in vars:
        if var in keys:
           value = dictionary[var];
           string = re.sub("{%s}"%var, value, string);
    return string;

