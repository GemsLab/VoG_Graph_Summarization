#!/usr/local/bin/python2.6

#########################################################################
#                                                                       #
# Implementation of the GreedyNForget heuristic described in the paper  #
# VOG: Summarizing and Understanding Large Graphs                       #
# by Danai Koutra, U Kang, Jilles Vreeken, Christos Faloutsos           #
# http://www.cs.cmu.edu/~dkoutra/papers/VoG.pdf                         #
#                                                                       #
# v1.1: faster implementation using dynamic programming and the         #
#       technique of memoization. Now, we can add to the summary many   #
#       more structures much faster (structLim = 10000+)                #
#                                                                       #
# v1: very slow, naive implementation, computing the MDL encoding cost  #
#     from scratch for each structure addition (structLim = 200)        #
#                                                                       #
#########################################################################


import sys
import os
import config
import copy

from time import time

from mdl import *;
from error import Error;
from graph import Graph;
from model import *;
from random import shuffle;
#from description_length import *;

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
    print "Number of structures in the model: %.0f" % m.numStructs;
    if config.optVerbosity > 1 : print "- M_x loaded."
    (l_total_x, l_model_x, l_error_x, E_x) = L(g,m, errorEnc);
    print "M_x:\t" + '%.0f' % l_total_x + "\t" + '%.0f' % l_model_x + "\t" + '%.0f' % l_error_x + "\t" + str(E_x.numModellingErrors) + '/' + str(E_x.numCellsCovered) + '\t' + str(E_x.numUnmodelledErrors)  + '/' + str(((E_x.numNodes * E_x.numNodes)-E_x.numNodes) - E_x.numCellsCovered) + '\t\t' + str(E_x.numCellsExcluded);
    
    # reinitialize the model for the greedy approach
    m = Model();

    # maximum number of structures considered
    structLim = 10000;
    # read maxStructs structures from the model file and save it in modelContent
    mHandle = open(mFilename, 'r')
    mContent = mHandle.readlines();  #(structLim);
#    print mContent[0]
#    print "length of model file: %.0f" % len(mContent);
    maxStructs = len(mContent);
#    print "length of model file: %.0f" % maxStructs;
    lines_all = [];
#    shuffle(mContent);
#    print mContent[0];

    l_total_prev = l_total_0;
    # the encoding costper structure is 0 initially
    lmodel_struct_prev = 0;
    E_x = E_0; 
    E_x_old = E_0;
    structsInSummary = [];
    times = 1;
    
    mFilename_list = mFilename.split('/');
    mFilename_main = mFilename_list[len(mFilename_list) - 1];
    print '%s' % mFilename_main
    mFilenameGreedy = 'heuristicSelection_nStop_ALL_' + mFilename_main;
    fgreedy = open(mFilenameGreedy,'w')
    mFilenameGreedyCost = 'heuristic_Selection_costs_ALL_' + mFilename_main;
    fgreedyCost = open(mFilenameGreedyCost,'w')

    fgreedyCost.write("l_total_0: %.0f\n" % l_total_0 )

    # number of structures in the summary
    kept_struct = 0;

    while times <= maxStructs : #min(structLim, maxStructs) :  # add upto structLim structures or as many as there are in the model file  
       print "time\t" + '%.0f' % times;
       # add to the model the new structure
       newStruct = m.loadLine(mContent, times-1);
       (l_total_x, l_model_x, l_model_struct, l_error_x, E_x) = Lgreedy(g, m, errorEnc, times, newStruct, l_total_prev, E_x_old, lmodel_struct_prev);
       print "M_x:\t" + '%.0f' % l_total_x + "\t" + '%.0f' % l_model_x + "\t" + '%.0f' % l_error_x + "\t" + str(E_x.numModellingErrors) + '/' + str(E_x.numCellsCovered) + '\t' + str(E_x.numUnmodelledErrors)  + '/' + str(((E_x.numNodes * E_x.numNodes)-E_x.numNodes) - E_x.numCellsCovered) + '\t\t' + str(E_x.numCellsExcluded);
       # print "l_total_x %.0f" % l_total_x + "l_total_prev %.0f" % l_total_prev;
       if l_total_x > l_total_prev :
          print "dropped the structure";
          l_total_x = l_total_prev;
	  # remove the last added structure
          # print "structs in model %.0f " % m.numStructs;
          m.rmStructure(newStruct);
          # print "structs in model %.0f " % m.numStructs;
          #E_x = copy.deepcopy(); #E_x.recoverOld(); 
          print "-----------------------------------------------------------"
       else : 
          # print "kept the structure";
          kept_struct += 1;
          # print "structs in model %.0f " % m.numStructs;
          # save the Error matrix to this point
          #E_x.saveOld();
          #E_x_old = copy.deepcopy(E_x);
          E_x_old = E_x; 
          #E_x_old = Error(g);
          #E_x_old.deepish_copy(E_x, g);
          
          l_total_prev = l_total_x;
          # update the up-to-now cost per structure
          lmodel_struct_prev = l_model_struct;
          structsInSummary.append(times);
          fgreedyCost.write("Time %.0f" % times + "\t%.0f\n" % l_total_x )
          print "-----------------------------------------------------------"
          if kept_struct == structLim :
             break;
       if times == 50 or times % 100 == 0 :
          mFilenameGreedyTemp = 'greedySelection_' + str(times) + '_' + mFilename_main;
          fgreedyTemp = open(mFilenameGreedyTemp, 'w');
          fgreedyTemp.write("Structures of model in the summary (each number is the corresponding line number of the structure in the model file)\n");
          for line in structsInSummary:
              # fgreedyTemp.write("%s" % line + "\t%s" % mContent[line]);
              fgreedyTemp.write("%s\n" % line);
       times += 1; 
	
    print "structs in model %.0f " % m.numStructs;

    for line in structsInSummary:
       fgreedy.write("%s\n" % line)
    
    fgreedy.close();
    fgreedyCost.close();


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

print time()-t0    
print "Total running time %.2f" % (time()-t0);

mHandle.close()
