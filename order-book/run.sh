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
{"type": "Iceberg", "order": {"direction": "Buy", "id": 1, "price": 14, "quantity": 20, "peak": 3}}
{"type": "Iceberg", "order": {"direction": "Buy", "id": 2, "price": 14, "quantity": 20, "peak": 3}}
{"type": "Iceberg", "order": {"direction": "Buy", "id": 3, "price": 14, "quantity": 20, "peak": 3}}
{"type": "Iceberg", "order": {"direction": "Sell", "id": 4, "price": 14, "quantity": 80, "peak": 4}}
EOF