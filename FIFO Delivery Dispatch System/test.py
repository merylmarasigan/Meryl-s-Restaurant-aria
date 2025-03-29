import json
import threading
from queue import Queue
import time
import random
from datetime import datetime

class threadSafeWriter:
    def __init__(self, file_name):
        self.lock = threading.Lock()
        self.file_name = file_name
    
    def write(self, text):
        with self.lock:
            with open(self.file_name,'a') as file:
                file.write(text)

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

class Courier:
    def __init__(self, order_counter):
        self.time_arrived = None
        self.time_received_order = None
        self.order_counter = order_counter
        self.time_of_dispatch = None
    
    def dispatch(self, travel_time,writer,ready_orders,placed_orders):
        #this function notifies when a courier has been dispatched and provides the courier's travel time 
        self.time_of_dispatch = time.time()
        text = f'The courier has been dispatched ({datetime.fromtimestamp(self.time_of_dispatch)}). They will arrive in {travel_time} seconds\n'
        writer.write(text)
        print(text)

        threading.Timer(travel_time, self.pickUpOrder, args=(ready_orders,placed_orders,writer,)).start()


    def pickUpOrder(self, ready_orders,placed_orders,writer):
        self.time_arrived = time.time()
        text = f'The courier for has arrived at the restaurant ({datetime.fromtimestamp(self.time_arrived)})\n'
        writer.write(text)
        print(text)
       
       #Picking up the order first available order
       
        if ready_orders.empty() == False or placed_orders.empty() == False:
            #This ensures that even if they arrive before an order is ready (aka while it's still being prepared), it'll wait
            order = ready_orders.get(block = True, timeout = 5)
            order_received_time = time.time()
            self.time_received_order = order_received_time
            order.setTimePickedUp(order_received_time)
            courier_wait_time = (self.time_received_order - self.time_arrived) * 1000
            order_wait_time = (order.getTimePickedUp() - order.getTimeReady()) * 1000
            text = f'\n******* Order {order.getID()} ({order.getName()}) has been picked up! ({datetime.fromtimestamp(order_received_time)}) *******\nCourier wait time: {courier_wait_time:.5f}ms\nFood wait time: {order_wait_time:.5f}ms\n'
            writer.write(text)
            print(text)
            
            # Increment the order counter
            self.order_counter.increment(courier_wait_time,order_wait_time,writer)

class OrderCounter:
    #This is a thread-safe counter of all the orders that have been picked up
    def __init__(self, total_orders):
        self.lock = threading.Lock()
        self.count = 0
        self.total_orders = total_orders
        self.food_wait_time = 0
        self.courier_wait_time = 0

    def increment(self,courier_wait_time, order_wait_time,writer):
        with self.lock:
            self.count += 1
            self.food_wait_time += order_wait_time
            self.courier_wait_time += courier_wait_time
            if self.count == self.total_orders:  
                #When all orders have been picked, it will calculate and print out average courier and order wait time in ms
                text = f'----------------------------------------------------------------------------------------------------------------------------\nAverage Courier Wait Time: {self.courier_wait_time/self.total_orders} ms\nAverage Order Wait Time: {self.food_wait_time/self.total_orders} ms'
                writer.write(text)
                print(text)


def prepareOrder(placed_orders, ready_orders, writer):
    #this function prepares the first order on the placed_orders queue
    # order = placed_orders.get()
    # ready_orders.put(order)
    # order.setTimeReady(time.time())
    # text = f'Order {order.getID()} ({order.getName()}) is ready for pick up!\n'
    # writer.write(text)
    # print(text)

    order = placed_orders.get()  # Get the order
    # Simulate prep time without sleep using event
    order_prep_time = order.getPrepTime()
    threading.Timer(order_prep_time, lambda: ready_orders.put(order)).start()
    order.setTimeReady(time.time())
    text = f'Order {order.getID()} ({order.getName()}) is ready for pick up!\n'
    writer.write(text)
    print(text)

   

def read_entries(data, index, ready_orders, placed_orders, order_counter,writer):
    entries_to_read = min(2, len(data) - index)

    for i in range(entries_to_read):
        order = data[index + i]
        new_order = Order(order['id'], order['name'], order['prepTime'])

        # PLACING ORDER
        placed_orders.put(new_order)
        time_order_placed = time.time()
        text = f'Order {new_order.getID()} ({new_order.getName()}) received! ({datetime.fromtimestamp(time_order_placed)})\n'
        writer.write(text)
        print(text)

        # DISPATCHING THE COURIER
        courier = Courier(order_counter)
        travel_time = random.randint(3, 15)
        courier.dispatch(travel_time,writer,ready_orders,placed_orders)
        
        # SIMULATING TRAVEL TIME
        # threading.Timer(travel_time, courier.pickUpOrder, args=(ready_orders,placed_orders,writer,)).start()

       
        # PREPARING THE ORDER
        prep_event = threading.Event()
        prep_thread = threading.Thread(target = prepareOrder, args=(placed_orders,ready_orders,writer,prep_event))
        prep_thread.start()


    index += entries_to_read

    if index < len(data):
        threading.Timer(1, read_entries, args=(data, index, ready_orders, placed_orders, order_counter,writer)).start()

def main():
    placed_orders = Queue()
    ready_orders = Queue()

   

    with open('dispatch_orders_copy.json', 'r') as file:
        data = json.load(file)
    
    writer = threadSafeWriter('output.txt')

    total_orders = len(data)  # Total number of orders
    order_counter = OrderCounter(total_orders)  # Initialize the order counter
    read_entries(data, 0, ready_orders, placed_orders, order_counter,writer)

if __name__ == '__main__':
    main()
