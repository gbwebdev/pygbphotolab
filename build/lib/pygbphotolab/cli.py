import click

@click.group()
def cli():
    pass

@cli.command()
def download():
    from pygbphotolab import download as module_download
    module_download.exec()

@cli.command()
def process_selection():
    from pygbphotolab import process_selection as module_process_selection
    module_process_selection.exec()

if __name__ == '__main__':
    cli()