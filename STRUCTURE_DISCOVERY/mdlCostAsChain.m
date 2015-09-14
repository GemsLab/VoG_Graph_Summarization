function [ MDLcost, chainExt ] = mdlCostAsChain( Asmall, N_tot )
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Encode given graph as chain                                            %
%  Start from a node with deg 1 (p_rand) and find its furthest node using %
%  BFS. Then, starting from the found node (p_init), redo BFS and find its%
%  furthest node (p_fin). Report the shortest path between p_init and     %
%  p_fin. If there are extra nodes in the shortest path, report them after%
%  the path (separating with comma from the path nodes).                  %
%  DESCRIPTION OF SOME VARS:                                              %
%    E = M xor Asmall, error matrix (xor between true model and adjacency %
%                                                                  mat)   %
%  OUTPUT                                                                 %
%    MDLcost: the cost of encoding Asmall as a chain                      %
%  Author: Danai Koutra                                                   %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

n = size(Asmall, 2);

if n < 3
    return;
end

deg = full(sum(Asmall));
deg1_nodes = find(deg==1);
if isempty( deg1_nodes )
    d = min(deg);
    deg1_nodes = find(deg==d);
end
p_rand = deg1_nodes(1); % pick as n_rand the first node with degree 1

[ p_init, ~, ~ ] = BFS( Asmall, p_rand, false );
[ p_fin, chain, extra_nodes, chainExt, extra_nodesExt ] = ...
                                          BFS( Asmall, p_init, true, true );

%% Creating the adjacency matrix for the chain model 
% it describes the longest chain that we found, w/o noise).
% % M(n,n) = 0;
% % for i = 1 : length(chainExt)-1
% %    M( chainExt(i), chainExt(i+1) ) = 1; 
% %    M( chainExt(i+1), chainExt(i) ) = 1;
% % end
% % % Error matrix
% % %E = xor(M,Asmall);
% % E1 = xor(M,Asmall);
% % 
% % Einc1 = nnz(E1)
% % Eexc1 = sum(E1(:)==0)

% 1s in the error matrix
% missing edges in bc + extra edges within sets
missing = 0;
existing = 0;
for i = 1 : length(chainExt)-1
   if Asmall( chainExt(i), chainExt(i+1) ) == 0
       missing = missing+1;
   else
       existing = existing+1;
   end
end
E(1) = 2* missing + (nnz(Asmall) - 2*existing );
% 0s in the error matrix
E(2) = n^2 - E(1);

fprintf('E(1)=%d, E(2)=%d\n', E(1), E(2));

%% MDL cost of encoding given substructure as a chain
MDLcost = compute_encodingCost( 'ch', N_tot, n, E);

% %% Printing the encoded structure.
% fprintf(out_fid, 'ch ');
% fprintf(out_fid, ' %d', top_gccind( curind(chain) ) );
% if ~isempty(extra_nodes)
%     fprintf(out_fid, ',');
%     fprintf(out_fid, ' %d', top_gccind( curind(extra_nodes) ) );
% end
% fprintf(out_fid, '  --- nearChain \n');
% 
% 
% fprintf(out_fid, 'ch ');
% fprintf(out_fid, ' %d', top_gccind( curind(chainExt) ) );
% %if ~isempty(extra_nodesExt)
% %    fprintf(out_fid, ',');
% %    fprintf(out_fid, ' %d', top_gccind( curind(extra_nodesExt) ) );
% %end
% fprintf(out_fid, '  --- nearChain Extended \n');

    
end
