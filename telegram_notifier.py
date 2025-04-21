import requests
import time
from typing import Dict, Optional

class TelegramNotifier:
    
    def __init__(self, token: str, chat_id: str):
        self.token = token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{token}/sendMessage"
        self.host_status: Dict[str, bool] = {}
        self.last_notification: Dict[str, float] = {}
        self.min_notification_interval = 10  # 10 segundos (NAO MEXA SEU APEDEUTA, SE MUDAR BUGA POR ALGUM MOTIVO E FICA SPAMMANDO)
        self.last_message: Dict[str, str] = {}
    
    def send_message(self, message: str) -> bool:
        try:
            data = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": "HTML"
            }
            response = requests.post(self.api_url, json=data)
            return response.status_code == 200
        except Exception as e:
            print(f"Erro ao enviar mensagem do Telegram: {e}")
            return False
    
    def check_and_notify(self, host: str, is_alive: bool) -> None:
        current_time = time.time()
        
        if host not in self.host_status:
            self.host_status[host] = is_alive
            return
        
        if self.host_status[host] != is_alive:
            last_notification = self.last_notification.get(host, 0)
            if current_time - last_notification >= self.min_notification_interval:
                status_text = "online" if is_alive else "offline"
                message = f"🔔 <b>Alerta de Status</b>\n\nO host <code>{host}</code> está {status_text}!"
                
                if host not in self.last_message or self.last_message[host] != message:
                    if self.send_message(message):
                        self.last_notification[host] = current_time
                        self.host_status[host] = is_alive
                        self.last_message[host] = message