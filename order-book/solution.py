import fileinput

import json

from datetime import datetime

class OrderBook():
    def __init__(self):
        self.orders = []
        self.buy_orders = []
        self.sell_orders = []

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
      if order['direction'] == 'Buy':
          order_book = self.sell_orders
      else:
          order_book = self.buy_orders
      if order_book[0]['price'] == order['price']:
         return True
      else:
         return False
      
    def get_fillable_orders(self, order):
      if order['direction'] == 'Buy':
          order_book = self.sell_orders
      else:
          order_book = self.buy_orders
      return list(
        filter(
            lambda o: o.price == order['price'],
            order_book
        )
      )
    
    def aggressive_fill(self, order, fillable_orders):
      order_quantity = order['quantity']
      if order_quantity > sum(o.quantity for o in fillable_orders):
        while order_quantity > 0 and fillable_orders:
            order_quantity = order_quantity - fillable_orders.pop().quantity
            if order['direction'] == 'Buy':
               self.sell_orders.pop()
            else:
               self.buy_orders.pop()
        
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

    def parse_order(self, order):
       pass

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

    def __str__(self):
       return f'{{“id”: {self.id}, “price”: {self.price}, “quantity”: {self.peak}}}'
    
    def update(self, value):
       self.quantity = self.quantity - value
       if self.peak < self.quantity:
          self.peak = self.quantity
       # Controls the LimitOrder and Remainder which belong to Iceberg Order instance
       pass


if __name__ == "__main__":
    order_book = OrderBook()
    for line in fileinput.input(files=('tests/test1.in'), encoding='utf-8'):
      order_book.add_order(json.loads(line))
      print('buyOrders:', [str(o) for o in order_book.buy_orders], 'sellOrders:', [str(o) for o in order_book.sell_orders])
      
