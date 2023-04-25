#!/bin/sh

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
python3 solution.py <&0 cat <<EOF
{"type":"Limit","order":{"direction":"Sell","id":1,"price":101,"quantity":20000}}
{"type":"Limit","order":{"direction":"Sell","id":3,"price":100,"quantity":10000}}
{"type":"Limit","order":{"direction":"Sell","id":4,"price":100,"quantity":7500}}
EOF