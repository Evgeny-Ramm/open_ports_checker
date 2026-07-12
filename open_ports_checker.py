#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# open_ports_checker.py
# Показывает открытые TCP-порты на локальной машине с указанием процесса.

import socket
import psutil

def get_open_ports():
    """Возвращает список открытых TCP-портов (LISTEN) с PID процесса."""
    ports = []
    for conn in psutil.net_connections(kind='tcp'):
        if conn.status == 'LISTEN':
            ports.append({
                'port': conn.laddr.port,
                'pid': conn.pid,
                'process_name': None,
            })
    return ports

def get_process_name(pid):
    """Возвращает имя процесса по PID."""
    try:
        return psutil.Process(pid).name()
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return "недоступно"

def main():
    print("=== Открытые TCP-порты (LISTEN) ===")
    ports = get_open_ports()
    if not ports:
        print("Нет открытых портов.")
        return

    print(f"{'Порт':>6} {'PID':>6} {'Процесс'}")
    for p in ports:
        if p['pid']:
            p['process_name'] = get_process_name(p['pid'])
        else:
            p['process_name'] = "неизвестно"
        print(f"{p['port']:>6} {p['pid']:>6} {p['process_name']}")

if __name__ == "__main__":
    main()
