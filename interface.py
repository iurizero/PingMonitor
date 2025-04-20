"""
Interface gráfica para o monitor de ping.
Desenvolvido por Iuri Costa.
"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime
from ping_monitor import PingMonitor

class StatusIndicator(ttk.Frame):
    def __init__(self, parent, status, online_color, offline_color):
        super().__init__(parent)
        self.online_color = online_color
        self.offline_color = offline_color
        
        self.indicator = tk.Canvas(self, width=15, height=15, highlightthickness=0)
        self.indicator.pack(side=tk.LEFT, padx=(0, 5))
        
        self.label = ttk.Label(self, text=status)
        self.label.pack(side=tk.LEFT)
        
        self.update_status(status)
    
    def update_status(self, status):
        color = self.online_color if status == "Online" else self.offline_color
        self.indicator.configure(bg=color)
        self.label.configure(text=status)

class PingApp:
    
    def __init__(self, root):
        
        self.root = root
        self.root.title("Monitor de Ping - Iuri Costa")
        self.root.geometry("800x600")
        
        self._setup_styles()
        
        self.online_color = "#2ecc71"
        self.offline_color = "#e74c3c"
        self.text_color = "#ffffff"
        self.bg_color = "#f0f0f0"
        
        self.monitor = PingMonitor([], 5)
        self.monitor.callback = self.update_status
        
        self.host_entries = []
        self.hosts_data = {}
        self.is_monitoring = False
        self.tree_items = {}
        
        self.setup_ui()
    
    def _setup_styles(self):
        self.style = ttk.Style()
        self.style.configure("Treeview", rowheight=30)
        self.style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))
    
    def setup_ui(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        control_frame = ttk.LabelFrame(main_frame, text="Controles", padding=10)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        host_input_frame = ttk.Frame(control_frame)
        host_input_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(host_input_frame, text="Novo Host:").pack(side=tk.LEFT, padx=(0, 5))
        self.host_entry = ttk.Entry(host_input_frame, width=30)
        self.host_entry.pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(host_input_frame, text="Adicionar", command=self.add_host).pack(side=tk.LEFT)
        
        settings_frame = ttk.Frame(control_frame)
        settings_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(settings_frame, text="Intervalo (s):").pack(side=tk.LEFT, padx=(0, 5))
        self.interval_var = tk.IntVar(value=5)
        ttk.Spinbox(settings_frame, from_=1, to=60, textvariable=self.interval_var, width=5).pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Button(settings_frame, text="Iniciar Monitoramento", command=self.start_monitoring).pack(side=tk.LEFT, padx=5)
        ttk.Button(settings_frame, text="Parar Monitoramento", command=self.stop_monitoring).pack(side=tk.LEFT)
        
        self.tree_frame = ttk.LabelFrame(main_frame, text="Hosts Monitorados", padding=10)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)
        
        self.tree = ttk.Treeview(self.tree_frame, columns=("host", "status", "last_seen", "packet_loss"), show="headings")
        self.tree.heading("host", text="Host")
        self.tree.heading("status", text="Status")
        self.tree.heading("last_seen", text="Última Verificação")
        self.tree.heading("packet_loss", text="Perda de Pacotes")
        
        self.tree.column("host", width=200)
        self.tree.column("status", width=100)
        self.tree.column("last_seen", width=150)
        self.tree.column("packet_loss", width=100)
        
        scrollbar = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def add_host(self):
        host = self.host_entry.get().strip()
        if host:
            self.host_entry.delete(0, tk.END)
            self.hosts_data[host] = {
                "status": "Offline",
                "last_seen": "Nunca",
                "packet_loss": "0%"
            }
            self.update_tree()
    
    def update_status(self, host, alive, packet_loss):
        current_time = datetime.now().strftime("%H:%M:%S")
        
        if host in self.hosts_data:
            status = "Online" if alive else "Offline"
            self.hosts_data[host]["status"] = status
            self.hosts_data[host]["last_seen"] = current_time
            self.hosts_data[host]["packet_loss"] = f"{packet_loss:.1f}%"
            self.update_tree_item(host)
    
    def update_tree_item(self, host):
        if host in self.tree_items:
            item = self.tree_items[host]
            data = self.hosts_data[host]
            
            self.tree.set(item, "status", data["status"])
            self.tree.set(item, "last_seen", data["last_seen"])
            self.tree.set(item, "packet_loss", data["packet_loss"])
            
            if self.is_monitoring:
                if data["status"] == "Online":
                    self.tree.tag_configure(f"status_{item}", background=self.online_color, foreground=self.text_color)
                    self.tree.item(item, tags=(f"status_{item}",))
                else:
                    self.tree.tag_configure(f"status_{item}", background=self.offline_color, foreground=self.text_color)
                    self.tree.item(item, tags=(f"status_{item}",))
            else:
                self.tree.tag_configure(f"status_{item}", background=self.bg_color, foreground="black")
                self.tree.item(item, tags=(f"status_{item}",))
    
    def update_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.tree_items = {}
        
        for host, data in self.hosts_data.items():
            status = data["status"]
            
            item = self.tree.insert("", tk.END, values=(
                host,
                status,
                data["last_seen"],
                data["packet_loss"]
            ))
            
            self.tree_items[host] = item
            
            if self.is_monitoring:
                if status == "Online":
                    self.tree.tag_configure(f"status_{item}", background=self.online_color, foreground=self.text_color)
                    self.tree.set(item, "status", status)
                    self.tree.item(item, tags=(f"status_{item}",))
                else:
                    self.tree.tag_configure(f"status_{item}", background=self.offline_color, foreground=self.text_color)
                    self.tree.set(item, "status", status)
                    self.tree.item(item, tags=(f"status_{item}",))
            else:
                self.tree.tag_configure(f"status_{item}", background=self.bg_color, foreground="black")
                self.tree.set(item, "status", status)
                self.tree.item(item, tags=(f"status_{item}",))
    
    def start_monitoring(self):
        hosts = list(self.hosts_data.keys())
        self.monitor.set_hosts(hosts)
        self.monitor.set_interval(self.interval_var.get())
        self.monitor.start()
        self.is_monitoring = True
        self.update_tree()
    
    def stop_monitoring(self):
        self.monitor.stop()
        self.is_monitoring = False
        self.update_tree()

if __name__ == "__main__":
    root = tk.Tk()
    app = PingApp(root)
    root.mainloop()
