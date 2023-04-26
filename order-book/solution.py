import sys
import json

from datetime import datetime


class OrderBook():

	def __init__(self):
		'''
		OrderBook class collects orders in two sub order-books: 'buy_orders' book and 'sell_orders' book.
		Transactions (incoming order matching existing order) are collected in 'transactions_history' list.
		'''
		self.buy_orders = []
		self.sell_orders = []
		self.transactions_history = []

	def parse_order(self, order):
		'''
		This is a pre-matching dispatch function to decide whether a new order will be added to the order book
		or it will matched (aggressively or passively) with existing order.
		
		Disregard orders with zero quantity
		'''
		if order['order']['quantity'] == 0:
			pass

		# Empty order book case - Are there any orders of the opposite direction in the book?
		# If no, simply add order to the book.
		if order['order']['direction'] == 'Buy':
			if not self.sell_orders:
				self.add_order(order)
				return
		else:
			if not self.buy_orders:
				self.add_order(order)
				return

		# Check if the order can be matched
		if self.immediate_fill_possible(order):
			self.match_orders(order)
		else:
			# Immediate fill not possible. Enter incoming order to the book
			self.add_order(order)


	def add_order(self, order):
		'''
		Create and add an an order to an order book. Since there are two sub order books (one for buy orders
		and one for sell orders), an object of either LimitOrder or IcebergOrder will be created first, and
		then it will be added to the appropriate sub order book.

		Finally, the sub order book is refreshed.
		'''

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

		# Book refresh
		self.reorder(order.direction)

	def reorder(self, direction):
		'''
		Reorder sub order book by price and entry time. Sort buy order book by price in ascending order first,
		and by most recent entry time second. Sort sell order book by price in ascending order first,
		and by the most recent entry time second.
		'''
		if direction == 'Buy':
			self.buy_orders.sort(key=lambda x: (-x.price, x.entry_time))
		else:
			self.sell_orders.sort(key=lambda x: (x.price, x.entry_time))

	def immediate_fill_possible(self, order):
		'''
		Check if the incoming order can be matched with an existing order book. Immediate fill is only possible
		if the price of the first order in the sell orders book is lower or equal to the price of the incoming
		order. For buy order book, price has to higher or equal to the price of the incoming order.
		'''
		try:
			if order['order']['direction'] == 'Buy':
				order_book = self.sell_orders
				if order_book[0].price <= order['order']['price']:
					return True
				else:
					return False
			else:
				order_book = self.buy_orders
				if order_book[0].price >= order['order']['price']:
					return True
				else:
					return False
		except IndexError:
			print('There are no orders in the sub order book yet, so immediate fill is not possible.')
			return False


	def match_orders(self, order):
		"""
		Main orders' matching engine. Responsible for matching and processing incoming orders
		recursively until full incoming quantity is either matched and/or added to the order book.

		Matching depends on the incoming and existing order type. There are 4 possible
		matching cases:

		Case 1: Incoming Limit order matching existing Limit order
		Case 2: Incoming Limit order mathcing existing Iceberg order
		Case 3: Incoming Iceberg order matching existing Limit order
		Case 4: Incoming Iceberg order matching existing Iceberg order

		Within each case, the processing path will further depend whether incoming order quantity is higher,
		lower or equal to existing order's quantity. Therefore, within case, we will have at most three
		processing path.  
		"""

		# Renaming variable for brevity
		incoming_order = order['order']
		if incoming_order['direction'] == 'Buy':
			order_book = self.sell_orders
		else:
			order_book = self.buy_orders
		pass
		existing_order = order_book[0]
		incoming_order_type = order['type']
		existing_order_type = existing_order.type

		# DISPATCHING
		# Check if an incoming order is a Limit order
		if incoming_order_type == 'Limit':
			# Incoming order is a Limit Order. Matching with existing limit order in Case 1,
			# and with an existing iceberg order in Case 2.
		
			# DISTINGUISH THE CASE
			# MATCHING WITH EXISTING LIMIT ORDER
			if existing_order_type == 'Limit':
				# 'CASE 1' - INCOMING LIMIT ORDER MATCHING WITH EXISTING LIMIT ORDER
				if incoming_order['quantity'] > existing_order.quantity:
					# 'CASE 1. PATH A.' - INCOMING ORDER'S QUANTITY IS HIGHER
					# THAN THE EXISTING'S ORDER QUANTITY

					matched_quantity = existing_order.quantity
					incoming_order['quantity'] = incoming_order['quantity'] - matched_quantity
					self.transactions_history.append(Transaction(existing_order, incoming_order, matched_quantity))
					print(self.transactions_history[-1])
					order_book.pop(0)
					self.parse_order(order)
				else:
					# 'CASE 1. PATH B' INCOMING ORDER'S QUANTITY IS LOWER THAN
					# EXISTING ORDER'S QUANTITY

					matched_quantity = incoming_order['quantity']
					self.transactions_history.append(Transaction(existing_order, incoming_order, matched_quantity))
					print(self.transactions_history[-1])
					existing_order.quantity = existing_order.quantity - matched_quantity
					incoming_order['quantity'] = 0

					# 'CASE 1. PATH C' INCOMING ORDER'S QUANTITY IS EQUAL TO EXISTING
					# ORDER'S QUANTITY
					if existing_order.quantity == 0:
						order_book.pop(0)
					return
			# MATCHING WITH EXISTING ICEBERG ORDER
			else:
				# 'CASE 2' - INCOMING LIMIT ORDER MATCHING WITH EXISTING ICEBERG ORDER
				if incoming_order['quantity'] > existing_order.quantity:
					# 'CASE 2. PATH A.' - INCOMING ORDER'S QUANTITY IS HIGHER
					# THAN THE EXISTING'S ORDER QUANTITY

					matched_quantity = min(existing_order.peak, existing_order.quantity)
					if matched_quantity != 0:

						self.transactions_history.append(Transaction(existing_order, incoming_order, matched_quantity))
						print(self.transactions_history[-1])
						incoming_order['quantity'] = incoming_order['quantity'] - matched_quantity
						existing_order.quantity = existing_order.quantity - matched_quantity
						
						existing_order.entry_time = datetime.now()
						self.reorder(existing_order.direction)
					else:
						order_book.pop(0)

					self.parse_order(order)

				else:
					# 'CASE 2. PATH B.' - INCOMING ORDER'S QUANTITY IS LOWER OR EQUAL
					# THAN THE EXISTING'S ORDER QUANTITY

					matched_quantity = min(existing_order.peak,
										   incoming_order['quantity'])
					self.transactions_history.append(Transaction(existing_order, incoming_order, matched_quantity))
					print(self.transactions_history[-1])

					# Updating incoming and existing order quantity
					if incoming_order['quantity'] >= existing_order.peak:
						existing_order.quantity = existing_order.quantity - matched_quantity
					existing_order.peak = existing_order.peak - matched_quantity
					existing_order.entry_time = datetime.now()
					incoming_order['quantity'] = incoming_order['quantity'] - matched_quantity

					# Updating peak
					if incoming_order['quantity'] == 0:
						if existing_order.peak == 0:
							existing_order.peak = min(existing_order.default_peak, existing_order.quantity)
							if existing_order.peak == 0:
								order_book.pop(0)
						return
					else:
						if existing_order.quantity < existing_order.peak:
							existing_order.peak = existing_order.quantity
						if existing_order.peak == 0:
							existing_order.peak = min(existing_order.default_peak, existing_order.quantity)
					
						self.reorder(existing_order.direction)
						self.parse_order(order)
		# Incoming order is an Iceberg Order		
		else:
			# Incoming order is an Iceberg Order. Matching with existing limit order in Case 3,
			# and with an existing iceberg order in Case 4.
		
			if existing_order_type == 'Limit':
				# 'CASE 3' - INCOMING ICEBERG ORDER MATCHING WITH EXISTING LIMIT ORDER
				if incoming_order['quantity'] > existing_order.quantity:
					# 'CASE 3. PATH A.' - INCOMING ORDER'S QUANTITY IS HIGHER
					# THAN THE EXISTING'S ORDER QUANTITY

					matched_quantity = min(existing_order.quantity, existing_order.quantity)
					if matched_quantity != 0:
						self.transactions_history.append(Transaction(existing_order, incoming_order, matched_quantity))
						print(self.transactions_history[-1])
						incoming_order['quantity'] = incoming_order['quantity'] - matched_quantity
						existing_order.quantity = existing_order.quantity - matched_quantity
						existing_order.entry_time = datetime.now()
					else:
						order_book.pop(0)

					self.parse_order(order)
				else:
					# 'CASE 3. PATH B' INCOMING ORDER'S QUANTITY IS LOWER OR EQUAL TO EXISTING ORDER'S QUANTITY
					
					matched_quantity = incoming_order['quantity']
					self.transactions_history.append(Transaction(existing_order, incoming_order, matched_quantity))
					print(self.transactions_history[-1])
					existing_order.quantity = existing_order.quantity - incoming_order['quantity']
					existing_order.entry_time = datetime.now()
					incoming_order['quantity'] = 0

					# 'CASE 3. PATH C'
					if existing_order.quantity == 0:
						order_book.pop(0)

					self.reorder(existing_order.direction)
			
			# MATCHING WITH EXISTING ICEBERG ORDER
			else:
				# 'CASE 4' - INCOMING ICEBERG ORDER MATCHING WITH EXISTING ICEBERG ORDER
				if incoming_order['quantity'] > existing_order.peak:
					# 'CASE 4. PATH A.' - INCOMING ORDER'S QUANTITY IS HIGHER
					# THAN THE EXISTING'S ORDER QUANTITY

					matched_quantity = min(existing_order.peak, existing_order.quantity)
					self.transactions_history.append(Transaction(existing_order, incoming_order, matched_quantity))
					print(self.transactions_history[-1])

					incoming_order['quantity'] = incoming_order['quantity'] - matched_quantity
					existing_order.quantity = existing_order.quantity - matched_quantity
					existing_order.entry_time = datetime.now()
					if existing_order.quantity == 0:
						order_book.pop(0)

					self.reorder(existing_order.direction)
					self.parse_order(order)

				else:
					# 'CASE 4. PATH B.' - INCOMING ORDER'S QUANTITY IS LOWER OR EQUAL
					# THAN THE EXISTING'S ORDER QUANTITY

					matched_quantity = incoming_order['quantity']
					self.transactions_history.append(Transaction(existing_order, incoming_order, matched_quantity))
					print(self.transactions_history[-1])

					existing_order.quantity = existing_order.quantity - incoming_order['quantity']
					if existing_order.quantity < existing_order.peak:
						existing_order.peak = existing_order.quantity
					existing_order.entry_time = datetime.now()
					if existing_order.quantity == 0:
						order_book.pop(0)

					self.reorder(existing_order.direction)

	def __str__(self):
		return f'Sell orders: {self.sell_orders}, Buy orders: {self.buy_orders}'

