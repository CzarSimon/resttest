# 3rd party modules
import fire

# Internal modules
from service import Reader
from service import get_random_port
from service import run_tests


class RestTest:
    """Cli tool for testing rest apis"""

    def run(self, port: int = 443) -> None:
        """Runs tests using provided port
        
        :param port: Port on which the api under test is exposed.
        """
        r = Reader("./test-cases")
        env = r.read_env(port)
        test_cases = r.read_test_cases()
        run_tests(test_cases, env)

    def get_port(self) -> None:
        """Selects a random unused port and prints it to stdout."""
        print(get_random_port())


if __name__ == "__main__":
    fire.Fire(RestTest)

