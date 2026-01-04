import requests
import time
import random
import os
import sys

# Cores para o terminal
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
{Colors.MAGENTA}          > Nexus Manenger Tools v1.0 <
{Colors.END}
{Colors.BOLD}{Colors.BLUE}Desenvolvido por:{Colors.END} {Colors.YELLOW}_muluck7z{Colors.END}
{Colors.BOLD}{Colors.BLUE}Discord:{Colors.END} {Colors.CYAN}https://discord.gg/bQmb6CKJBx{Colors.END}

{Colors.RED}{Colors.BOLD}[ AVISO DE SEGURANÇA ]{Colors.END}
{Colors.YELLOW}Use esta ferramenta exclusivamente em contas alternativas no Discord. A plataforma pode banir contas principais detectando uso inadequado. Não me responsabilizo por ações ou consequências resultantes.{Colors.END}
"""
    print(banner)

def send_message(token, channel_id, message):
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
    headers = {
        "authorization": token, 
        "content-type": "application/json",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    payload = {"content": message}
    
    try:
        res = requests.post(url, headers=headers, json=payload)
        if res.status_code == 200:
            print(f"{Colors.GREEN}[✔] SUCESSO:{Colors.END} Mensagem enviada para o canal {Colors.BOLD}{channel_id}{Colors.END}")
            return True
        else:
            print(f"{Colors.RED}[✘] ERRO:{Colors.END} Status {res.status_code} ao enviar para {channel_id}")
            return False
    except Exception as e:
        print(f"{Colors.RED}[!] FALHA CRÍTICA:{Colors.END} {e}")
        return False

def get_input(prompt, color=Colors.CYAN):
    return input(f"{color}{prompt}{Colors.END}").strip()

def get_multiline_message():
    print(f"\n{Colors.YELLOW}Insira sua mensagem.{Colors.END}")
    print(f"{Colors.YELLOW}Para finalizar, pressione {Colors.BOLD}ENTER{Colors.END}{Colors.YELLOW} e depois {Colors.BOLD}Ctrl+D{Colors.END}{Colors.YELLOW}:{Colors.END}")
    lines = sys.stdin.readlines()
    return "".join(lines).strip()

def main():
    clear_screen()
    print_banner()
    
    configs = []
    last_token = None
    
    while True:
        print(f"\n{Colors.BOLD}{Colors.YELLOW}--- Configuração de Envio ---{Colors.END}")
        
        token = ""
        if last_token:
            use_same = get_input(f"Usar o mesmo token anterior? (S/n): ", Colors.YELLOW).lower()
            if use_same != 'n':
                token = last_token
        
        if not token:
            token = get_input("Insira o Token de Autorização: ")
            last_token = token
            
        channel_id = get_input("Insira o ID do Canal: ")
        message = get_multiline_message()
        
        while True:
            try:
                t_min = int(get_input("Tempo MÍNIMO de espera (segundos): "))
                t_max = int(get_input("Tempo MÁXIMO de espera (segundos): "))
                if t_min <= t_max:
                    break
                print(f"{Colors.RED}O tempo mínimo deve ser menor ou igual ao máximo!{Colors.END}")
            except ValueError:
                print(f"{Colors.RED}Por favor, insira apenas números inteiros.{Colors.END}")
        
        configs.append({
            "token": token,
            "channel_id": channel_id,
            "message": message,
            "t_min": t_min,
            "t_max": t_max
        })
        
        outro = get_input("\nVocê quer configurar envio de mensagens em outro canal? (S/n): ", Colors.MAGENTA).lower()
        if outro == 'n':
            break
        clear_screen()
        print_banner()

    clear_screen()
    print_banner()
    print(f"{Colors.BOLD}{Colors.GREEN}>>> INICIANDO AUTOMAÇÃO EM {len(configs)} CANAL(IS) <<<{Colors.END}")

    try:
        while True:
            for i, config in enumerate(configs):
                print(f"{Colors.BLUE}[Canal {i+1}]{Colors.END} Enviando mensagem...")
                send_message(config["token"], config["channel_id"], config["message"])
                
                delay = random.randint(config["t_min"], config["t_max"])
                for remaining in range(delay, 0, -1):
                    sys.stdout.write(f"\r{Colors.YELLOW}[⏳] Próximo envio em: {remaining}s...   {Colors.END}")
                    sys.stdout.flush()
                    time.sleep(1)
                print(f"\r{Colors.GREEN}[✓] Aguardo concluído!                     {Colors.END}")
                
    except KeyboardInterrupt:
        print(f"\n\n{Colors.RED}{Colors.BOLD}Automação interrompida pelo usuário.{Colors.END}")

if __name__ == "__main__":
    main()
    
