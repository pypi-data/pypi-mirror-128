import logging, typer # pragma: no cover
from . import BaseClass, base_function


def main() -> None:  # pragma: no cover
    """
    The main function executes on commands:
    `python -m vaede` and `$ vaede `.
    """
    cli_runner = typer.Typer()

    @cli_runner.command()
    def help():
        raise NotImplemented

    @cli_runner.command()
    def prepare(verbose: bool):
        raise NotImplemented

    @cli_runner.command()
    def train(verbose: bool):
        raise NotImplemented

    @cli_runner.command()
    def test(verbose: bool):
        raise NotImplemented

    print("Executing main function")
    base = BaseClass()
    print(base.base_method())
    print(base_function())
    print("End of main function")


if __name__ == "__main__":  # pragma: no cover
    main()
