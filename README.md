# Hierarchical Needs Based SASS

## Abtract
Research in multi-robot and swarm systems has seen significant interest in cooperation of agents in complex and dynamic environments. 
To effectively adapt to unknown environments and maximize the utility of the group, robots need to cooperate, share information, and make a suitable plan according to the specific scenario. Inspired by Maslow's hierarchy of human needs and systems theory, we introduce Agent(Robot) Needs Hierarchy and propose a new solution called Self-Adaptive Swarm System (SASS). It combines multi-robot perception, communication, planning, and execution with the cooperative management of conflicts through a distributed Negotiation-Agreement Mechanism that prioritizes robot's needs. We also decompose the complex tasks into simple executable behaviors through several Atomic Operations, such as selection, formation, and routing. We evaluate SASS through simulating static and dynamic tasks and comparing them with the state-of-the-art collision-aware task assignment method integrated into our framework.

> Self-Adaptive_Swarm_System (SASS) original version: [Self-Reactive Swarm-Robotic System (SRSS)](https://ieeexplore.ieee.org/abstract/document/8901075)

> [SMC](http://smc2020.org/) version: [Hierarchical Needs Based Self-Adaptive Framework For Cooperative Multi-Robot System](https://ieeexplore.ieee.org/abstract/document/9283249)

> Agent(Robot) Needs Hierarchy
    <div align = center>
    <img src="https://github.com/RickYang2016/Self-Adaptive-Swarm-System_SASS_MRS2019/blob/master/figures/robot-needs.png" height="360" alt="Hopper-V2 3SABC"/>
    </div>

## Approach Overview
We design a simple scenario to implement SASS and distributed algorithms. In our scenarios, a group of swarm robots will cooperate to complete some tasks. Since the tasks are dynamically assigned, the robots need to change their plans and adapt to the new scenario to guarantee the group utility. In our framework, we decompose the complex tasks into a series of  sub-tasks and recursively achieve those sub-tasks until the entire task is completed. Accordingly,  we can divide the task allocation and execution into three steps: selection, formation, and routing. This process can be illustrated as a Behavior Tree that integrates the sense-think-act cycle. The robots are assumed to have low-level motion control and sensor-based perception system for sensing and navigation.

<div align = center>
<img src="https://github.com/RickYang2016/Self-Adaptive-Swarm-System_SASS_MRS2019/blob/master/figures/diagram.png" height="195" alt="Hopper-V2 3SABC"><img src="https://github.com/RickYang2016/Self-Adaptive-Swarm-System_SASS_MRS2019/blob/master/figures/bt.png" height="195" alt="Hopper-V2 3SABC Video"/>
</div>

<div align = center>
<img src="https://github.com/RickYang2016/Self-Adaptive-Swarm-System_SASS_MRS2019/blob/master/figures/Overview.png" height="225" alt="Hopper-V2 3SABC"><img src="https://github.com/RickYang2016/Self-Adaptive-Swarm-System_SASS_MRS2019/blob/master/figures/overview.gif" height="225" alt="Hopper-V2 3SABC Video"/>
</div>

## Evaluation through Simulation Studies
### Experiment Setting
To simulate our framework, we chose to use the [Common Open Research Emulator (CORE)](https://www.nrl.navy.mil/Our-Work/Areas-of-Research/Information-Technology/NCS/CORE/) network simulator since we are interested in implementing our algorithm in a network-based tool as CORE allows dynamic changes in the node/agent mobility and communication. 

<div align = center>
<img src="https://github.com/RickYang2016/Self-Adaptive-Swarm-System_SASS_MRS2019/blob/master/figures/task_decompose.png" height="250" alt="Hopper-V2 3SABC"><img src="https://github.com/RickYang2016/Self-Adaptive-Swarm-System_SASS_MRS2019/blob/master/figures/setting.gif" height="250" alt="Hopper-V2 3SABC Video"/>
</div>

#### Manually Configure CORE
```
If set CORE.sh is not working, follow these steps to manually configure CORE.

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
```

### Demonstration
#### Static Tasks
<div align = center>
<img src="https://github.com/RickYang2016/Self-Adaptive-Swarm-System_SASS_MRS2019/blob/master/figures/static.gif" height="215" alt="Hopper-V2 3SABC"><img src="https://github.com/RickYang2016/Self-Adaptive-Swarm-System_SASS_MRS2019/blob/master/figures/sameE.gif" height="215" alt="Hopper-V2 3SABC Video"/>
</div>

<div align = center>
<img src="https://github.com/RickYang2016/Self-Adaptive-Swarm-System_SASS_MRS2019/blob/master/figures/diffE.gif" height="215" alt="Hopper-V2 3SABC"><img src="https://github.com/RickYang2016/Self-Adaptive-Swarm-System_SASS_MRS2019/blob/master/figures/SC.gif" height="215" alt="Hopper-V2 3SABC Video"/>
</div>

#### Dynamic Tasks

## Conclusion
Our work introduces a novel SASS framework for cooperation heterogeneous multi-robot systems for dynamic task assignments and automated planning. It combines robot perception, communication, planning, and execution in MRS, which considers individual robot's needs and action plans and emphasizes the complex relationships created through communication between the robots. Specifically, we proposed \textit{Robot's Needs Hierarchy} to model the robot's motivation and offer a priority queue in a distributed \textit{Negotiation-Agreement Mechanism} avoiding plan conflicts effectively. Then, we provide several \textit{Atomic Operations} to decompose the complex tasks into a series of simple sub-tasks. The proposed solution is evaluated through extensive simulations under different static and dynamic task scenarios. The experimental analysis showed that the needs-based cooperation mechanism outperformed state-of-the-art methods in maximizing global team utility and reducing conflicts in planning and negotiation.
