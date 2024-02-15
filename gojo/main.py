""" cli/entrypoint to interact with our App
"""
import typer
from pyfiglet import Figlet
# from operations.cli import quality_runner
from gojo.utils.log import get_logger


logger = get_logger(__name__)

# TODO: Add author and more about the App
f = Figlet(font='slant')
print(f.renderText('Welcome to Gojo data quality tool!!'))


app = typer.Typer()


@app.command()
def run_test():
   logger.info("Run quality_runner")
   print("Run quality_runner")
   # quality_runner()


@app.command()
def send_slack_message():
   logger.info("Run quality_runner")
   # quality_runner()
