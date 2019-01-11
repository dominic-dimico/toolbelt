import time
import parsedatetime

cal = parsedatetime.Calendar();
def date(string):
      parsed = cal.parse(string)[0]
      dt = time.strftime('%Y-%m-%d %H:%M:%S', parsed)
      return dt;
