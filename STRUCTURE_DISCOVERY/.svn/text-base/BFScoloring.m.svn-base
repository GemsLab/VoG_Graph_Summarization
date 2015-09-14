function [ set1, set2 ] = BFScoloring( Asmall )
%% Given a bipartite graph, find the two node-sets memberships

n = size(Asmall,2);
[seed ~] = find(Asmall);
queue = [min(seed)];
% sets = 2 (if unvisited) or 0 (if in set 1) or 1 (if in set 2)
sets = zeros(1,n)+2;
color = 1;
% coloring node 1 with color "0"
sets(min(seed)) = 0;
usedColor = false;


while ~( isempty(queue) )
    neighbors = find( Asmall(queue(1),:) ) ;
    
    for i = 1 : length(neighbors)
        if sets( neighbors(i) ) == 2 % unvisited neighbor
            sets( neighbors(i) ) = color;
            queue = [ queue, neighbors(i) ];
            usedColor = true;
        end
    end
    
    qsize = length(queue);
    queue = queue(2:qsize);
    if usedColor
        color = mod(color+1, 2);
    end
    usedColor = false;
end

set1 = find( sets == 0 );
set2 = find( sets == 1 );

end