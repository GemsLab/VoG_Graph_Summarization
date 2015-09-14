function [ ] = encodeAsBC( curind, top_gccind, set1, set2, costGain, costGain_notEnc, out_fid, info )
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Print the encoding of the given graph as bipartite core                %
%   Output is stored in the model file in the form:                       %
%     bc node_ids_of_1st_set, node_ids_of_2nd_set, costGain               %
%  Author: Danai Koutra                                                   %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
global model; 
global model_idx;

if ~isempty(set1) && ~isempty(set2)
    fprintf(out_fid, 'bc');
    fprintf(out_fid, ' %d', top_gccind( curind(set1) ));
    fprintf(out_fid, ',');
    fprintf(out_fid, ' %d', top_gccind( curind(set2) ) );
    if info == false
            fprintf(out_fid, '\n');
        else
            fprintf(out_fid, ', %f | %f------ nearBC \n', costGain, costGain_notEnc);
    end
end

model_idx = model_idx + 1;
model(model_idx) = struct('code', 'bc', 'edges', 0, 'nodes1', top_gccind(curind(set1)), 'nodes2', top_gccind(curind(set2)), 'benefit', costGain, 'benefit_notEnc', costGain_notEnc);
         
%model(n+1) = struct('code', 'bc', 'nodes1', top_gccind(curind(set1)), 'nodes2', top_gccind(curind(set2)), 'benefit', costGain);
    
end