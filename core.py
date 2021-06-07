import argparse
import os
import subprocess

from server import app


def prepare_parser():
    parser = argparse.ArgumentParser(description="Paper Manager")
    subparsers = parser.add_subparsers(dest="command")

    add_server_parser(subparsers)
    add_client_parser(subparsers)

    return parser


def add_server_parser(subparsers):
    parser = subparsers.add_parser("launch_server", description="Launch api server.")
    parser.add_argument("--port", default=2022, type=int)
    parser.add_argument("--config", default="datasets.json")


def launch_api_server(args):
    app.path_config = args.config
    app.app.run(host="0.0.0.0", port=args.port)


def add_client_parser(subparsers):
    parser = subparsers.add_parser(
        "launch_client", description="Launch client user interface."
    )
    parser.add_argument("--port", default=8080, type=int)


def launch_client(args):
    os.chdir("client")
    command = "yarn serve --port {}".format(args.port)
    subprocess.call(command, shell=True)


if __name__ == "__main__":
    parser = prepare_parser()
    args = parser.parse_args()

    if args.command == "launch_server":
        launch_api_server(args)
    elif args.command == "launch_client":
        launch_client(args)
    else:
        pass
