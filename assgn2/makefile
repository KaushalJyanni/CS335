all : binary

binary :
	mkdir -p bin
	cp src/codegen.py bin/codegen
	cp src/asmcode.py bin/asmcode.py
	cp src/basicblocks.py bin/basicblocks.py
	cp src/descriptors.py bin/descriptors.py
	cp src/generateasm.py bin/generateasm.py
	cp src/useinfo.py bin/useinfo.py
	cp src/utils.py bin/utils.py
	chmod +x bin/codegen

clean:
	rm -r bin
