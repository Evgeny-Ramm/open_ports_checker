#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# open_ports_checker.py
# Показывает открытые TCP-порты с цветным выводом и фильтрацией.

import psutil
import argparse
from colorama import init, Fore, Style

init(autoreset=True)

def get_open_ports():
    ports = []
    for conn in psutil.net_connections(kind='tcp'):
        if conn.status == 'LISTEN' and conn.pid is not None:
            ports.append({
                'port': conn.laddr.port,
                'pid': conn.pid,
                'process_name': 'неизвестно',
            })
    return ports

def get_process_name(pid):
    try:
        return psutil.Process(pid).name()
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return 'неизвестно'

def main():
    parser = argparse.ArgumentParser(description="открытые TCP-порты")
    parser.add_argument("--port", type=int, help="фильтр по порту")
    parser.add_argument("--process", help="фильтр по имени процесса")
    args = parser.parse_args()

    ports = get_open_ports()
    if not ports:
        print("нет открытых портов")
        return

    # добавляем имена процессов
    for p in ports:
        p['process_name'] = get_process_name(p['pid'])

    # фильтрация
    if args.port:
        ports = [p for p in ports if p['port'] == args.port]
    if args.process:
        ports = [p for p in ports if p['process_name'].lower() == args.process.lower()]

    if not ports:
        print("порты не найдены по заданным фильтрам")
        return

    print(f"{'Порт':>6} {'PID':>6} {'Процесс'}")
    for p in ports:
        color = Fore.YELLOW if p['port'] in [22, 443, 8443] else Fore.GREEN
        print(f"{color}{p['port']:>6} {p['pid']:>6} {p['process_name']}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
