import os
import tempfile 
import subprocess
import code
import re
import json

tf = tempfile.NamedTemporaryFile
ed = os.environ.get('EDITOR', 'vim')


def writetemp(x, suffix=".note"):
    x = bytes(x, "utf8");
    f = tf(   mode="a+b", 
           suffix=suffix,
           delete=False);
    f.write(x);
    f.flush();
    f.close();
    return f.name;


def file2str(path):
    if os.path.exists(path):
       f = open(path, 'r');
       note = f.read();
       f.close();
       return note;
    return None;


def vim(note=""):
    if not isinstance(note, str):
       note = str(note);
    path = writetemp(note);
    subprocess.call([ed, path]);
    note = file2str(path);
    os.unlink(path);
    return note;


def vimfile(path=""):
    subprocess.call([ed, path]);
    return file2str(path);


def vimlist(ls=[]):
    note = "\n".join(ls);
    note = vim(note);
    return note.split("\n")[:-1];


def dict2str(d):
    note = str(d);
    note = re.sub('\',', '\',\n', note);
    note = re.sub('}',     '}\n', note);
    note = re.sub('{',     '{\n', note);
    note = re.sub('\'',      '"', note);
    return note;


def vimdbloop(note):
    while True:
        note = vim(note);
        try: db = json.loads(note);
        except Exception as e:
               print(e); 
               x = input();
               continue;
        else: break;
    return db;


def vimdict(d={}):
    note = dict2str(d);
    return vimdbloop(note);


sampledb = [
  {'id': 1, 'tags': 'happy'},
  {'id': 2, 'tags': 'rating=5'},
  {'id': 3, 'tags': 'red'},
];

def vimdb(db=[]):
    if not db: db += sampledb;
    ds = [str(x) for x in db];
    note = '[\n  ' + ",\n  ".join(ds) + '\n]';
    note = re.sub('\'', '"', note);
    return vimdbloop(note);
