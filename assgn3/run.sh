#!/bin/bash
echo "
<HTML>
<BODY> " > ${1:5:-3}.html
python bin/parser $1 > bin/out.html
tac bin/out.html >> ${1:5:-3}.html
echo "
</BODY>
</HTML>
" >> ${1:5:-3}.html
