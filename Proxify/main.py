from concurrent.futures import ThreadPoolExecutor, as_completed
import shutil
import random
from time import time
import os

try:
    import colorama, pystyle, bs4, tqdm, pandas, tabulate, requests
except ModuleNotFoundError:
    os.system("pip install requests")
    os.system("pip install colorama")
    os.system("pip install pystyle")
    os.system("pip install bs4")
    os.system("pip install tqdm")
    os.system("pip install pandas")
    os.system("pip install tabulate")

from colorama import Fore
from pystyle import Colors, Colorate, Write
from threading import Lock
from bs4 import BeautifulSoup
from tabulate import tabulate
import pandas as pd
import requests

# blue_to_cyan
# red_to_blue

titleColor = Colors.red_to_blue
toolColor = Colors.red_to_blue

# Définir le nom de la fenêtre du terminal
os.system("title Proxify 🚀 / Dev by rayan38000")

write_lock = Lock()

def clearConsole():
    os.system('cls' if os.name == 'nt' else 'clear')

def home(animation=True):

    if animation == True:
        animateText = 0.02
    else:
        animateText = 0

    clearConsole()
    title = """
    ________                    _____________        
    ___  __ \________________  ____(_)__  __/____  __
    __  /_/ /_  ___/  __ \_  |/_/_  /__  /_ __  / / /
    _  ____/_  /   / /_/ /_>  < _  / _  __/ _  /_/ / 
    /_/     /_/    \____//_/|_| /_/  /_/    _\__, /  
                                            /____/     
    ~~ Tools for proxies developed by rayan38000 ~~          
    """
    # Create a gradient effect with the Colorate function
    styled_title = Colorate.Horizontal(titleColor, title)
    print(styled_title)

    print(f"\n[{Colors.green}1{Colors.reset}] > ", end="")
    Write.Print("Proxies scraper", toolColor , interval=animateText)

    print(f"\n[{Colors.green}2{Colors.reset}] > ", end="")
    Write.Print("Proxies checker", toolColor , interval=animateText)

    print(f"\n[{Colors.green}3{Colors.reset}] > ", end="")
    Write.Print("Get information about one proxy", toolColor , interval=animateText)


# Partie vérification des proxies -----------------------------------------------------------------------------------------------------------------------




# Liens à scraper ----------------------------------------------------------------------------------------------------------------------------------------------
# [Liens vérifié le 23/08/2024]

with open(f"links/http.txt", 'r', encoding='utf-8') as f:
    http_links = [line.strip() for line in f if line.strip()]  

with open(f"links/socks4.txt", 'r', encoding='utf-8') as f:
    socks4_links = [line.strip() for line in f if line.strip()]  

with open(f"links/socks5.txt", 'r', encoding='utf-8') as f:
    socks5_links = [line.strip() for line in f if line.strip()]  


# SCRAPING PROXIES FUNCTIONS -----------------------------------------------------------------------------------------------------------------------------------
user_agent = [
    'Mozilla/5.0 (X11; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9a1) Gecko/20060814 Firefox/51.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/58.0.1',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.74 Safari/537.36 Edg/79.0.309.43',
]
headers = {
    'User-Agent': random.choice(user_agent),
}


class ProxyChecker:

    def __init__(self):
        self.ip = self.get_my_ip()

    def get_my_ip(self):
        sites = ['http://ipinfo.io/ip', 'https://api.ipify.org/', 'http://ifconfig.io/ip'] # Liens vérifié le 23/08/2024
        ip = self.get_info(url=random.choice(sites))
        return ip.text

    def get_info(self, url=None, proxy=None):
        info = {}
        proxy_type = []
        judges = ['http://azenv.net/', 'http://httpheader.net/azenv.php', 'http://mojeip.net.pl/asdfa/azenv.php'] # Liens vérifié le 23/08/2024
        if url != None:
            try:
                response = requests.get(url, headers=headers, timeout=5)
                return response
            except:
                pass
        elif proxy != None:

            for protocol in ['http', 'socks4', 'socks5']:
                proxy_dict = {
                    'https': f'{protocol}://{proxy}',
                    'http': f'{protocol}://{proxy}',
                }
                try:
                    start = time()
                    response = requests.get(random.choice(judges), proxies=proxy_dict, headers=headers, timeout=5)
                    finish = time() - start
                    if response.status_code == 200:
                        proxy_type.append(protocol)
                        info['type'] = proxy_type
                        info['time_response'] = ("%.3f" % finish)
                        info['status'] = True
                        
                        if str(self.ip) in response.text:
                            info['anonymity'] = 'Transparent'

                        else:
                            info['anonymity'] = 'Anonymous'
                        if protocol == 'http':
                            return info
                except:
                    pass

            if 'status' not in info.keys():
                info['status'] = False
                return info
            else:
                return info

    def get_geo(self, ip):
        url = ['http://ipwhois.app/json/', 'http://ip-api.com/json/', 'https://api.techniknews.net/ipgeo/'] # Liens vérifié le 23/08/2024
        resp = self.get_info(url=f'{random.choice(url)}{ip}')
        return resp

    def check_proxy(self, proxy):
        ip = proxy.split(':')
        resp = self.get_info(proxy=proxy)

        if resp['status'] == True:
            result = {}
            geo = self.get_geo(ip[0])
            geo_info = geo.json()
            result['status'] = resp['status']
            result['type'] = resp['type']
            result['time_response'] = resp['time_response']
            result['anonymity'] = resp['anonymity']
            result['country'] = geo_info['country']
            result['city'] = geo_info['city']
            try:
                result['country_code'] = geo_info['country_code']
            except:
                result['country_code'] = geo_info['countryCode']

            return result

        else:
            return resp


