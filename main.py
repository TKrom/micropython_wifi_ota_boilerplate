# Change the github repo link below. This will be used for the OTA updates for your specific project.
github_repo_link = "https://github.com/TKrom/micropython_wifi_ota_boilerplate"

"""
NOTE: The Over The Air (OTA) updates will only update the /app directory. All other files (such as in the root directory)
will not be updated. Make sure that you setup new devices with the correct root files as well. For instance the
networks.json file containing your specific WiFi hotspots of preference. Also the wifi_manager directory should be present.
The integrated WiFi manager will automatically connect to the closest WiFi hotspot you specify in the networks.json file.
If no such station is found within reasonable time, the device will setup its own AP hotspot, with which you can connect,
and then use the WEB REPL and communicate with the device as well. WEB REPL is also reachable when using regular wifi.
"""

# Now using asyncio.
import uasyncio as asyncio
# import logging
from wifi_manager import WifiManager
from app.start import MainApp

import network

# # logging.basicConfig(level=logging.WARNING)
# WifiManager.start_managing()
# asyncio.get_event_loop().run_forever()


# Below must be an ordinary function (not asyncio)
def connectToWifiAndUpdate():
    import time, machine, network, gc, app.secrets as secrets
    print('Memory free', gc.mem_free())

    from app.ota_updater import OTAUpdater
    
    otaUpdater = OTAUpdater(github_repo_link, main_dir='app', secrets_file=None)
    hasUpdated = otaUpdater.install_update_if_available()
    if hasUpdated:
        machine.reset()
    else:
        del(otaUpdater)
        gc.collect()


# Below must be an ordinary function (not asyncio)
async def startApp():
    MainApp.start_run_app()
                  

async def start_wifi_manager():
    WifiManager.start_managing()
    # asyncio.get_event_loop().run_forever() # This is no longer needed, as this is run at the end for all async scripts.


async def OTA_and_run():
    i = 1
    # Try to do this to check if there is an internet connection.
    sta_if = network.WLAN(network.STA_IF)
    
    while True:
        
        # Wrapping the whole procedure in a try-except handler in order to mitigate possible errors in main
        # script whenever an active connection is lost.
        try:
            # First check if there is an internet connection.
            if sta_if.isconnected():
                # When there is a connection execute main script here.
                print("There is internet: Doing something")
                print(sta_if.active())
                print(sta_if.ifconfig())
                await asyncio.sleep_ms(180000) # After boot wait 3 minutes before checking for updates.
                
                # [PLACE connectToWifiAndUpdate() HERE]
                # After boot, checking for updates.
                connectToWifiAndUpdate() # # Below must be an ordinary function (not asyncio)
                
                # Checking for updates every 30 minutes.
                await asyncio.sleep_ms(1800000)
                
                # [PLACE startApp() HERE]
                # In the class below the actual main script with intended added value of the project must be included.
                # startApp() # Below must be an ordinary function (not asyncio)
                # (Removing it here for now since the code must also run if there is no internet connection).
                
                
            else:
                print("No internet connection yet, waiting for automatic connection...")
                await asyncio.sleep_ms(5000)
        except Exception as exception_message:
            # Something went wrong in above script (possibly connection lost)
            print(exception_message)
            
            print("An error occurred during the execution of the main script. Possibly lost connection.")
            print("Waiting for the connection to be restored by waiting for 10 sec, after which it is reattempted")
            print("In the mean time, the parallelly run wifi connection script should retry to make a connection...")
            await asyncio.sleep_ms(10000)

   
async def main():
    # First start with starting the wifi connection and reconnection attempt architecture.
    # Whenever there is a disconnect, the connection should attempted to reconnect. Also, when there is a
    # structural connection issue, the AP mode will be activated, with which one can directly connect via wifi,
    # and then start the WEBREPL if required.
    asyncio.create_task(start_wifi_manager())

    # Then run the main script (but do first check for internet connection).
    asyncio.create_task(OTA_and_run())
    
    # Then run the actual app containing the relevant project code.
    # In the class below the actual main script with intended added value of the project must be included.
    asyncio.create_task(startApp())
    

asyncio.run(main())

# Aparently, this code below must also be executed in order to run the asycnio procedure.
asyncio.get_event_loop().run_forever()