class Transaction():

	def __init__(self, matchable_order, incoming_order, matched_quantity):
		'''
		Object representing transaction which took place through match_order method of OrderBook class. 
		Transaction is only executed if at least part of an incoming order's quantity was matched with an
		existing order quantity.
		'''

		if matchable_order.direction == 'Buy':
			self.buy_order_id = matchable_order.id
			self.sell_order_id = incoming_order['id']
		else:
			self.buy_order_id = incoming_order['id']
			self.sell_order_id = matchable_order.id

		self.price = matchable_order.price
		self.quantity = matched_quantity

	def __str__(self):
		return f'''{{"buyOrderId": {self.buy_order_id}, "sellOrderId": {self.sell_order_id}, "price": {self.price},  "quantity": {self.quantity}}}'''


class LimitOrder():

	type = 'Limit'

	def __init__(self, type: str, direction: str, id: int, price: int, quantity: int):
		self.type = type
		self.direction = direction
		self.id = id
		self.price = price
		self.quantity = quantity
		self.entry_time = datetime.now()

	def as_json(self):
		return {"id": self.id, "price": self.price, "quantity": self.quantity}


class IcebergOrder():

	type = 'Iceberg'

	def __init__(self, type: str, direction: str, id: int, price: int, quantity: int, peak: int):
		self.type = type
		self.direction = direction
		self.id = id
		self.price = price
		self.quantity = quantity
		self.peak = peak
		self.default_peak = peak
		self.entry_time = datetime.now()

	def as_json(self):
		return {"id": self.id, "price": self.price, "quantity": self.peak}


if __name__ == "__main__":

	order_book = OrderBook()

	for line in sys.stdin:
		order_book.parse_order(json.loads(line))
		print(json.dumps({"sellOrders": [o.as_json() for o in order_book.sell_orders],
		    			  "buyOrders": [o.as_json() for o in order_book.buy_orders]
		    			  }))
