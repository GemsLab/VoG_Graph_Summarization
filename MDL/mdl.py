import config;
import mdl_base;
import mdl_structs;
import mdl_error;
from copy import deepcopy;

from math import log,factorial;
from error import Error;
from graph import Graph;
from model import Model;

from mdl_base import *;
from mdl_structs import *;
from mdl_error import *;


### Our Encoding Starts Here ###

### Total Encoded Size
def L(G, M, errorEnc): 
    E = Error(G); # initially, everything is error, nothing is covered
    error_cost = 0;
 
   

    model_cost = LN(M.numStructs+1);    # encode number of structures we're encoding with
    model_cost += LwC(M.numStructs, M.numStrucTypes);            # encode the number per structure

    # encode the structure-type identifier per type
    if M.numFullCliques > 0 :
        model_cost += M.numFullCliques * log(M.numFullCliques / float(M.numStructs), 2);
    if M.numNearCliques  > 0 :
        model_cost += M.numNearCliques * log(M.numNearCliques / float(M.numStructs), 2);
    if M.numChains > 0 :
        model_cost += M.numChains * log(M.numChains / float(M.numStructs), 2);
    if M.numStars > 0 :
        model_cost += M.numStars * log(M.numStars / float(M.numStructs), 2);
    # off-diagonals
    if M.numFullOffDiagonals > 0 :
        model_cost += M.numFullOffDiagonals * log(M.numFullOffDiagonals / float(M.numStructs), 2);
    if M.numNearOffDiagonals > 0 :
        model_cost += M.numNearOffDiagonals * log(M.numNearOffDiagonals / float(M.numStructs), 2);
    # bipartite-cores
    if M.numBiPartiteCores > 0 :
        model_cost += M.numBiPartiteCores * log(M.numBiPartiteCores / float(M.numStructs), 2);
    if M.numNearBiPartiteCores > 0 :
        model_cost += M.numNearBiPartiteCores * log(M.numNearBiPartiteCores / float(M.numStructs), 2);
    if M.numJellyFishes > 0 :
        model_cost += M.numJellyFishes * log(M.numJellyFishes / float(M.numStructs), 2);
    if M.numCorePeripheries > 0 :
        model_cost += M.numCorePeripheries * log(M.numCorePeripheries / float(M.numStructs), 2);

    # encode the structures
    for struc in M.structs :
        if struc.isFullClique() :
            model_cost += LfullClique(struc,M,G,E);
        elif struc.isNearClique() :
            model_cost += LnearClique(struc,M,G,E);
        elif struc.isChain() :
            model_cost += Lchain(struc,M,G,E);
        elif struc.isStar() :
            model_cost += Lstar(struc,M,G,E);
        elif struc.isCorePeriphery() :
            model_cost += LcorePeriphery(struc,M,G,E);
        elif struc.isJellyFish() :
            model_cost += LjellyFish(struc,M,G,E);
        elif struc.isBiPartiteCore() :
            model_cost += LbiPartiteCore(struc,M,G,E);
        elif struc.isNearBiPartiteCore() :
            model_cost += LnearBiPartiteCore(struc,M,G,E);
        elif struc.isFullOffDiagonal() :
            model_cost += LfullOffDiagonal(struc,M,G,E);
        elif struc.isNearOffDiagonal() :
            model_cost += LnearOffDiagonal(struc,M,G,E);
    
    # encode the error
    error_cost += 0 if E.numCellsCovered == 0 else log(E.numCellsCovered, 2);    # encode number of additive Errors
    if ((G.numNodes * G.numNodes - G.numNodes) / 2) - E.numCellsCovered > 0 :
        error_cost += log(((G.numNodes * G.numNodes - G.numNodes) / 2) - E.numCellsCovered, 2);    # encode number of Errors
        
    if errorEnc == "NP" :
        error_cost += LErrorNaivePrefix(G,M,E);
    elif errorEnc == "NB" :
        error_cost += LErrorNaiveBinom(G,M,E);
    elif errorEnc == "TP" :
        error_cost += LErrorTypedPrefix(G,M,E);
    elif errorEnc == "TB" :
        error_cost += LErrorTypedBinom(G,M,E);
    
    total_cost = model_cost + error_cost;
    
    return (total_cost, model_cost, error_cost, E);

    
    
