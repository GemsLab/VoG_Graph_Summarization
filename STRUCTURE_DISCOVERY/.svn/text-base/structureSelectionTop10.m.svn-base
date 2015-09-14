function [  ] = structureSelectionTop10(graphFile, model_ordered, outfile)
%% Select the top 10 substructures to output to the user.
% The ranking of the substructures is based on their MDL benefit.

fid = fopen(outfile, 'w');

for i = 1 : min( 10, length(model_ordered) )
    printStructureToModelFile( model_ordered(i), fid );
end

%comm = sprintf('python ../mdl/score.py %s %s > pythonOutput.txt;', ...
%    graphFile, outfile )
%system(comm)
%pythonOutput = importdata('pythonOutput.txt');
%cost0 = str2num(pythonOutput.textdata{2,2});
%cost = str2num(pythonOutput.textdata{3,2});

fclose(fid);

end
