import fileinput

import json

from datetime import datetime

import sys

class OrderBook():

	def __init__(self):
		self.buy_orders = []
		self.sell_orders = []
		self.transactions_history = []
		self.order_book_status = []

	def parse_order(self, order):
		# This is a matching algorithm. It's a dispatch place to decide whether a new order
		# will be added to the order book or it will matched (aggressively or passively)
		
		# Disregard orders with zero quantity
		if order['order']['quantity'] == 0:
			pass

		# Are there any orders of the opposite direction in the book? If no, simply add
		# order to the book.
		#print('Debugging', order)
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

			# Immediate fill not possible. Enter to the book
			self.add_order(order)


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
			# There are no orders in the order book yet, so immediate fill is not possible.
			return False


	def match_orders(self, order):

		# Defininng variables
		order = order
		incoming_order = order['order']
		if incoming_order['direction'] == 'Buy':
			order_book = self.sell_orders
		else:
			order_book = self.buy_orders
		pass
		matchable_order = order_book[0]
	
		incoming_order_type = order['type']
		matchable_order_type = matchable_order.type

		if incoming_order_type == 'Limit' and matchable_order_type in ['Limit', 'Iceberg']:
			## CASE 1 and 4: Matching incoming limit or iceberg order with existing limit order
			# Incoming order's quantity is higher than existing order quantity

			# DISTINGUISH THE CASE
			if matchable_order_type == 'Limit':
				# MATCHING WITH LIMIT ORDER
				if incoming_order['quantity'] > matchable_order.quantity:
					#print('CASE 1. PATH A')
					
					matched_quantity = matchable_order.quantity
					incoming_order['quantity'] = incoming_order['quantity'] - matched_quantity
					
					self.transactions_history.append(Transaction(matchable_order, incoming_order, matched_quantity))

					order_book.pop(0)
					self.parse_order(order)

				# Incoming order's quantity is equal or lower than existing order quantity
				else:
					#print('CASE 1. PATH B')
					#print('INCOMING ORDER QUANTITY', incoming_order['quantity'])
					#print('EXISTING ORDER QUANTITY', matchable_order.quantity)
					matched_quantity = incoming_order['quantity']
					self.transactions_history.append(Transaction(matchable_order, incoming_order, matched_quantity))

					matchable_order.quantity = matchable_order.quantity - incoming_order['quantity']
					incoming_order['quantity'] = 0
					if matchable_order.quantity == 0:
						order_book.pop(0)
					return
			else:
				# MATCHING WITH ICEBERG ORDER
				if incoming_order['quantity'] >= matchable_order.quantity:
					#print('CASE 4. PATH A')
					#print('CURRENT TOP ORDER', matchable_order.quantity, matchable_order.peak)
					
					matched_quantity = min(matchable_order.peak, matchable_order.quantity)
					if matched_quantity != 0:

						self.transactions_history.append(Transaction(matchable_order, incoming_order, matched_quantity))

						incoming_order['quantity'] = incoming_order['quantity'] - matched_quantity
						matchable_order.quantity = matchable_order.quantity - matched_quantity
						matchable_order.entry_time = datetime.now()
						self.reorder(matchable_order.direction)
					else:
						order_book.pop(0)

					self.parse_order(order)

				# Incoming order's quantity is lower or equal than existing order quantity
				else:
					matched_quantity = min(matchable_order.peak,
										   incoming_order['quantity'])
					#print('CASE 4. PATH B')
					#print('PEAK', matchable_order.peak)
					#print('INCOMING ORDER QUANTITY', incoming_order['quantity'])
					#print('EXISTING ORDER QUANTITY', matchable_order.quantity)
					self.transactions_history.append(Transaction(matchable_order, incoming_order, matched_quantity))

					
					if incoming_order['quantity'] < matchable_order.peak:
						matchable_order.peak = matchable_order.peak - matched_quantity
					else:
						matchable_order.quantity = matchable_order.quantity - matched_quantity
						matchable_order.peak = matchable_order.peak - matched_quantity
					matchable_order.entry_time = datetime.now()

					incoming_order['quantity'] = incoming_order['quantity'] - matched_quantity
					if incoming_order['quantity'] == 0:
						if matchable_order.peak == 0:
							matchable_order.peak = min(matchable_order.default_peak, matchable_order.quantity)
					
						return
					else:
						if matchable_order.quantity < matchable_order.peak:
							matchable_order.peak = matchable_order.quantity
						if matchable_order.peak == 0:
							matchable_order.peak = min(matchable_order.default_peak, matchable_order.quantity)
					
						self.reorder(matchable_order.direction)
						self.parse_order(order)
		else:
			## CASE 2 AND 3: Matching incoming limit or iceberg order with existing iceberg order
			# Incoming order's quantity is higher or equal than existing order quantity
			if matchable_order_type == 'Limit':
				if incoming_order['quantity'] > matchable_order.quantity:
					#print('CASE 2 MATCHING LIMIT. PATH A')
					#print("Incoming order's quantity is HIGHER or equal than existing order quantity")
					matched_quantity = min(matchable_order.quantity, matchable_order.quantity)
					if matched_quantity != 0:
						self.transactions_history.append(Transaction(matchable_order, incoming_order, matched_quantity))

						incoming_order['quantity'] = incoming_order['quantity'] - matched_quantity
						matchable_order.quantity = matchable_order.quantity - matched_quantity
						matchable_order.entry_time = datetime.now()
					else:
						order_book.pop(0)

					self.parse_order(order)
				

				# Incoming order's quantity is lower than existing order quantity
				else:
					#print('CASE 2 MATCHING LIMIT. PATH B')
					#print("Incoming order's quantity is LOWER or equal than existing order quantity")
					matched_quantity = incoming_order['quantity']
					self.transactions_history.append(Transaction(matchable_order, incoming_order, matched_quantity))

					matchable_order.quantity = matchable_order.quantity - incoming_order['quantity']
					matchable_order.entry_time = datetime.now()
					incoming_order['quantity'] = 0
					self.reorder(matchable_order.direction)
			else:
				if incoming_order['quantity'] > matchable_order.peak:
					#print('CASE 3 MATCHING ICEBERG. PATH A')
					#print("Incoming order's quantity is HIGHER or equal than existing order quantity")
					matched_quantity = min(matchable_order.peak, matchable_order.quantity)
					if matched_quantity != 0:
						self.transactions_history.append(Transaction(matchable_order, incoming_order, matched_quantity))

						incoming_order['quantity'] = incoming_order['quantity'] - matched_quantity
						matchable_order.quantity = matchable_order.quantity - matched_quantity
						matchable_order.entry_time = datetime.now()
						if matchable_order.quantity == 0:
							order_book.pop(0)
						self.reorder(matchable_order.direction)
					else:
						order_book.pop(0)

					self.parse_order(order)
				# Incoming order's quantity is lower or equal than existing order quantity
				else:
					#print('CASE 3 MATCHING ICEBERG. PATH B')
					#print("Incoming order's quantity is LOWER or equal than existing order quantity")
					#print('INCOMING ORDER QUANTITY', incoming_order['quantity'])
					#print('EXISTING ORDER QUANTITY', matchable_order.quantity)
					matched_quantity = incoming_order['quantity']
					self.transactions_history.append(Transaction(matchable_order, incoming_order, matched_quantity))

					matchable_order.quantity = matchable_order.quantity - incoming_order['quantity']
					if matchable_order.quantity < matchable_order.peak:
						matchable_order.peak = matchable_order.quantity
					matchable_order.entry_time = datetime.now()
					incoming_order['quantity'] = 0
					self.reorder(matchable_order.direction)

	def __str__(self):
		return f'Buy orders: {self.buy_orders}, Sell orders: {self.sell_orders}'

