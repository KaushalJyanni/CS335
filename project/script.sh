#!/bin/bash
cd project
make --quiet
rm -f ../test.ir
bin/irgen test/$1 > ../test.ir
cd ..
sed -i '/^$/d' test.ir
python project/line.py test.ir
cd assgn2
make --quiet
rm -f ../test.s
python bin/codegen ../test.ir > ../test.s
cd ..
rm -f a.out
gcc -m32 test.s
./a.out