# Monitor de Ping com Interface Gráfica

![Python](https://img.shields.io/badge/python-3.7%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Monitor de rede com interface gráfica que verifica o status de hosts através de ping, exibindo status de conectividade em tempo real, com suporte a alertas via Telegram.

## 🚀 Funcionalidades

- **Monitoramento em tempo real** de múltiplos hosts
- **Histórico de status** com cálculo de perda de pacotes (últimos 10 pings)
- **Interface visual intuitiva** com indicação colorida de status
- **Configuração flexível** de intervalo de verificação
- **Registro de última verificação** com timestamp
- **Sistema de callback** para atualizações em tempo real
- **Alertas via Telegram** quando um host ficar offline ou voltar a ficar online

## ⚙️ Instalação

**Pré-requisitos:**
   - Python 3.7+
   - Tkinter (normalmente incluído no Python)
   - Conta no Telegram com um bot configurado (veja abaixo)

## 📲 Configurando os Alertas do Telegram

1. Crie um bot no Telegram com o [BotFather](https://t.me/BotFather)
2. Anote o **token** do bot
3. Inicie uma conversa com o bot e envie uma mensagem qualquer
4. Obtenha seu **chat_id** (pode ser feito usando a API do Telegram ou um bot que exibe seu ID)
5. Configure o Token do bot e o chat id no próprio aplicativo de monitoramento
6. Escolha se quer ativar ou desativar os alertas via Telegram a qualquer momento

## 🖥️ Como Usar

1. Adicione hosts usando o campo "Novo Host"
2. Defina o intervalo de verificação (1-60 segundos)
3. Clique em "Iniciar Monitoramento"
4. Visualize os status em tempo real:
   - 🟢 Online: Verde
   - 🔴 Offline: Vermelho
   - 📊 Perda de pacotes: Porcentagem calculada
5. Receba notificações no Telegram quando os hosts mudarem de status

---

**Desenvolvido por**
**Iuri Costa**
[![GitHub](https://img.shields.io/badge/GitHub-Profile-blue?style=flat&logo=github)](https://github.com/iurizero)
