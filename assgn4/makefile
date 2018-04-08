all : binary

binary :
	mkdir -p bin
	cp src/parser.py bin/irgen
	chmod +x bin/irgen
	cp src/lexer.py bin/lexer.py
	cp src/sym_table.py bin/sym_table.py

clean:
	rm -r bin
	
