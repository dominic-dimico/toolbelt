import datetime
import toolbelt
import random
import time


def random_date(start, end):
    random.seed(time.time());
    start = toolbelt.converters.date(start);
    end   = toolbelt.converters.date(end);
    delta = end - start
    if delta.days > 0:
          random_day = random.randrange(delta.days)
    else: random_day = 0;
    random_sec = random.randrange(delta.seconds);
    secs = random_day * 24 * 60 * 60 + random_sec;
    return start + datetime.timedelta(seconds=secs)


def random_int(a, b):
    random.seed(time.time());
    return random.randint(a, b);


def random_index(n):
    random.seed(time.time());
    return random.randint(0, n-1);
