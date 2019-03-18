#!/usr/bin/env python3

#Author: Zhiwei Luo

import signal
import sys
import os
import string
import random
import time
import socket
import json
import threading
from datetime import datetime

debug_mode = True

class Logger():
    is_local_initialized = False
    log_file_path = ''
    log_file = None
    sock_remote = None
    monitor_addr = None
    is_sock_ready = False

    def __init__(self, local_enable=True, path='', filename='', mode='w'):
        if local_enable == True:
            # path
            if path == 'pwd':
                self.log_file_path = os.getcwd()
            elif path != '':
                if os.path.exists(path):
                    self.log_file_path = path
                else:
                    self.error_print('Path %s not exists.' % path)
                    return
            else:
                self.error_print('Path should be either \'pwd\' or a absolute one.')
                return

            # file name
            if filename != '':
                self.log_file_path = self.log_file_path + '/' + filename
            else:
                self.log_file_path = self.log_file_path + '/%s_%s.log' % (self.time_generator(type='minutes'), self.id_generator())
            self.debug_print('Log file name is %s.' % self.log_file_path)

            # mode
            if not (mode == 'a+' or mode == 'w'):
                self.error_print('Log file open mode should be either \'a+\' or \'w\'.')
                return
            try:
                self.log_file = open(self.log_file_path, mode)
                self.is_local_initialized = True
            except FileNotFoundError:
                self.error_print('Log file open failed.')
            except Exception as e:
                self.error_print('Unknown Exception. %s', str(e))

    def log_local(self, log_str, tag='default', append_time=False):
        if self.is_local_initialized == True:
            try:
                write_str = '[%s]%s\n' % (tag, log_str)
                if append_time == True:
                    write_str = self.time_generator(type='milliseconds') + write_str
                self.log_file.write(write_str)
            except Exception as e:
                self.error_print('Log file appending failed.')
                self.is_local_initialized == False
        else:
            self.error_print('Log file is not initialized when log locally.')

    def enable_remote(self, monitor_addr):
        self.sock_remote = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock_remote.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock_remote.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock_remote.setblocking(0)
        if type(monitor_addr) == tuple and len(monitor_addr) == 2:
            if type(monitor_addr[1]) == int and monitor_addr[1] > 10000:
                try:
                    # check if addr is valid
                    socket.inet_aton(monitor_addr[0])
                    try:
                        self.sock_remote.bind(('0.0.0.0', 0))
                        self.is_sock_ready = True
                        self.monitor_addr = monitor_addr
                    except Exception as error:
                        self.error_print('Socket bind failed. %s' % str(error))
                except socket.error:
                    self.error_print('IP address is not valid.')
            else:
                self.error_print('monitor_addr[1] should be a port > 10000.')
        else:
            self.error_print('monitor_addr should be a tuple with an IP address and a port.')
        

    # single thread - multithread needed?
    def log_remote(self, log_str, tag='default', append_time=False):
        if self.is_sock_ready == True:
            write_str = '[%s]%s\n' % (tag, log_str)
            if append_time == True:
                write_str = self.time_generator(type='milliseconds') + write_str
            send_data = {'tag': tag, 'data': log_str, 'time': self.time_generator(type='milliseconds')}
            json_data = json.dumps(send_data)
            try:
                self.sock_remote.sendto(json_data.encode('utf-8'), self.monitor_addr)
            except socket.error as msg:
                self.error_print('Send data failed. ' + str(msg))
            except Exception as error:
                self.error_print('Send data unknown error: ' + str(error))
        else:
            self.error_print('Socket is not ready or closed.')

    def log_local_and_remote(self, log_str, tag='default', append_time=False):
        self.log_local(log_str, tag, append_time)
        self.log_remote(log_str, tag, append_time)

    def disable_remote(self):
        if self.is_sock_ready == True:
            try:
                self.sock_remote.close()
                self.is_sock_ready = False
            except socket.error as msg:
                self.error_print('Socket closed failed. ' + str(msg))

    def log_end(self):
        if self.is_local_initialized == True:
            try:
                self.log_file.close()
                self.is_local_initialized = False
            except Exception as e:
                self.error_print('Log file closes failed.')
        else:
            self.error_print('Log file is not initialized when closed.')

    def error_print(self, err_str):
        print('[Error] %s' % err_str)

    def debug_print(self, debug_str):
        if debug_mode == True:
            print('[Debug] %s' % debug_str)

    def id_generator(self, size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))

    def time_generator(self, type='minutes'):
        if type == 'minutes':
            return datetime.now().strftime('%Y-%m-%d_%H:%M')
        elif type == 'milliseconds':
            return datetime.now().strftime('%Y-%m-%d_%H:%M:%S.%f')[:-3]
        else:
            return datetime.now().strftime('%Y-%m-%d_%H:%M:%S')

