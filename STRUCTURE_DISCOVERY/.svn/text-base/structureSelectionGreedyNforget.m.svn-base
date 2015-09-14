function [ cost_noModel historyCosts historyCostsInc] = structureSelectionGreedyNforget(A, graphFile, model_ordered, cost_ALLencoded_struct, outfile)
%% Select the substructures to output to the user.
% The ranking of the substructures is based on their MDL benefit. Add one
% substructure at a time and compute the mdl cost of encoding the whole
% graph. If the MDL cost starts increasing, stop adding more structures.
%
% Inputs:
%    A: adjacency matrix of the whole graph
%    graphFile: edge file of the input graph (csv file, without weights)
%               if 'none', create the edge file from matrix A
%    model_ordered: the substructures ordered in decreasing mdl benefit
%    final_fid: the model file with the substructures (until the current
%               step)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

cost = zeros(1,2);

if strcmp(graphFile, 'none')
    %% Creation of graph from adjacency matrix (may skip if already have the
    %% file)
    [~, fname, ~] = fileparts(outfile);
    graphFile = sprintf('%s.graph', fname)
    [i j k] = find( A );
    graph_fid = fopen( graph_name, 'w' );
    fprintf( graph_fid, '%d,%d\n', i, j );
    fclose( graph_fid );
end

% currentDirectory = pwd
% [~, deepestFolder, ~] = fileparts(currentDirectory)

fid = fopen(outfile, 'w');

comm = sprintf('python2.6 ../mdl/score.py %s > pythonOutput.txt;', graphFile )
system( comm )

pythonOutput = importdata('pythonOutput.txt');
% Initial cost: the MDL cost of the Empty Model.
cost(1) = str2num(pythonOutput.textdata{2,2});
cost_noModel = cost(1);
cost(2) = cost(1);

cnt = 0;
historyCosts(cnt+1) = cost(1);
historyCostsInc(cnt+1) = cost(1);

consecutiveInc = 0;
cnt_structsInc = 0;

[~,graphname,~] = fileparts(graphFile);


while cnt < length(model_ordered) || historyCostsInc(cnt_structsInc+1) > cost_ALLencoded_struct %cnt < length(model_ordered) && historyCosts(cnt+1) > cost_ALLencoded_struct  && consecutiveInc ~= 5 %cost(2) <= cost(1)
    cnt = cnt + 1;
    if mod(cnt,10) == 0 
        cnt
    end
    cost(1) = cost(2);
    printStructureToModelFile(model_ordered(cnt), fid);
    comm = sprintf('time -p python2.6 ../mdl/score.py %s %s > pythonOutput.txt;', ...
                    graphFile, outfile );
    %comm = sprintf('cd ../mdl; python score.py ../%s/%s ../%s/%s > ../%s/pythonOutput.txt; cd ../%s', ...
    %    deepestFolder, graph_name, deepestFolder, outfile, deepestFolder, deepestFolder )
    system(comm);
    pythonOutput = importdata('pythonOutput.txt');
    cost(2) = str2num(pythonOutput.textdata{3,2});
    historyCosts(cnt+1) = cost(2);
    % removing the structure that caused the increase in the encoding cost
    if cost(2) > cost(1)
        fclose(fid);
        fid = fopen(outfile, 'a');
        %comm = sprintf('cp %s tmp', outfile);
        comm = sprintf('head -n %d %s > tmp; cp tmp %s', cnt_structsInc, outfile, outfile);
        system(comm);
        %comm = sprintf('sed "N;$!P;$!D;$d" < tmp > %s; rm tmp', outfile);
        %system(comm);
        % update the cost to its last value
        cost(2) = historyCostsInc(cnt_structsInc+1);
    else
        cnt_structsInc = cnt_structsInc + 1;
        historyCostsInc(cnt_structsInc+1) = cost(2);
    end
   cnm=sprintf('%s_cost_nomodel_gnf', graphname);
   save(cnm, 'cost_noModel')
   cnm=sprintf('%s_all_costs_gnf', graphname);
   save(cnm, 'historyCosts')
   cnm=sprintf('%s_all_costs_incStruct_gnf', graphname);
   save(cnm, 'historyCostsInc')

end

fclose(fid);

% remove the structure at the last line, since it caused increase in the
% MDL encoding cost.
% comm = sprintf('cp %s tmp', outfile);
% system(comm);
% if consecutiveInc == 2
%     comm = sprintf('sed "N;$!P;$!D;$d" < tmp > %s; rm tmp', outfile);
%     system(comm);
%     comm = sprintf('sed "$d" < %s > tmp; cp tmp %s; rm tmp', outfile, outfile);
% else
%     comm = sprintf('sed "N;$!P;$!D;$d" < tmp > %s; rm tmp', outfile);
% end
% system(comm);


end
