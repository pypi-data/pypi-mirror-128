#!/usr/bin/env python
import click

from .generators import GENERATOR_BY_OUTPUT_FORMAT

@click.command()
@click.option('--title', prompt='Title for the book', type=str)
@click.argument('output_format', default="pdf", type=str)
@click.argument('chapters_dir', default="chapters", type=str)
@click.argument('release_dir', default="release", type=str)
def build_book(title, output_format, chapters_dir, release_dir):
	click.echo(f"Building book with output format {output_format}")
	try:
		book_generator_class = GENERATOR_BY_OUTPUT_FORMAT[output_format]
	except KeyError:
		click.echo(f"Output format {output_format} is currently not supported, consider opening an issue or contributing")
	else:
		click.echo(f"Found parser for {output_format} output type, generating book")
		generator = book_generator_class(title=title, chapters_dir=chapters_dir, release_dir=release_dir)
		generator.build_book()

if __name__ == '__main__':
    build_book()