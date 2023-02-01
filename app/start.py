"""
Note that the decorator @classmethod are used here, and class variables (not instance variables) are used here.
That is because this is required for proper functioning in asyncio. In more detail:

@classmethod is a decorator used in Python to define a method that belongs to the class and not the
instance of the class. When used with async, it creates an asynchronous class method. Class methods
can be used to share functionality between instances of a class, for example, for setup or utility
functions. In the case of an asynchronous class method, the method can run concurrently with other
async tasks and won't block the event loop. For classes used with asyncio, it is a good idea to use
class methods instead of instance methods to make sure the methods don't interfere with the
asyncio event loop or other concurrent tasks. This is because asyncio only runs async functions,
not instance methods, and to run an instance method as an async task, it must be wrapped in an
async function. So, to make it simple, you should use @classmethod for a method that is not
dependent on instance-specific data and does not modify instance-specific data, and
when the method needs to be run asynchronously in the context of an asyncio event loop.
(OpenAI ChatGPT ;))
"""

import json
import time
import os
from machine import Pin

# Micropython modules
import network
try:
    import webrepl
except ImportError:
    pass
try:
    import uasyncio as asyncio
except ImportError:
    pass

class MainApp:
    """
    A class that acts as the main code that is relevant for a project. The project must be
    implemented in this class.
    """
    # Everything used in the class could be declared locally, or preferably, like is done hereunder,
    # by using class variables. These are called in downstream classmethods by MainApp.class_variable.
    on_board_led = Pin(2, Pin.OUT)
    
    def __init__(self, sample_argument):
        self.sample_argument = sample_argument
        
        
    @classmethod
    def start_run_app(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.run_app()) # Schedule ASAP
        # Make sure you loop.run_forever() (we are a guest here)
        
        
    # Checks the status and configures if needed
    @classmethod
    async def run_app(self):
        """
        In this section you can put the actual code that is relevant for your specific project;
        Keep in mind that the code must be non-blocking! This is to make sure that it runs in
        parallel and does not block the wifi connecting code and OTA code. Feel free to add
        code as you feel fit!
        """
        while True:
            try:
                sta_if = network.WLAN(network.STA_IF)

                # print(f"sta_if.isconnected(): {sta_if.isconnected()}")

                if sta_if.isconnected() == False:
                    raise ValueError('A very specific bad thing happened')
                else:
                    # Put code here that needs an internet connection first to function.
                    # Whenever a connection is lost throughout this main code execution, in the meantime,
                    # the WifiManager will try to reconnect. If done successfully, the code returns to this segment.
                    # Since this is a asyncrounous script that needs to run concurrently with other tasks, e.g.
                    # WifiManager and OTAUpdate, this code also needs to incorporate frequent asyncio sleep statements.
                    # This is important in order to yield the processor to do other things as well.
                    # [PUT RELEVANT PROJECT CODE HERE]                   
                    print("Doing actual project-relevant tasks...")
                    # on_board_led = Pin(2, Pin.OUT)
                    for i in range(10):
                        # on_board_led.value(1)
                        MainApp.on_board_led.value(1)
                        await asyncio.sleep_ms(500)
                        #on_board_led.value(0)
                        MainApp.on_board_led.value(0)
                        await asyncio.sleep_ms(500)
                    
                    # Yielding the processor ever so often to do other tasks.
                    await asyncio.sleep_ms(5000)
                
            except Exception as exception_message:
                # Something went wrong in above script (possibly connection lost)
                print(exception_message)
                
                print("An error occurred during the execution of the main script. Possibly lost connection.")
                print("Waiting for the connection to be restored by waiting for 10 sec, after which it is reattempted")
                print("In the mean time, the parallelly run wifi connection script should retry to make a connection...")
                await asyncio.sleep_ms(10000)