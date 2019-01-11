import os
import tempfile 
import subprocess
ed = os.environ.get('EDITOR', 'vim')
def vim(note):
    if not note: note = ""
    tf = tempfile.NamedTemporaryFile(suffix=".tmp", delete=False);
    tf.write(note)
    tf.flush()
    name = tf.name
    tf.close()
    tf = open(name, 'rw')
    subprocess.call([ed, tf.name])
    tf.flush()
    note = tf.read()
    os.unlink(tf.name)
    return note
