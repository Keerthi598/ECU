## Raspberry Pi BLE & Ethernet LED Control System
A hybrid communication system that lets a Raspberry Pi control LEDs through both Bluetooth Low Energy (BLE) and Ethernet (CAN).
LED states remain synchronized whether commands come from a mobile app (via BLE) or an ECU (via Ethernet).

Originally built during my internship, this project explores multi-protocol synchronization between embedded and IoT systems.

### System Overview
[LED Controller]
[Raspberry Pi 4+] <--------BLE -------->[Mobile Application]

&nbsp;&nbsp;&nbsp;&nbsp;|

&nbsp;&nbsp;&nbsp;&nbsp;|

&nbsp;&nbsp;&nbsp;&nbsp;|  Ethernet (CAN)

&nbsp;&nbsp;&nbsp;&nbsp;|

&nbsp;&nbsp;&nbsp;&nbsp;|

[ECU Emulator] 
        
### :warning: Note

This project is a **proof of concept** created during my internship.  
It’s included here to highlight my work with embedded communication and hybrid networking.

Because most Bluetooth characteristics, LED mappings, and network IDs were hardcoded for a specific internal setup, this project isn’t designed to be reused or replicated without significant adaptation.


If you’re here from my [Portfolio Website](https://keerthi-ramesh.com), thank you for checking this out!  
For more hands-on projects that are easier to run or explore, you can take a look at:

-   [Note Taking Web App](https://notes-scribe.com) - a full-stack web app with authentication and live updates
-  [Portfolio Website](https://keerthi-ramesh.com) - this project’s home and overview of my other work

### Requirements

#### Hardware
-   Raspberry Pi 4 (or newer)
-   Breadboard with LEDs and resistors
-   Ethernet connection to ECU (or dummy ECU)
-   BLE-capable device (e.g., smartphone)


#### Software
-   Python 3.x
-   BLE library: `bluepy` and 'bless ble'
-   CAN/Ethernet: `python-can` or socket-based interface


Developed by me during an internship focused on embedded communication and IoT system design.  
This project bridges BLE and CAN/Ethernet communication, a small but practical exploration of how mixed-network embedded systems can stay in sync.
