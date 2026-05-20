import socket
import subprocess
from datetime import datetime

domain = input("Domaine cible : ").strip()

output_file = f"rapport_{domain}.txt"

def write_result(title, content):
    print(f"\n[+] {title}")
    print(content)
    with open(output_file, "a") as f:
        f.write(f"\n\n===== {title} =====\n")
        f.write(str(content))

with open(output_file, "w") as f:
    f.write(f"Rapport de reconnaissance passive\n")
    f.write(f"Domaine : {domain}\n")
    f.write(f"Date : {datetime.now()}\n")

try:
    ip = socket.gethostbyname(domain)
    write_result("Adresse IP", ip)
except Exception as e:
    write_result("Adresse IP", f"Erreur : {e}")

for cmd_name, cmd in {
    "WHOIS": ["whois", domain],
    "DNS A": ["dig", domain, "A", "+short"],
    "DNS MX": ["dig", domain, "MX", "+short"],
    "DNS NS": ["dig", domain, "NS", "+short"],
    "DNS TXT": ["dig", domain, "TXT", "+short"],
}.items():
    try:
        result = subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT)
        write_result(cmd_name, result)
    except Exception as e:
        write_result(cmd_name, f"Erreur : {e}")

subdomains = ["www", "mail", "ftp", "admin", "vpn", "dev", "test"]

found = []
for sub in subdomains:
    full_domain = f"{sub}.{domain}"
    try:
        ip = socket.gethostbyname(full_domain)
        found.append(f"{full_domain} -> {ip}")
    except:
        pass

write_result("Sous-domaines trouvés", "\n".join(found) if found else "Aucun sous-domaine trouvé")

print(f"\n[✓] Rapport généré : {output_file}")
