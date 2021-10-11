
def unique(a):
  return list(set(a))

def intersect(a, b):
  return list(set(a) & set(b))

def union(a, b):
  return list(set(a) | set(b))

def concat(a, b):
  return a + b;

def difference(a, b):
  return list(set(a) - set(b))

