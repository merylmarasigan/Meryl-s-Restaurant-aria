import unittest
from unittest.mock import MagicMock
from queue import Queue
import time
import threading
from datetime import datetime
import random
import unittest.util

# Importing classes from the delivery module
from FIFO_delivery import threadSafeWriter, Order, Courier, OrderCounter, prepareOrder, placeOrder

# class TestPlacedOrderAndReadyOrder(unittest.TestCase):
#     def setUp(self):
#         self.writer = threadSafeWriter('unittest_output.txt')  
#         self.placed_orders = Queue()
#         self.ready_orders = Queue()
#         self.order_counter = OrderCounter(4)

#         self.order_data = [
#             {"id":7, "name": "Poke Bowl", "prepTime": 2},
#             {"id":29, "name": "Pasta", "prepTime": 5},
#             {"id":19, "name": "Bagel", "prepTime": 3},
#             {"id":99, "name": "Chips", "prepTime": 3},
#         ]

#     def test_add_to_placed_order(self):
#         order1 = Order(self.order_data[0]['id'],self.order_data[0]['name'],self.order_data[0]['prepTime'])
#         placeOrder(order1,self.placed_orders,self.writer)
#         self.assertEqual(self.placed_orders.qsize(), 1)

#         order2 = Order(self.order_data[1]['id'],self.order_data[1]['name'],self.order_data[1]['prepTime'])
#         placeOrder(order1,self.placed_orders,self.writer)
#         self.assertEqual(self.placed_orders.qsize(), 2)
    
#     def test_lists_after_preparing(self):
#         order1 = Order(self.order_data[0]['id'],self.order_data[0]['name'],self.order_data[0]['prepTime'])
#         placeOrder(order1,self.placed_orders,self.writer)

#         order2 = Order(self.order_data[1]['id'],self.order_data[1]['name'],self.order_data[1]['prepTime'])
#         placeOrder(order1,self.placed_orders,self.writer)

#         prepareOrder(self.placed_orders, self.ready_orders,self.writer)
#         self.assertEqual(self.placed_orders.qsize(), 1)
#         self.assertEqual(self.ready_orders.qsize(),1)

#         prepareOrder(self.placed_orders,self.ready_orders,self.writer)
#         self.assertEqual(self.placed_orders.qsize(),0)
#         self.assertEqual(self.ready_orders.qsize(), 2)

#     def test_lists_after_prep_and_pickup(self):

#         #receiving an order
#         order1 = Order(self.order_data[0]['id'],self.order_data[0]['name'],self.order_data[0]['prepTime'])
#         #placing an order
#         placeOrder(order1,self.placed_orders,self.writer)
#         self.assertEqual(self.placed_orders.qsize(), 1)
#         courier = Courier(self.order_counter)
#         #set travel time to zero for instant pick up
       
#         prepareOrder(self.placed_orders,self.ready_orders,self.writer)
#         #check that the order is ready
#         self.assertEqual(self.placed_orders.qsize(), 0)
#         self.assertEqual(self.ready_orders.qsize(), 1)
#         #allow the courier to arrive to the store and pick up the order
#         courier.dispatch(1,self.writer,self.ready_orders,self.placed_orders)
#         time.sleep(5)
#         self.assertEqual(self.ready_orders.qsize(), 0)

# class TestingPrepTime(unittest.TestCase):
#     def setUp(self):
#         self.writer = threadSafeWriter('unittest_output.txt')  
#         self.placed_orders = Queue()
#         self.ready_orders = Queue()
#         self.order_counter = OrderCounter(4)

#         self.order_data = [
#             {"id":7, "name": "Poke Bowl", "prepTime": 2},
#             {"id":29, "name": "Pasta", "prepTime": 5},
#             {"id":19, "name": "Bagel", "prepTime": 3},
#             {"id":99, "name": "Chips", "prepTime": 3},
#         ]
    

#     def testPrepTime(self):
#         for i in range(len(self.order_data)):
#             data = self.order_data[i]
#             order = Order(data['id'],data['name'],data['prepTime'])
#             #place the order
#             placeOrder(order,self.placed_orders,self.writer)

#             #preparing order
#             start_prep = time.time()
#             prepareOrder(self.placed_orders, self.ready_orders, self.writer)
#             #end_prep = time.time()

#             self.assertLessEqual(order.time_ready - start_prep,0.5)


# class TestSingleCourierArrival(unittest.TestCase):
    
#     def setUp(self):
#         self.writer = threadSafeWriter('unittest_output.txt') 
#         self.placed_orders = Queue()
#         self.ready_orders = Queue()
#         self.order_counter = OrderCounter(1)  # Only one order for the test

