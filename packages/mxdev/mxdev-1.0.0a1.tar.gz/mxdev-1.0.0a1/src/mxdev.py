import re
from urllib import parse
from urllib import request

import argparse
import configparser
import logging
import pkg_resources
import typing


logger = logging.getLogger("mxdev")

parser = argparse.ArgumentParser(
    description="Make it easy to work with Python projects containing lots "
    "of packages, of which you only want to develop some.",
    formatter_class=argparse.RawDescriptionHelpFormatter,
)
parser.add_argument(
    "-c",
    "--configuration",
    help="configuration file in INI format",
    nargs="?",
    type=argparse.FileType("r"),
    required=True,
)


class Configuration:
    def __init__(self, tio: typing.TextIO) -> None:
        ini = configparser.ConfigParser(
            default_section="settings",
            interpolation=configparser.ExtendedInterpolation(),
        )
        ini.read_file(tio)
        self.infile: str = ini["settings"].get("requirements-in", "requirements.txt")
        self.out_requirements: str = ini["settings"].get(
            "requirements-out", "requirements-dev.txt"
        )
        self.out_constraints: str = ini["settings"].get(
            "constraints-out", "constraints-dev.txt"
        )
        self.packages = {}
        for name in ini.sections():
            url = ini[name].get("url")
            if not url:
                raise ValueError(f"Section {name} has no URL set!")
            self.packages[name] = {
                "url": url,
                "branch": ini[name].get("branch", "main"),
                "extras": ini[name].get("extras", ""),
            }

    @property
    def keys(self) -> typing.List[str]:
        return [k.lower() for k in self.packages]


def process_line(
    line: str, package_keys: typing.List[str], variety: str
) -> typing.Tuple[typing.List[str], typing.List[str]]:
    if isinstance(line, bytes):
        line = line.decode("utf8")
    if line.startswith("-c"):
        return read(line.split(" ")[1].strip(), package_keys=package_keys, variety="c")
    elif line.startswith("-r"):
        return read(line.split(" ")[1].strip(), package_keys=package_keys, variety="r")
    try:
        parsed = pkg_resources.Requirement.parse(line)
    except Exception:
        pass
    else:
        if parsed.key in package_keys:
            line = f"# mxdev disabled: {line}"
    if variety == "c":
        return [], [line]
    return [line], []


def read(
    file_or_url: str,
    package_keys: typing.List[str],
    variety: str = "r",
) -> typing.Tuple[typing.List[str], typing.List[str]]:
    requirements: typing.List[str] = []
    constraints: typing.List[str] = []
    logger.info(f"Read {file_or_url}")
    parsed = parse.urlparse(file_or_url)
    if not parsed.scheme:
        opener = open, (file_or_url, "r")
    else:
        opener = request.urlopen, (file_or_url,)
    with opener[0](*opener[1]) as fio:
        for line in fio:
            new_requirements, new_constraints = process_line(
                line, package_keys, variety
            )
            requirements += new_requirements
            constraints += new_constraints
    if requirements and variety == "r":
        requirements = (
            [
                "#" * 79 + "\n",
                f"# begin requirements from: {file_or_url}\n\n",
            ]
            + requirements
            + ["", f"# end requirements from: {file_or_url}\n", "#" * 79 + "\n"]
        )
    if constraints and variety == "c":
        constraints = (
            [
                "#" * 79 + "\n",
                f"# begin constraints from: {file_or_url}\n",
                "\n",
            ]
            + constraints
            + ["\n", f"# end constraints from: {file_or_url}\n", "#" * 79 + "\n\n"]
        )
    return (requirements, constraints)


def write(
    requirements: typing.List[str],
    requirements_filename: str,
    constraints: typing.List[str],
    constraints_filename: str,
    packages,
):
    with open(requirements_filename, "w") as fio:
        fio.write("#" * 79 + "\n")
        fio.write("# mxdev combined constraints\n")
        fio.write(f"-c {constraints_filename}\n\n")
        fio.writelines(requirements)
        fio.write("\n"+ "#" * 79 + "\n")
        fio.write("# mxdev development sources:\n\n")
        for name in packages:
            package = packages[name]
            fio.write(f"-e {package['url']}@{package['branch']}#egg={name}\n")
        fio.write("\n")

    with open(constraints_filename, "w") as fio:
        fio.writelines(constraints)


def main() -> None:
    args = parser.parse_args()
    cfg = Configuration(args.configuration)
    requirements, constraints = read(cfg.infile, cfg.keys)
    write(
        requirements,
        cfg.out_requirements,
        constraints,
        cfg.out_constraints,
        cfg.packages,
    )


if __name__ == "__main__":  # pragma: no cover
    main()
