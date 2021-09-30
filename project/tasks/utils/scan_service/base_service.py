from abc import abstractmethod, ABC
from tasks.utils.mapper import Mapper


class ScanService(ABC):
    """Сервис сканирования сети."""
    _address = None

    def __init__(self, address) -> None:
        self._address = address

    @abstractmethod
    def scan(self, execute_args: str = None) -> dict:
        """Начать сканирование по переданному диапазону адресов.

        Args:
            ip_diap (str): Дипазон адресов

        Returns:
            dict: результат сканирования
        """
        pass
