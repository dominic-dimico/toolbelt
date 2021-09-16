import time
import re
import parsedatetime
import datetime
import random
import time
import pytz

cal = parsedatetime.Calendar();
class TagException(Exception):
      pass;


# More stuff?
#   before, after
#   which day of week it is


class QuickDate():

    query = ""


    def __init__(self,query="now"):
        self.set(query);


    # Set all members
    def set(self,query="now"):
        self.now  = self.qry2dt("now");
        self.lex  = self.qry2lex(query);
        self.dt   = self.lex2dt(self.lex);
        self.iso  = self.dt2iso(self.dt);
        self.secs = self.dt2secs(self.dt);
        self.file = self.dt2file(self.dt);


    # Set all member with dt
    def setbydt(self,dt):
        self.dt   = dt;
        self.now  = self.qry2dt("now");
        self.lex  = self.dt2lex(dt);
        self.iso  = self.dt2iso(dt);
        self.secs = self.dt2secs(dt);
        self.file = self.dt2file(dt);


    # Convert query to lexicographic format
    def qry2lex(self,query):
          parsed = cal.parse(query)[0]
          dt = time.strftime('%Y-%m-%d %H:%M:%S', parsed)
          return dt;


    # Convert string date to datetime
    def lex2dt(self,lex):
         return cal.parseDT(datetimeString=lex, tzinfo=pytz.timezone("America/New_York"))[0]


    # Convert query directly to date
    def qry2dt(self,query):
        return self.lex2dt(self.qry2lex(query));


    # Convert datetime to string
    def dt2iso(self,dt):
         return time.strftime('%Y-%m-%dT%H:%M:%S-04:00', dt.timetuple())


    # Convert datetime to lexicographic string
    def dt2lex(self,dt):
         return time.strftime('%Y-%m-%d %H:%M:%S', dt.timetuple())


    # Convert datetime to lexicographic string
    def dt2file(self,dt):
         return time.strftime('%Y-%m-%d_%H:%M:%S', dt.timetuple())


    # Return number of seconds of a query specification (e.g. "1 minute")
    def qry2secs(self,query):
        then = self.qry2dt(query);
        now  = self.qry2dt("now");
        delta = then - now;
        return abs(delta.seconds);


    # Return number of seconds of a datetime specification (e.g. "1 minute")
    def dt2secs(self,dt):
        then = dt;
        now  = self.qry2dt("now");
        delta = then - now;
        return abs(delta.seconds);


    # Return number of seconds of a datetime specification (e.g. "1 minute")
    def before(self,qd):
        return self.dt < qd.dt;


    # Generate a random date within range
    def random(self,d1,d2):

        random.seed(time.time());
        d1dt = self.qry2dt(d1);
        d2dt = self.qry2dt(d2);
        delta = d2dt - d1dt;

        random_day = 0;
        plural     = 0;
        if delta.days > 0:
           if delta.days > 1:
              random_day = random.randrange(delta.days-1)
           plural = 1;

        random_sec = random.randrange(
           plural*(24*60*60) + delta.seconds
        );

        secs = random_day * 24 * 60 * 60 + random_sec;
        rdt = d1dt + datetime.timedelta(seconds=secs);

        self.query = "between %s and %s" % (d1, d2);
        self.setbydt(rdt);

        return rdt;
