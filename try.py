from rich.console import Console
from rich.table import Table
from rich.live import Live
import psutil
import time

def rich_stats():
    console = Console()

    def create_table():
        table = Table(title="System Stats")
        table.add_column("Metric", justify="left", style="cyan", no_wrap=True)
        table.add_column("Value", justify="right", style="magenta")
        table.add_row("CPU Usage", f"{psutil.cpu_percent()}%")
        table.add_row("Memory Usage", f"{psutil.virtual_memory().percent}%")
        table.add_row("Disk Usage", f"{psutil.disk_usage('/').percent}%")
        net_io = psutil.net_io_counters()
        table.add_row("Network Sent", f"{net_io.bytes_sent / 1e6:.2f} MB")
        table.add_row("Network Received", f"{net_io.bytes_recv / 1e6:.2f} MB")
        return table

    with Live(console=console, refresh_per_second=1):

        console.print(create_table())

rich_stats()
