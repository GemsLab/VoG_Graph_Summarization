%  Author: Danai Koutra
%  Adaptation and extension of U Kang's code for SlashBurn 
%   (http://www.cs.cmu.edu/~ukang/papers/sb_icdm2011.pdf)
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                                                           %
% SlashBurn Encode: encode graph using SlashBurn                            %
%                                                                           %
% Parameter                                                                 %
%   AOrig : adjacency matrix of a graph. We assume symmetric matrix with    %
%           both upper- and lower- diagonal elements are set.               %
%   k : # of nodes to cut in SlashBurn                                      %
%   outfile : file name to output the model                                 %
%   info : true for detailed output (encoding gain reported)                %
%          false for brief output (no encoding gain reported)               %
%   starOption: true for encoding the vicinities of top degree nodes as     %
%                     stars                                                 %
%               false for encoding these vicinities as stars, nc or fc      %
%               (depending on the smallest mdl cost)                        %
%   minSize: minimum size of structure that we want to encode               %
%   graphFile: path to the edge file                                        %
%                                                                           %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function [ ] = SlashBurnEncode(AOrig, k, outFolder, info, starOption, minSize, graphFile )

%addpath('./VariablePrecisionIntegers/VariablePrecisionIntegers');

%% Definition of global variables:
%  model:
global model;
global model_idx;

dir=0;
% cost of encoding all the structures
cost_ALLencoded_struct = 0;
% if greedy is selected, all_costs has all the costs by adding one extra
% structure for encoding
all_costs = 0;

%if nargin < 3
%    info = false;
%end
[~, fname, ~] = fileparts(graphFile);
allOutFile = sprintf('%s/%s_ALL.model', outFolder, fname);
outfile_ordered = sprintf('%s/%s_orderedALL.model', outFolder, fname);
% Open 'outfile' for writing
out_fid = fopen(allOutFile, 'w');

% Initialize variables
gccsize = zeros(0,0);
niter=0;
n = max(size(AOrig,1),size(AOrig,2));
AOrig(n,n)=0;
totalind = zeros(1,n);
cur_lpos = 1;
cur_rpos = n;
gccind = [1:n];
cur_gccsize = n;
total_SB_stars = 0;
encoded_SB_stars = 0;
total_cost = 0;

if info == true
    info = false
    changingYourOption = 'Setting info to false, so that we can compute the encoding cost of all the found structures'
end

tic 

while niter == 0 || cur_gccsize > k
    niter = niter+1;
    fprintf('Iteration %d...\n', niter);
    
    A = AOrig(gccind,gccind);
    [disind,newgccind,topind] = RemHdegreeGccEncode(A, k, dir, out_fid, gccind, n, info, minSize);
    % save 'star' structures
    star_cores = topind;
    for i=1:size(star_cores, 2)
        E = zeros(1,2);
        cur_center = star_cores(i);
        
        satellites = find(A(cur_center, :)>0);
        
        % If the structure has less than minSize nodes, do not report it in the
        % model file
        if length(satellites) < minSize
            continue;
        end
        
        n_star = length(satellites) + 1;
        Asmall = A([cur_center, satellites],[cur_center, satellites]);
        MDLcostNC = compute_encodingCost( 'nc', n, n_star, Asmall);
        % 1s in the error matrix
        % missing edges in star + extra edges not in star
        E(1) = 2* (n_star-1-nnz(A(cur_center,satellites))) + nnz(A(satellites, satellites));
        % 0s in the error matrix
        E(2) = n_star^2 - E(1);
        
        cost_notEnc = compute_encodingCost( 'err', 0, 0, [nnz(Asmall) n_star^2-nnz(Asmall)]);
        
        test_error_edges(E);
        
        % MDL cost of encoding given substructure as a star
        MDLcostST = compute_encodingCost( 'st', n, n_star, E);
        total_SB_stars = total_SB_stars + 1;
        
        if isinf(MDLcostNC) || isinf(MDLcostST)
            costGain = 0;
            costGain_notEnc = 0;
        else
            costGain = MDLcostNC - MDLcostST;
            costGain_notEnc = cost_notEnc - MDLcostST;
        end
        
        % encode the vicinities of high-deg nodes as stars
        if starOption == true
            fprintf( out_fid, 'st %d,', gccind(cur_center));
            fprintf( out_fid, ' %d', gccind(satellites) );
            encoded_SB_stars = encoded_SB_stars + 1;
            
            
            if info == false
                fprintf( out_fid, '\n');
            else
                fprintf( out_fid, ', %f | %f -- SB \n', costGain, costGain_notEnc);
            end
            model_idx = model_idx + 1;
            model(model_idx) = struct('code', 'st', 'edges', 0, 'nodes1', gccind(cur_center), 'nodes2', gccind(satellites), 'benefit', costGain, 'benefit_notEnc', costGain_notEnc);
            % check which of the structures is best for encoding: star, fc, nc
        elseif starOption == false
            % 0s in the error matrix  --- edges included in the structure (full clique)
            E(2) = nnz(Asmall);
            % 1s in the error matrix  --- edges excluded from the structure (full clique)
            E(1) = n_star^2 - n_star - E(2);
            
            % MDL cost of encoding given substructure as a full clique
            MDLcostFC = compute_encodingCost( 'fc', n, n_star, E);
            MDLcosts = [ MDLcostFC, MDLcostNC, MDLcostST ];
            [minCost minIdx] = min(MDLcosts);
            top_gccind = sort([gccind(cur_center), gccind(satellites)]);
            curind = 1:size(top_gccind,2);
            switch minIdx
                case 1
                    costGain = MDLcostNC - MDLcostFC;
                    costGain_notEnc = cost_notEnc - MDLcostFC;
                    encodeAsFClique( curind, top_gccind, costGain, costGain_notEnc, out_fid, info );
                case 2
                    costGain = MDLcostNC - MDLcostNC;
                    costGain_notEnc = cost_notEnc - MDLcostNC;
                    m = nnz(Asmall);
                    encodeAsNClique( curind, top_gccind, m, costGain, costGain_notEnc, out_fid, info );
                case 3
                    fprintf( out_fid, 'st %d,', gccind(cur_center));
                    for j=1:size(satellites,2)
                        fprintf( out_fid, ' %d', gccind(satellites(j)) );
                    end
                    
                    if info == false
                        fprintf( out_fid, '\n');
                    else
                        fprintf( out_fid, ', %f | %f -- SB \n', costGain, costGain_notEnc);
                    end
                    model_idx = model_idx + 1;
                    model(model_idx) = struct('code', 'st', 'edges', 0, 'nodes1', gccind(cur_center), 'nodes2', gccind(satellites), 'benefit', costGain, 'benefit_notEnc', costGain_notEnc);
                    encoded_SB_stars = encoded_SB_stars + 1;
            end
            
        else
            wrongMessage = 'starOption should be true or false. Invalid value given.'
            return
        end
    end
    
    % save structures on the disconnected components
    
    % reorganize the matrix
    topind_size = size(topind, 2);
    
    totalind(cur_lpos:cur_lpos + topind_size - 1) = gccind(topind);
    cur_lpos = cur_lpos + topind_size;
    totalind(cur_rpos - size(disind,2) + 1:cur_rpos) = gccind(disind);
    cur_rpos = cur_rpos - size(disind,2);
    
    gccind = gccind(newgccind);
    cur_gccsize = size(gccind, 2);
    
end

if k > 1 && cur_gccsize >= 2
    EncodeSubgraph(AOrig(gccind,gccind), [1:size(gccind,2)], gccind, n, out_fid, info, minSize);
end

%% Selection of structures:
% Method 1: top 10
% Method 2: greedy selection


[~, order] = sort([model(:).benefit_notEnc], 'descend');
model_ordered = model(order);
printModel(model_ordered, outfile_ordered);
all_costs = 0;
all_costs_incStruct = 0;

runtime = toc
time_stored = sprintf('%s/%s_runtime.txt', outFolder, fname);
save(time_stored, 'runtime', '-ascii');

disp('=== Graph decomposition and structure labeling: finished! ===')

fclose(out_fid);

end
