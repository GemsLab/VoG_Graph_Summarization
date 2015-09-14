function [ ] = printModel( model_ordered, outfile)
%% Select the top 10 substructures to output to the user.
% The ranking of the substructures is based on their MDL benefit.

fid = fopen(outfile, 'w');

for i = 1 : length(model_ordered) 
    printStructureToModelFile( model_ordered(i), fid );
end

fclose(fid);

end
