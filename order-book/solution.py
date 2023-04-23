import fileinput

import json

from datetime import datetime


class OrderBook():
	def __init__(self):
		self.orders = []
		self.buy_orders = []
		self.sell_orders = []

	def parse_order(self, order):
		# Check if there are any orders to match against
		if order['order']['direction'] == 'Buy':
			if not self.sell_orders:
				self.add_order(order)
		else:
			if not self.buy_orders:
				self.add_order(order)

		# Check if the order can be matched
		if self.immediate_fill_possible(order):
			self.aggressive_fill(order, self.get_fillable_orders(order))
			print('aggresive_fill')

	def add_order(self, order):

		if order['type'] == 'Limit':
			order_details = order['order']
			order = LimitOrder(order['type'],
							   order_details['direction'],
							   order_details['id'],
							   order_details['price'],
							   order_details['quantity'])
			if order.direction == 'Buy':
				self.buy_orders.append(order)
			else:
				self.sell_orders.append(order)
		else:
			order_details = order['order']
			order = IcebergOrder(order['type'],
								 order_details['direction'],
								 order_details['id'],
								 order_details['price'],
								 order_details['quantity'],
								 order_details['peak'])
			if order.direction == 'Buy':
				self.buy_orders.append(order)
			else:
				self.sell_orders.append(order)

		self.reorder(order.direction)

	def reorder(self, direction):
		if direction == 'Buy':
			self.buy_orders.sort(key=lambda x: (-x.price, x.entry_time))
		else:
			self.sell_orders.sort(key=lambda x: (x.price, x.entry_time))

	def immediate_fill_possible(self, order):
		if order['order']['direction'] == 'Buy':
			order_book = self.sell_orders
		else:
			order_book = self.buy_orders
		try:
			if order_book[0].price == order['order']['price']:
				return True
			else:
				return False
		except IndexError:
			# There are no orders in the order book yet, so immediate fill is not possible.
			return False

	def get_fillable_orders(self, order):
		# Get a subset of existing orders of the opposite direction which match with the
		# incoming order's price
		if order['order']['direction'] == 'Buy':
			order_book = self.sell_orders
		else:
			order_book = self.buy_orders
		return list(
			filter(
				lambda o: o.price == order['order']['price'],
				order_book
			)
		)

	def aggressive_fill(self, order, fillable_orders):
		# Incoming order's quantity is higher than fillable orders' quantity
		order_quantity = order['order']['quantity']
		if order_quantity > sum(o.quantity for o in fillable_orders):
			while order_quantity > 0 and fillable_orders:
				order_quantity = order_quantity - fillable_orders.pop().quantity
				if order['order']['direction'] == 'Buy':
					self.sell_orders.pop()
				else:
					self.buy_orders.pop()
		# Incoming order's quantity is lower than fillable orders' quantity

	def single_aggressive_fill(self, order):
		if order['direction'] == 'Buy':
			order_book = self.sell_orders
		else:
			order_book = self.buy_orders
		pass
		
		## CASE 1 and 4: Matching incoming limit or iceberg order with existing limit order
		# Incoming order's quantity is higher than existing order quantity
		if order['order']['quantity'] > order_book[0].quantity:
			order_book.pop(0)
			# STDOUT: Log succesful filling of the incoming limit order
			order['order']['quantity'] = order['order']['quantity'] - order_book[0].quantity
			self.parse_order(order)

		# Incoming order's quantity is lower than existing order quantity
		else:
			order_book[0].quantity = order_book[0].quantity - order['order']['quantity']
			order['order']['quantity'] = 0
			# STDOUT: Log succesful filling of the incoming limit order
		
		## CASE 2 AND 3: Matching incoming limit or iceberg order with existing iceberg order
		# Incoming order's quantity is higher or equal than existing order quantity
		if order['order']['quantity'] > order_book[0].peak:
			current_orderbook_peak = order_book[0].peak
			self.refresh_iceberg_order(order_book, order)
			order['order']['quantity'] = order['order']['quantity'] - current_orderbook_peak
			self.parse_order(order)

		# Incoming order's quantity is lower than existing order quantity
		else:
			self.refresh_iceberg_order(order_book, order)
			# STDOUT: Log succesful filling of the incoming limit order 


	def refresh_iceberg_order(self, order_book, filling_order):
		# If filling orders' quantity is higher than the available peak in the matched order, only part of
		# the filling order will matched. This part is equal to the peak of the matched order.
		if filling_order['order']['quantity'] >= order_book[0]['peak']:
			filling_order['order']['quantity'] = order_book[0]['peak']
			order_book[0]['quantity'] = order_book[0]['quantity'] - filling_order['order']['quantity']
			order_book[0]['entry_time'] = datetime.now()
		else:
			order_book[0]['peak'] = order_book[0]['peak'] - filling_order['order']['quantity']
		self.reorder(filling_order['order']['direction'])
			

	def full_fill(self):

		pass

	def partial_fill(self):
		pass

		'''
	  if order['direction'] == 'Buy':
		  order_book = self.sell_orders
	  else:
		  order_book = self.buy_orders
	  filtered_list = list(
		filter(
			lambda o: o.price == order['price'],
			order_book
		)
	  )

	  filled_ids = []
	  while 
	  '''
		pass

	def remove_filled_order(self, order_direction):
		# Orders are filled according to their order in the order_book, therefore
		# always the top item from the list is removed one by one.
		if order_direction == 'Buy':
			self.buy_orders.pop(0)
		else:
			self.sell_orders.pop(0)

	def execute(self):
		pass

	def __str__(self):
		return f'Current order book is {self.orders}'


class LimitOrder():

	type = 'Limit'

	def __init__(self, type, direction, id, price, quantity):
		self.type = type
		self.direction = direction
		self.id = id
		self.price = price
		self.quantity = quantity
		self.entry_time = datetime.now()
		print(self.direction, self.id, self.price, self.quantity)

	def __str__(self):
		return f'{{“id”: {self.id}, “price”: {self.price}, “quantity”: {self.quantity}}}'


class IcebergOrder():

	type = 'Iceberg'

	def __init__(self, type, direction, id, price, quantity, peak):
		self.type = type
		self.direction = direction
		self.id = id
		self.price = price
		self.quantity = quantity
		self.peak = peak
		self.entry_time = datetime.now()
		print(self.direction, self.id, self.price, self.quantity, self.peak)

	def fill_peak(self, match):
		if match >= self.peak:
			self.quantity

	def update(self, value):
		self.quantity = self.quantity - value
		if self.peak < self.quantity:
			self.peak = self.quantity
		# Controls the LimitOrder and Remainder which belong to Iceberg Order instance
		pass

	def __str__(self):
		return f'{{“id”: {self.id}, “price”: {self.price}, “quantity”: {self.peak}}}'


if __name__ == "__main__":
	order_book = OrderBook()
	# for line in fileinput.input(files=('tests/test1.in'), encoding='utf-8'):
	for line in fileinput.input(files=('../tests/AGGRESSIVE-SELL.in'), encoding='utf-8'):
		order_book.parse_order(json.loads(line))
		print('buyOrders:', [str(o) for o in order_book.buy_orders], 'sellOrders:', [
			  str(o) for o in order_book.sell_orders])