### Total Encoded Size for the greedy heuristic -- incrementally update the MDL cost
## for the newly added stucture 'struc'
def Lgreedy(G, M, errorEnc, time, struc, totalCostOld, Eold, model_cost_struct): 
    
    if time == 1:
        E = Error(G); # initially, everything is error, nothing is covered
        #E.saveOld();
        # the cost for encoding each structure (to avoid recomputing it for the greedy updates)
        model_cost2 = 0;
    else :
        E = Error(G, Eold);
        #E.deepish_copy(Eold);
        #E = copy.deepcopy(Eold);
        #E = Eold;
        # the cost for encoding each structure separately 
        # Just update the up-to-now cost by adding the cost of the new structure
        model_cost2 = model_cost_struct;

    error_cost = 0;
    
    model_cost = LN(M.numStructs+1);    # encode number of structures we're encoding with
    model_cost += LwC(M.numStructs, M.numStrucTypes);            # encode the number per structure

    # encode the structure-type identifier per type
    if M.numFullCliques > 0 :
        model_cost += M.numFullCliques * log(M.numFullCliques / float(M.numStructs), 2);
    if M.numNearCliques  > 0 :
        model_cost += M.numNearCliques * log(M.numNearCliques / float(M.numStructs), 2);
    if M.numChains > 0 :
        model_cost += M.numChains * log(M.numChains / float(M.numStructs), 2);
    if M.numStars > 0 :
        model_cost += M.numStars * log(M.numStars / float(M.numStructs), 2);
    # off-diagonals
    if M.numFullOffDiagonals > 0 :
        model_cost += M.numFullOffDiagonals * log(M.numFullOffDiagonals / float(M.numStructs), 2);
    if M.numNearOffDiagonals > 0 :
        model_cost += M.numNearOffDiagonals * log(M.numNearOffDiagonals / float(M.numStructs), 2);
    # bipartite-cores
    if M.numBiPartiteCores > 0 :
        model_cost += M.numBiPartiteCores * log(M.numBiPartiteCores / float(M.numStructs), 2);
    if M.numNearBiPartiteCores > 0 :
        model_cost += M.numNearBiPartiteCores * log(M.numNearBiPartiteCores / float(M.numStructs), 2);
    if M.numJellyFishes > 0 :
        model_cost += M.numJellyFishes * log(M.numJellyFishes / float(M.numStructs), 2);
    if M.numCorePeripheries > 0 :
        model_cost += M.numCorePeripheries * log(M.numCorePeripheries / float(M.numStructs), 2);

    # encode the structures
    if struc.isFullClique() :
        model_cost2 += LfullClique(struc,M,G,E);
    elif struc.isNearClique() :
        model_cost2 += LnearClique(struc,M,G,E);
    elif struc.isChain() :
        model_cost2 += Lchain(struc,M,G,E);
    elif struc.isStar() :
        model_cost2 += Lstar(struc,M,G,E);
    elif struc.isCorePeriphery() :
        model_cost2 += LcorePeriphery(struc,M,G,E);
    elif struc.isJellyFish() :
        model_cost2 += LjellyFish(struc,M,G,E);
    elif struc.isBiPartiteCore() :
        model_cost2 += LbiPartiteCore(struc,M,G,E);
    elif struc.isNearBiPartiteCore() :
        model_cost2 += LnearBiPartiteCore(struc,M,G,E);
    elif struc.isFullOffDiagonal() :
        model_cost2 += LfullOffDiagonal(struc,M,G,E);
    elif struc.isNearOffDiagonal() :
        model_cost2 += LnearOffDiagonal(struc,M,G,E);
    
    # encode the error
    error_cost += 0 if E.numCellsCovered == 0 else log(E.numCellsCovered, 2);    # encode number of additive Errors
    if ((G.numNodes * G.numNodes - G.numNodes) / 2) - E.numCellsCovered > 0 :
        error_cost += log(((G.numNodes * G.numNodes - G.numNodes) / 2) - E.numCellsCovered, 2);    # encode number of Errors
 
    if errorEnc == "NP" :
        error_cost += LErrorNaivePrefix(G,M,E);
    elif errorEnc == "NB" :
        error_cost += LErrorNaiveBinom(G,M,E);
    elif errorEnc == "TP" :
        error_cost += LErrorTypedPrefix(G,M,E);
    elif errorEnc == "TB" :
        error_cost += LErrorTypedBinom(G,M,E);
    
    total_cost = model_cost + model_cost2 + error_cost;
    model_cost_total = model_cost + model_cost2;    

    return (total_cost, model_cost_total, model_cost2, error_cost, E);

    
    
    
    
