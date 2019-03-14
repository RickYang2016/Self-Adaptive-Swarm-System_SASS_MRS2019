#!/usr/bin/env python3

#Author: Zhiwei Luo

from COREDebugger import COREDebuggerMonitor

if __name__ == '__main__':
    monitor = COREDebuggerMonitor(port=12888)
    monitor.start_monitoring()
