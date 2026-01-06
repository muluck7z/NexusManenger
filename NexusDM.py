import requests
import time
import random
import os
import sys
import shutil
import getpass
import itertools

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


def get_term_width():
    return shutil.get_terminal_size().columns

def print_header(title, color=Colors.CYAN):
    """Limpa a tela e imprime um cabeçalho centralizado no formato --- Título ---."""
    clear_screen()
    width = get_term_width()
    formatted_title = f"--- {title} ---"
    print(f"\n{color}{formatted_title.center(width)}{Colors.END}\n")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def spinner_animation(duration, message):
    """Exibe uma animação de 'spinner' formatada com --- ---."""
    spinner = itertools.cycle(['⠇', '⠏', '⠋', '⠙', '⠸', '⠴', '⠦', '⠧'])
    end_time = time.time() + duration
    while time.time() < end_time:
        display_text = f"--- {next(spinner)} {message}... ---"
        sys.stdout.write(f'\r{Colors.YELLOW}{display_text}{Colors.END}')
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\r' + ' ' * (len(message) + 10) + '\r')

def print_log(icon, message, color):
    """Imprime uma linha de log formatada no painel de controle."""
    print(f"{color}--- [{icon}] {message} ---{Colors.END}")

def get_secure_input(prompt_color=Colors.CYAN):
    """Obtém entrada do usuário de forma oculta."""
    return getpass.getpass(f"{prompt_color}{Colors.BOLD}> {Colors.END}")


def get_ultra_headers(token):
    return {
        "authority": "discord.com", "accept": "*/*", "accept-language": "pt-BR,pt;q=0.9",
        "authorization": token, "content-type": "application/json", "origin": "https://discord.com",
        "referer": "https://discord.com/channels/@me", "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120"',
        "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": '"Windows"', "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }

def send_message(token, channel_id, message):
    headers = get_ultra_headers(token)
    try: requests.post(f"https://discord.com/api/v9/channels/{channel_id}/typing", headers=headers, timeout=5)
    except: pass
    time.sleep(min(max(len(message) * random.uniform(0.05, 0.15), 2), 7))
    payload = {"content": message, "nonce": str(random.randint(10**18, 10**19))}
    try:
        res = requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", headers=headers, json=payload)
        return res.status_code == 200
    except: return False

def load_responded_users(filename="responded_users.txt"):
    if not os.path.exists(filename): return set()
    with open(filename, 'r') as f: return set(line.strip() for line in f)

def save_responded_user(user_id, filename="responded_users.txt"):
    with open(filename, 'a') as f: f.write(str(user_id) + '\n')

def main_loop(token, auto_message, my_id):
    responded_users = load_responded_users()
    
    print_header("Painel de Controle", Colors.MAGENTA)
    print_log("📈", f"{len(responded_users)} usuário(s) já respondido(s)", Colors.CYAN)

    while True:
        try:
            headers = get_ultra_headers(token)
            channels_res = requests.get("https://discord.com/api/v9/users/@me/channels", headers=headers)

            if channels_res.status_code == 401:
                print_log("❌", "Conta banida ou token inválido", Colors.RED + Colors.BOLD)
                break
            if channels_res.status_code != 200:
                print_log("⚠️", f"Queda de conexão (Status: {channels_res.status_code})", Colors.YELLOW)
                time.sleep(30)
                continue

            channels = channels_res.json()
            new_users_to_message = []
            
            for channel in channels:
                if channel.get('type') == 1:
                    user_id = next((r['id'] for r in channel['recipients'] if r['id'] != my_id), None)
                    if not user_id or user_id in responded_users: continue
                    
                    m_res = requests.get(f"https://discord.com/api/v9/channels/{channel['id']}/messages?limit=1", headers=headers)
                    if m_res.status_code == 200 and m_res.json() and m_res.json()[0]['author']['id'] != my_id:
                        new_users_to_message.append({'user_id': user_id, 'channel_id': channel['id']})

            if not new_users_to_message:
                print_log("🔎", "Nenhum usuário novo encontrado", Colors.CYAN)
            else:
                for user_data in new_users_to_message:
                    print_log("👤", "Usuário encontrado. Enviando mensagem...", Colors.BLUE)
                    if send_message(token, user_data['channel_id'], auto_message):
                        responded_users.add(user_data['user_id'])
                        save_responded_user(user_data['user_id'])
                        print_log("📈", f"{len(responded_users)} usuário(s) já respondido(s)", Colors.CYAN)
                        time.sleep(random.uniform(5, 12))

            wait = random.randint(20, 40)
            for i in range(wait, 0, -1):
                line = f"--- [🛡️] Próxima varredura em {i:02d}s ---"
                sys.stdout.write(f"\r{Colors.YELLOW}{line}{' ' * 5}{Colors.END}")
                sys.stdout.flush()
                time.sleep(1)
            sys.stdout.write('\r' + ' ' * (len(line) + 5) + '\r')

        except KeyboardInterrupt:
            print(f"\n{Colors.MAGENTA}--- Desligamento solicitado. Até logo! ---{Colors.END}")
            break
        except requests.exceptions.ConnectionError:
            print_log("⚠️", "Queda de conexão. Tentando novamente em 30s", Colors.YELLOW)
            time.sleep(30)
        except Exception as e:
            print_log("⚠️", f"Erro inesperado: {e}", Colors.RED)
            time.sleep(30)

def main():
    try:
        print_header("Insira seu token Discord")
        token = get_secure_input()
        
        spinner_animation(2, "Validando token")
        
        headers = get_ultra_headers(token)
        res = requests.get("https://discord.com/api/v9/users/@me", headers=headers)
        if res.status_code != 200:
            print(f"\n{Colors.RED}--- Token inválido ou falha na conexão ---\n{Colors.END}")
            return

        user = res.json()
        print(f"{Colors.GREEN}--- Sucesso! Logado como {user['username']} ---\n{Colors.END}")
        time.sleep(2)

        print_header("Insira a mensagem de resposta automática")
        auto_message = get_secure_input(Colors.YELLOW)
        
        spinner_animation(1.5, "Salvando mensagem")
        
        if not auto_message:
            print(f"\n{Colors.RED}--- A mensagem não pode estar vazia ---\n{Colors.END}")
            return
        
        print(f"{Colors.GREEN}--- Mensagem salva com sucesso! ---\n{Colors.END}")
        time.sleep(2)

        main_loop(token, auto_message, user['id'])

    except (KeyboardInterrupt, EOFError):
        print(f"\n{Colors.MAGENTA}--- Operação cancelada pelo usuário ---\n{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}--- Ocorreu um erro crítico: {e} ---\n{Colors.END}")

if __name__ == "__main__":
    main()
    