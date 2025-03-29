import json
import threading
from queue import Queue
import time
import random
from datetime import datetime

class threadSafeDict:
    # CREATING A THREAD-SAFE DICTIONARY (ID:ORDER ITEM) THAT HOLDS ORDERS THAT ARE READY 
    def __init__(self):
        self.dict = dict()
        self.lock = threading.Lock()
    
    def add(self, key, value):
        with self.lock:
            self.dict[key] = value
    
    def remove(self, key):
        with self.lock:
            del self.dict[key]
        
    def getDict(self):
        with self.lock:
            return self.dict

class Order:
    def __init__(self, id, name, prep_time):
        self.id = id 
        self.name = name
        self.prep_time = prep_time
        self.time_ready = None
        self.time_picked_up = None
    
    def getID(self):
        return self.id
    
    def getName(self):
        return self.name
    
    def getPrepTime(self):
        return self.prep_time
    
    def getTimeReady(self):
        return self.time_ready
    
    def setTimeReady(self, time_ready):
        self.time_ready = time_ready
    
    def getTimePickedUp(self):
        return self.time_picked_up
    
    def setTimePickedUp(self, pickup_time):
        self.time_picked_up = pickup_time

    def prepare(self, ready_orders):
        # ADDING ORDER TO THE DICTIONARY OF READY ORDERS
        ready_orders.add(self.id, self)
        self.time_ready = time.time()
        print(f'Order {self.id} ({self.name}) is ready for pick up! ({datetime.fromtimestamp(self.time_ready)})')

class Courier:
    def __init__(self, assigned_order, order_counter):
        self.assigned_order = assigned_order
        self.time_arrived = None
        self.time_received_order = None
        self.order_counter = order_counter
    
    def dispatch(self, travel_time):
        time_of_dispatch = time.time()
        print(f'The courier for Order {self.assigned_order} has been dispatched ({datetime.fromtimestamp(time_of_dispatch)}). They will arrive in {travel_time} seconds')

    def pickUpOrder(self, ready_orders, placed_orders):
        self.time_arrived = time.time()
        print(f'The courier for Order {self.assigned_order} has arrived at the restaurant ({datetime.fromtimestamp(self.time_arrived)})')
        orders = ready_orders.getDict()

        while self.assigned_order not in orders.keys():
            # WHILE THE ORDER IS NOT READY, JUST WAIT
            pass

        order = orders[self.assigned_order]
        order_received_time = time.time()
        self.time_received_order = order_received_time
        order.setTimePickedUp(order_received_time)
        print()
        courier_wait_time = (self.time_received_order - self.time_arrived) * 1000
        order_wait_time = (order.getTimePickedUp() - order.getTimeReady()) * 1000
        print(f'******* Order {order.getID()} ({order.getName()}) has been picked up! ({datetime.fromtimestamp(order_received_time)}) *******\nCourier wait time: {courier_wait_time:.5f}ms\nFood wait time: {order_wait_time:.5f}ms\n')
        
        # Increment the order counter
        self.order_counter.increment(courier_wait_time,order_wait_time)

class OrderCounter:
    def __init__(self, total_orders):
        self.lock = threading.Lock()
        self.count = 0
        self.total_orders = total_orders
        self.food_wait_time = 0
        self.courier_wait_time = 0

    def increment(self,courier_wait_time, order_wait_time):
        with self.lock:
            self.count += 1
            self.food_wait_time += order_wait_time
            self.courier_wait_time += courier_wait_time
            if self.count == self.total_orders:  # Check if all orders are processed
                print('----------------------------------------------------------------------------------------------------------------------------')
                print(f'Average Courier Wait Time: {self.courier_wait_time/self.total_orders} ms')
                print(f'Average Order Wait Time: {self.food_wait_time/self.total_orders} ms')
def read_entries(data, index, ready_orders, placed_orders, order_counter):
    entries_to_read = min(2, len(data) - index)

    for i in range(entries_to_read):
        order = data[index + i]
        new_order = Order(order['id'], order['name'], order['prepTime'])

        # PLACING ORDER
        placed_orders.put(new_order)
        time_order_placed = time.time()
        print(f'Order {new_order.getID()} ({new_order.getName()}) received! ({datetime.fromtimestamp(time_order_placed)})')

        # DISPATCHING THE COURIER
        courier = Courier(new_order.getID(), order_counter)
        travel_time = random.randint(3, 15)
        
        courier.dispatch(travel_time)
        
        # SIMULATING TRAVEL TIME
        threading.Timer(travel_time, courier.pickUpOrder, args=(ready_orders, placed_orders,)).start()

        # PREPARING THE ORDER
        threading.Timer(new_order.getPrepTime(), new_order.prepare, args=(ready_orders,)).start()

    index += entries_to_read

    if index < len(data):
        threading.Timer(1, read_entries, args=(data, index, ready_orders, placed_orders, order_counter)).start()

def main():
    placed_orders = Queue()
    ready_orders = threadSafeDict()

    with open('dispatch_orders.json', 'r') as file:
        data = json.load(file)

    total_orders = len(data)  # Total number of orders
    order_counter = OrderCounter(total_orders)  # Initialize the order counter
    read_entries(data, 0, ready_orders, placed_orders, order_counter)

if __name__ == '__main__':
    main()
