# Order Dispatch System

## Description
This project implements a thread-safe order dispatch system for a restaurant. It simulates the process of order intake, order preparation,  courier dispatchings, and courier pickup in a first-come-first-serve  pick-up system (meaning, a courier can only pick up the first available order upon their arrival). The program also  tracks the time taken for each step and calculates an average for courier and order wait times.The program reads orders from a JSON file, processes them concurrently, and logs the results in a text file.

## Features
- Thread-safe writing to a file
- Concurrent handling of orders using threads
- Calculation of average wait times for couriers and food
- JSON input for orders with unique IDs
- Detailed logging of each step in the order process

## Requirements
- Python 3.x
- `json` module (standard library)
- `threading` module (standard library)
- `queue` module (standard library)
- `datetime` module (standard library)
- `time` module (standard library)
- `queue` module (standard library)
- `random` module (standard library)
   
## Input Format
The input json should should have an array of order objects, each containing the following: 
1. `id` : A unique identifier number of an order
2. `name`: Name of the order (usually described as the order that the food contains)
3. `prepTime`: The amount of time it takes to prepare the food (in seconds)

Example:
```json
{
    "id": "a8cfcb76-7f24-4420-a5ba-d46dd77bdffd", 
    "name": "Banana Split",
    "prepTime": 4
}
```

## Usage
1. Edit the ```with open('dispatch_orders.json','r') as file:``` line inside `main()` so that `'dispatch_order.json'` is replaced by the appropriate json file name. 
2. Ensure that `FIFO_delivery_output.txt` is a blank file (optional)
3. In the directory of the program file,run the main script by running ```python FIFO_delivery.py``` in the command line/terminal.

## Output
1. The results will be printed to console in real-time
2. The results will also be logged in `FIFO_delivery_output.txt`, including:

* When each order is received
* When each courier is dispatched
* When the order is done being prepared
* When each order is picked up
* Average courier wait time and food wait time after all orders are processed