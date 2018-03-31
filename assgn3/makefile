all : binary

binary :
	mkdir -p bin
	cp src/parser.py bin/parser.py
	cp src/run.sh bin/parser
	chmod +x bin/parser
	cp src/lexer.py bin/lexer.py

clean:
	rm -r bin
	rm *.html
