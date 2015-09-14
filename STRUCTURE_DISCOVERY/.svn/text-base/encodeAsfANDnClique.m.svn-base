function [] = encodeAsfANDnClique( Asmall, curind, top_gccind, out_fid )
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Encode given graph as clique and near-clique                           %
%  Author: Danai Koutra                                                   %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

n = size(curind, 2);
m = nnz(Asmall);

% encode as full clique
fprintf(out_fid, 'fc');
for i=1:size(curind, 2)
    fprintf(out_fid, ' %d', top_gccind( curind(i) ) );
end
fprintf(out_fid, '--- full clique \n');

% encode as near clique
fprintf(out_fid, 'nc %d,', m/2);
for i=1:size(curind, 2)
    fprintf(out_fid, ' %d', top_gccind( curind(i) ) );
end
fprintf(out_fid, '--- nearClique \n');

end