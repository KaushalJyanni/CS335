#!/bin/bash
echo "
<HTML>
<BODY> " > ${1:5:-3}.html
python src/parser.py $1 > src/out.html
tac src/out.html >> ${1:5:-3}.html
echo "
</BODY>
</HTML>
" >> ${1:5:-3}.html
