import io
import csv
import json
import math
import time
import string
import argparse
import random, secrets
from . import __version__
from .update import check_for_update
from colorama import Fore, init; init(autoreset=True);
import xml.etree.ElementTree as ET

try:
    import yaml
except ImportError:
    yaml = None

def positive_int(value):
    value = int(value)
    if value <= 0:
        raise argparse.ArgumentTypeError("must be greater than 0")
    return value

CHARSETS = {
    # Basic
    "digits": string.digits,
    "letters": string.ascii_letters,
    "lower": string.ascii_lowercase,
    "upper": string.ascii_uppercase,
    "special": string.punctuation,

    # Numeric
    "bin": "01",
    "oct": "01234567",
    "hex": "0123456789ABCDEF",
    "lhex": "0123456789abcdef",
    "allhex": "0123456789ABCDEFabcdef",

    # URL / filename friendly
    "url": string.ascii_letters + string.digits + "-._~",
    "urlsafe": string.ascii_letters + string.digits + "-_",
    "filename": string.ascii_letters + string.digits + "-_.",

    # Human-friendly
    "lowerx": "abcdefghijkmnopqrstuvwxyz",  # lower without "l" which can be misread as I/1
    "upperx": "ABCDEFGHJKLMNPQRSTUVWXYZ",   # upper without "I", "O" which can be misread as l/1, 0
    "digitssafe": "23456789",              # digits without "0", "1" which can be misread as O, I/l

    # Base encodings
    "base32": "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567",
    "lbase32": "abcdefghijklmnopqrstuvwxyz234567",
    "base36": "0123456789abcdefghijklmnopqrstuvwxyz",
    "ubase36": "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "base62": string.digits + string.ascii_letters,

    # Base64 alphabets
    "base64": string.ascii_letters + string.digits + "+/",
    "base64url": string.ascii_letters + string.digits + "-_",

    # Common symbols
    "symbols": string.punctuation,
    "brackets": "()[]{}<>",
    "quotes": "\"'`",
    "math": "+-=*/%<>^~|&",
}

