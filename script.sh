#!/bin/bash
cd project
make --quiet
rm ../test.ir -f
bin/irgen test/$1 > ../test.ir
cd ..
sed -i '/^$/d' test.ir
python project/line.py test.ir
cd assgn2
make --quiet
rm ../test.s -f
python bin/codegen ../test.ir > ../test.s
cd ..
rm a.out -f
gcc -m32 test.s
./a.out