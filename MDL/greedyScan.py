#!/usr/local/bin/python2.6

import sys
import os
import config

from time import time

#from mdl import *
from error import Error;
from graph import Graph;
from model import *;
from mdl import *;

if len(sys.argv) <= 1 :
    print 'at least: <graph.graph> [model.model] [-pC] [-lC] [-pE] [-lE] [-e{NP,NB,TP,TB}]';
    print ' optional argument model = file to read model from, otherwise only empty model';
    print ' optional argument -vX    = verbosity (1, 2, or 3)';
    print ' optional argument -pG    = plot Graph adjacency matrix';
    print ' optional argument -pC    = plot Cover matrix';
    print ' optional argument -pE    = plot Error matrix';
    print ' optional argument -lC    = list Cover entries';
    print ' optional argument -lE    = list Error entries';
    print ' optional argument -eXX   = encode error resp. untyped using prefix (NP), or';
    print '                            binomial (NB) codes, or using typed';
    print '                            prefix (TP) or binomial (TB, default) codes';
    exit();

if (len(sys.argv) > 1 and ("-v1" in sys.argv)) :
    config.optVerbosity = 1;
elif (len(sys.argv) > 1 and ("-v2" in sys.argv)) :
    config.optVerbosity = 2;
if (len(sys.argv) > 1 and ("-v3" in sys.argv)) :
    config.optVerbosity = 3;

t0 = time()

gFilename = sys.argv[1];
g = Graph();
g.load(gFilename);


if config.optVerbosity > 1 : print "- graph loaded."

m = Model();

errorEnc = config.optDefaultError;
if (len(sys.argv) > 1 and ("-eNP" in sys.argv or "-NP'" in sys.argv)) :
    errorEnc = "NP";
elif (len(sys.argv) > 1 and ("-eNB" in sys.argv or "-NB" in sys.argv)) :
    errorEnc = "NB";
elif (len(sys.argv) > 1 and ("-eTP" in sys.argv or "-TP" in sys.argv)) :
    errorEnc = "TP";
elif (len(sys.argv) > 1 and ("-eTB" in sys.argv or "-TB" in sys.argv)) :
    errorEnc = "TB";
        
if config.optVerbosity > 1 : print "- calculating L(M_0,G)"
(l_total_0, l_model_0, l_error_0, E_0) = L(g,m, errorEnc);
if config.optVerbosity > 1 : print "- calculated L(M_0,G)"
print "   \t" + "L(G,M)" + "\tL(M)" + "\tL(E)" + "\t#E+" + "\t#E-" + "\t\t#Ex";
print "M_0:\t" + '%.0f' % l_total_0 + "\t" + '%.0f' % l_model_0 + "\t" + '%.0f' %  l_error_0 + "\t" + str(E_0.numModellingErrors) + '/' + str(E_0.numCellsCovered) + '\t' + str(E_0.numUnmodelledErrors)  + '/' + str(((E_0.numNodes * E_0.numNodes)-E_0.numNodes) - E_0.numCellsCovered) + '\t' + str(E_0.numCellsExcluded);


if len(sys.argv) > 2 and sys.argv[2][0] != '-' :
    mFilename = sys.argv[2];
    m.load(mFilename);
    if config.optVerbosity > 1 : print "- M_x loaded."
    (l_total_x, l_model_x, l_error_x, E_x) = L(g,m, errorEnc);
    print "M_x:\t" + '%.0f' % l_total_x + "\t" + '%.0f' % l_model_x + "\t" + '%.0f' % l_error_x + "\t" + str(E_x.numModellingErrors) + '/' + str(E_x.numCellsCovered) + '\t' + str(E_x.numUnmodelledErrors)  + '/' + str(((E_x.numNodes * E_x.numNodes)-E_x.numNodes) - E_x.numCellsCovered) + '\t\t' + str(E_x.numCellsExcluded);
    
    l_total_all = l_total_x;
    lines = [];
    lines_all = [];
    l_total_prev = l_total_0;
    times = 1;
    maxStructs = m.numStructs;
    
    mFilename_list = mFilename.split('/');
    mFilename_main = mFilename_list[len(mFilename_list) - 1];
    print '%s' % mFilename_main
    #mFilenameGreedy = 'greedySelection_' + mFilename_main;
    #fgreedy = open(mFilenameGreedy,'w')
    #mFilenameGreedyCost = 'greedySelection_costs_' + mFilename_main;
    mFilenameTotalCost = 'greedyScan_totalCosts_' + mFilename_main;
    #fgreedyCost = open(mFilenameGreedyCost,'w')
    ftotalCost = open(mFilenameTotalCost,'w')    

    #fgreedyCost.write("%.0f\n" % l_total_0 )
    ftotalCost.write("%.0f\n" % l_total_0 )

    while times <= maxStructs :
       print "time\t" + '%.0f' % times;
       lines.append(times);
       m = Model();
       m.loadLines(mFilename, lines);
       (l_total_x, l_model_x, l_error_x, E_x) = L(g,m, errorEnc);
       print "M_x:\t" + '%.0f' % l_total_x + "\t" + '%.0f' % l_model_x + "\t" + '%.0f' % l_error_x + "\t" + str(E_x.numModellingErrors) + '/' + str(E_x.numCellsCovered) + '\t' + str(E_x.numUnmodelledErrors)  + '/' + str(((E_x.numNodes * E_x.numNodes)-E_x.numNodes) - E_x.numCellsCovered) + '\t\t' + str(E_x.numCellsExcluded);
       ftotalCost.write("%.0f\n" % l_total_x )
       times = times + 1; 
       
    ftotalCost.close();
    #return l_total_x;

    #print " -= ", l_total_0 - l_total_x, "\t" + str(l_model_0 - l_model_x), "\t" + str(l_error_0 - l_error_x), "\t" + str(E_0.numModellingErrors - E_x.numModellingErrors), "\t" + str(E_0.numUnmodelledErrors - E_x.numUnmodelledErrors);
    #print " %= ", "%.2f\t\t%.2f\t%.2f\t\t%.2f" % ((l_total_x / l_total_0 * 100), (l_model_x / l_model_0 * 100), (l_error_x / l_error_0 * 100), (E_x.numModellingErrors / E_0.numModellingErrors * 100));

if (len(sys.argv) > 3 and "-pG" in sys.argv) :
    print "Adjacency matrix:";
    g.plot();

if (len(sys.argv) > 3 and "-pC" in sys.argv) :
    print "Cover matrix:";
    E_x.plotCover();

if (len(sys.argv) > 3 and "-pE" in sys.argv) :
    print "Error matrix:";    
    E_x.plotError();

if (len(sys.argv) > 3 and "-lC" in sys.argv) :
    print "Cover list:";
    E_x.listCover();

if (len(sys.argv) > 3 and "-lE" in sys.argv) :
    print "Error list:";    
    E_x.listError();
    
t1 = time()
#print 'function vers1 takes %f' %(t1-t0)