class Zora:
    def __init__(self):
        self.lines = []

    def run(self):
        self.start_timer()
        self.parse_args()
        self.validate_args()
        self.build_charset()
        if self.args.benchmark:
            self.calculate_benchmark()
        self.validate_charset()
        self.generate_keys()
        self.output()
        self.show_timer()
        self.show_entropy()
        if not self.args.quiet:
            self.check_update()

    def check_update(self):
        latest = check_for_update()

        if latest:
            print(
                f"\n{Fore.WHITE}"
                f"A new version of zora-cli is available: "
                f"{Fore.RED}{__version__} {Fore.WHITE}→ {Fore.GREEN}{latest}"
            )
            print(
                f"{Fore.WHITE}"
                f"Run: {Fore.LIGHTYELLOW_EX}pip install --upgrade zora-cli\n"
            )

    def build_charset(self):
        value = self.args.charset
        charset = ""

        while value:
            if value.startswith("@"):
                value = value[1:]

                matches = [
                    name for name in CHARSETS
                    if value.startswith(name)
                ]

                if not matches:
                    self.parser.error(f"unknown charset preset near: @{value}")

                name = max(matches, key=len)
                charset += CHARSETS[name]
                value = value[len(name):]

            else:
                charset += value[0]
                value = value[1:]

        self.charset = "".join(dict.fromkeys(charset))

    def validate_charset(self):
        """Make sure the final charset is usable."""
        if not self.charset:
            self.parser.error("charset cannot be empty")

        if len(self.charset) < 2:
            self.parser.error("charset must contain at least 2 unique characters")

    def parse_args(self):
        """
        Parses all the arguments
        """
        self.parser = argparse.ArgumentParser(
            description="Cryptographically secure generator of random keys with tons of options and customizations."
        )

        sc = self.parser.add_argument

        #
        # ARGUMENTS
        #
        sc("--charset-list", action="store_true", help="Shows available charset lists")
        sc("--version", action="version", version=f"%(prog)s {__version__}")
        sc("--benchmark", action="store_true", help="Benchmark key generation")

        sc("length", type=positive_int, help="Length of the key", nargs="?")
        sc("--seed", type=str, help="Seed for generation")
        sc("--prefix", type=str, default="", help="Prefix the generated keys")
        sc("--suffix", type=str, default="", help="Suffix the generated keys")
        sc("--group", type=positive_int, help="Add separator each X chars (use --sep [str] to set separator)")
        sc("--sep", type=str, default="-", help="Grouping separator string")
        sc("--format", type=str, default="text", choices=["text", "json", "csv", "xml", "yml"], help="Set the output format")

        sc("-n", "--count", type=positive_int, default=1, help="Number of keys to generate")
        sc("-o", "--output", type=str, metavar="FILE", help="Write output to file")

        sc("--unsafe", action="store_true", help="Use PRNG instead of CSPRNG for generation")
        sc("-q", "--quiet", action="store_true", help="Suppress non-essential output")

        sc("-x", "--charset", default="@letters", help="Character set to use (see --charset-list)")

        self.args = self.parser.parse_args()

    def validate_args(self):
        """Validate parsed command-line arguments."""
        if self.args.length is None and not self.args.charset_list:
            self.parser.error("length is required")

        if self.args.seed is not None and not self.args.unsafe:
            self.parser.error("--seed requires --unsafe (seeding is insecure)")

        if self.args.group is not None:
            if self.args.length is not None and self.args.group > self.args.length:
                self.parser.error("--group cannot be greater than length")

        if self.args.charset_list:
            lines = ["\nAvailable charsets to use:"]

            for name, chars in CHARSETS.items():
                lines.append(f"  @{name:<12} = {chars}")

            lines.append(
                "\nUse as:"
                "\n  zora --charset @digits"
                "\n  zora --charset @letters@digits"
                "\n  zora --charset @hexXYZ"
            )

            self.parser.exit(0, "\n".join(lines) + "\n")

        if self.args.unsafe and not self.args.quiet:
            print(f"{Fore.RED}Program will output cryptographically insecure keys.\n")


    def format_key(self, key):
        if self.args.group is not None:
            key = self.args.sep.join(
                key[i:i + self.args.group]
                for i in range(0, len(key), self.args.group)
            )

        return f"{self.args.prefix}{key}{self.args.suffix}"

    def generate_keys(self):
        """
        Generates all the keys
        """
        def gen():
            chooser = random.choice if self.args.unsafe else secrets.choice
            return "".join(
                chooser(self.charset)
                for _ in range(self.args.length)
            )

        if self.args.seed is not None:
            random.seed(self.args.seed)

        for _ in range(self.args.count):
            self.lines.append(self.format_key(gen()))

    def output(self):
        """
        Print or save generated keys in the selected format.
        """

        output_format = self.args.format

        if output_format == "text":
            data = "\n".join(self.lines) + "\n"

        elif output_format == "json":
            data = json.dumps(
                {
                    "keys": self.lines
                },
                indent=2
            ) + "\n"

        elif output_format == "csv":

            buffer = io.StringIO()
            writer = csv.writer(buffer)

            writer.writerow(["key"])

            for key in self.lines:
                writer.writerow([key])

            data = buffer.getvalue()

        elif output_format == "xml":
            root = ET.Element("zora")

            keys = ET.SubElement(root, "keys")

            for key in self.lines:
                element = ET.SubElement(keys, "key")
                element.text = key

            ET.indent(root, space="    ")

            data = ET.tostring(root, encoding="unicode") + "\n"

        elif output_format == "yml":
            if yaml is None:
                self.parser.error(
                    "YAML output requires PyYAML. "
                    "Install it with: pip install pyyaml"
                )

            data = yaml.safe_dump(
                {
                    "keys": self.lines,
                },
                sort_keys=False
            )

        else:
            self.parser.error(f"unsupported output format: {output_format}")

        if self.args.output:
            with open(self.args.output, "w", encoding="utf-8", newline="") as f:
                f.write(data)
        else:
            print(f"{Fore.LIGHTYELLOW_EX}{data}", end="")

    def start_timer(self):
        """
        Starts the timer
        """
        self.time_start = time.perf_counter()


    def show_timer(self, ms_threshold: int = 1000):
        """
        Stops the timer and prints elapsed time
        """
        if self.args.quiet:
            return

        if not hasattr(self, "time_start"):
            print("Timer has not been started properly.")
            return

        elapsed = time.perf_counter() - self.time_start

        total_ms = int(elapsed * 1000)
        total_seconds = total_ms // 1000

        if total_ms < ms_threshold:
            print(f"\n{Fore.GREEN}Timer: {total_ms}ms elapsed")
        else:
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60

            parts = []

            if hours > 0:
                parts.append(f"{hours}h")

            if minutes > 0:
                parts.append(f"{minutes}m")

            if seconds > 0 or not parts:
                parts.append(f"{seconds}s")

            print(f"\n{Fore.GREEN}Timer: {' '.join(parts)} elapsed")

    def show_entropy(self):
        """
        Shows final charset, entropy, strength and used generator."""
        # MARK PRNG's STRIKETHROUGH
        STRIKETHROUGH = "\033[9m" if self.args.unsafe else ""
        if not self.args.quiet:
            entropy = self.entropy()
            print(f"{Fore.LIGHTBLUE_EX}Charset: {len(self.charset)}")
            print(f"{STRIKETHROUGH}{Fore.CYAN}Entropy: {entropy:.2f} bits")
            print(f"{STRIKETHROUGH}{Fore.CYAN}Strength: {self.strength(entropy)}")
            print(f"{Fore.LIGHTCYAN_EX}Generator: {Fore.RED + 'PRNG' if self.args.unsafe else Fore.GREEN + 'CSPRNG'}")

    def entropy(self):
        return self.args.length * math.log2(len(self.charset))

    def strength(self, entropy):
        """
        Finds out the strength according to the entropy
        """
        if entropy < 40:
            return Fore.RED + "Very weak"
        elif entropy < 60:
            return Fore.LIGHTRED_EX + "Weak"
        elif entropy < 80:
            return Fore.YELLOW + "Moderate"
        elif entropy < 100:
            return Fore.LIGHTGREEN_EX + "Strong"
        else:
            return Fore.GREEN + "Very strong"

    def calculate_benchmark(self):
        """
        Benchmark key generation using the current CLI arguments.
        Does not produce normal key output.
        """

        chooser = random.choice if self.args.unsafe else secrets.choice

        # Respect --seed for reproducible PRNG benchmarks.
        if self.args.seed is not None:
            random.seed(self.args.seed)

        start = time.perf_counter()

        for _ in range(self.args.count):
            for _ in range(self.args.length):
                chooser(self.charset)

        elapsed = time.perf_counter() - start

        total_keys = self.args.count
        total_characters = total_keys * self.args.length

        keys_per_second = (
            total_keys / elapsed
            if elapsed > 0
            else 0
        )

        characters_per_second = (
            total_characters / elapsed
            if elapsed > 0
            else 0
        )

        generator = "PRNG" if self.args.unsafe else "CSPRNG"

        print(f"{Fore.LIGHTYELLOW_EX}Zora Benchmark")
        print(f"{Fore.WHITE}{'─' * 32}")
        print(f"{Fore.CYAN}Generator: {generator}")
        print(f"{Fore.CYAN}Length: {self.args.length}")
        print(f"{Fore.CYAN}Count: {self.args.count}")
        print(f"{Fore.CYAN}Charset: {len(self.charset)}")
        print(f"{Fore.CYAN}Characters: {total_characters}")
        print(f"{Fore.CYAN}Time: {elapsed:.6f}s")
        print(f"{Fore.GREEN}Keys/sec: {keys_per_second:,.2f}")
        print(f"{Fore.GREEN}Characters/sec: {characters_per_second:,.2f}")
        self.parser.exit(0)

def main():
    zora = Zora()
    zora.run()


if __name__ == "__main__":
    main()