# Combine les url avec leur type
def get_urls_with_type(proxyType="all"):
    if proxyType == "http":
        return[(url, 'http') for url in http_links]
    elif proxyType == "socks4":
        return [(url, 'socks4') for url in socks4_links]
    elif proxyType == "socks5":
        return [(url, 'socks5') for url in socks5_links]
    else:
        return [(url, 'http') for url in http_links] + [(url, 'socks5') for url in socks5_links] + [(url, 'socks4') for url in socks4_links]

def gradient_bar(value, max_value):
    gradient = Colors.blue
    ratio = int((value / max_value) * 100)
    return gradient * (ratio // 2)

def fetch_proxies(urls_with_type, description):
    proxies = {'http': set(), 'socks4': set(), 'socks5': set()}
    total_urls = len(urls_with_type)
    with tqdm.tqdm(total=total_urls, desc=Colors.reset+description, unit="URL") as pbar:
        for i, (url, proxy_type) in enumerate(urls_with_type):
            try:
                response = requests.get(url)
                response.raise_for_status()
                proxies[proxy_type].update(line.strip() for line in response.text.splitlines() if line.strip())
            except requests.RequestException as e:
                ...

            # Mise à jour de la barre de progression
            bar = gradient_bar(i + 1, total_urls)
            pbar.set_description(f"{description}: {bar} {i + 1}/{total_urls}")
            pbar.update()
    
    return proxies

# Scraping header's proxy & informations ------------------------------------------------------------------------------------------------------------------
def fetch_ip_info(ip):
    """
    Récupère les informations IP et retourne les données sous forme de dictionnaire.

    :param ip: Adresse IP pour laquelle obtenir les informations
    :return: Dictionnaire contenant les informations IP
    """
    try:
        # URL avec l'IP à tester
        url = f'https://ipwhois.app/json/{ip}'

        # Effectue la requête
        response = requests.get(url, timeout=10)
        
        # Vérifie si la réponse est réussie (status_code 200)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Erreur lors de la récupération des informations pour l'IP {ip} : {response.status_code}")
            return None
    
    except requests.RequestException as e:
        # Affiche l'erreur en cas de problème
        print(f"Erreur lors de la connexion : {e}")
        return None

def ip_info_to_dataframe(ip_info):
    """
    Convertit les informations IP en DataFrame avec des lignes pour chaque clé.

    :param ip_info: Dictionnaire contenant les informations IP
    :return: DataFrame pandas avec les informations IP en lignes
    """
    if ip_info:
        # Convertit le dictionnaire en DataFrame avec chaque clé comme ligne
        df = pd.DataFrame(list(ip_info.items()), columns=['Key', 'Value'])
        return df
    else:
        print("Aucune information disponible pour créer un DataFrame.")
        return pd.DataFrame(columns=['Key', 'Value'])

def format_dataframe(df):
    """
    Formate le DataFrame pour afficher les données en deux colonnes sans en-têtes ni numéros de lignes.

    :param df: DataFrame contenant les informations IP
    :return: DataFrame formaté avec les informations IP affichées en deux colonnes
    """
    if not df.empty:
        # Réinitialise les noms de colonnes
        df.columns = ['Key', 'Value']
        return df
    else:
        return pd.DataFrame(columns=['Key', 'Value'])

def display_table(df):
    """
    Affiche le DataFrame sous forme de tableau stylisé avec deux colonnes.

    :param df: DataFrame contenant les informations IP
    """
    if not df.empty:
        # Convertit le DataFrame en liste de listes pour tabulate
        table = df.values.tolist()
        # Affiche le tableau en utilisant tabulate
        print(tabulate(table, tablefmt='fancy_grid', showindex=False))
    else:
        print("Le DataFrame est vide.")

def fetchProxyHeaders(proxy_url):
    """
    Effectue une requête vers http://azenv.net/ via un proxy et renvoie les en-têtes détectés par le site.
    
    :param proxy_url: URL du proxy au format 'http://adresse:port'
    :return: Dictionnaire contenant les en-têtes HTTP retournés par http://azenv.net/
    """
    try:
        url = 'http://azenv.net/'
        proxies = {
            'http': proxy_url,
            'https': proxy_url
        }

        response = requests.get(url, proxies=proxies, timeout=10)
        
        if response.status_code == 200:
            return response.text
        else:
            print(f"Erreur lors de la récupération des en-têtes via le proxy : {response.status_code}")
            return None
    
    except requests.RequestException as e:
        print(f"Erreur lors de la connexion : {e}")
        return None

def extractHeadersFromHtml(html_content):

    soup = BeautifulSoup(html_content, 'html.parser')
    pre_tag = soup.find('pre')
    
    if pre_tag:
        # Sépare chaque ligne en liste et supprime les lignes vides
        headers_lines = [line.strip() for line in pre_tag.text.splitlines() if line.strip()]
        
        # Fais un dictionnaire à partir des lignes de type clé=valeur
        headers = dict(line.split(' = ', 1) for line in headers_lines if ' = ' in line)
        return headers
    else:
        # Aucune balise <pre> trouvée dans le contenu HTML.
        return False

def dictToTable(headers_dict):
    """
    Convertit un dictionnaire en tableau avec tabulate.

    :param headers_dict: Dictionnaire contenant les en-têtes HTTP
    :return: Tableau formaté avec tabulate
    """
    # Convertir le dictionnaire en une liste de tuples (clé, valeur)
    table_data = list(headers_dict.items())
    
    # Utiliser tabulate pour créer le tableau avec deux colonnes
    table = tabulate(table_data, tablefmt="fancy_grid")
    
    return table


def write_proxy_to_file(filename, data):
    """
    Écrit les données de proxy dans le fichier spécifié.
    Utilise un verrou pour éviter les conflits lors de l'écriture depuis plusieurs threads.
    """
    with write_lock:  # Verrouille l'accès à la ressource partagée
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(data + '\n')







badChoice = False
home()
while True:

    if badChoice == True:
        print(f"\n\n{Colors.reset} ╭─[{Colors.purple}Whats your choice ?{Colors.reset}] {Colors.red}Invalid choice ! Please retry with a number{Colors.reset}")
    else:
        print(f"\n\n{Colors.reset} ╭─[{Colors.purple}Whats your choice ?{Colors.reset}]")
        
    clientRequest = input(" ╰┈➤  "+Colors.green)

    match clientRequest:
        case "1":
            badChoice = False
            print(f"\n{Colors.reset}[{Colors.green}1{Colors.reset}] > ", end="")
            Write.Print("Scrape all proxies", toolColor , interval=0.02)

            print(f"\n[{Colors.green}2{Colors.reset}] > ", end="")
            Write.Print("Scrape http/s proxies only", toolColor , interval=0.02)

            print(f"\n[{Colors.green}3{Colors.reset}] > ", end="")
            Write.Print("Scrape socks4 proxies only", toolColor , interval=0.02)

            print(f"\n[{Colors.green}4{Colors.reset}] > ", end="")
            Write.Print("Scrape socks5 proxies only", toolColor , interval=0.02)

            userChoice = False

            while userChoice is False:
                if userChoice == True:
                    print(f"\n\n{Colors.reset} ╭─[{Colors.purple}Whats your choice ?{Colors.reset}] ~ {Colors.gray}/ScrapingProxies{Colors.reset} {Colors.red}Invalid choice ! Please retry with a number{Colors.reset}")
                else:
                    print(f"\n\n{Colors.reset} ╭─[{Colors.purple}Whats your choice ?{Colors.reset}] ~ {Colors.gray}/ScrapingProxies{Colors.reset}")
                    
                typeChoice = input(" ╰┈➤  "+Colors.green)

                if typeChoice in ["1", "2", "3", "4"]:
                    userChoice = True
                else:
                    badChoiceFile = True

            if typeChoice == "1":

                proxies = fetch_proxies(get_urls_with_type("all"), "Scraping proxies")
                os.makedirs('scraped_proxies', exist_ok=True)

                # Enregistrer les proxies dans des fichiers pour vérification
                with open('scraped_proxies/http_proxies.txt', 'w', encoding='utf-8') as f:
                    f.write("\n".join(proxies['http']))

                with open('scraped_proxies/socks4_proxies.txt', 'w', encoding='utf-8') as f:
                    f.write("\n".join(proxies['socks4']))

                with open('scraped_proxies/socks5_proxies.txt', 'w', encoding='utf-8') as f:
                    f.write("\n".join(proxies['socks5']))

                print(f"HTTP proxies scraped: {Fore.GREEN}{len(proxies['http'])}{Fore.RESET}")
                print(f"SOCKS4 proxies scraped: {Fore.GREEN}{len(proxies['socks4'])}{Fore.RESET}")
                print(f"SOCKS5 proxies scraped: {Fore.GREEN}{len(proxies['socks5'])}{Fore.RESET}")

            elif typeChoice == "2":

                proxies = fetch_proxies(get_urls_with_type("http"), "Scraping HTTP/s proxies")
                os.makedirs('scraped_proxies', exist_ok=True)

                with open('scraped_proxies/http_proxies.txt', 'w', encoding='utf-8') as f:
                    f.write("\n".join(proxies['http']))

                print(f"HTTP proxies scraped: {Fore.GREEN}{len(proxies['http'])}{Fore.RESET}")

            elif typeChoice == "3":

                proxies = fetch_proxies(get_urls_with_type("socks4"), "Scraping SOCKS4 proxies")
                os.makedirs('scraped_proxies', exist_ok=True)

                with open('scraped_proxies/socks4_proxies.txt', 'w', encoding='utf-8') as f:
                    f.write("\n".join(proxies['socks4']))

                print(f"SOCKS4 proxies scraped: {Fore.GREEN}{len(proxies['socks4'])}{Fore.RESET}")

            elif typeChoice == "4":
                proxies = fetch_proxies(get_urls_with_type("socks5"), "Scraping SOCKS5 proxies")

                # Créer le dossier 'scraped_proxies' s'il n'existe pas
                os.makedirs('scraped_proxies', exist_ok=True)

                # Enregistrer les proxies dans des fichiers pour vérification
                with open('scraped_proxies/socks5_proxies.txt', 'w', encoding='utf-8') as f:
                    f.write("\n".join(proxies['socks5']))

                print(f"SOCKS5 proxies scraped: {Fore.GREEN+len(proxies['socks5'])+Fore.RESET}")

        case "2":
            badChoiceFile = False

            if not os.path.isdir('scraped_proxies'):
                os.makedirs('scraped_proxies', exist_ok=True)
                print("No proxy list detected in “scraped_proxies” folder")

            else:
                text_files = [f for f in os.listdir('scraped_proxies') if f.endswith('.txt')]
                if len(text_files) == 0:
                    print("No proxy list detected in “scraped_proxies” folder")
                else:
                    for i in range(1, len(text_files)+1):
                        print(f"\n{Colors.reset}[{Colors.green}{i}{Colors.reset}] > ", end="")
                        Write.Print(f"Start proxies verification on ", toolColor , interval=0.02)
                        print(f"{Colors.green}{text_files[i-1]}{Colors.reset}", end="")
            
                    userChoice = False

                    while userChoice is False:
                        if badChoiceFile == True:
                            print(f"\n\n{Colors.reset} ╭─[{Colors.purple}Whats your choice ?{Colors.reset}] ~ {Colors.gray}/CheckingProxies{Colors.reset} {Colors.red}Invalid choice ! Please retry with a number{Colors.reset}")
                        else:
                            print(f"\n\n{Colors.reset} ╭─[{Colors.purple}Whats your choice ?{Colors.reset}] ~ {Colors.gray}/CheckingProxies{Colors.reset}")
                            
                        fileChoice = input(" ╰┈➤  "+Colors.green)

                        if fileChoice in [f"{i}" for i in range(1, len(text_files)+1) ]:
                            userChoice = True
                            fileTargeted = text_files[int(fileChoice)-1]
                            print("Checking proxies in",fileTargeted)
                        else:
                            badChoiceFile = True

                    print()

                    anon_prompt = Write.Print(f"Sorting proxies by anonymity? (y/n): ", toolColor , interval=0.02)
                    anonSortedChoice = input(anon_prompt or "")

                    while anonSortedChoice not in ['y','n','Y','N','yes','no','Yes','No','YES','NO']:
                        print(f'{Colors.red}Answer YES or NO.{Colors.reset}')
                        anonSortedChoice = input(anon_prompt or "")

                    country_prompt = Write.Print(f"Sorting proxies by country? (y/n): ", toolColor , interval=0.02)
                    countrySortedChoice = input(country_prompt or "")

                    while countrySortedChoice not in ['y','n','Y','N','yes','no','Yes','No','YES','NO']:
                        print(f'{Colors.red}Answer YES or NO.{Colors.reset}')
                        countrySortedChoice = input(country_prompt or "")

                    print()

                    folderWorkProxies = "checked_proxies"

                    # ON suppr le folder si il existe sinon on fait rien
                    if os.path.exists(folderWorkProxies):
                        shutil.rmtree(folderWorkProxies)
                        print(f"Le dossier {folderWorkProxies} a été supprimé avec succès.")
                    
                    # ON (re)créer un dossier 
                    os.makedirs(folderWorkProxies)




                        

                    def process_proxy(proxy):
                        checker = ProxyChecker()
                        return checker.check_proxy(proxy)

                    with open(f"scraped_proxies/{fileTargeted}", 'r', encoding='utf-8') as f:
                        proxies = [line.strip() for line in f if line.strip()]

                    with ThreadPoolExecutor(max_workers=100) as executor:
                        future_to_proxy = {executor.submit(process_proxy, proxy): proxy for proxy in proxies}
                        for future in as_completed(future_to_proxy):
                            proxy = future_to_proxy[future]
                            try:
                                checkingProxy = future.result()
                                if checkingProxy and checkingProxy['status'] == True:
                                    print(
                                        f"{Colors.green}➜{Colors.reset} "
                                        f" [{Colorate.Horizontal(toolColor, proxy)}] - Type: {Colorate.Horizontal(toolColor, str(checkingProxy['type']))} "
                                        f"Proxy speed: {Colorate.Horizontal(toolColor, str(checkingProxy['time_response']) + ' s')} - "
                                        f"Country: {Colorate.Horizontal(toolColor, checkingProxy['country'])} - "
                                        f"Anonymity: {Colorate.Horizontal(toolColor, checkingProxy['anonymity'])}"
                                    )


                                    if anonSortedChoice in ['y','Y','yes','Yes','YES'] and countrySortedChoice in ['y','Y','yes','Yes','YES']:

                                        # Creer le dossier d'anonymat spécifique au proxy si il n'existe pas déjà
                                        if not os.path.exists(f'{folderWorkProxies}/{checkingProxy['anonymity']}'):
                                            os.makedirs(f'{folderWorkProxies}/{checkingProxy['anonymity']}', exist_ok=True)

                                        for type in checkingProxy['type']:

                                            # Creer le dossier de type spécifique au proxy si il n'existe pas déjà
                                            if not os.path.exists(f'{folderWorkProxies}/{checkingProxy["anonymity"]}/{type}'):
                                                os.makedirs(f'{folderWorkProxies}/{checkingProxy["anonymity"]}/{type}', exist_ok=True)

                                            write_proxy_to_file(f'{folderWorkProxies}/{checkingProxy["anonymity"]}/{type}/{checkingProxy['country']}.txt', proxy)
                                    
                                    elif anonSortedChoice in ['y','Y','yes','Yes','YES'] and countrySortedChoice in ['n','N','no','No','NO']:

                                        # Creer le dossier d'anonymat spécifique au proxy si il n'existe pas déjà
                                        if not os.path.exists(f'{folderWorkProxies}/{checkingProxy['anonymity']}'):
                                            os.makedirs(f'{folderWorkProxies}/{checkingProxy['anonymity']}', exist_ok=True)

                                        for type in checkingProxy['type']:
                                            write_proxy_to_file(f'{folderWorkProxies}/{checkingProxy["anonymity"]}/{type}.txt', proxy)
                                    
                                    elif anonSortedChoice in ['n','N','no','No','NO'] and countrySortedChoice in ['y','Y','yes','Yes','YES']:

                                        for type in checkingProxy['type']:

                                            # Creer le dossier de type spécifique au proxy si il n'existe pas déjà
                                            if not os.path.exists(f'{folderWorkProxies}/{type}'):
                                                os.makedirs(f'{folderWorkProxies}/{type}', exist_ok=True)

                                            write_proxy_to_file(f'{folderWorkProxies}/{type}/{checkingProxy['country']}.txt', proxy)

                                    elif anonSortedChoice in ['n','N','no','No','NO'] and countrySortedChoice in ['n','N','no','No','NO']:

                                        for type in checkingProxy['type']:
                                            write_proxy_to_file(f'{folderWorkProxies}/{type}.txt', proxy)


                            except Exception as e:
                                print(f"Error processing proxy {proxy}: {e}")

        case "3":
            badChoice = False

            proxyChoice = False
            badProxyChoice = False

            while proxyChoice is False:
                if badProxyChoice == True:
                    print(f"\n\n{Colors.reset} ╭─[{Colors.purple}Enter your proxy{Colors.reset}] ~ {Colors.gray}/ProxyData{Colors.reset} {Colors.red}Invalid choice ! Please retry with this pattern > [ip]:[port]{Colors.reset}")
                else:
                    print(f"\n\n{Colors.reset} ╭─[{Colors.purple}Enter your proxy{Colors.reset}] ~ {Colors.gray}/ProxyData{Colors.reset}")
                    
                proxyTargeted = input(" ╰┈➤  "+Colors.green)

                try:
                    ip_info = fetch_ip_info(proxyTargeted.split(':')[0])
                    df = ip_info_to_dataframe(ip_info)
                    df_formated = format_dataframe(df)
                    proxyHeaderDict = extractHeadersFromHtml(fetchProxyHeaders(f'http://{proxyTargeted}'))
                    proxy_headers = dictToTable(proxyHeaderDict)

                    if proxy_headers != False:
                        print()
                        print(Colorate.Horizontal(toolColor, "PROXY LOOKUP"))
                        display_table(df_formated)
                        print()
                        print(Colorate.Horizontal(toolColor, "PROXY HEADER"))
                        print(proxy_headers)
                        print()
                        
                        headers_to_check = [
                            # Format avec tirets
                            'X-REAL-IP', 'X-FORWARDED-FOR', 'X-PROXY-ID', 'VIA', 'FORWARDED-FOR', 'X-FORWARDED',
                            'HTTP-FORWARDED', 'CLIENT-IP', 'FORWARDED-FOR-IP', 'FORWARDED_FOR', 'X-FORWARDED FORWARDED', 'CLIENT_IP',
                            'PROXY-CONNECTION', 'XROXY-CONNECTION', 'X-IMFORWARDS',
                            
                            # Format avec underscores
                            'X_REAL_IP', 'X_FORWARDED_FOR', 'X_PROXY_ID', 'VIA', 'FORWARDED_FOR', 'X_FORWARDED',
                            'HTTP_FORWARDED', 'CLIENT_IP', 'FORWARDED_FOR_IP', 'FORWARDED_FOR', 'X_FORWARDED_FOR', 'CLIENT_IP',
                            'PROXY_CONNECTION', 'XROXY_CONNECTION', 'X_IMFORWARDS',
                            
                            # Préfixes HTTP
                            'HTTP_X_REAL_IP', 'HTTP_X_FORWARDED_FOR', 'HTTP_X_PROXY_ID', 'HTTP_VIA', 'HTTP_FORWARDED_FOR', 'HTTP_X_FORWARDED',
                            'HTTP_CF_CONNECTING_IP', 'HTTP_CF_RAY', 'HTTP_CF_VISITOR', 'HTTP_CDN_LOOP', 'HTTP_CF_IPCOUNTRY',
                            'HTTP_CLIENT_IP', 'HTTP_X_CLIENT_IP'
                        ]

                        headerList = list(proxyHeaderDict.keys())
                        
                        anonScore = 0

                        for header in headerList:
                            if header in headers_to_check:
                                anonScore += 1
                        
                        realIP = ProxyChecker()
                        
                        if realIP.ip in list(proxyHeaderDict.values()):
                            print(f"{Colors.yellow}Your ip is disclosed in the proxy header, so this type of proxy is not recommended if you're looking for anonymity.{Colors.reset}")
                        else:
                            print("Your IP is not disclosed in the proxy header, so you can trust this proxy to keep your anonymity.")

                        print(f"The header contains {Colors.green}{anonScore}{Colors.reset} pieces of information that can be used to discover the proxy.")


                    else:
                        print("A problem occurred when retrieving the proxy header.")

                    proxyChoice = True
                except:
                    badProxyChoice = True
        case _ :
            home(animation=False)
            badChoice = True