Author: Jilles Vreeken
Email:  jilles@mmci.uni-saarland.de


:: General Assumptions on Input
	We deal with undirected, nonloopy graphs, where each node has an id, and node ids start with 1.

:: Usage
	python score.py <graph file> <model file>

	It prints the possible parameters if you give no options at all; if you only give a graph file it shows the encoded size by the empty model.


:: Input Data Format for Graphs
	One edge per row, comma separated: 
	<source nodeId>,<dest nodeId>

	e.g.
	1,2
	1,3
	...
	
	As we are working with undirected graphs, for pairs i,j it does not matter whether i<j or j>i. (non-loopy, so no i=j, though I currently don't check for that)


:: Input Data Format for Models
	One structure per row, e.g.:
	fc 1 2 3 4
	fc 5 4 2 6
	bc 1 2 3, 21 2 1
	ch 10 11 200 12

	The ordering of the rows does influence which structure encodes what part of the graph. Later, when we introduce structure-Typed-error encoding this may matter.

	Where for the different structure types (and hence encodings) I have


	Full clique:
fc [node ids]
	e.g.
	fc 1 2 3 4			for a full-clique over nodes 1 to 4. 
						This encoding is great for full cliques, and near-cliques with high connectivity
						E += { (1,2), (1,3), (1,4), (2,3), (2,4), (3,4) }


nc <# of edges>, [node ids]
     e.g.
     nc 5, 1 2 3 4		for a near-clique over nodes 1 to 4, with 5 edges among them.
						This encoding gives the exact connections, without making error. 
						! in certain cases the full-clique encoding may be more efficient:
						  depending on Error encoding, encoding some superfluous edges can 
						  be cheaper. Formal analysis needed.
						E= exactly what is in the data, using (locally optimal) prefix codes

	Chain
ch [node ids]
	e.g.
	ch 4 2 1 3			for a chain from node 4 to 2 to 1 to 3
						E+={ (4,2), (2,1), (1,3) }

	Star
st <hub id>, [node ids]
	e.g.
	st 1, 2 3 4			for a star with node 1 as hub, and spokes to nodes 2, 3 and 4
						E+={ (1,2), (1,3), (1,4) }
	- BiPartiteCore of size 1


	BiPartiteCore
bc [node id set A], [node id set B]
	e.g.
	bc 1 2 3, 4 5		for a fully connected bi-partite graph between node sets 1,2,3 and 4,5
						! also means there are no edges between nodes 1,2,3, nor between nodes 4,5
						E+={ (1,4), (1,5), (2,4), (2,5), (3,4), (3,5) }

	NearBiPartiteCore
nb [node id set A], [node id set B]
	e.g.
	nb 1 2 3, 4 5		for a possibly not fully connected bi-partite graph between node sets 1,2,3 and 4,5
						! implies there are no edges between nodes 1,2,3, nor between nodes 4,5 --- errors are pushed into error matrix
						E= edges within sets A and B, no errors between A and B


