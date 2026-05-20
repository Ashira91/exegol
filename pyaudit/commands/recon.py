from __future__ import annotations
import socket
from pathlib import Path
from typing import Any
import dns.resolver
import whois
from pyaudit.models.report import Report
from pyaudit.models.target import Target
from pyaudit.utils.logger import get_logger

logger = get_logger("pyaudit.recon")
_COMMON_SUBDOMAINS = ["www","mail","ftp","ssh","vpn","api","dev","staging","admin","ns1","ns2"]

def _get_ip(domain: str) -> str | None:
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return None

def _whois_info(domain: str, timeout: int) -> dict[str, Any]:
    try:
        w = whois.whois(domain)
        return {
            "registrar": str(w.registrar or "N/A"),
            "creation_date": str(w.creation_date or "N/A"),
            "expiration_date": str(w.expiration_date or "N/A"),
            "name_servers": str(w.name_servers or "N/A"),
        }
    except Exception as exc:
        logger.warning("WHOIS échoué pour %s : %s", domain, exc)
        return {"erreur": str(exc)}

def _dns_records(domain: str) -> dict[str, list[str]]:
    records: dict[str, list[str]] = {}
    for rtype in ("A", "MX", "NS", "TXT"):
        try:
            answers = dns.resolver.resolve(domain, rtype)
            records[rtype] = [str(r) for r in answers]
        except Exception:
            records[rtype] = []
    return records

def _find_subdomains(domain: str, subdomains: list[str]) -> list[str]:
    found: list[str] = []
    for sub in subdomains:
        fqdn = f"{sub}.{domain}"
        ip = _get_ip(fqdn)
        if ip:
            found.append(f"{fqdn} -> {ip}")
    return found

def run(domain: str, config: dict[str, Any], output_dir: Path, log_dir: Path) -> None:
    logger.info("Démarrage de la reconnaissance passive sur : %s", domain)
    recon_cfg = config.get("recon", {})
    timeout: int = recon_cfg.get("timeout", 5)
    subdomains: list[str] = recon_cfg.get("subdomains", _COMMON_SUBDOMAINS)
    target = Target(host=domain)
    if not target.is_reachable:
        logger.error("Impossible de résoudre %s", domain)
        return
    report = Report(command=f"recon {domain}", target=domain)
    report.add_section("Résolution IP", {"Domaine": domain, "IP": target.ip})
    logger.info("Collecte WHOIS...")
    report.add_section("WHOIS", _whois_info(domain, timeout))
    logger.info("Collecte DNS...")
    dns_data = _dns_records(domain)
    report.add_section("Enregistrements DNS", {k: ", ".join(v) if v else "Aucun" for k, v in dns_data.items()})
    logger.info("Recherche sous-domaines...")
    found = _find_subdomains(domain, subdomains)
    report.add_section("Sous-domaines", found if found else ["Aucun trouvé"])
    fmt: str = config.get("report", {}).get("format", "txt")
    saved = report.save(output_dir, fmt=fmt)
    logger.info("Rapport sauvegardé : %s", saved)
    print(report.to_text())
