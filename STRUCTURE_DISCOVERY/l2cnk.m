function [nbits] = l2cnk(n,k)
	nbits = 0;
	for i = n:-1:n-k+1
		nbits = nbits + log2(i);
	end
	
	for i = k:-1:1
		nbits = nbits - log2(i);
	end
end
