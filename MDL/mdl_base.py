import config;

from math import log,factorial;
from error import Error;
from graph import Graph;
from model import Model;

### basic functions
# determine possible number of edges between `numEdges' nodes
def CalcCliqueNumPosEdges(numEdges):
  # directed graph, no self-loops
  # (|n|^2)-n
  return numEdges*numEdges - numEdges;

# (n choose k)
def choose(n, k):
 if 0 <= k <= n:
   p = 1
   for t in xrange(min(k, n - k)):
     p = (p * (n - t)) // (t + 1)
   return p;
 else:
   return 0;

def composition(n,k) :
    return choose(n-1,k-1);

def LC(n,k) :
    return log(composition(n,k),2);

def weakcomposition(n,k) :
    return choose(n+k-1,k-1);
    
def LwC(n,k) :
    return log(weakcomposition(n,k),2);

# Encoded length of `n` 0/1 entries with `k` 1s (aka, Naive Uniform)
def LnU(n,k):
    #print 'LnU', n, k
    if n==0 or k==0 or k==n:
        return 0;    
    x = -log(k / float(n),2);
    y = -log((n-k)/float(n),2);
    return k * x + (n-k) * y;
    
# Encoded length of `n` 0/1 entries with `k` 1s (aka, Uniform)
def LU(n,k) :
    if n==0 or k==0 :
        return 0;   
    return log(choose(n,k),2);

# encoded size of an integer >=1 as by Rissanen's 1983 Universal code for integers
def LN(z) :
  if z <= 0 :
    return 0;
  c = log(2.865064,2);
  i = log(z,2);
  while i > 0 :
    c = c + i;
    i = log(i,2);
  return c;
