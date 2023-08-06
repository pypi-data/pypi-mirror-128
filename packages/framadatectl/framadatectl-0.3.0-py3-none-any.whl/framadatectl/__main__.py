import argparse
import locale
import pathlib
import sys

from .__about__ import (
    __description__,
    __version__,
)
from .framadate import Framadate
from .commands import COMMANDS_DICT
from .configuration import Configuration


def main():
    locale.setlocale(locale.LC_ALL, '')
    parser = argparse.ArgumentParser(description=__description__)

    parser.add_argument('-c', '--config', type=pathlib.Path,
                        help='Path to a config file')
    parser.add_argument('--url', type=str,
                        help='Full Framadate URL (admin or public)')
    parser.add_argument('--min-votes', type=int,
                        help='Minimum number of required votes'
                        ' (used by check commands)')
    parser.add_argument('--max-votes', type=int,
                        help='Maximum number of required votes'
                        ' (used by check commands)')
    parser.add_argument('--quiet', action='store_true',
                        help='Make the output less verbose')
    parser.add_argument('-v',
                        '--version',
                        action='version',
                        version='%s %s' % (__package__, __version__))

    subparsers_cmd = parser.add_subparsers(
        title='commands', dest='command', required=True
    )
    for cmd, cmdinfo in COMMANDS_DICT.items():
        subparser_cmd = subparsers_cmd.add_parser(cmd, help=cmdinfo['help'])
        if 'subcommands' in cmdinfo:
            subparsers_scmd = subparser_cmd.add_subparsers(
                title='subcommands', dest='subcommand', required=True
            )
            for subcmd, subcmdinfo in cmdinfo['subcommands'].items():
                subparser_scmd = subparsers_scmd.add_parser(
                    subcmd, help=subcmdinfo['help']
                )
                if 'args' in subcmdinfo:
                    for arg in subcmdinfo['args']:
                        subparser_scmd.add_argument(
                            arg['name'], help=arg['help'], type=arg['type']
                        )
        elif 'args' in cmdinfo:
            for arg in cmdinfo['args']:
                subparser_cmd.add_argument(
                    arg['name'], help=arg['help'], type=arg['type']
                )

    if len(sys.argv) <= 1:
        args = parser.parse_args(['--help'])
    else:
        args = parser.parse_args()
    config = Configuration(
        yaml_path=args.config,
        url=args.url,
        votes_min=args.min_votes,
        votes_max=args.max_votes,
        quiet=args.quiet
    )
    if config.get_url() is None:
        sys.exit('error: Framadate URL is null')
    if hasattr(args, 'subcommand'):
        func = COMMANDS_DICT[args.command]['subcommands'][
            args.subcommand]['func']
    else:
        func = COMMANDS_DICT[args.command]['func']
    framadate = Framadate(config.get_url())
    return func(config, framadate, args)


if __name__ == '__main__':
    sys.exit(main())
