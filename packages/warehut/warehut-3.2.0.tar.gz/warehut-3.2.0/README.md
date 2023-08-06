# warehut

## Installation
```sh
pip install warehut
```

## Example

```py
import time
import datetime
import random

from warehut import Warehut
from warehut import Producer
from warehut import Consumer, listen

# There also exists a `Hybrid` worker,
# that can both listen to events and
# when responding, can forward to other consumers.
# Use this with caution and consideration.

from warehut.worker import Worker



class MyWarehut(Warehut):
    def handle_error(self, worker_type: type[Worker], exception: Exception):
        # Handle exception raised within a worker process
        # You could launch a window, write the error to a log file, etc.

        # Stopping all other workers
        self.stop()

        # And printing the error
        print(
            f'\nWorker of type {worker_type.__name__} '
            f'encountered an error.\n{exception!r}\n')



class MyProducer(Producer):

    async def __aenter__(self):
        print(f'Preparing environment for {self}')

    async def __aexit__(self, exc_type, exc_value, trace):
        print(f'Gracefully closing environment for {self}')
    
    async def update(self):
        # Put whatever you want your producer to do, here.
        # It can read from any source and `forward` data to consumer queues.
        # This method is run on repeat in-between status checks of the worker.

        # Forward the current timestamp to 'ping'
        self.forward('ping', time.time())
        print('Pinged!')
        
        # Sleep a random amount of time to create obvious offset
        time.sleep(random.random() * 2)

        # Forward a randomly generated number to 'random'
        self.forward('random', random.randint(0, 100))
        print('Randomed!')

        # Sleep again ... same reason.
        time.sleep(random.random() * 2)


class MyConsumer(Consumer):
    
    async def __aenter__(self):
        print(f'Preparing environment for {self}')

    async def __aexit__(self, exc_type, exc_value, trace):
        print(f'Gracefully closing environment for {self}')


    # `listen` defines a function to be called with data
    # that is labeled with the specified event name.
    
    @listen('ping')
    async def on_ping(self, timestamp):
        """Print the time at which a ping was sent"""        
        timestamp = datetime.datetime.fromtimestamp(int(timestamp))
        print(f'Ping at {timestamp.strftime("%Y-%m-%d %H:%M:%S")}')
    
    @listen('random')
    async def on_random(self, number):
        """Print generated random numbers"""

        if number > 80:
            raise RuntimeError('An error to show off the `Warehut` error handler')

        print(f'Random number generated: {number}')



if __name__ == '__main__':
    
    with MyWarehut([MyProducer, MyConsumer]):
        # `Warehut.start` is called upon entering the context
        input('\nPress Enter to exit\n\n')
        # `Warehut.stop` is called upon exiting the context


    # They can be called on their own with the same effect
    # 
    # Ex.
    # warehut = MyWarehut([MyProducer, MyConsumer])
    # warehut.start()
    # input('\nPress Enter to exit\n\n')
    # warehut.stop()
```