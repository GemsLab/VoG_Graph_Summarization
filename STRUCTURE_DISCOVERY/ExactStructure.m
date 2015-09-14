% Encode the connected component from SlashBurn.
function [ exact_found ] = ExactStructure( Asmall, curind, top_gccind, N_tot, out_fid, info, minSize )

global model;
global model_idx;

% Asmall = B(curind,curind);

exact_found = false;
n = size(curind, 2);
m = nnz(Asmall);

if n==1
    return;
end
%fprintf('n=%d, m=%d\n', n, m);

% cost of encoding the structure as near-clique
MDLcost_nc = compute_encodingCost( 'nc', N_tot, n, Asmall);
% cost of not encoding the structure at all (noise)
cost_notEnc = compute_encodingCost( 'err', 0, 0, [nnz(Asmall) n^2-nnz(Asmall)]);

if ( m == n*n - n )      % full clique
    if n ~= 2
        MDLcost_fc = compute_encodingCost( 'fc', N_tot, n, zeros(n,n));
        costGain = MDLcost_nc - MDLcost_fc;
        costGain_notEnc = cost_notEnc - MDLcost_fc;
        fprintf(out_fid, 'fc');
        for i=1:size(curind, 2)
            fprintf(out_fid, ' %d', top_gccind( curind(i) ) );
        end
        if info == false
            fprintf(out_fid, '\n');
        else
            fprintf(out_fid, ', %f | %f -- exact \n', costGain, costGain_notEnc);
        end
        exact_found = true;
        model_idx = model_idx + 1;
        model(model_idx) = struct('code', 'fc', 'edges', 0, 'nodes1', top_gccind(curind), 'nodes2', [], 'benefit', costGain, 'benefit_notEnc', costGain_notEnc);
        %entries = size(model, 2);
        %model(entries+1) = struct('code', 'fc', 'nodes1', top_gccind(curind), 'nodes2', [], 'benefit', costGain);
    elseif n==2
        MDLcost_ch = compute_encodingCost( 'ch', N_tot, n, zeros(n,n));
        costGain = MDLcost_nc - MDLcost_ch;
        costGain_notEnc = cost_notEnc - MDLcost_ch;
        fprintf(out_fid, 'ch');
        fprintf(out_fid, ' %d', top_gccind( curind(1:2) ));
        if info == false
            fprintf(out_fid, '\n');
        else
            fprintf(out_fid, ', %f | %f -- exact \n', costGain, costGain_notEnc);
        end
        exact_found = true;
        model_idx = model_idx + 1;
        model(model_idx) = struct('code', 'ch', 'edges', 0, 'nodes1', top_gccind(curind), 'nodes2', [], 'benefit', costGain, 'benefit_notEnc', costGain_notEnc);
        %entries = size(model, 2);
        %model(entries+1) = struct('code', 'ch', 'nodes1', top_gccind(curind), 'nodes2', [], 'benefit', costGain);
    end
elseif (m == 2*(n-1))   % chain or star
    degree = sum(Asmall);
    ind = find(degree > 0);
    d1count=0;
    d2count=0;
    dn1count=0;
    
    for i=1:size(degree, 2)
        if( degree(i) == 1 )
            d1count = d1count + 1;
        elseif degree(i) == 2
            d2count = d2count + 1;
        elseif degree(i) == n-1
            dn1count = dn1count + 1;
        end
    end
    
    %fprintf('d1count=%d, d2count=%d, dn1count=%d\n', d1count, d2count, dn1count);
    
    if d1count == 2 && d2count == n-2     % chain
        MDLcost_ch = compute_encodingCost( 'ch', N_tot, n, zeros(n,n));
        costGain = MDLcost_nc - MDLcost_ch;
        costGain_notEnc = cost_notEnc - MDLcost_ch;
        fprintf(out_fid, 'ch');
        d1ind = find( degree == 1);
        fprintf(out_fid, ' %d', top_gccind( curind(d1ind(1)) ) );
        
        d2ind = find(degree==2);
        %for i=1:size(d2ind, 2)
        fprintf(out_fid, ' %d', top_gccind( curind(d2ind(1:size(d2ind, 2))) ) );
        %end
        
        fprintf(out_fid, ' %d', top_gccind( curind(d1ind(2) )) );
        
        if info == false
            fprintf(out_fid, '\n');
        else
            fprintf(out_fid, ', %f | %f -- exact \n', costGain, costGain_notEnc);
        end
        exact_found = true;
        model_idx = model_idx + 1;
        model(model_idx) = struct('code', 'ch', 'edges', 0, 'nodes1', [top_gccind(curind(d1ind(1))) top_gccind(curind(d2ind(1:size(d2ind, 2)))) top_gccind(curind(d1ind(2)))], 'nodes2', [], 'benefit', costGain, 'benefit_notEnc', costGain_notEnc);
        %entries = size(model, 2);
        %model(entries+1) = struct('code', 'ch', 'nodes1', top_gccind(curind), 'nodes2', [], 'benefit', costGain);
        
        %     elseif d1count==n-1 & dn1count==1   % star
        %         fprintf(out_fid, 'st');
        %         dn1ind = find( degree == n-1);
        %         fprintf(out_fid, ' %d,', top_gccind( dn1ind(1) ) );
        %
        %         d1ind = find(degree==2);
        %         for i=1:size(d1ind, 2)
        %             fprintf(out_fid, ' %d', top_gccind( d1ind(i) ) );
        %         end
        %
        %         fprintf(out_fid, '\n');
        %         exact_found = true;
        %     end
        % else            % near clique
        %     fprintf(out_fid, 'nc %d,', m/2);
        %     for i=1:size(curind, 2)
        %         fprintf(out_fid, ' %d', top_gccind( curind(i) ) );
        %     end
        %     fprintf(out_fid, '\n');
    end
