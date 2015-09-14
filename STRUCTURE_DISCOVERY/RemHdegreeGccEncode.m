function [disind,gccind,topind] = RemHdegreeGccEncode(B,k,dir,out_fid, top_gccind, N_tot, info, minSize)


if nargin<3
    dir=1;
end

n = size(B,1);

if (dir == 1)
	%D = inout_degree(B);
	D = sum(B,2);
	D = D + sum(B,1)';
else
	D=sum(B,2);
end
[Dsort,I]=sort(D);


topind = flipud(I(n-k+1:n));

B(topind, :) = 0;
B(:, topind) = 0;

[gccind,disind] = ExtractGccEncode(B, out_fid, topind, top_gccind, N_tot, info, minSize );
%fullind = 1:n;
%disind = setdiff(fullind, gccind);
topind = topind';

mask = ismember(disind, topind);
disind = disind(~mask);
