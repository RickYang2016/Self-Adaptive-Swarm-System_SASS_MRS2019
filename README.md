# SRSS
Self-Adaptive_Swarm_System (SASS) original version Self-Reactive Swarm-Robotic System (SRSS)

Manually Configure CORE

If setCORE.sh is not working, follow these steps to manually configure CORE.

Let the MDR node runs Micromouse automatically by adding a customized service.

$ sudo nano /etc/core/core.conf

Uncomment the line of custom_services_dir and set:

custom_services_dir = /path/you/downloaded/SRSS

Save and Exit.

$ cd /path/you/downloaded/SRSS
$ nano ./preload.py

Modify this line:

_startup = ('/path/you/downloaded/SRSS/strategy.sh',)

Save and Exit.

$ nano ./backservice.sh

Modify this line:

export ServiceHOME=/path/you/downloaded/SRSS

Save and Exit.

$ nano ~/.core/nodes.conf

Modify line 4: Add a MyService.

{ mdr mdr.gif mdr.gif {zebra OSPFv3MDR vtysh IPForward MyService}  netns {built-in type for wireless routers} }

Save and Exit.

$ chmod 755 __init__.py preload.py backservice.sh

To check whether the Micromouse service has been added, restart core-daemon and open CORE:

$ sudo service core-daemon restart
$ core-gui

$ sudo vim /etc/hosts

add:

10.0.0.1	n1
10.0.0.2	n2
10.0.0.3	n3
....
