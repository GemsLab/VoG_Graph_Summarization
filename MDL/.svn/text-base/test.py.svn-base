import sys
import os

#from mdl import *
from error import Error;
from graph import Graph;
from model import *;
from mdl import *;

gFilename = "cliqueStarClique.graph";
mFilename = "cliqueStarClique_st1.model";

g = Graph();
g.Load(gFilename);
m = Model();

#g.Plot();

(l_total, l_model, l_error, E) = L(g,m);
print "empty model:"
print "  ", l_total, l_model, l_error, E.numErrors;

if(False) :
    m = Model();
    fc1 = FullClique([x for x in range(1,21)]);
    m.addStruct(fc1);
    fc2 = FullClique([x for x in range(27,52)]);
    m.addStruct(fc2);
    st1 = Star(21,[18,19,20,22,23,24,25,26,27,28,29]);
    m.addStruct(st1);

    nc1 = NearClique([x for x in range(1,21)]);
    #m.addStruct(nc1);
    
    (l_total, l_model, l_error, E) = L(g,m);
    print "model with two full cliques, resp. over nodes 1--20, and 27--38:"
    print "  ", l_total, l_model, l_error, E.numErrors;
    
if(True) :
    m = Model();
    m.Load(mFilename);

    (l_total, l_model, l_error, E) = L(g,m);
    print "model \'" + mFilename + "\'";
    print "  ", l_total, l_model, l_error, E.numErrors;
    


if(False):
    #g.Plot()
    E.plotCover();
    E.plotError();
    #print " ".join([str(x)+" "+str(E.errors[x]) for x in range(len(E.errors))])
    #print " ".join([str(x)+" "+str(E.covered[x]) for x in range(len(E.covered))])
