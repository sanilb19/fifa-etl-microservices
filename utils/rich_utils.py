from rich.console import Console
from rich.traceback import install

install(show_locals=True, suppress=[])
console = Console()