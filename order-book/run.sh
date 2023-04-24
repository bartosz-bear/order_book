#!/bin/sh

# YOU ARE EXPECTED TO MODIFY THIS FILE - DELETE ALL CONTENT BELOW AND EXECUTE YOUR OWN CODE
# Please remember to pass stdin to your solution (see example below)
#
# For example, if your solution is in Python, we expect you provide something like:
# python3 <your-solution.py> <&0

# The trivial way to pass provided tests (test1 in this case) is to just print your expected solution 
# but of course you should execute your code here.

# MY SOLUTION

python solution.py <&0 cat <<EOF
{"type":"Limit","order":{"direction":"Sell","id":1,"price":101,"quantity":20000}}
{"type":"Limit","order":{"direction":"Buy","id":2,"price":99,"quantity":50000}}
{"type":"Limit","order":{"direction":"Sell","id":3,"price":100,"quantity":10000}}
{"type":"Limit","order":{"direction":"Sell","id":4,"price":100,"quantity":7500}}
{"type":"Limit","order":{"direction":"Buy","id":5,"price":98,"quantity":25500}}
{"type":"Iceberg","order":{"direction":"Buy","id":6,"price":100,"quantity":100000,"peak":10000}}
{"type":"Limit","order":{"direction":"Sell","id":7,"price":100,"quantity":10000}}
{"type":"Limit","order":{"direction":"Sell","id":8,"price":100,"quantity":11000}}
{"type":"Iceberg","order":{"direction":"Buy","id":9,"price":100,"quantity":50000,"peak":20000}}
{"type":"Limit","order":{"direction":"Sell","id":10,"price":100,"quantity":35000}}
EOF