#         # Create sample orders for testing
#         self.order_data =[{"id": 1, "name": "Pizza", "prepTime": 5},
#             {"id": 2, "name": "Sushi", "prepTime": 3},
#             {"id": 3, "name": "Burger", "prepTime": 4},
#         ]
        
#         new_order = Order(self.order_data[0]['id'], self.order_data[0]['name'], self.order_data[0]['prepTime'])
#         placeOrder(new_order, self.placed_orders, self.writer)

#     def test_single_courier_arrival(self):
#         courier = Courier(self.order_counter)
#         travel_time = 3  # Fixed travel time for testing
        
#         # Dispatch the courier
#         courier.dispatch(travel_time, self.writer, self.ready_orders, self.placed_orders)

#         # Simulate order preparation
#         threading.Timer(self.order_data[0]['prepTime'], prepareOrder, args=(self.placed_orders, self.ready_orders, self.writer)).start()

#         # Allow some time for the courier to arrive and pick up the order
#         time.sleep(travel_time + 1)
        
#         # Ensure the arrival time is approximately after the travel time
#         self.assertGreaterEqual(courier.time_arrived, courier.time_of_dispatch + travel_time, 
#                                 "Courier did not arrive after specified travel time.")

#     def test_multiple_courier_arrivals(self):
#         # Placing orders in the queue
#         for order in self.order_data[1:]:
#             new_order = Order(order['id'], order['name'], order['prepTime'])
#             placeOrder(new_order, self.placed_orders, self.writer)
        
#         couriers = []
#         courier_travel_times = [3, 4, 2]

#         for i in range(len(self.order_data)):
#             courier = Courier(self.order_counter)
#             travel_time = courier_travel_times[i]
#             couriers.append(courier)

#             # Dispatch couriers
#             courier.dispatch(travel_time, self.writer, self.ready_orders, self.placed_orders)
        
#         # Simulate order preparation
#         for order in self.placed_orders.queue:
#             threading.Timer(order.getPrepTime(), prepareOrder, args=(self.placed_orders, self.ready_orders, self.writer)).start()
        
#         # Allow some time for the couriers to arrive
#         time.sleep(5)

#         for courier in couriers:
#             self.assertGreaterEqual(courier.time_arrived, courier.time_of_dispatch + min(courier_travel_times),
#                                     "Courier did not arrive after specified travel time.")

# class TestWaitTimeCalculations(unittest.TestCase):
#     def setUp(self):
#         self.writer = threadSafeWriter('unittest_output.txt')  
#         self.placed_orders = Queue()
#         self.ready_orders = Queue()
#         self.order_counter = OrderCounter(4)

#         self.order_data = [
#             {"id":7, "name": "Poke Bowl", "prepTime": 2},
#             {"id":29, "name": "Pasta", "prepTime": 5},
#             {"id":19, "name": "Bagel", "prepTime": 3},
#             {"id":99, "name": "Chips", "prepTime": 3},
#         ]
    
#     def testWaitTimeCGTO(self):

#         #in this test case, order prep time = 2 and courier travel time = 5
#         o = self.order_data[0]
#         order = Order(o['id'],o['name'],o['prepTime'])

#         #placing the order
#         placeOrder(order,self.placed_orders,self.writer)
#         courier_travel_time = 5
#         wait_time = max(order.getPrepTime(),courier_travel_time)

#         #dispatching the courier
#         courier = Courier(self.order_counter)
#         courier.dispatch

#         #preparing the order
#         threading.Timer(order.getPrepTime(),prepareOrder, args=(self.placed_orders, self.ready_orders, self.writer)).start()

#         #allowing the program enough time for courier to get there and for order to be ready
#         time.sleep(wait_time)

#         #picking up the order
#         courier.pickUpOrder(self.ready_orders,self.placed_orders,self.writer)

#         order_wait_time = order.getTimePickedUp() - order.getTimeReady()
#         courier_wait_time = courier.time_received_order - courier.time_arrived

#         # self.assertAlmostEqual(order_wait_time, time_picked_up - time_order_ready)
#         self.assertGreater(order_wait_time, courier_wait_time)

#     def testWaitTimeOGTC(self):
#         o = self.order_data[1]
#         order = Order(o['id'],o['name'],o['prepTime'])

#         #placing the order
#         placeOrder(order,self.placed_orders,self.writer)
#         courier_travel_time = 2
#         wait_time = max(order.getPrepTime(),courier_travel_time)

#         #dispatching the courier
#         courier = Courier(self.order_counter)
#         courier.dispatch(wait_time,self.writer, self.ready_orders, self.placed_orders)

