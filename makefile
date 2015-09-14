VOGFILES=README \
 makefile \
 license.txt \
 DATA \
 STRUCTURE_DISCOVERY \
 MDL \
 demo_vog.bash \
 run_structureDiscovery.m

all:	demo

demo:
	bash demo_vog.bash

zip: tar

tar: ${VOGFILES} 
	tar -cvf vog.tar ${VOGFILES}

