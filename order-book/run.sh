#!/bin/sh

# YOU ARE EXPECTED TO MODIFY THIS FILE - DELETE ALL CONTENT BELOW AND EXECUTE YOUR OWN CODE
# Please remember to pass stdin to your solution (see example below)
#
# For example, if your solution is in Python, we expect you provide something like:
# python3 <your-solution.py> <&0

# The trivial way to pass provided tests (test1 in this case) is to just print your expected solution 
# but of course you should execute your code here.
cat <<EOF
{"buyOrders": [{"id":1, "price": 14, "quantity": 20}], "sellOrders": []}
{"buyOrders": [{"id": 2, "price": 15, "quantity": 20}, {"id": 1, "price": 14, "quantity": 20}], "sellOrders": []}
{"buyOrders": [{"id": 2, "price": 15, "quantity": 20}, {"id": 1, "price": 14, "quantity": 20}], "sellOrders": [{"id": 3, "price": 16, "quantity": 15}]}
{"buyOrders": [{"id": 1, "price": 14, "quantity": 10}], "sellOrders": [{"id": 3, "price": 16, "quantity": 15}]}
{"buyOrderId": 2, "sellOrderId": 4, "price": 15, "quantity": 20}
{"buyOrderId": 2, "sellOrderId": 4, "price": 15, "quantity": 20}
{"buyOrderId": 2, "sellOrderId": 4, "price": 15, "quantity": 10}
{"buyOrderId": 1, "sellOrderId": 4, "price": 14, "quantity": 10}
EOF