class COREDebuggerVirtual():
    logger = None

    def __init__(self, monitor_addr, is_local_log=False, path='pwd', filename=''):
        # TODO: recv and parse command -> bind some response functions to command
        self.logger = Logger(local_enable=is_local_log, path=path, filename=filename)
        self.logger.enable_remote(monitor_addr)

    def send_to_monitor(self, log_str, tag='default', append_time=True):
        self.logger.log_local_and_remote(log_str, tag=tag, append_time=append_time)

    def log_local(self, log_str):
        self.logger.log_local(log_str)

    def close_socket(self):
        self.logger.disable_remote()

    def start_recv_cmd(self):
        pass

    def bind_response_func(self, cmd, func):
        pass

class COREDebuggerMonitor():
    sock_monitor = None
    is_sock_ready = False
    stop_sign = False # for controlling the socket threads
    bufferList = []
    recv_thread = None
    white_list_enabled = False
    black_list_enabled = False
    white_list = None
    black_list = None

    def __init__(self, port):
        print('*** Welcome to CORE Debugger Monitor! ***')
        signal.signal(signal.SIGINT, self.signal_handler)
        self.sock_remote = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock_remote.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock_remote.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock_remote.setblocking(0)
        if type(port) == int and port > 10000:
            try:
                self.sock_remote.bind(('0.0.0.0', port))
                print('Monitor binds to port %d.' % port)
                self.recv_thread = threading.Thread(target=self.recv_UDP)
                self.recv_thread.start()
                self.is_sock_ready = True
            except Exception as error:
                self.error_print('Socket bind failed. %s' % str(error))
        else:
            self.error_print('monitor_addr[1] should be a port > 10000.')

    def recv_UDP(self):
        while True:
            try:
                if self.stop_sign == True:
                    break
                recv_buffer, recvfrom_addr = self.sock_remote.recvfrom(1024)
                self.bufferList.append((recv_buffer, recvfrom_addr))
                # print("Received a package from %s and len = %d." %(str(recvfrom_addr), len(recv_buffer)))
            except NameError:
                self.error_print('The sock is broken when recv.')
                break
            except socket.error as error:
                if error.errno != socket.errno.EAGAIN:
                    # data not available
                    self.error_print('The sock error. %s' % str(error))
                    break

    def signal_handler(self, sig, frame):
        self.stop_sign = True
        if self.is_sock_ready == True:
            try:
                self.sock_remote.close()
            except socket.error as msg:
                self.error_print("Socket closed failed. %s" % str(msg))
            if self.recv_thread.is_alive:
                self.recv_thread.join()
        print('CORE Debugger Monitoring ended!')
        sys.exit(0)

    def retrieveData(self):
        if len(self.bufferList) > 0:
            recvData = self.bufferList[0]
            self.bufferList = self.bufferList[1:]
            return recvData
        else:
            return None

    def start_monitoring(self):
        print('Start Monitoring...')
        while True:
            recv_data = self.retrieveData()
            # recv_data = (json({'id':1, 'tag': 'STATUS', ...}), ('172.16.0.1', 12777))
            if recv_data != None:
                try:
                    recv_dict = json.loads(recv_data[0].decode('utf-8'))
                    recv_addr = recv_data[1]
                    if self.white_list_enabled == True:
                        if self.white_list['tag'] == 'tag' and (recv_dict['tag'] in self.white_list['white_list']) or \
                        (self.white_list['tag'] == 'ip' and (recv_addr[0] in self.white_list['white_list'])):
                            print('%s[%s][%s]%s' % (recv_dict['time'], recv_addr[0], recv_dict['tag'], recv_dict['data']))
                        else:
                            pass # filter out
                    elif self.black_list_enabled == True:
                        if self.black_list['tag'] == 'tag' and (recv_dict['tag'] in self.black_list['black_list']):
                            continue # filter out
                        elif self.black_list['tag'] == 'ip' and (recv_addr[0] in self.black_list['black_list']):
                            continue # filter out
                        else:
                            print('%s[%s][%s]%s' % (recv_dict['time'], recv_addr[0], recv_dict['tag'], recv_dict['data']))
                    else:
                        print('%s[%s][%s]%s' % (recv_dict['time'], recv_addr[0], recv_dict['tag'], recv_dict['data']))
                except Exception as e:
                    raise e
                    self.error_print("Error when received message: %s." % str(e))

    def set_black_list(self, tag, black_list):
        if self.white_list_enabled != True:
            if type(black_list) == list:
                self.black_list = {'tag': tag, 'black_list': black_list}
                self.black_list_enabled = True
            else:
                self.error_print('The black list is not a list.')
        else:
            self.error_print('You cannot specify a black list if you already have a white list.')

    def set_white_list(self, tag, white_list):
        if type(white_list) == list:
            self.white_list = {'tag': tag, 'white_list': white_list}
            self.white_list_enabled = True
        else:
            self.error_print('The white list is not a list.')

    def error_print(self, err_str):
        print('[Error] %s' % err_str)
                

