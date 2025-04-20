"""
Módulo para monitoramento de ping.
Desenvolvido por Iuri Costa.
"""

import subprocess
import platform
import threading
import time
from typing import List, Dict, Callable, Optional

class PingMonitor:
    
    def __init__(self, hosts: List[str], interval: int = 5):
        self.hosts = hosts
        self.interval = interval
        self.status = {host: False for host in hosts}
        self.packet_loss = {host: 0 for host in hosts}
        self.ping_history = {host: [] for host in hosts}
        self.running = False
        self._thread: Optional[threading.Thread] = None
        self.callback: Optional[Callable[[str, bool, float], None]] = None
    
    def _ping_host(self, host: str) -> bool:
        param = "-n" if platform.system().lower() == "windows" else "-c"
        
        if platform.system().lower() == "windows":
            command = ["ping", param, "1", "-w", "1000", host]  # Timeout de 1 segundo no Windows
        else:
            command = ["ping", param, "1", "-W", "1", host]  # Timeout de 1 segundo no Linux/Mac
        
        try:
            result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=2)
            success = result.returncode == 0
            
            self.ping_history[host].append(success)
            
            if len(self.ping_history[host]) > 10:
                self.ping_history[host].pop(0)
            
            if self.ping_history[host]:
                lost = self.ping_history[host].count(False)
                total = len(self.ping_history[host])
                self.packet_loss[host] = (lost / total) * 100
            
            return success
        except (subprocess.TimeoutExpired, Exception):
            self.ping_history[host].append(False)
            if len(self.ping_history[host]) > 10:
                self.ping_history[host].pop(0)
            return False
    
    def _monitor(self) -> None:
        while self.running:
            for host in self.hosts:
                alive = self._ping_host(host)
                self.status[host] = alive
                
                if self.callback:
                    self.callback(host, alive, self.packet_loss[host])
            
            time.sleep(self.interval)
    
    def start(self) -> None:
        self.running = True
        self._thread = threading.Thread(target=self._monitor, daemon=True)
        self._thread.start()
    
    def stop(self) -> None:
        self.running = False
        if self._thread:
            self._thread.join()
    
    def set_hosts(self, new_hosts: List[str]) -> None:
        self.hosts = new_hosts
        self.status = {host: False for host in new_hosts}
        self.packet_loss = {host: 0 for host in new_hosts}
        self.ping_history = {host: [] for host in new_hosts}
    
    def set_interval(self, interval: int) -> None:
        self.interval = interval
