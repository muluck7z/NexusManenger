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
    clear_screen()
    width = get_term_width()
    credits = f"{Colors.BOLD}{Colors.MAGENTA}Nexus{Colors.END} {Colors.CYAN}Manager Tools{Colors.END}"
    author = f"{Colors.YELLOW}By: _muluck7z{Colors.END}"
    discord_link = f"{Colors.BLUE}Discord: https://discord.gg/bQmb6CKJBx{Colors.END}"
    print(f"\n{credits.center(width + 20)}")
    print(f"{author.center(width + 10)}")
    print(f"{discord_link.center(width + 10)}")
    formatted_title = f"--- {title} ---"
    print(f"\n{color}{formatted_title.center(width)}{Colors.END}\n")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def spinner_animation(duration, message):
    spinner = itertools.cycle(['⠇', '⠏', '⠋', '⠙', '⠸', '⠴', '⠦', '⠧'])
    end_time = time.time() + duration
    while time.time() < end_time:
        display_text = f"--- {next(spinner)} {message}... ---"
        sys.stdout.write(f'\r{Colors.YELLOW}{display_text}{Colors.END}')
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\r' + ' ' * (len(message) + 15) + '\r')

def print_log(icon, message, color):
    print(f"{color}--- [{icon}] {message} ---{Colors.END}")


def get_secure_input(prompt_color=Colors.CYAN):
    return getpass.getpass(f"{prompt_color}{Colors.BOLD}> {Colors.END}")

def get_input(prompt, color=Colors.CYAN):
    print(f"{color}{Colors.BOLD}{prompt}{Colors.END}")
    return input(f"{color}{Colors.BOLD}> {Colors.END}").strip()


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
    session = requests.Session()
    headers = get_ultra_headers(token)
    nonce = "".join([str(random.randint(0, 9)) for _ in range(19)])
    payload = {"content": message, "nonce": nonce, "tts": False}
    
    try:
        res = session.post(
            f"https://discord.com/api/v9/channels/{channel_id}/messages", 
            headers=headers, 
            json=payload, 
            timeout=15
        )
        if res.status_code == 200:
            return "SUCCESS", None
        elif res.status_code == 429:
            retry_after = res.json().get('retry_after', 5)
            return "RATE_LIMIT", retry_after
        else:
            return "ERROR", res.status_code
    except:
        return "CONNECTION_ISSUE", None

def check_mentions(token, my_id):
    headers = get_ultra_headers(token)
    try:
        res = requests.get("https://discord.com/api/v9/users/@me/mentions?limit=5", headers=headers, timeout=10)
        if res.status_code == 200:
            return res.json()
    except: pass
    return []

def get_guild_info(token, channel_id):
    headers = get_ultra_headers(token)
    try:
        res = requests.get(f"https://discord.com/api/v9/channels/{channel_id}", headers=headers, timeout=10)
        if res.status_code == 200:
            channel_data = res.json()
            guild_id = channel_data.get('guild_id')
            if guild_id:
                g_res = requests.get(f"https://discord.com/api/v9/guilds/{guild_id}", headers=headers, timeout=10)
                if g_res.status_code == 200:
                    return g_res.json().get('name', 'Servidor Desconhecido')
    except: pass
    return "Servidor"

def check_access_status(token, channel_id):
    headers = get_ultra_headers(token)
    try:
        res_me = requests.get("https://discord.com/api/v9/users/@me", headers=headers, timeout=10)
        if res_me.status_code == 401:
            return "ACCOUNT_BANNED"
        res_ch = requests.get(f"https://discord.com/api/v9/channels/{channel_id}", headers=headers, timeout=10)
        if res_ch.status_code in [403, 404]:
            return "GUILD_BANNED"
    except:
        return "CONNECTION_ISSUE"
    return "OK"

