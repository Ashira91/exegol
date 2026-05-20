from __future__ import annotations
from pathlib import Path
import pytest
from pyaudit.models.port import Port, PortStatus
from pyaudit.models.report import Report
from pyaudit.models.service import Service
from pyaudit.models.target import Target

class TestTarget:
    def test_valid_domain(self) -> None:
        t = Target(host="example.com")
        assert t.ip is not None
        assert t.is_reachable is True
    def test_invalid_domain(self) -> None:
        t = Target(host="domaine-inexistant-xyz-99999.xyz")
        assert t.ip is None
        assert t.is_reachable is False
    def test_explicit_ip_not_overwritten(self) -> None:
        t = Target(host="example.com", ip="1.2.3.4")
        assert t.ip == "1.2.3.4"

class TestPort:
    def test_default_status(self) -> None:
        p = Port(number=80)
        assert p.status == PortStatus.UNKNOWN
    def test_open_port(self) -> None:
        p = Port(number=443, status=PortStatus.OPEN)
        assert "open" in str(p)

class TestService:
    def test_str_with_version(self) -> None:
        s = Service(name="SSH", port=22, version="OpenSSH 9.0")
        assert "SSH" in str(s) and "22" in str(s)

class TestReport:
    def test_add_section(self) -> None:
        r = Report(command="recon test.com", target="test.com")
        r.add_section("IP", {"Domaine": "test.com", "IP": "1.2.3.4"})
        assert "IP" in r.sections
    def test_to_text(self) -> None:
        r = Report(command="recon test.com")
        r.add_section("Test", ["item1", "item2"])
        assert "item1" in r.to_text()
    def test_save_file(self, tmp_path: Path) -> None:
        r = Report(command="recon test.com")
        r.add_section("Test", "contenu")
        f = r.save(tmp_path, fmt="txt")
        assert f.exists()
