function [ furthest_node, chain, extra_nodes, ...
           chainExt, extra_nodesExt ] = BFS( Asmall, start, path, extend )
%% Given a graph and a node, find the node that
%  is furthest away from it. Also, report the path,
%  the variable 'path' is set to true.
%  DISCLAIMER: This will not give the longest chain in the graph, but
%              the shortest path between the furthest apart nodes.
%              Finding the longest path in a graph is NP-complete in
%              graphs with cycles. It is polynomial for DAGs.

n = size(Asmall,2);
extra_nodes = [];
extra_nodesExt = [];
extra_nodes_search = ones(1,n);
chain = [];
chainExt = [];
queue = [start];
% nodesList = 0 (if unvisited) or parentId (if visited)
nodesList = zeros(1,n);
nodesList(start)=start; % set as parent of the start node itself.

while ~( isempty(queue) )
    neighbors = find( Asmall(queue(1),:) ) ;
    
    for i = 1 : length(neighbors)
        if nodesList( neighbors(i) ) == 0 % unvisited neighbor
            nodesList( neighbors(i) ) = queue(1);
            queue = [ queue, neighbors(i) ];
        end
    end
    
    qsize = length(queue);
    % has the furthest node from start up to that point
    furthest_node = queue(qsize);
    queue = queue(2:qsize);
end

if path == true
    curr = furthest_node;
    while curr ~= start
        chain = [ curr, chain];
        extra_nodes_search(curr) = 0;
        curr = nodesList(curr);
    end
    chain = [ start, chain];
    extra_nodes_search(start) = 0;
    extra_nodes = find(extra_nodes_search==1);
    
    % heuristic: check for the extra nodes if they are neighboring with one
    % of the end points - then we can update our chain and make it longer
    % Do BFS in the induced subgraph of one endpoint and extra_nodes.
    % Repeat for the other endpoint. If a chain is returned, then make the
    % previously found path longer.
    
    if extend == true
        
        % chain except from p_init
        chain_head = chain(1:length(chain)-1);
        % chain except from p_fin
        chain_tail = chain(2:length(chain));
        
        %extend chain from start point (if possible)
        indSub_start = Asmall;
        indSub_start(chain_tail, :) = 0;
        indSub_start(:, chain_tail) = 0;
        [ furthestStart, chain1, ~ ] = BFS( indSub_start, chain(1), true, false );
        
        
        % extend chain from end point (if possible)
        indSub_end = Asmall;
        indSub_end(chain_head, :) = 0;
        indSub_end(:, chain_head) = 0;
        [ furthestEnd, chain2, ~ ] = BFS( indSub_end, chain(end), true, false );
    
        % checking if the chains have been extended to the same nodes.
        % This happened when I tried to encode a clique as a chain.
        overlap = false;
        for i = 2 : length(chain1)
            if ismember(chain1(i), chain2)
                overlap = true;
                % we include the nodes from chain1 up to the overlapped node
                % (excluding the overlapped node)
                chainExt = [ chain1((i-1):-1:2), chain, chain2(2:end) ];
                break;
            end
        end
        
        % merging locally extended chains
        if overlap == false
            chainExt = [ chain1(end:-1:2), chain, chain2(2:end) ];
        end
        extra_nodesExtIdx = ~ismember(extra_nodes, chainExt);
        extra_nodesExt = extra_nodes(extra_nodesExtIdx);
        
    end 
    
end

end
