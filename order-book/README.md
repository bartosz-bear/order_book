# Order Book
​
Your task is to implement an Order Book that handles two order types: Limit Order and Iceberg Order.

A Limit Order specifies the highest price at which we are willing to buy (for "buy" orders) or the lowest price at which we are willing to sell (for "sell" orders). An Iceberg Order is described in section 4.2 of the `setsmm-and-iceberg` document.
​
The program should read incoming order information from standard input, continuously update the Order Book's status, and, when a transaction occurs as a result of adding an order, output the corresponding information to standard output. Additionally, after adding each order, the updated state of the Order Book should be written to standard output.

## Input
​
Each entry line corresponds to one new order in JSON format:
- `type`: equal to `"Iceberg"` or `"Limit"`
- `order`: contains detailed information about the order:
  - `direction`: equal to `"Buy"` or `"Sell"`
  - `id`: consecutive positive integers: `1`, `2`, `3`, ...
  - `price`: positive integer
  - `quantity`: positive integer
  - `peak`: positive integer, this field is only present in the Iceberg orders
​
It can be assumed that the input data will be correct and all integers appearing on the input will fit in a 32-bit signed integer variable.
​
## Output
​
After reading the new order information from **stdin**, add it to the Order Book and then output the updated status of the Order Book as a JSON object to **stdout**.
​
The output JSON object should contain two fields: `buyOrders` and `sellOrders`, which represent lists of buy or sell orders. Each order should include `id`, `price`, and `quantity` fields. The order in the list is determined by the price. "Buy" orders are sorted by `price` in non-ascending order, while "sell" orders are sorted by `price` in non-descending order. If the price is the same, the `id` determines the order, meaning orders are sorted in ascending order by the time they were added to the Order Book.
​
If any transactions occur as a result of adding an order, they should be printed to **`stdout`** as a JSON object with the following fields: `buyOrderId`, `sellOrderId`, `price`, `quantity`.

## Examples
1. For the following orders:
```json
{"type": "iceberg", "order": {"direction": "sell", "id": 1, "price": 100, "quantity": 200,"peak": 100}}
{"type": "iceberg", "order": {"direction": "sell", "id": 2, "price": 100, "quantity": 300,"peak": 100}}
{"type": "iceberg", "order": {"direction": "sell", "id": 3, "price": 100, "quantity": 200,"peak": 100}}
{"type": "iceberg", "order": {"direction": "buy", "id": 4, "price": 100, "quantity": 500,"peak": 100}}
```
The final state of order book should be:
```json
{"sellOrders": [{"id": 3, "price": 100, "quantity": 100}, {"id": 2, "price": 100, "quantity":100}], "buyOrders": []}
```
2. See `tests/` directory.
3. See sections `4.2.3.1` and `4.2.3.2` in `setsmm-and-iceberg.pdf` document.

## Solution
Submit your project as a `.zip` archive with a bundle you received used as base with addition of files required to
run your solution. 

The entry point to your program should be a `run.sh` script that reads from *stdin* and writes to *stdout*.

Your code, depending on the language you used, will be executed in an automatic testing environment using a Docker container based on the `python:3.11-buster` or `node:19-buster` image. 

If you need any additional system packages, please provide a Dockerfile or a name of the Docker image that we should use.

For your convenience, we have included a few test cases to help you verify the input/output format and configuration script. You may add more test cases to that directory if desired.

To run a test, execute the following command from the root directory of the project (this assumes you have `jq` available for JSON formatting and key sorting):

```docker run -i -v $(pwd):/app python:3.11-buster /app/run.sh < tests/test1.in | jq -S . | diff - <(jq -S . tests/test1.out)```

Good luck!