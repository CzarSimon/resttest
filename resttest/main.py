# Standard library
from typing import Optional

# 3rd party modules
import fire

# Internal modules
from resttest.service import Reader, FileReader
from resttest.service import get_random_port
from resttest.service import run_tests


class RestTest:
    """Cli tool for testing rest apis"""

    def __init__(self):
        self._reader: Reader = FileReader("./test-cases")

    def get_port(self) -> None:
        """Selects a random unused port and prints it to stdout."""
        print(get_random_port())

    def run(self, port: int = 443, name: Optional[str] = None) -> None:
        """Runs tests using provided port
        
        :param port: Port on which the api under test is exposed.
        :param name: Optional test case name.
        """
        if name:
            self._run_test_case(port, name)
            return
        self._run_all(port)

    def _run_test_case(self, port: int, name: str) -> None:
        """Runs a specific test using provided port
        
        :param port: Port on which the api under test is exposed.
        :param name: Test case name.
        """
        env = self._reader.read_env(port)
        test_case = self._reader.read_test_case(name)
        run_tests([test_case], env)

    def _run_all(self, port: int) -> None:
        """Runs all test using provided port
        
        :param port: Port on which the api under test is exposed.
        """
        env = self._reader.read_env(port)
        test_cases = self._reader.read_test_cases()
        run_tests(test_cases, env)


def main() -> None:
    fire.Fire(RestTest)


if __name__ == "__main__":
    main()

