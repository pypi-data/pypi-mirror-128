import argparse
from utils import config_util

DEFAULT_SIDEBAR = -1


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Generate HTML website from raw data"
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="cool_ssg_generator release 0.1",
        help="display the current version",
    )
    parser.add_argument(
        "-i",
        "--input",
        nargs="+",
        help="path to input file or directory",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="path to output directory",
    )
    parser.add_argument(
        "-s",
        "--stylesheets",
        nargs="+",
        help="attach stylesheet URLs",
    )
    parser.add_argument(
        "-l",
        "--lang",
        help="language of the generated documents, default is en-CA",
    )
    parser.add_argument(
        "-c",
        "--config",
        help="path to the config file",
    )
    parser.add_argument(
        "-sb",
        "--sidebar",
        nargs="?",
        help="generate sidebar from a sidebar config file, default sidebar will be used if no config file is specified",  # noqa: E501
        const=DEFAULT_SIDEBAR,
        default=None,
    )

    args = parser.parse_args()

    options = vars(args)

    if args.config:
        config_util.get_config(args.config, options)

    if args.sidebar:
        if args.sidebar != DEFAULT_SIDEBAR:
            config_util.get_sidebar_config(args.sidebar, options)

    # Assign default value for unspecified required options
    options["lang"] = "en-CA" if options["lang"] is None else options["lang"]

    return options
