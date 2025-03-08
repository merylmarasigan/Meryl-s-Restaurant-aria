# Meryl's-Restaurant-aria
## Overview

This restaurant pick up system using multithreading in Python. It efficiently manages order preparation and courier dispatch while ensuring thread safety for shared resources.

## Features

- Thread-Safe File Writing: Ensures that logs are written without race conditions.

- Thread-Safe Dictionary & Queue: Maintains a safe record of ready-for-pickup orders.

- Thread-Safe Counter: Tracks order pickup statistics and calculates average wait times.

- Order Processing: Handles order preparation and logging.

- Courier Dispatch: Simulates courier travel and order pickup with wait time tracking.

- Asynchronous Execution: Uses Python threads and timers to manage concurrent processes.

## Dependencies

- Python 3.x

- json module (standard library)

- threading module (standard library)

- queue module (standard library)

- datetime module (standard library)

- time module (standard library)

- random module (standard library)

## Installation

- Clone the repository and ensure Python 3.x is installed.

# Clone the repository
- git clone <repository_url>
- cd <repository_directory>

## Usage

Ensure you have an order file named dispatch_orders_copy.json in the same directory. This file should contain JSON-formatted order details.

### Run the script:

`python FIFO_delivery.py` or `python Matched_delivery.py`

## Expected Output

- Logs in matched_delivery_output.txt and output.txt

- Console output showing order placement, courier dispatch, and pickup timing.

## File Structure

- FIFO_delivery.py: Main script to run the first simulation.

- Matched_delviery_script.py: Alternative script with a queue-based approach.

- dispatch_orders_copy.json: JSON file containing order data.

- matched_delivery_output.txt: Output file logging order events and average wait times.

- output.txt: Additional log file for the queue-based implementation.

## How It Works

- FIFO_delivery.py
  - Orders are read from dispatch_orders_copy.json.

  - Each order is processed and assigned a preparation time.
    
  - A courier is dispatched with a random travel time.
 

  - The courier waits until the order is ready before picking it up.
    
  - The pickup time is recorded and average wait times are calculated.

-Matched_Delivery.py

  - Uses Queue instead of a dictionary to store placed and ready orders.

  - Couriers pick up the first available order once they arrive.

  - Wait times are calculated similarly.

## Example Order Format

[
  {"id": 1, "name": "Burger", "prepTime": 5},
  {"id": 2, "name": "Pizza", "prepTime": 8}
]
