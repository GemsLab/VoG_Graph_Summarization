function [ MDLcost ] = compute_encodingCost( subgraph, N_tot, n_sub, E, n_sub2, nb_edges, ca)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Computation of the local encoding cost of a given substructure:        %
%   INPUTS:                                                               %
%   subgraph: 'fc', 'nc', 'st', 'ch', 'bc', 'err'                               %
%   N_tot:  total number of nodes in the whole graph                      %
%   n_sub: number of nodes in the given substructure OR number of nodes   %
%           in the first set of a 'bc' (k)                                %
%   E         : error matrix                                              %
%   n_sub2:   optional - number of nodes in the second set of a 'bc' (l)  %
%   nb_edges:   optional -  edges *between* the two sets of               %
%                        the near-bipartite core                          %
%   ca:       true if cross-association is used (encoding of nc)          %
%  ---------------                                                        %
%  OUTPUTS:                                                               %
%   MDLcost = model_cost + error cost                                     %
%  Author: Danai Koutra                                                   %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if nargin < 7
    ca = false;
end

test_error_edges(E);

switch subgraph
    case 'fc'
        if E(1) == 0 || E(2) == 0 % no excluded edges
            MDLcost = LN( n_sub ) + log2( nchoosek(vpi(N_tot), n_sub) );
        else
            MDLcost = LN( n_sub ) + log2( nchoosek(vpi(N_tot), n_sub) ) + Lnu_opt( E );
        end
    case 'nc'
        % for the near clique: E is the Asmall matrix
        edges_inc = nnz(E);
        if ca == true % cross-association for bipartite graph (rectangular mat)
            edges_exc = size(E,1)*size(E,2)-nnz(E);%sum(E(:)==0); % computing the mdl cost of a bipartite graph encoded as near clique
        else
            edges_exc = size(E,1)*size(E,2)-nnz(E);%sum(E(:)==0)-n_sub; % diagonal elements are always 0 (no self-loops)
        end
        if edges_exc ~= 0 && edges_inc ~= 0
            MDLcost = LN( n_sub ) + log2(nchoosek(vpi(N_tot), n_sub)) + ...
                log2( n_sub^2 ) + edges_inc * NLL( edges_inc, edges_exc, 1) + ...
                edges_exc * NLL( edges_inc, edges_exc, 0);
        else
            MDLcost = LN( n_sub ) + log2(nchoosek(vpi(N_tot), n_sub));
        end
    case 'st'
        if E(1) == 0 || E(2) == 0 %if sum(sum(E)) == 0
            MDLcost = LN( n_sub-1 ) + log2( N_tot ) + log2( nchoosek( vpi(N_tot-1), n_sub-1 ) );
        else
            MDLcost = LN( n_sub-1 ) + log2( N_tot ) + ...
                log2( nchoosek( vpi(N_tot-1), n_sub-1 ) ) + Lnu_opt( E );
        end
    case 'ch'
        x = 0:(n_sub-1);
        N_tot_vec = N_tot * ones(1, n_sub);
        if E(1) == 0 || E(2) == 0 %if sum(sum(E)) == 0
            MDLcost = LN( n_sub-1 ) + sum( log2(N_tot_vec - x) );
        else
            MDLcost =  LN( n_sub-1 ) + sum( log2(N_tot_vec - x) ) + Lnu_opt( E );
        end
    case 'bc'
        k = n_sub;
        l = n_sub2;
        if E(1) == 0 || E(2) == 0 %if sum(sum(E)) == 0
            MDLcost = LN(k) + LN(l) + log2( nchoosek(vpi(N_tot), k) ) + log2( nchoosek(vpi(N_tot-k), l) );
        else
            MDLcost = LN(k) + LN(l) + log2( nchoosek(vpi(N_tot), k) ) + ...
                log2( nchoosek(vpi(N_tot-k), l) ) + Lnu_opt( E );
        end
    case 'nb'
        k = n_sub;
        l = n_sub2;
        if E(1) == 0 || strcmp('ca', true) || E(2) == 0 %if sum(sum(E)) == 0
            MDLcost = LN(k) + LN(l) + log2( nchoosek(vpi(N_tot), k) ) + log2( nchoosek(vpi(N_tot-k), l) );
        else
            % The error matrix E has only the edges *within* the two sets
            % of nodes.
            edges_inc = nb_edges(1); %nnz(nb_mat);
            edges_exc = nb_edges(2); %2*k*l - edges_inc; % the bipartite core model has 2*k*l edges (all the edges between the two sets of nodes - counting them 2 times, because the adjacency matrix is symmetric)
            if edges_inc == 0 || edges_exc == 0
                MDLcost = LN(k) + LN(l) + log2( nchoosek(vpi(N_tot), k) ) + ...
                    log2( nchoosek(vpi(N_tot-k), l) ) + Lnu_opt( E);
            else
                MDLcost = LN(k) + LN(l) + log2( nchoosek(vpi(N_tot), k) ) + ...
                    log2( nchoosek(vpi(N_tot-k), l) ) + log2( n_sub^2 ) + ...
                    edges_inc * NLL( edges_inc, edges_exc, 1) + ...
                    edges_exc * NLL( edges_inc, edges_exc, 0) + Lnu_opt( E );
                
            end
        end
    case 'err'
        if E(1) ~= 0 && E(2) ~= 0
            MDLcost = Lnu_opt( E );
        elseif E(1) ~= 0 
            MDLcost = LN( E(1) );
        elseif E(2) ~= 0
            MDLcost = LN( E(2) );
        end
    otherwise
        error_message = 'error: invalid structure...\n'
end

testMDLcost(MDLcost);

%% encoded size of an integer >=1 as by Rissanen's 1983 Universal code for integers
    function [ c ] = LN( n )
        c0 = 2.865064;
        c = log2(c0);
        logTerm = log2(n);
        while logTerm > 0
            c = c + logTerm;
            logTerm = log2(logTerm);
        end
    end

%% error per structure: Naive Uniform
    function [ c_err ] = Lnu( E )
        Einc = nnz(E);
        Eexc = sum(E(:)==0);
        c_err = LN( Einc ) + ...
            Einc * NLL( Einc, Eexc, 1) + ...
            Eexc * NLL( Einc, Eexc, 0);
    end

%% error per full clique: Naive Uniform
    function [ c_err ] = Lnu_opt( E )
        % E has two entries: # of included edges, # of excluded edges
        Einc = E(1);
        Eexc = E(2);
        c_err = LN( Einc ) + ...
            Einc * NLL( Einc, Eexc, 1) + ...
            Eexc * NLL( Einc, Eexc, 0);
    end


%% Alternative error per structure: Naive Data-to-Model
    function [ c_err ] = Lnd( E )
        Einc = nnz(E);
        c_err = LN( Einc ) + log2( nchoosek(vpi(N_tot^2), Einc) );
    end


%% Alternative error per structure: Naive Data-to-Model
    function [ c_err ] = Lnd_opt( E )
        Einc = E(1);
        c_err = LN( Einc ) + log2( nchoosek(vpi(N_tot^2), Einc) );
    end

%% Negative log-likelihood
% If sub = 0: p0 = -log2(excl / (incl + excl))
% if sub = 1: p1 = -log2(incl / (incl + excl))
    function [ l ] = NLL( incl, excl, sub )
        if sub == 0
            l = -log2(excl / (incl + excl));
        elseif sub == 1
            l = -log2(incl / (incl + excl));
        else
            err = 'error... Can only compute l0 ot l1 (negative log-likelihood)'
        end
    end

end