class COREDebuggerCommander():
    sock_cmd = None
    network_addr = None
    is_sock_ready = False

    def __init__(self, network_addr):
        self.sock_cmd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock_cmd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock_cmd.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock_cmd.settimeout(2)
        if type(network_addr) == tuple and len(network_addr) == 2:
            if type(network_addr[1]) == int and network_addr[1] > 10000:
                try:
                    # check if addr is valid
                    socket.inet_aton(network_addr[0])
                    try:
                        self.sock_cmd.bind(('0.0.0.0', network_addr[1]))
                        self.is_sock_ready = True
                        self.network_addr = network_addr
                    except Exception as error:
                        self.error_print('Socket bind failed. %s' % str(error))
                except socket.error:
                    self.error_print('IP address is not valid.')
            else:
                self.error_print('network_addr[1] should be a port > 10000.')
        else:
            self.error_print('network_addr should be a tuple with an IP address and a port.')

    def recv_data(self, max_size=1024, max_display=80):
        if self.is_sock_ready == True:
            try:
                recv_buffer, recvfrom_addr = sock_cmd.recvfrom(max_size)
                recv_dict = json.loads(self.recv_buffer.decode('utf-8'))
                display_str = ('%s[%s][%s]%s' % (recv_dict['time'], self.recvfrom_addr[0], recv_dict['tag'], recv_dict['data']))
                if len(display_str) > max_display:
                    print("%s...(%s bytes omitted)." % (display_str[:max_display], len(display_str)-max_display))
                else:
                    print(display_str)
            except NameError:
                print('The sock is broken when trying to receive data.')
            except socket.error as error:
                if error.errno == socket.errno.EAGAIN:
                    # data not available
                    pass
                else:
                    print('Received data unknown error. %s' % str(error))

    def exit(self):
        try:
            self.sock_cmd.close()
        except socket.error as msg:
            print("Socket closed failed. %s", str(msg))
        sys.exit(0)

    def send_cmd(self, cmd, params):
        send_data = {'cmd': cmd, 'params': params}
        json_data = json.dumps(send_data)
        try:
            self.sock_cmd.sendto(json.dumps(send_data).encode('utf-8'), self.network_addr)
        except socket.error as error:
            print('Send data failed. ' + str(msg))
            raise error
        except Exception as error:
            print('Unknown error: ' + str(error))

    def start_input_cmd(self):
        print_help = lambda : print('Supported commands: %s' % ', '.join(supported_cmd))
        supported_cmd = {\
        'start': None, \
        'stop': None, \
        'quit': self.exit, \
        'help': print_help}
        # time out strategy
        while True:
            try:
                input_str = input('>> ')
            except Exception as error:
                raise error

            parsed_cmd = input_str.split(' ')[0]
            parsed_params = input_str.split(' ')[1:]
            print('cmd: [%s], params: [%s]' % (str(parsed_cmd), str(parsed_params)))
            if parsed_cmd in supported_cmd:
                key_cmd = parsed_cmd
                if supported_cmd[key_cmd] == None:
                    self.send_cmd(parsed_cmd, parsed_params)
                else:
                    # call the function
                    supported_cmd[key_cmd]()
            else:
                print('Unknown command.')
                print_help()

