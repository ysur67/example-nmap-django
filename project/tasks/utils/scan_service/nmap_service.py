import nmap
from .base_service import ScanService


class NmapService(ScanService):
    """Сервис сканирования сети, основанный на работе nmap."""
    def scan(self, execute_args: str = None) -> dict:
        network_mapper = nmap.PortScanner()
        scan_result = network_mapper.scan(hosts=self._address, arguments=execute_args)
        return scan_result["scan"]
