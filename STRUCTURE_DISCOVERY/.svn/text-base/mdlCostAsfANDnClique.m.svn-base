function [ MDLcost_fc, MDLcost_nc ] = mdlCostAsfANDnClique( Asmall, N_tot )
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Encode given graph as clique and near-clique                           %
%  Author: Danai Koutra                                                   %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

n = size(Asmall, 2);

%% Creating the adjacency matrix for the clique model (w/o noise).
% Note that there is no Error matrix for the near-clique model.
%M = ones(n,n) - eye(n);
% Error matrix.
%E1 = xor(M,Asmall);

% 0s in the error matrix  --- edges included in the structure (full clique)
E(2) = nnz(Asmall);
% 1s in the error matrix  --- edges excluded from the structure (full clique)
E(1) = n^2 - n - E(2);

%% MDL cost of encoding given substructure as a full clique
MDLcost_fc = compute_encodingCost( 'fc', N_tot, n, E);
%% MDL cost of encoding given substructure as a near clique
MDLcost_nc = compute_encodingCost( 'nc', N_tot, n, Asmall);


% % %% Printing the encoded structure.
% % % encode as full clique
% % fprintf(out_fid, 'fc');
% % for i=1:size(curind, 2)
% %     fprintf(out_fid, ' %d', top_gccind( curind(i) ) );
% % end
% % fprintf(out_fid, '--- full clique \n');
% % 
% % % encode as near clique
% % fprintf(out_fid, 'nc %d,', m/2);
% % for i=1:size(curind, 2)
% %     fprintf(out_fid, ' %d', top_gccind( curind(i) ) );
% % end
% % fprintf(out_fid, '--- nearClique \n');

end