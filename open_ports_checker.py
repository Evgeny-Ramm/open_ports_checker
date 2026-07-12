#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# open_ports_checker.py
# Показывает открытые TCP-порты (LISTEN) с PID.

import psutil

def get_open_ports():
    """Возвращает список открытых TCP-портов с PID (только если PID существует)."""
    ports = []
    for conn in psutil.net_connections(kind='tcp'):
        if conn.status == 'LISTEN' and conn.pid is not None:
            ports.append({
                'port': conn.laddr.port,
                'pid': conn.pid,
            })
    return ports

def main():
    print("=== Открытые TCP-порты (LISTEN) ===")
    ports = get_open_ports()
    if not ports:
        print("Нет открытых портов.")
        return

    print(f"{'Порт':>6} {'PID':>6}")
    for p in ports:
        # Защита от None (на всякий случай)
        port = str(p['port']) if p['port'] is not None else '—'
        pid = str(p['pid']) if p['pid'] is not None else '—'
        print(f"{port:>6} {pid:>6}")

if __name__ == "__main__":
    main()