class Transaction():

	def __init__(self, matchable_order, incoming_order, matched_quantity):

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

	def __init__(self, type, direction, id, price, quantity):
		self.type = type
		self.direction = direction
		self.id = id
		self.price = price
		self.quantity = quantity
		self.entry_time = datetime.now()

	def __asjson__(self):
		return {"id": self.id, "price": self.price, "quantity": self.quantity}

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
		self.default_peak = peak
		self.entry_time = datetime.now()

	def __asjson__(self):
		return {"id": self.id, "price": self.price, "quantity": self.peak}

	def __str__(self):
		return f'{{“id”: {self.id}, “price”: {self.price}, “quantity”: {self.peak}}}'


if __name__ == "__main__":
	order_book = OrderBook()
	# for line in fileinput.input(files=('tests/test1.in'), encoding='utf-8'):
	#for line in fileinput.input(files=('../tests/AGGRESSIVE-SELL.in'), encoding='utf-8'):
	#lst = []
	for line in sys.stdin:
		order_book.parse_order(json.loads(line))
	#	lst.append('{"buyOrders": ' + '[' + ''.join([str(o) for o in order_book.buy_orders]) + ']' ', "sellOrders": ' + '[' + ''.join([str(o) for o in order_book.sell_orders]) + ']' + '}')
	#	for i in lst:
	#		print(i)
		#print('{"buyOrders":', [str(o) for o in order_book.buy_orders], ', "sellOrders":', [
		#	  str(o) for o in order_book.sell_orders], '}')
		print(json.dumps({"buyOrders": [o.__asjson__() for o in order_book.buy_orders], "sellOrders":  [o.__asjson__() for o in order_book.sell_orders]}))
	for t in order_book.transactions_history:
		print(t)