#         #preparing the order
#         threading.Timer(order.getPrepTime(),prepareOrder, args=(self.placed_orders, self.ready_orders, self.writer)).start()

#         #allowing the program enough time for courier to get there and for order to be ready
#         time.sleep(wait_time)

#         #picking up the order
#         courier.pickUpOrder(self.ready_orders,self.placed_orders,self.writer)

#         order_wait_time = order.getTimePickedUp() - order.getTimeReady()
#         courier_wait_time = courier.time_received_order - courier.time_arrived

#         self.assertGreater(courier_wait_time,order_wait_time)

class TestAverages(unittest.TestCase):
    def setUp(self):
        self.writer = threadSafeWriter('unittest_output.txt')  
        self.placed_orders = Queue()
        self.ready_orders = Queue()
        self.order_counter = OrderCounter(4)

        self.order_data = [
            {"id":7, "name": "Poke Bowl", "prepTime": 2},
            {"id":29, "name": "Pasta", "prepTime": 5},
            {"id":19, "name": "Bagel", "prepTime": 3},
            {"id":99, "name": "Chips", "prepTime": 3},
        ]

        self.travel_times = [1,1,1,1]
        self.travel_times2 = [1,3,5,7]



    # def testWaitAveragesSameTravelTime(self):
    #     courier_wait_times = []
    #     order_wait_times = []

    #     for i in range(len(self.order_data)):
    #         o = self.order_data[i]
    #         order = Order(o['id'],o['name'], o['prepTime'])

    #         #placing order
    #         placeOrder(order, self.placed_orders, self.writer)

    #         #wait_time = max(order.getPrepTime(), self.travel_times[i])
            
    #         #dispatching the courier
    #         courier = Courier(self.order_counter)
    #         courier.dispatch(1,self.writer, self.ready_orders, self.placed_orders)

    #         #preparing the order
    #         prepareOrder(self.placed_orders, self.ready_orders, self.writer)

    #         #allowing the program to wait til the courier is at the restaurant and the order is ready
    #         time.sleep(3)

    #         courier.pickUpOrder(self.ready_orders, self.placed_orders, self.writer)
    #         courier_wait_time = courier.time_received_order-courier.time_arrived
    #         order_wait_time = order.getTimePickedUp() - order.getTimeReady()

    #         courier_wait_times.append(courier_wait_time)
    #         order_wait_times.append(order_wait_time)
        
    #     time.sleep(5)
        
    #     courier_avg = sum(courier_wait_times)/len(courier_wait_times)
    #     order_avg = sum(order_wait_times)/len(order_wait_times)

    #     print(f'courier wait times: {courier_wait_times}, courier_avg: {courier_avg}\norder wait times: {order_wait_times}, order_avg: {order_avg}')
    #     print(f'c_avg: {self.order_counter.c_avg}\no_avg: {self.order_counter.o_avg}')
              
        # self.assertEqual(self.order_counter.o_avg ,order_avg*1000)
        # self.assertEqual(self.order_counter.c_avg ,courier_avg*1000)

    def testWaitAveragesDiffTravelTime(self):
        courier_wait_times = []
        order_wait_times = []

        for i in range(len(self.order_data)):
            o = self.order_data[i]
            order = Order(o['id'],o['name'], o['prepTime'])

            #placing order
            placeOrder(order, self.placed_orders, self.writer)

            #wait_time = max(order.getPrepTime(), self.travel_times2[i])
            
            #dispatching the courier
            courier = Courier(self.order_counter)
            courier.dispatch(self.travel_times2[i],self.writer, self.ready_orders, self.placed_orders)

            #preparing the order
            prepareOrder(self.placed_orders, self.ready_orders, self.writer)

            #allowing the program to wait til the courier is at the restaurant and the order is ready
            time.sleep(order.getPrepTime() + self.travel_times2[i])

            courier.pickUpOrder(self.ready_orders, self.placed_orders, self.writer)
            courier_wait_time = courier.time_received_order - courier.time_arrived
            order_wait_time = order.getTimePickedUp() - order.getTimeReady()

            courier_wait_times.append(courier_wait_time)
            order_wait_times.append(order_wait_time)
        courier_avg = sum(courier_wait_times)/len(courier_wait_times)
        order_avg = sum(order_wait_times)/len(order_wait_times)
       
        time.sleep(2)
        # self.assertEqual(self.order_counter.o_avg ,order_avg*1000)
        # self.assertEqual(self.order_counter.c_avg ,courier_avg*1000)



if __name__ == '__main__':
    unittest.main()
