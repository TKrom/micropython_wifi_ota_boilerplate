# Micropython WiFi OTA Boilerplate

A boilerplate (base template) written in MicroPython for IoT projects running on Microcontrollers such as the ESP32 that
require an active wifi connection and remote Over The Air (OTA) updates. Use this to easily build and manage your IoT-enabled and hard to reach solutions.

# Setup:
1) Fork this repository and name it to whatever suits your project. Later the device will use this repo to synchronize and perform OTA updates with.
2) Add your preferred WiFi networks to the networks.json file and save this to your device locally (be careful not to push this to the GitHub repo). You can also change the AP hotspot name of the device. This will only be used whenever no of the provided WiFi hotspots are available or near. In that case, still one can connect to the device and use the WEB REPL (of course this is also possible over the regular WiFi connections).
3) In the main.py file change the github_repo_link variable to your newly created GitHub repo link.
4) Add custom project-specific code to the /app/start.py file. You can build your project in the MainApp class. Make sure that all code you write is **non-blocking**, i.e., allows the other processes (wifi-manager and OTA updater) to run concurrently.
5) Enjoy your IoT device that will connect to specified WiFi stations and which can be managed and updated completely remotely. This is particularly useful for hard to reach remote applications.

# Credits
This code is completely based on the work of:
* @rdehuyss (https://github.com/rdehuyss/micropython-ota-updater)
* @mitchins (https://github.com/mitchins/micropython-wifimanager)

This work is solely an integration of both of the aforementioned works. Please refer to these repositories for in-depth information of the underlying modules.