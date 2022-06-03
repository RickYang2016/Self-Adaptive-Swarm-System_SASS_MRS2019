# Hierarchical Needs Based SASS

## Abtract
Research in multi-robot and swarm systems has seen significant interest in cooperation of agents in complex and dynamic environments. 
To effectively adapt to unknown environments and maximize the utility of the group, robots need to cooperate, share information, and make a suitable plan according to the specific scenario. Inspired by Maslow's hierarchy of human needs and systems theory, we introduce Robot's Need Hierarchy and propose a new solution called Self-Adaptive Swarm System (SASS). It combines multi-robot perception, communication, planning, and execution with the cooperative management of conflicts through a distributed Negotiation-Agreement Mechanism that prioritizes robot's needs. We also decompose the complex tasks into simple executable behaviors through several Atomic Operations, such as selection, formation, and routing. We evaluate SASS through simulating static and dynamic tasks and comparing them with the state-of-the-art collision-aware task assignment method integrated into our framework.

> Self-Adaptive_Swarm_System (SASS) original version: [Self-Reactive Swarm-Robotic System (SRSS)](https://ieeexplore.ieee.org/abstract/document/8901075)

> [SMC](http://smc2020.org/) version: [Hierarchical Needs Based Self-Adaptive Framework For Cooperative Multi-Robot System](https://ieeexplore.ieee.org/abstract/document/9283249)

## Evaluation through Simulation Studies
### Experiment Setting
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


## Conclusion
Our work introduces a novel SASS framework for cooperation heterogeneous multi-robot systems for dynamic task assignments and automated planning. It combines robot perception, communication, planning, and execution in MRS, which considers individual robot's needs and action plans and emphasizes the complex relationships created through communication between the robots. Specifically, we proposed \textit{Robot's Needs Hierarchy} to model the robot's motivation and offer a priority queue in a distributed \textit{Negotiation-Agreement Mechanism} avoiding plan conflicts effectively. Then, we provide several \textit{Atomic Operations} to decompose the complex tasks into a series of simple sub-tasks. The proposed solution is evaluated through extensive simulations under different static and dynamic task scenarios. The experimental analysis showed that the needs-based cooperation mechanism outperformed state-of-the-art methods in maximizing global team utility and reducing conflicts in planning and negotiation.