def main_loop(configs, my_id):
    print_header("Painel de Controle", Colors.MAGENTA)
    last_mention_ids = set()
    guild_names = {}
    
    for config in configs:
        if config['channel_id'] not in guild_names:
            guild_names[config['channel_id']] = get_guild_info(config['token'], config['channel_id'])

    while True:
        try:
            for config in configs:
                status = check_access_status(config['token'], config['channel_id'])
                
                if status == "ACCOUNT_BANNED":
                    print_log("❌", "Sua conta foi banida do Discord", Colors.RED + Colors.BOLD)
                    continue
                elif status == "GUILD_BANNED":
                    guild_name = guild_names.get(config['channel_id'], "Servidor")
                    print_log("🛑", f"Sua conta foi banida da {guild_name}", Colors.RED)
                    continue
                elif status == "CONNECTION_ISSUE":
                    print_log("⚠️", "Queda de conexão", Colors.YELLOW)
                    time.sleep(5)
                    continue

                mentions = check_mentions(config['token'], my_id)
                for mention in mentions:
                    m_id = mention['id']
                    if m_id not in last_mention_ids:
                        author = mention['author']['username']
                        print_log("🔎", f"O usuário {author} mencionou você", Colors.YELLOW)
                        last_mention_ids.add(m_id)

                result, data = send_message(config['token'], config['channel_id'], config['message'])
                
                if result == "SUCCESS":
                    print_log("💬", f"Mensagem enviada para o canal {config['channel_id']}", Colors.GREEN)
                elif result == "RATE_LIMIT":
                    print_log("⚠️", f"Limite de velocidade atingido. Aguardando {data}s...", Colors.YELLOW)
                    time.sleep(data)
                elif result == "CONNECTION_ISSUE":
                    print_log("⚠️", "Queda de conexão", Colors.YELLOW)
                else:
                    print_log("⚠️", f"Erro ao enviar (Status: {data})", Colors.RED)

                time.sleep(random.uniform(5, 8))

            avg_min = sum(c['t_min'] for c in configs) // len(configs)
            avg_max = sum(c['t_max'] for c in configs) // len(configs)
            delay = random.randint(avg_min, avg_max)
            
            for remaining in range(delay, 0, -1):
                line = f"--- [🛡️] Próxima varredura em {remaining:02d}s ---"
                sys.stdout.write(f"\r{Colors.YELLOW}{line}{' ' * 5}{Colors.END}")
                sys.stdout.flush()
                time.sleep(1)
            sys.stdout.write('\r' + ' ' * (len(line) + 15) + '\r')

        except KeyboardInterrupt:
            print(f"\n{Colors.MAGENTA}--- Desligamento solicitado. Até logo! ---{Colors.END}")
            break
        except Exception as e:
            print_log("⚠️", f"Erro inesperado: {e}", Colors.RED)
            time.sleep(30)

def main():
    try:
        configs = []
        last_token = None
        my_id = None
        
        while True:
            print_header("Insira seu token Discord")
            if last_token:
                print(f"{Colors.YELLOW}--- Pressione ENTER para usar o token anterior ---{Colors.END}")
            
            token = get_secure_input()
            if not token and last_token:
                token = last_token
            
            if not token:
                print(f"\n{Colors.RED}--- O token não pode estar vazio ---\n{Colors.END}")
                time.sleep(2)
                continue

            spinner_animation(1.5, "Validando token")
            
            headers = get_ultra_headers(token)
            try:
                res = requests.get("https://discord.com/api/v9/users/@me", headers=headers, timeout=10)
                if res.status_code != 200:
                    print(f"\n{Colors.RED}--- Token inválido ou falha na conexão ---\n{Colors.END}")
                    time.sleep(2)
                    continue
                user_data = res.json()
                my_id = user_data['id']
                print(f"{Colors.GREEN}--- Sucesso! Logado como {user_data['username']} ---\n{Colors.END}")
                last_token = token
                time.sleep(1.5)
            except:
                print(f"\n{Colors.RED}--- Erro de conexão ao validar token ---\n{Colors.END}")
                time.sleep(2)
                continue

            print_header("Insira o ID do Canal")
            channel_id = get_input("ID do Canal")
            
            print_header("Insira a mensagem de resposta automática")
            message = get_secure_input(Colors.YELLOW)
            
            spinner_animation(1, "Salvando mensagem")
            
            if not message:
                print(f"\n{Colors.RED}--- A mensagem não pode estar vazia ---\n{Colors.END}")
                time.sleep(2)
                continue
            
            print(f"{Colors.GREEN}--- Mensagem salva com sucesso! ---\n{Colors.END}")
            time.sleep(1.5)

            print_header("Configuração de Tempos")
            try:
                t_min = int(get_input("Tempo MÍNIMO de espera (segundos)"))
                t_max = int(get_input("Tempo MÁXIMO de espera (segundos)"))
                if t_min > t_max:
                    print(f"\n{Colors.RED}--- O tempo mínimo deve ser menor que o máximo ---\n{Colors.END}")
                    time.sleep(2)
                    continue
            except ValueError:
                print(f"\n{Colors.RED}--- Por favor, insira apenas números ---\n{Colors.END}")
                time.sleep(2)
                continue

            configs.append({
                "token": token,
                "channel_id": channel_id,
                "message": message,
                "t_min": t_min,
                "t_max": t_max
            })

            print_header("Configuração Concluída")
            outro = get_input("Deseja configurar outro canal? (S/n)", Colors.MAGENTA).lower()
            if outro == 'n':
                break

        main_loop(configs, my_id)

    except (KeyboardInterrupt, EOFError):
        print(f"\n{Colors.MAGENTA}--- Operação cancelada pelo usuário ---\n{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}--- Ocorreu um erro crítico: {e} ---\n{Colors.END}")

if __name__ == "__main__":
    main()
    