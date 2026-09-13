import math
import time
import string
import argparse
import random, secrets
from colorama import Fore, init; init(autoreset=True);

def positive_int(value):
    value = int(value)
    if value <= 0:
        raise argparse.ArgumentTypeError("must be greater than 0")
    return value

CHARSETS = {
    "digits": string.digits,
    "letters": string.ascii_letters,
    "lower": string.ascii_lowercase,
    "upper": string.ascii_uppercase,
    "hex": string.hexdigits,
    "oct": string.octdigits,
    "bin": "01",
    "special": string.punctuation,
}

class Zora:
    def __init__(self):
        self.lines = []

    def run(self):
        self.start_timer()
        self.parse_args()
        self.build_charset()
        self.generate_keys()
        self.output()
        self.show_timer()
        self.show_entropy()


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

    def parse_args(self):
        """
        Parses all the arguments
        """
        self.parser = argparse.ArgumentParser(
            description="Generate random AUTH keys."
        )

        sc = self.parser.add_argument

        #
        # ARGUMENTS
        #
        sc("--charset-list", action="store_true", help="Shows available charset lists")

        sc("length", type=positive_int, help="Length of the key", nargs="?")
        sc("--seed", type=str, help="Seed for generation")
        sc("--prefix", type=str, default="", help="Prefix the generated keys")
        sc("--suffix", type=str, default="", help="Suffix the generated keys")
        sc("--group", type=positive_int, help="Add separator each X chars (use --sep [str] to set separator)")
        sc("--sep", type=str, default="-", help="Grouping separator string")

        sc("-n", "--count", type=positive_int, default=1, help="Number of keys to generate")
        sc("-o", "--output", type=str, metavar="FILE", help="Write output to file")

        sc("--unsafe", action="store_true", help="Use PRNG instead of CSPRNG for generation")
        sc("-q", "--quiet", action="store_true", help="Suppress non-essential output")


        sc("--charset", default="@letters", help="Character set to use (see --charset-list)")

        self.args = self.parser.parse_args()

        if self.args.length is None and not self.args.charset_list:
            self.parser.error("length is required")

        # RANDOM MODULE DISALLOWED + SEED SET
        if self.args.seed is not None and not self.args.unsafe:
            self.parser.error("--seed requires --unsafe (seeding is insecure)")

        if self.args.charset_list:
            self.parser.exit(0, ("\nAvailable charsets to use:\n  @"+("\n  @".join(CHARSETS.keys())) + f"\n\n Use as:\n  zora --charset @digits            = For digits only charset\n  zora --charset @letters@digits    = For alphanumeric charset\n  zora --charset @hex\"XYZ\"          = For hexadecimal charset extended with letters X, Y and Z\n"))

        if self.args.unsafe and not self.args.quiet:
            print(f"{Fore.RED}Program will output cryptographically insecure keys.\n")

    def generate_keys(self):
        """
        Generates all the keys
        """
        def gen():
            if self.args.unsafe:
                return "".join(random.choice(self.charset) for _ in range(self.args.length))
            else:
                return "".join(secrets.choice(self.charset) for _ in range(self.args.length))

        if self.args.seed is not None:
            random.seed(self.args.seed)
                 
        for _ in range(self.args.count):
            key = gen()
            if self.args.group is not None:
                key = self.args.sep.join(
                    key[i:i + self.args.group]
                    for i in range(0, len(key), self.args.group)
                )
            self.lines.append(
                f"{self.args.prefix}{key}{self.args.suffix}"
            )

    def output(self):
        """
        Prints out / Saves the keys (lines)
        """
        if self.args.output:
            with open(self.args.output, "w") as f:
                f.write("\n".join(self.lines))

        else:
            print("\n".join(_ for _ in self.lines))

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


def main():
    zora = Zora()
    zora.run()


if __name__ == "__main__":
    main()