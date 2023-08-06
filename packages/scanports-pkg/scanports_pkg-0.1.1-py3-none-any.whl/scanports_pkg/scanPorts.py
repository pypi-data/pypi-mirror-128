#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from socket import socket, AF_INET, SOCK_STREAM
import time
from asyncio import Queue, TimeoutError, gather
from typing import List
from async_timeout import timeout
from optparse import OptionParser


class ScanPort(object):
    def __init__(self, ip: str = '', time_out: float = 0.1, port: List[int] = None, concurrency: int = None):
        if not ip:
            raise ValueError(f'wrong ip! {ip}')
        self.ip = ip
        self.port = port
        self.result: List[int] = []
        self.loop = self.get_event_loop()
        # 队列的事件循环用同一个
        self.queue = Queue(loop=self.loop)
        self.timeout = time_out
        # 并发数
        self.concurrency = concurrency

    @staticmethod
    def get_event_loop():
        if sys.platform == 'win32':
            from asyncio import ProactorEventLoop
            # 用 "I/O Completion Ports" (I O C P) 构建的专为Windows 的事件循环
            return ProactorEventLoop()
        else:
            from asyncio import SelectorEventLoop
            return SelectorEventLoop()

    async def scan(self):
        while True:
            port = await self.queue.get()
            sock = socket(AF_INET, SOCK_STREAM)
            try:
                with timeout(self.timeout):
                    # 这里windows和Linux返回值不一样 windows返回sock对象，Linux返回None
                    await self.loop.sock_connect(sock, (self.ip, port))
                    if sock:
                        self.result.append(port)
                        print(f'{self.ip}的{port}端口开启')
            # 这里要捕获所有可能的异常，windows会抛出前两个异常，Linux直接抛最后一个异常
            except (TimeoutError, PermissionError, ConnectionRefusedError) as _:
                sock.close()
                # print(f"\033[0;31m{self.ip}的{port}端口关闭")
            sock.close()
            self.queue.task_done()

    async def start(self):
        start = time.time()
        if self.port:
            for a in self.port:
                self.queue.put_nowait(a)
        else:
            for a in range(1, 65535 + 1):
                self.queue.put_nowait(a)
        task = [self.loop.create_task(self.scan()) for _ in range(self.concurrency)]
        # 如果队列不为空，则一直在这里阻塞
        await self.queue.join()
        # 依次退出
        for a in task:
            a.cancel()
        await gather(*task, return_exceptions=True)
        print(f'扫描所用时间为：{time.time() - start:.2f}')


# 对IP和端口进行过滤与组合
def data_get(data, status):
    data_list = data.split(',')
    data_cont = []
    for i in data_list:
        if '-' in i:
            data_division = i.split('-')
            if status == '端口':
                for j in range(int(data_division[0]), int(data_division[1]) + 1):
                    data_cont.append(str(j))
            elif status == 'IP':
                data_start = data_division[0].split('.')
                data_end = data_division[1].split('.')
                for j in range(int(data_start[-1]), int(data_end[-1]) + 1):
                    data_range = f'{data_start[0]}.{data_start[1]}.{data_start[2]}.{j}'
                    data_cont.append(data_range)
        else:
            data_cont.append(i)
    return data_cont


def main():
    print("""
                                         _______                        __              
                                        /       \                      /  |             
  _______   _______   ______   _______  $$$$$$$  | ______    ______   _$$ |_    _______ 
 /       | /       | /      \ /       \ $$ |__$$ |/      \  /      \ / $$   |  /       |
/$$$$$$$/ /$$$$$$$/  $$$$$$  |$$$$$$$  |$$    $$//$$$$$$  |/$$$$$$  |$$$$$$/  /$$$$$$$/ 
$$      \ $$ |       /    $$ |$$ |  $$ |$$$$$$$/ $$ |  $$ |$$ |  $$/   $$ | __$$      \ 
 $$$$$$  |$$ \_____ /$$$$$$$ |$$ |  $$ |$$ |     $$ \__$$ |$$ |        $$ |/  |$$$$$$  |
/     $$/ $$       |$$    $$ |$$ |  $$ |$$ |     $$    $$/ $$ |        $$  $$//     $$/ 
$$$$$$$/   $$$$$$$/  $$$$$$$/ $$/   $$/ $$/       $$$$$$/  $$/          $$$$/ $$$$$$$/  
""")
    parser = OptionParser()
    parser.add_option("-i", "--ip", dest="ipaddress",
                      help="输入域名或IP地址(多个可用,分割;连续使用-分隔)", metavar="127.0.0.1")
    parser.add_option("-p", "--port", dest="port",
                      help="输入端口(多个使用,分隔;连续使用-分隔)", metavar="80")
    parser.add_option("-t", "--time", dest="timeout",
                      help="输入超时(毫秒),默认0.1", metavar="0.1")
    parser.add_option("-c", "--con", dest="concurrent",
                      help="并发数,默认500", metavar="500")

    (options, args) = parser.parse_args()
    if options.timeout is None:
        time_out = 0.1
    else:
        time_out = float(options.timeout)
    if options.concurrent is None:
        concurrent = 500
    else:
        concurrent = int(options.concurrent)
    if options.ipaddress is not None and options.port is not None:
        ipaddress = options.ipaddress
        ports = options.port
        ip_data = data_get(ipaddress, 'IP')
        port_data = data_get(ports, '端口')
        port_list = [int(i) for i in port_data]
        print('-' * 30 + '扫描开始' + '-' * 30)
        for ip in ip_data:
            scan = ScanPort(ip, port=port_list, concurrency=concurrent)
            scan.loop.run_until_complete(scan.start())
        print('-' * 30 + '扫描结束' + '-' * 30)
