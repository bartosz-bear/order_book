# Introduction

Order book program to match between Limit and Iceberg orders.

Matching depends on the incoming and existing order type. There are 4 possible
matching cases:

Case 1: Incoming Limit order matching existing Limit order
Case 2: Incoming Limit order mathcing existing Iceberg order
Case 3: Incoming Iceberg order matching existing Limit order
Case 4: Incoming Iceberg order matching existing Iceberg order

Within each case, the processing path will further depend whether incoming order quantity is higher, lower or equal to existing order's quantity.

# Input

Program `stdin` JSON from either command line or a file.

```json
{"type": "Limit", "order": {"direction": "Buy", "id":1, "price": 14, "quantity":20}}
```

See `Run` section for more details.

# Output

Program outputs following items in JSON format:
- order book summary after each completed transaction or order entry

```json
{"buyOrders": [{"id": 2, "price": 99, "quantity": 50000}], "sellOrders": [{"id": 1, "price": 101, "quantity": 20000}]}
```

- transaction details

```json
{"buyOrderId": 6, "sellOrderId": 3, "price": 100,  "quantity": 10000}
```

# Run

To run the program standalone, type:

`./run.sh '{"type": "Limit", "order": {"direction": "Buy", "id":1, "price": 14, "quantity":20}}'`

To run the program and take `stdin` from a file, pass the file path and name:

`./run.sh ./tests/test-1.in`

# Tests

There are 12 test cases covering each of 12 possible paths of order matching:

1. Case 1 A Limit-Limit incoming > existing
2. Case 1 B Limit-Limit incoming < existing
3. Case 1 C Limit-Limit incoming = existing
4. Case 2 A Limit-Iceberg incoming > existing
5. Case 2 B Limit-Iceberg incoming < existing
6. Case 2 C Limit-Iceberg incoming = existing
7. Case 3 A Iceberg-Limit incoming > existing
8. Case 3 B Iceberg-Limit incoming < existing
9. Case 3 C Iceberg-Limit incoming = existing
10. Case 4 A Iceberg-Iceberg incoming > existing
11. Case 4 B Iceberg-Iceberg incoming < existing
12. Case 4 C Iceberg-Iceberg incoming = existing

To run all tests cases:

`./run.sh tests`

To run a single test case:

`./run.sh test1`

To run your own test case:

- the easier way to run you own case is to add it `./tests/` folder, name it `test-next_$next_digit`, and modify `test_cases` variable in `run.sh` file, in order to include it in the testing set

- after that you make the edits can run it as part of the full set of cases or separately by passing your test number, eg. `./run sh 999`

