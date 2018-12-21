# 3rd party modules
import fire

# Internal modules
from resttest.service import Reader
from resttest.service import get_random_port
from resttest.service import run_tests


class RestTest:
    """Cli tool for testing rest apis"""

    def run(self, port: int = 443) -> None:
        """Runs tests using provided port
        
        :param port: Port on which the api under test is exposed.
        """
        r = Reader("./test-cases")
        env = r.read_env(port)
        test_cases = r.read_test_cases()
        for tc in test_cases:
            print(tc)
        return
        run_tests(test_cases, env)

    def get_port(self) -> None:
        """Selects a random unused port and prints it to stdout."""
        print(get_random_port())


def main() -> None:
    fire.Fire(RestTest)


if __name__ == "__main__":
    main()

