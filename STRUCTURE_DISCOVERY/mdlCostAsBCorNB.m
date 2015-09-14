function [ MDLcostBC, MDLcostNB, set1, set2 ] = mdlCostAsBCorNB( Asmall, N_tot )
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Encode given graph as bipartite core                                   %
%  max cut problem --> NP hard                                            %
% Heuristic: we use FaBP with heterophily and we initialize               %
%            two nodes that are connected by an edge in opposite classes  %
%  Author: Danai Koutra                                                   %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% Constants and variables of FaBP
% heterophily factor
h = -0.01;
% prior belief for belonging in the pos/neg class
positive = 0.01;
negative = -0.01;

a = 4*h^2/(1-4*h^2);
c = 2*h/(1-4*h^2);

%% setting up the matrices and vectors involved in FaBP
n = size(Asmall, 2);
deg = full(sum(Asmall));
%D = diag(deg);
D = spdiags(deg', 0, n, n);
matI = speye(n);

%% Initialization: pick high degree node, and initialize as positive.
% Set all its neighbors in the opposite class.
phi = zeros(n,1);
[ ~, idx ] = max(deg);
neighbors = find(Asmall(idx,:));
phi(idx) = positive;
phi(neighbors) = negative;

%% FaBP: main equation
b = ( matI + a * D - c * Asmall ) \ phi;

%% Find the members of the two sets
set1 = b > 0;
set2 = b < 0;

%% Creating the adjacency matrix for the bc model (w/o noise).
% According to this model, all the nodes in set1 are connected to all the
% nodes in set2.
% % M(n,n) = 0;
% % M( set1, set2 ) = 1;
% % % M should be symmetric
% % M( set2, set1 ) = 1;
% % % Error matrix
% % %E = xor(M,Asmall);
% % E1 = xor(M,Asmall);
% % 
% % Einc1 = nnz(E1)
% % Eexc1 = sum(E1(:)==0)

% 1s in the error matrix
% missing edges in bc + extra edges within sets
E(1) = 2* (sum(set1)*sum(set2)-nnz(Asmall(set1,set2))) + nnz(Asmall(set1, set1)) + nnz(Asmall(set2, set2));
% 0s in the error matrix
E(2) = n^2 - E(1);

%% MDL cost of encoding given substructure as a bipartite core
MDLcostBC = compute_encodingCost( 'bc', N_tot, sum(set1), E, sum(set2) );

%% Creating the adjacency matrix for the nb model (w/o noise).
% % % According to this model, some nodes in set1 are connected to some of the
% % % nodes in set2.
% % M(n,n) = 0;
% % B(n,n) = 0;
% % B(set1, set2) = Asmall(set1, set2);
% % M = B + B';
% % % Error matrix
% % E1 = xor(M,Asmall);
% % 
% % Einc1 = nnz(E1)
% % Eexc1 = sum(E1(:)==0)

% 1s in the error matrix
% extra edges within sets
E(1) = nnz(Asmall(set1, set1)) + nnz(Asmall(set2, set2));
% 0s in the error matrix
E(2) = n^2 - E(1);

%% MDL cost of encoding given substructure as a bipartite core
MDLcostNB = compute_encodingCost( 'nb', N_tot, sum(set1), E, sum(set2), [nnz(Asmall(set1,set2)), sum(set1)*sum(set2)-nnz(Asmall(set1,set2))] );

% % if nargin == 4 && ~isempty(set1) && ~isempty(set2)
% %     fprintf(out_fid, 'bc');
% %     fprintf(out_fid, ' %d', top_gccind( curind(set1) ));
% %     fprintf(out_fid, ',');
% %     fprintf(out_fid, ' %d', top_gccind( curind(set2) ) );
% %     fprintf(out_fid, ' --- nearBC \n');
% % end
    
end