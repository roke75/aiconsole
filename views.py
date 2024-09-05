import time
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown

console = Console()


def console_print(message):
    console.print(message)

def console_print_markdown(message):
    console.print(Markdown(message))


def create_and_show_store_table(rows):
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Name", style="cyan")
    table.add_column("Id", style="magenta")
    table.add_column("Created", style="green")
    table.add_column("Files", style="blue")
    table.add_column("Size", style="blue")
    table.add_column("Status", style="blue")
    table.add_column("Expires after", style="blue")
    table.add_column("Expires at", style="blue")

    for row in rows:
        table.add_row(
            row.name,
            row.id,
            time.strftime(
                '%H:%M:%S %d.%m.%Y',
                time.gmtime(row.created_at)
            ),
            str(row.file_counts.total),
            str(row.usage_bytes),
            row.status,
            str(row.expires_after.days) if row.expires_after else "None",
            time.strftime(
                '%H:%M:%S %d.%m.%Y',
                time.gmtime(row.expires_at)
            ) if row.expires_at else "None"
        )

    console.print(table)


def create_and_show_file_table(rows):
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Id", style="cyan")
    table.add_column("Created", style="green")
    table.add_column("Size", style="blue")
    table.add_column("Status", style="blue")

    for row in rows:
        table.add_row(
            row.id,
            time.strftime(
                '%H:%M:%S %d.%m.%Y',
                time.gmtime(row.created_at)
            ),
            str(row.usage_bytes),
            row.status
        )

    console.print(table)


def create_and_show_assistant_table(rows):
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Name", style="cyan")
    table.add_column("Id", style="magenta")
    table.add_column("Created", style="green")
    table.add_column("Description", style="blue")
    table.add_column("Model", style="blue")

    for row in rows:
        table.add_row(
            row.name,
            row.id,
            time.strftime(
                '%H:%M:%S %d.%m.%Y',
                time.gmtime(row.created_at)
            ),
            row.description,
            row.model
        )

    console.print(table)


def create_and_show_thread_table(rows):
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Id", style="magenta")
    table.add_column("Created", style="green")

    for row in rows:
        table.add_row(
            row.id,
            time.strftime(
                '%H:%M:%S %d.%m.%Y',
                time.gmtime(row.created_at)
            ),
        )

    console.print(table)


def create_and_show_message_table(rows):
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Id", style="cyan")
    table.add_column("Created at", style="green")

    for row in rows:
        table.add_row(
            str(row.id),
            time.strftime(
                '%H:%M:%S %d.%m.%Y',
                time.gmtime(row.created_at)
            ),
        )

    console.print(table)


def create_and_show_run_table(rows):
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Id", style="cyan")
    table.add_column("Assistant Id", style="green")
    table.add_column("Thread Id", style="blue")
    table.add_column("Created at", style="green")
    table.add_column("Completed at", style="blue")

    for row in rows:
        table.add_row(
            str(row.id),
            row.assistant_id,
            row.thread_id,
            time.strftime(
                '%H:%M:%S %d.%m.%Y',
                time.gmtime(row.created_at)
            ),
            time.strftime(
                '%H:%M:%S %d.%m.%Y',
                time.gmtime(row.completed_at)
            ),
        )

    console.print(table)
