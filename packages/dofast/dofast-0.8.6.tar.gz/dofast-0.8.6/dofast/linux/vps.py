#!/usr/bin/env python
import json
import subprocess
import sys
import time
from typing import List, Set, Tuple

import arrow
import requests

from dofast.toolkits.telegram import Channel


class Time:
    @classmethod
    def get_time(cls) -> dict:
        return requests.get(
            "http://worldtimeapi.org/api/timezone/Asia/Shanghai").json()

    @classmethod
    def get_hour_minute(cls):
        return arrow.get(cls.get_time()['datetime']).format('HH-mm')


class VPS:
    def __init__(self,
                 init_day: int = 1,
                 interface: str = 'eth0',
                 vps_name: str = 'vps') -> None:
        self.init_day = int(init_day)
        self.interface = interface
        self.name = vps_name

    @property
    def ip(self) -> str:
        return requests.get('http://ip.42.pl/raw').text

    def vnstat(self) -> str:
        js = subprocess.check_output('vnstat --json d', shell=True).decode()
        js = json.loads(js)
        bit_shift: int = 20
        daykey:str = 'days'
        interface_key:str = 'id'
        if js['vnstatversion'].startswith('2.'):
            bit_shift = 30
            daykey = 'day'
            interface_key = 'name'

        js = next((e for e in js['interfaces'] if e[interface_key] == self.interface),
                  {})
        if not js:
            return ''
        daily = js['traffic'][daykey]
        _id = next((i for i, e in enumerate(daily)
                    if e['date']['day'] == self.init_day),
                   len(daily) - 1)
        rx = sum(e['rx'] for e in daily[:_id + 1]) / (1 << bit_shift)
        tx = sum(e['tx'] for e in daily[:_id + 1]) / (1 << bit_shift)
        return 'TX {:.2f} GB. RX {:.2f} GB. Total {:.2f} GB'.format(
            tx, rx, rx + tx)

    def __repr__(self) -> str:
        return 'name: {} \nip: {}\n'.format(self.name, self.ip)


class Monitor:
    def __init__(self, vps: VPS, task_types: List[str]) -> None:
        self.task_types = task_types
        self.vps = vps

    def post_telegram(self, text: str) -> None:
        Channel('messalert').post(text)

    def run(self) -> None:
        msg = str(self.vps)
        for task_type in self.task_types:
            if task_type.strip() == 'vnstat':
                msg += self.vps.vnstat()
        self.post_telegram(msg)


class Context:
    def parse_args(self) -> dict:
        dct = {}
        pre: str
        for arg in sys.argv[1:]:
            if arg.startswith('-'):
                pre = arg.replace('-', '')
                dct[pre] = []
            else:
                dct[pre].append(arg)
        return dct

    def get_first_arg(self, args: dict, key: str, default: str) -> str:
        if key in args:
            return args[key][0]
        return default

    def run(self):
        args = self.parse_args()
        vps_name = self.get_first_arg(args, 'vps_name', 'vps')
        alert_time = self.get_first_arg(args, 'alert_time', '08-01')
        interface = self.get_first_arg(args, 'interface', 'eth0')
        init_day = self.get_first_arg(args, 'init_day', 1)
        vps = VPS(init_day=init_day, vps_name=vps_name, interface=interface)
        monitor = Monitor(vps, task_types=args.get('task_types', []))

        while True:
            if Time.get_hour_minute() == alert_time:
                monitor.run()
                time.sleep(60)
            time.sleep(10)


def main():
    Context().run()