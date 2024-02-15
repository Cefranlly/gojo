""" cli/entrypoint to interact with our App
"""
import typer
from operations.cli import quality_runner
from utils.log import get_logger
from pyfiglet import Figlet


logger = get_logger(__name__)


# TODO: Add author and more about the App
f = Figlet(font='slant')
print(f.renderText('Welcome to Gojo data quality tool!!'))


app = typer.Typer()


@app.command()
def run_test():
   logger.info("Run quality_runner")
   quality_runner()


app()
