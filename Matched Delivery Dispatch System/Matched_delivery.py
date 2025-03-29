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


class threadSafeDict:
    #Creating a thread-safe dictionary {id: order} that holds orders that are ready for pick up (Operating under the assumption that each order ID is unique)
    def __init__(self):
        self.dict = dict()
        self.lock = threading.Lock()
    
    def add(self,key,value):
        with self.lock:
            self.dict[key] = value
    
    def pop(self,key):
        with self.lock:
            return self.dict.pop(key)
        
    def getDict(self):
        with self.lock:
            return self.dict
class Counter:
    #This is a thread-safe counter of all orders that have been picked up
    def __init__(self,total_orders):
        self.lock = threading.Lock()
        self.num_picked_up = 0 
        self.total_orders = total_orders
        self.food_wait_time = 0
        self.courier_wait_time = 0 

    def increment(self, courier_wait_time, order_wait_time,writer):
        with self.lock:
            #each time an order is picked up, we increment number of orders that have been picked up and add the courier and order wait time so we can later calculate average
            self.num_picked_up += 1
            self.food_wait_time += order_wait_time
            self.courier_wait_time += courier_wait_time

            if self.num_picked_up == self.total_orders:
                #When all orders have been picked up, print the average courier and order wait time
                text = f"----------------------------------------------------------------------------------------------------------------------------\nAverage Courier Wait Time: {self.courier_wait_time/self.total_orders} ms\nAverage Order Wait Time: {self.food_wait_time/self.total_orders} ms"
                print(text)
                writer.write(text)
                print("PROGRAM DONE EXECUTING")



class Order:
    def __init__(self,id,name,prep_time):
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
    def setTimeReady(self,time_ready):
        self.time_ready = time_ready
    
    def getTimePickedUp(self):
        return self.time_picked_up
    def setTimePickedUp(self,pickup_time):
        self.time_picked_up = pickup_time

    def prepare(self,ready_orders,writer):
        #Once the order is done preparing, it is added to the dictionary of ready orders
        ready_orders.add(self.id,self)
        self.time_ready = time.time()
        
        text = f'Order {self.id} ({self.name}) is ready for pick up! ({datetime.fromtimestamp(self.time_ready)})\n'
        writer.write(text)
        print(text)


class Courier:
    def __init__(self,assigned_order,counter):
        self.assigned_order = assigned_order
        self.time_arrived = None
        self.time_received_order = None
        self.counter = counter
    
    def getAssignedOrder(self):
        return self.assigned_order

    
    def dispatch(self, travel_time,writer):
        time_of_dispatch = time.time()
        text = f'The courier for Order {self.assigned_order} has been dispatched ({datetime.fromtimestamp(time_of_dispatch)}). They will arrive in {travel_time} seconds.\n'
        writer.write(text)
        print(text)

    def pickUpOrder(self,ready_orders,counter,writer):
       
        self.time_arrived = time.time()
        text =f'The courier for Order {self.assigned_order} has arrived at the restaurant ({datetime.fromtimestamp(self.time_arrived)}).\n'
        writer.write(text)
        print(text)
        orders = ready_orders.getDict()

        while self.assigned_order not in orders.keys():
            #while the order is not ready, just wait
            pass

        #picking up the order
        order = ready_orders.pop(self.assigned_order)
        order_received_time = time.time()
        self.time_received_order = order_received_time
        order.setTimePickedUp(order_received_time)
        courier_wait_time = (self.time_received_order - self.time_arrived)* 1000
        order_wait_time = (order.getTimePickedUp() - order.getTimeReady()) * 1000
        text = f'\n******* Order {order.getID()} ({order.getName()}) has been picked up! ({datetime.fromtimestamp(order_received_time)}) *******\nCourier wait time: {courier_wait_time:.5f}ms\nFood wait time: {order_wait_time:.5f}ms\n'
        writer.write(text)
        print(text)

        #Increment counter
        self.counter.increment(courier_wait_time,order_wait_time,writer)


def read_entries(data,index,ready_orders,counter,writer):

    #Processing at most two orders per second
    entries_to_read = min(2,len(data) - index)

    for i in range(entries_to_read):
        order = data[index +i]
        new_order = Order(order['id'],order['name'],order['prepTime'])

        #Placing order
        #placed_orders.put(new_order)
        time_order_placed  = time.time()
        text = f'Order {new_order.getID()} ({new_order.getName()}) received! ({datetime.fromtimestamp(time_order_placed)})\n'
        writer.write(text)
        print(text)

        #Dispatching the courier
        courier = Courier(new_order.getID(), counter)
        travel_time = random.randint(3,15)
        
        courier.dispatch(travel_time,writer)
        
        #Simulating travel time
        threading.Timer(travel_time,courier.pickUpOrder, args=(ready_orders,counter,writer)).start()

        #Simulating prep time
        threading.Timer(new_order.getPrepTime(),new_order.prepare, args=(ready_orders,writer)).start()

    index += entries_to_read

    if index < len(data):
        threading.Timer(1,read_entries, args=(data,index,ready_orders,counter,writer)).start()



def main():
    ready_orders = threadSafeDict()

    with open('dispatch_orders_copy.json','r') as file:
        data = json.load(file)

    counter = Counter(len(data))
    write_to = "matched_delivery_output.txt"
    writer = threadSafeWriter(write_to)
    
    read_entries(data,0,ready_orders,counter,writer)

    

if __name__ == '__main__':
    main()


