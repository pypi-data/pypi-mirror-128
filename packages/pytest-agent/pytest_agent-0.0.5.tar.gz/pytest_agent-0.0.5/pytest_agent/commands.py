"""
This module defines functions used to run commands and retrieve their output
"""
import re
import select
import html
import subprocess
from typing import Tuple

STYLE_PATTERN = re.compile(r"\x1b\[\d+m")


class StyleContext:  # pylint: disable=too-few-public-methods
    """
    Keep track of context to be able to properly close tags depending on current styling.
    """

    mapping = {
        "\x1b[31m": ("color", "red"),
        "\x1b[32m": ("color", "green"),
        "\x1b[33m": ("color", "orange"),
        "\x1b[36m": ("color", "blue"),
        "\x1b[1m": ("tag", "strong"),
        "\x1b[0m": ("clear", None),
    }

    def __init__(self):
        self.styles = []

    def get(self, match: re.Match):
        """
        Get replacement for an ascii styling character depending on previous context.
        """
        try:
            style = self.mapping[match.group(0)]
        except KeyError:
            return ""

        kind, value = style
        if kind == "color":
            self.styles.append(style)
            output = f'<span color="{value}">'
        elif kind == "tag":
            self.styles.append(style)
            output = f"<{value}>"
        elif kind == "clear":
            output = ""
            for _ in range(len(self.styles)):
                rkind, rvalue = self.styles.pop(-1)
                if rkind == "color":
                    output += "</span>"
                elif rkind == "tag":
                    output += f"</{rvalue}>"
            return output

        return output


def execute_command(command: str, capture_stderr=False) -> Tuple[str, int]:
    """
    Execute command, then return its output and returncode
    """
    # wrap command execution with "script" command to mock a real terminal and retrieve styling
    with subprocess.Popen(
        ["script", "-e", "-q", "-c", command],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE if capture_stderr else None,
    ) as process:
        # simultaneously read stdin and stdout to get both in same output variable
        output = b""

        while True:
            reads = [process.stdout.fileno()]
            if capture_stderr:
                reads.append(process.stderr.fileno())

            ret = select.select(reads, [], [])

            for file in ret[0]:
                if file == process.stdout.fileno():
                    output += process.stdout.readline()
                if capture_stderr and file == process.stderr.fileno():
                    output += process.stderr.readline()

            if process.poll() is not None:
                break

        status_code = process.returncode

    # convert bytes to str
    output = output.decode("utf-8")

    # escape unsafe html characters from output
    output = html.escape(output)

    # replace terminal style with html style
    context = StyleContext()
    output = re.sub(STYLE_PATTERN, context.get, output)

    return output, status_code
