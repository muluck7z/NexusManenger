import requests
import time
import random
import os
import sys
from datetime import datetime

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
    ███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗
    ████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝
    ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗
    ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║
    ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║
    ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝
{Colors.MAGENTA}        > NexusManager Tools V1.0 <
{Colors.END}
{Colors.BOLD}{Colors.BLUE}Créditos: {Colors.GREEN}_muluck7z{Colors.END}
"""
    print(banner)

def get_input(prompt, color=Colors.CYAN):
    return input(f"{color}{prompt}{Colors.END}").strip()

def get_multiline_message():
    print(f"\n{Colors.YELLOW}Insira sua mensagem{Colors.END}")
    print(f"{Colors.YELLOW}Para finalizar, pressione {Colors.BOLD}ENTER{Colors.END}{Colors.YELLOW} e depois {Colors.BOLD}Ctrl+D{Colors.END}")
    try:
        lines = sys.stdin.readlines()
        return "".join(lines).strip()
    except EOFError:
        return ""

def get_ultra_headers(token):
    return {
        "authority": "discord.com",
        "accept": "*/*",
        "accept-language": "pt-BR,pt;q=0.9",
        "authorization": token,
        "content-type": "application/json",
        "origin": "https://discord.com",
        "referer": "https://discord.com/channels/@me",
        "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "x-discord-locale": "pt-BR",
        "x-super-properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6InB0LUJSIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEyMC4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTIwLjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjI1NjYwMCwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0="
    }

def send_message(token, channel_id, message):
    headers = get_ultra_headers(token)
    try: requests.post(f"https://discord.com/api/v9/channels/{channel_id}/typing", headers=headers, timeout=3)
    except: pass
    time.sleep(random.uniform(2, 5))
    payload = {"content": message, "nonce": str(random.randint(10**18, 10**19))}
    try:
        res = requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", headers=headers, json=payload)
        return res.status_code == 200
    except: return False

def channel_sender():
    configs = []
    while True:
        clear_screen()
        print_banner()
        print(f"{Colors.BOLD}{Colors.YELLOW}--- Configuração de Canais ---{Colors.END}\n")
        token = get_input("Token: ")
        channel_id = get_input("ID do Canal: ")
        message = get_multiline_message()
        t_min = int(get_input("\nTempo Mínimo (s): "))
        t_max = int(get_input("Tempo Máximo (s): "))
        
        configs.append({"token": token, "channel_id": channel_id, "message": message, "t_min": t_min, "t_max": t_max})
        if get_input("\nAdicionar outro canal? (s/N): ").lower() != 's': break

    print(f"\n{Colors.GREEN}[!] Iniciando automação de canais...{Colors.END}")
    try:
        while True:
            for config in configs:
                if send_message(config['token'], config['channel_id'], config['message']):
                    print(f"{Colors.GREEN}[✔] Enviado para {config['channel_id']}{Colors.END}")
                time.sleep(random.randint(config['t_min'], config['t_max']))
    except KeyboardInterrupt: return

def dm_auto_responder():
    configs = []
    while True:
        clear_screen()
        print_banner()
        print(f"{Colors.BOLD}{Colors.YELLOW}--- Configuração de Auto-Responder DMs ---{Colors.END}\n")
        token = get_input("Token: ")
        
        res = requests.get("https://discord.com/api/v9/users/@me", headers=get_ultra_headers(token))
        if res.status_code != 200:
            print(f"{Colors.RED}[!] Token inválido!{Colors.END}")
            time.sleep(2)
            continue
            
        my_id = res.json()['id']
        message = get_multiline_message()
        
        ignored_channels = set()
        headers = get_ultra_headers(token)
        c_res = requests.get("https://discord.com/api/v9/users/@me/channels", headers=headers)
        if c_res.status_code == 200:
            for c in c_res.json():
                if c.get('type') == 1: ignored_channels.add(c['id'])
        
        configs.append({
            "token": token, 
            "message": message, 
            "my_id": my_id, 
            "ignored_channels": ignored_channels,
            "responded_channels": set()
        })
        
        if get_input("\nAdicionar outra conta/configuração? (s/N): ").lower() != 's': break

    print(f"\n{Colors.GREEN}[!] Monitorando NOVAS DMs...{Colors.END}")
    try:
        while True:
            for config in configs:
                headers = get_ultra_headers(config['token'])
                
                if random.random() < 0.4:
                    req_res = requests.get("https://discord.com/api/v9/users/@me/message-requests", headers=headers)
                    if req_res.status_code == 200:
                        for req in req_res.json():
                            c_id = req['id']
                            if c_id in config['ignored_channels']: config['ignored_channels'].remove(c_id)
                            requests.put(f"https://discord.com/api/v9/channels/{c_id}/message-requests", headers=headers, json={"consent": True})
                            time.sleep(random.uniform(2, 4))

                channels_res = requests.get("https://discord.com/api/v9/users/@me/channels", headers=headers)
                if channels_res.status_code == 200:
                    channels = channels_res.json()
                    random.shuffle(channels)
                    for channel in channels[:10]:
                        c_id = channel['id']
                        if c_id not in config['ignored_channels'] and c_id not in config['responded_channels']:
                            time.sleep(random.uniform(1, 2))
                            m_res = requests.get(f"https://discord.com/api/v9/channels/{c_id}/messages?limit=1", headers=headers)
                            if m_res.status_code == 200:
                                msgs = m_res.json()
                                if msgs and msgs[0]['author']['id'] != config['my_id']:
                                    if send_message(config['token'], c_id, config['message']):
                                        print(f"{Colors.GREEN}[✔] Nova DM respondida: {c_id}{Colors.END}")
                                        config['responded_channels'].add(c_id)
                                        time.sleep(random.uniform(5, 10))
            
            wait = random.randint(10, 30)
            for i in range(wait, 0, -1):
                sys.stdout.write(f"\r{Colors.YELLOW}[🛡️] Próxima varredura em: {i}s...   {Colors.END}")
                sys.stdout.flush()
                time.sleep(1)
    except KeyboardInterrupt: return

def main():
    while True:
        clear_screen()
        print_banner()
        print(f"{Colors.BOLD}Escolha uma ferramenta:{Colors.END}")
        print(f"{Colors.CYAN}(1) Enviar mensagens em canais{Colors.END}")
        print(f"{Colors.CYAN}(2) Enviar mensagens automáticas nas DMs{Colors.END}")
        print(f"{Colors.RED}(0) Sair{Colors.END}")
        
        choice = get_input("\nOpção: ")
        if choice == '1': channel_sender()
        elif choice == '2': dm_auto_responder()
        elif choice == '0': break
        else:
            print(f"{Colors.RED}Opção inválida!{Colors.END}")
            time.sleep(1)

if __name__ == "__main__":
    main()
    
