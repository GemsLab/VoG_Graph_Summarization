function [cur_gccind,cur_disind] = ExtractGccEncode(B, out_fid, topind, top_gccind, N_tot, info, minSize)

[S,C]=graphconncomp(B, 'WEAK', true);

maxind=-1;
maxsize=0;

size_v = zeros(0, S);

for k=1:S
    size_v(k)=size(find(C == k), 2);
end

[size_sort,I]=sort(size_v, 'descend');

cur_gccind = find(C == I(1));

cur_disind = zeros(0,0);

for k=2:S
    curind = find(C == I(k));
    
    if( size(curind,2) ==1 )
        mask = ismember(curind, topind);
        if sum(mask) == 1
            continue;
        end
    end            
    
    if length(curind) > minSize
%     EncodeConnComp(B, curind, top_gccind, out_fid);
        EncodeSubgraph(B, curind, top_gccind, N_tot, out_fid, info, minSize);
    end
    cur_disind = [cur_disind curind];
end

% fprintf('\tgccsize\t%d\n', size(cur_gccind,2));

