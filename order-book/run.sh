#!/bin/bash

# YOU ARE EXPECTED TO MODIFY THIS FILE - DELETE ALL CONTENT BELOW AND EXECUTE YOUR OWN CODE
# Please remember to pass stdin to your solution (see example below)
#
# For example, if your solution is in Python, we expect you provide something like:
# python3 <your-solution.py> <&0

# The trivial way to pass provided tests (test1 in this case) is to just print your expected solution 
# but of course you should execute your code here.

# MY SOLUTION
#< ./tests/test2.in
#< ../tests/4-2-3-1-AGGRESSIVE.in
#python3 solution.py < ./tests/test-1.in > ./tests/test-1.result
#python3 solution.py < ./tests/test-2.in > ./tests/test-1.result

#<&0 cat <<EOF
#{"type": "Limit", "order": {"direction": "Buy", "id":1, "price": 14, "quantity":20}}
#{"type": "Iceberg", "order": {"direction": "Buy", "id":2, "price": 15, "quantity":50, "peak": 20}}
#{"type": "Limit", "order": {"direction": "Sell", "id":3, "price": 16, "quantity": 15}}
#{"type": "Limit", "order": {"direction": "Sell", "id":4, "price": 13, "quantity": 60}}
#EOF
#if diff ./tests/test-1.out ./tests/test-1.result > /dev/null; then 
#    echo "the outputs are identical"
#else
#    echo "the outputs differ"
#fi

#diff ./tests/test-1.out ./tests/test-1.result

#cat ./tests/test-1.in

if [ "$1" = "test" ]; then
  green='\e[0;32m'
  white='\e[0;37m'

  for i in $(seq 1 19);
  do
    echo "./tests/test-${i}.out"
    python3 solution.py < ./tests/test-${i}.in > ./tests/test-${i}.result
    if diff ./tests/test-${i}.out ./tests/test-${i}.result > /dev/null; then 
      echo -e "${green}Pass${white}"
    else
      echo -e "${red}Fail${white}"
    fi
  done

else
  python3 solution.py < ./tests/test-26.in > ./tests/test-26.result
fi




#MULTILINE COMMENT: start: : ' end: '