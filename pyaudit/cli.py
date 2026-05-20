from __future__ import annotations
import argparse
import sys
from pathlib import Path
from typing import Any
from pyaudit import __version__
from pyaudit.utils.config import load_config
from pyaudit.utils.logger import get_logger

def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pyaudit",
        description=f"PyAudit v{__version__} — Outil offensif d'audit réseau\nUsage strictement autorisé sur Kactus-Net",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--config", "-c", type=Path, metavar="FICHIER", help="Fichier de configuration YAML")
    parser.add_argument("--output", "-o", type=Path, default=Path("reports"), metavar="DOSSIER", help="Dossier de sortie des rapports")
    parser.add_argument("--log-dir", type=Path, default=Path("logs"), metavar="DOSSIER", help="Dossier des logs")
    parser.add_argument("--log-level", choices=["DEBUG","INFO","WARNING","ERROR"], default=None)
    subparsers = parser.add_subparsers(dest="command", title="Sous-commandes", metavar="<commande>")
    recon_p = subparsers.add_parser("recon", help="Reconnaissance passive d'un domaine")
    recon_p.add_argument("domain", help="Domaine cible (ex: example.com)")
    recon_p.add_argument("--timeout", type=int, default=None, metavar="SEC")
    subparsers.add_parser("scan", help="[Phase 3] Wrapper Nmap")
    subparsers.add_parser("portscan", help="[Phase 4] Scanner TCP asynchrone")
    subparsers.add_parser("sniff", help="[Phase 7] Analyse trafic Scapy")
    subparsers.add_parser("ssh-audit", help="[Phase 8] Audit SSH + CVE")
    subparsers.add_parser("llm-audit", help="[Phase 9] Audit KactusBot OWASP LLM")
    return parser

def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        sys.exit(0)
    try:
        config: dict[str, Any] = load_config(args.config)
    except FileNotFoundError as exc:
        print(f"[ERREUR] {exc}", file=sys.stderr)
        sys.exit(1)
    if args.log_level:
        config.setdefault("general", {})["log_level"] = args.log_level
    log_level: str = config.get("general", {}).get("log_level", "INFO")
    logger = get_logger("pyaudit", log_dir=args.log_dir, level=log_level)
    try:
        if args.command == "recon":
            from pyaudit.commands.recon import run as recon_run
            if args.timeout is not None:
                config.setdefault("recon", {})["timeout"] = args.timeout
            recon_run(domain=args.domain, config=config, output_dir=args.output, log_dir=args.log_dir)
        elif args.command in ("scan","portscan","sniff","ssh-audit","llm-audit"):
            print(f"[INFO] '{args.command}' sera implémenté dans une phase ultérieure.", file=sys.stderr)
    except KeyboardInterrupt:
        logger.info("Interruption (Ctrl+C)")
        sys.exit(130)
    except Exception as exc:
        logger.exception("Erreur non gérée : %s", exc)
        sys.exit(1)

if __name__ == "__main__":
    main()
