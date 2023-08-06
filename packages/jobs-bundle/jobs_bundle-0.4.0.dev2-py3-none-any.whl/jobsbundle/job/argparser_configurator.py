import sys
from argparse import ArgumentParser, Namespace


def add_kwargs(argument_parser: ArgumentParser):
    args = [arg for arg in sys.argv[3:] if not arg.startswith("--env")]

    for arg in args:
        arg_parsed = arg.split("=")

        argument_parser.add_argument(arg_parsed[0])


def extract_kwargs(input_args: Namespace):
    values = input_args.__dict__

    values.pop("help_selected", None)
    values.pop("command_name", None)

    return values
