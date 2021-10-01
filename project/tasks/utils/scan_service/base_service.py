from abc import abstractmethod, ABC


class ScanService(ABC):
    """Сервис сканирования сети."""
    _address = None

    def __init__(self, address) -> None:
        self._address = address

    @abstractmethod
    def scan(self, execute_args: str = None) -> dict:
        """Начать сканирование по переданному диапазону адресов.

        Args:
            execute_args (str): Дополнительные параметры запуска

        Returns:
            dict: результат сканирования
        """
        pass
