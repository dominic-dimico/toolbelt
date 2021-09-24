import os
import tempfile 
import subprocess
import code

ed = os.environ.get('EDITOR', 'vim')
def vim(note=""):
    tf = tempfile.NamedTemporaryFile(mode="a+b", suffix=".note", delete=False);
    b = bytes(note, "utf8");
    tf.write(b);
    tf.flush();
    name = tf.name;
    tf.close();
    tf = open(name, 'a');
    subprocess.call([ed, tf.name]);
    tf.flush();
    tf.close();
    tf = open(name, 'r');
    note = tf.read();
    os.unlink(tf.name);
    return note;