else
    %evalmax = eigs( Asmall,1, 'LA' );
    %evalmin = eigs( Asmall,1, 'SA' );
    opts.tol = 1e-2; 
    evals = eigs(Asmall, 2, 'lm', opts); % the eigenvalues with maximum magnitude
    
    if ( max(evals) == - min(evals) )  % bipartite graph (special case: star)
        [ set1, set2 ] = BFScoloring( Asmall );
        if length(set1)+length(set2) < minSize
            exact_found = true;
            return;
        end
        if length(set1) == 1 && length(set2) == 1
            MDLcost_ch = compute_encodingCost( 'ch', N_tot, n, zeros(n,n));
            costGain = MDLcost_nc - MDLcost_ch;
            costGain_notEnc = cost_notEnc - MDLcost_ch;
            fprintf(out_fid, 'ch');
            fprintf(out_fid, ' %d', top_gccind( curind([set1, set2]) ));
            if info == false
                fprintf(out_fid, '\n');
            else
                fprintf(out_fid, ', %f | %f -- exact \n', costGain, costGain_notEnc);
            end
            exact_found = true;
            model_idx = model_idx + 1;
            model(model_idx) = struct('code', 'ch', 'edges', 0, 'nodes1', top_gccind(curind([set1, set2])), 'nodes2', [], 'benefit', costGain, 'benefit_notEnc', costGain_notEnc);
        elseif length(set1) == 1
            MDLcost_st = compute_encodingCost( 'st', N_tot, n, zeros(n,n));
            costGain = MDLcost_nc - MDLcost_st;
            costGain_notEnc = cost_notEnc - MDLcost_st;
            fprintf(out_fid, 'st %d,', top_gccind( curind(set1) ));
            fprintf(out_fid, ' %d', top_gccind( curind(set2) ) );
            if info == false
                fprintf(out_fid, '\n');
            else
                fprintf(out_fid, ', %f | %f -- exact \n', costGain, costGain_notEnc);
            end
            exact_found = true;
            model_idx = model_idx + 1;
            model(model_idx) = struct('code', 'fc', 'edges', 0, 'nodes1', top_gccind(curind), 'nodes2', [], 'benefit', costGain, 'benefit_notEnc', costGain_notEnc);
            %entries = size(model, 2);
            %model(entries+1) = struct('code', 'st', 'nodes1', top_gccind(curind(set1)), 'nodes2', top_gccind(curind(set2)), 'benefit', costGain);
        elseif length(set2) == 1
            MDLcost_st = compute_encodingCost( 'st', N_tot, n, zeros(n,n));
            costGain = MDLcost_nc - MDLcost_st;
            costGain_notEnc = cost_notEnc - MDLcost_st;
            fprintf(out_fid, 'st %d,', top_gccind( curind(set2) ));
            fprintf(out_fid, ' %d', top_gccind( curind(set1) ) );
            if info == false
                fprintf(out_fid, '\n');
            else
                fprintf(out_fid, ', %f | %f -- exact \n', costGain, costGain_notEnc);
            end
            exact_found = true;
            model_idx = model_idx + 1;
            model(model_idx) = struct('code', 'st', 'edges', 0, 'nodes1', top_gccind(curind(set1)), 'nodes2', top_gccind(curind(set1)), 'benefit', costGain, 'benefit_notEnc', costGain_notEnc);
            %entries = size(model, 2);
            %model(entries+1) = struct('code', 'st', 'nodes1', top_gccind(curind(set2)), 'nodes2', top_gccind(curind(set1)), 'benefit', costGain);
        else % bipartite graph
            degrees = sum(Asmall,2);
            % First check if it is bipartite core: The degrees of the nodes
            % in the first set should be equal to the number of nodes in
            % the second set, and vice versa.
            if sum(full(degrees(set1)) ~= length(set2)*ones(length(set1),1)) && ...
                    sum(full(degrees(set2)) ~= length(set1)*ones(length(set2),1)) == 0
                MDLcost_bc = compute_encodingCost( 'bc', N_tot, length(set1), zeros(n,n), length(set2));
                costGain = MDLcost_nc - MDLcost_bc;
                costGain_notEnc = cost_notEnc - MDLcost_bc;
                fprintf(out_fid, 'bc');
                fprintf(out_fid, ' %d', top_gccind( curind(set1) ));
                fprintf(out_fid, ',');
                fprintf(out_fid, ' %d', top_gccind( curind(set2) ) );
                if info == false
                    fprintf(out_fid, '\n');
                else
                    fprintf(out_fid, ', %f | %f -- exact \n', costGain, costGain_notEnc);
                end
                exact_found = true;
                model_idx = model_idx + 1;
                model(model_idx) = struct('code', 'bc', 'edges', 0, 'nodes1', top_gccind(curind(set1)), 'nodes2', top_gccind(curind(set2)), 'benefit', costGain, 'benefit_notEnc', costGain_notEnc);
            else
                % it's not a bipartite core (full bipartite graph) -
                % However, it is a bipartite graph. Let's see if we should
                % encode it as a bipartite core or a near bipartite core.
                MDLcost_bc = compute_encodingCost( 'bc', N_tot, length(set1), zeros(n,n), length(set2));
                MDLcost_nb = compute_encodingCost( 'nb', N_tot, length(set1), zeros(n,n), length(set2));
                if MDLcost_bc <= MDLcost_nb
                    costGain = MDLcost_nc - MDLcost_bc;
                    costGain_notEnc = cost_notEnc - MDLcost_bc;
                    fprintf(out_fid, 'bc');
                    fprintf(out_fid, ' %d', top_gccind( curind(set1) ));
                    fprintf(out_fid, ',');
                    fprintf(out_fid, ' %d', top_gccind( curind(set2) ) );
                    if info == false
                        fprintf(out_fid, '\n');
                    else
                        fprintf(out_fid, ', %f | %f -- not exact \n', costGain, costGain_notEnc);
                    end
                    exact_found = true;
                    model_idx = model_idx + 1;
                    model(model_idx) = struct('code', 'bc', 'edges', 0, 'nodes1', top_gccind(curind(set1)), 'nodes2', top_gccind(curind(set2)), 'benefit', costGain, 'benefit_notEnc', costGain_notEnc);
                else % better to encode it as near-bipartite core
                    costGain = MDLcost_nc - MDLcost_nb;
                    costGain_notEnc = cost_notEnc - MDLcost_nb;
                    fprintf(out_fid, 'nb');
                    fprintf(out_fid, ' %d', top_gccind( curind(set1) ));
                    fprintf(out_fid, ',');
                    fprintf(out_fid, ' %d', top_gccind( curind(set2) ) );
                    if info == false
                        fprintf(out_fid, '\n');
                    else
                        fprintf(out_fid, ', %f | %f -- not exact \n', costGain, costGain_notEnc);
                    end
                    exact_found = true;
                    model_idx = model_idx + 1;
                    model(model_idx) = struct('code', 'nb', 'edges', 0, 'nodes1', top_gccind(curind(set1)), 'nodes2', top_gccind(curind(set2)), 'benefit', costGain, 'benefit_notEnc', costGain_notEnc);
                end
            end
            
            %entries = size(model, 2);
            %model(entries+1) = struct('code', 'bc', 'nodes1', top_gccind(curind(set1)), 'nodes2', top_gccind(curind(set2)), 'benefit', costGain);
        end
        
        
    end
end
end


