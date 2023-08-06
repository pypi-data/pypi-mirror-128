import argparse
import sys
from qrunner import __version__, __description__
from qrunner.scaffold import init_scaffold_project, main_scaffold_project
from qrunner.scaffold_case import init_scaffold_case, main_scaffold_case
from qrunner.scaffold_page import init_scaffold_page, main_scaffold_page


def main():
    """ API test: parse command line options and run commands.
    """
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument(
        "-V", "--version", dest="version", action="store_true", help="show version"
    )

    subparsers = parser.add_subparsers(help="sub-command help")
    sub_parser_project = init_scaffold_project(subparsers)
    sub_parser_case = init_scaffold_case(subparsers)
    sub_parser_page = init_scaffold_page(subparsers)

    if len(sys.argv) == 1:
        # qrun
        parser.print_help()
        sys.exit(0)
    elif len(sys.argv) == 2:
        # print help for sub-commands
        if sys.argv[1] in ["-V", "--version"]:
            # qrun -V
            print(f"{__version__}")
        elif sys.argv[1] in ["-h", "--help"]:
            # qrun -h
            parser.print_help()
        elif sys.argv[1] == "startpro":
            # qrun startpro
            sub_parser_project.print_help()
        elif sys.argv[1] == "startcase":
            # qrun startcase
            sub_parser_case.print_help()
        elif sys.argv[1] == "startpage":
            # qrun startpage
            sub_parser_page.print_help()
        sys.exit(0)
    elif len(sys.argv) == 3:
        if sys.argv[1] == "startpro":
            print('missing project_name')
        elif sys.argv[1] == "startcase":
            print('missing case_name')
        elif sys.argv[1] == "startpage":
            print('missing page_name')
        sys.exit(0)
    elif len(sys.argv) == 4:
        if sys.argv[1] == "startpro":
            args = parser.parse_args()
            main_scaffold_project(args)
        elif sys.argv[1] == "startcase":
            args = parser.parse_args()
            main_scaffold_case(args)
        elif sys.argv[1] == "startpage":
            args = parser.parse_args()
            main_scaffold_page(args)
        sys.exit(0)


if __name__ == "__main__":
    main()
