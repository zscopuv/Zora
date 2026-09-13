# ![Logo](zora.jpg)
> **Early release (`v0.1.2`)**

Zora generates random keys using Python's cryptographically secure
`secrets` module by default. It supports customizable character sets,
charset presets, prefixes, suffixes, grouping, multiple outputs, file
output, entropy estimation, and an optional deterministic PRNG mode.


---

## Features

- 🔐 **Cryptographically secure** generation by default
- ⚠️ Optional insecure **PRNG mode** with `--unsafe`
- 🎲 **Deterministic generation** with `--seed` in unsafe mode
- 🔤 **Custom character sets**
- 🧩 **Composable charset presets** such as `@letters@digits`
- 🔢 **Built-in hexadecimal, octal, binary, digit, and symbol presets**
- ➕ Add **custom characters** to presets
- 📏 Configurable **key length**
- 📦 Generate **multiple keys** at once
- 🔗 Add **prefixes and suffixes**
- 📐 **Group keys with custom separators**
- 💾 Write generated **keys to a file**
- 📊 Calculate **theoretical entropy**
- 💪 **Estimate key strength** from entropy
- ⏱️ Display **generation time**
- 🤫 **Quiet mode** for scripting
- 📋 **Charset preset listing**


# Usage

Basic usage:

```bash
python zora.py LENGTH [OPTIONS]
```

For example:

```bash
python zora.py 32
```

Example output:

```text
GxKqTnJpYwRzLhBcVfQmNsXeUaPkTdWr

Timer: 13ms elapsed
Charset: 52
Entropy: 182.41 bits
Strength: Very strong
Generator: CSPRNG
```

---

# Arguments

## `length`

The length of the random portion of the generated key.

```bash
python zora.py 32
```

The value must be greater than `0`.

---

## `--charset`

Select the character set used to generate keys.

```bash
python zora.py 32 --charset @digits
```

By default:

```text
@letters
```

is used.

Zora supports both predefined charset presets and literal characters.

### Presets

Use `--charset-list` to display all available presets:

```bash
python zora.py --charset-list
```

Currently available presets:

| Preset     | Characters                    |
| ---------- | ----------------------------- |
| `@digits`  | `0-9`                  |
| `@letters` | `a-zA-Z`                      |
| `@lower`   | `a-z`                         |
| `@upper`   | `A-Z`                         |
| `@hex`     | `0-9ABCDEFabcdef`        |
| `@oct`     | `01234567`              |
| `@bin`     | `01`                          |
| `@special` | all punctuation/symbol characters |

---

## Combining presets

Presets can be combined:

```bash
python zora.py 32 --charset @letters@digits
```

This creates an alphanumeric character set.

Multiple presets can be combined:

```bash
python zora.py 32 --charset @upper@lower@digits
```

Duplicate characters are automatically removed.

For example:

```text
@letters@upper
```

does not contain uppercase characters twice.

---

## Custom characters

Literal characters can be included alongside presets.

For example:

```bash
python zora.py 32 --charset @hexXYZ
```

This means:

```text
@hex + X + Y + Z
```

Another example:

```bash
python zora.py 32 --charset XYZ@hex
```

means:

```text
X + Y + Z + @hex
```

This allows arbitrary character sets without needing to add a new preset.

---

# `--charset-list`

Display the available charset presets:

```bash
python zora.py --charset-list
```

Example:

```text
Available charsets:

  @digits
  @letters
  @lower
  @upper
  @hex
  @oct
  @bin
  @special

Use as:

  zora --charset @digits
  zora --charset @letters@digits
  zora --charset @hexXYZ
```

---

# Multiple keys

Use `-n` or `--count`:

```bash
python zora.py 32 --count 10
```

or:

```bash
python zora.py 32 -n 10
```

Zora generates each key independently.

When using the secure default generator, each key is generated using the
cryptographically secure random generator.

---

# Prefixes and suffixes

Add a prefix:

```bash
python zora.py 32 --prefix "AUTH_"
```

Example:

```text
AUTH_GxKqTnJpYwRzLhBcVfQmNsXeUaPkTdWr
```

Add a suffix:

```bash
python zora.py 32 --suffix "_KEY"
```

Both can be used together:

```bash
python zora.py 32 --prefix "AUTH_" --suffix "_KEY"
```

> Prefixes and suffixes are not random and therefore do not contribute to
> the calculated entropy.

---

# Grouping

Use `--group` to insert a separator every N characters.

For example:

```bash
python zora.py 32 --group 4
```

Output:

```text
GxKq-TnJp-YwRz-LhBc-VfQm-NsXe-UaPk-TdWr
```

The default separator is:

```text
-
```

Use `--sep` to change it:

```bash
python zora.py 32 --group 4 --sep ":"
```

Output:

```text
GxKq:TnJp:YwRz:LhBc:VfQm:NsXe:UaPk:TdWr
```

Grouping only changes the presentation of the key. It does not affect
entropy.

---

# File output

Use `-o` or `--output` to write generated keys to a file:

```bash
python zora.py 32 -n 10 --output keys.txt
```

The generated keys are written one per line.

Example:

```text
GxKqTnJpYwRzLhBcVfQmNsXeUaPkTdWr
aQmXzPjLtVrNsYkBcWdHgFqAeUxRoZiLp
...
```

---

# Secure generation

Zora uses Python's `secrets` module by default.

This is the recommended mode when generating authentication tokens,
API keys, secrets, or other security-sensitive random values.

```bash
python zora.py 32
```

The output will report:

```text
Generator: CSPRNG
```

---

# Unsafe / PRNG mode

Use:

```bash
python zora.py 32 --unsafe
```

to use Python's normal pseudo-random number generator instead of the
cryptographically secure generator.

Zora will display a warning:

```text
Program will output cryptographically insecure keys.
```

and:

```text
Generator: PRNG
```

This mode exists primarily for testing, reproducibility, benchmarking,
and experimentation.

**Do not use `--unsafe` for real authentication keys or other
security-sensitive secrets.**

---

# Seeds

Seeds are only allowed with `--unsafe`.

This is intentional.

The following will fail:

```bash
python zora.py 32 --seed example
```

because Zora's secure generator should not be made deterministic through
the normal CLI.

Instead:

```bash
python zora.py 32 --unsafe --seed example
```

A seed can be useful for testing reproducibility.

For example:

```bash
python zora.py 32 --unsafe --seed test
```

will produce the same deterministic sequence when run with the same
configuration.

When generating multiple keys, the PRNG is seeded once before generation
rather than being reseeded for every key.

---

# Quiet mode

Use `-q` or `--quiet` to suppress non-essential output:

```bash
python zora.py 32 --quiet
```

This is useful when using Zora inside scripts or shell pipelines.

For example:

```bash
python zora.py 32 --quiet > key.txt
```

---

# Entropy

Zora calculates the theoretical entropy of the random portion of the
key.

The formula is:

$entropy = length \times \log{_2}{(charset size)}$

For example, using 52 possible characters:

$32 \times log{_2}\space 52$

produces approximately:

```text
182.17 bits
```

The entropy calculation only considers random characters.

Known prefixes, suffixes, and grouping separators do not increase the
entropy.

For example:

```bash
python zora.py 32 --prefix "AUTH_"
```

has the same theoretical entropy as:

```bash
python zora.py 32
```

assuming the same charset and length.

---

# Strength

Zora provides a simple entropy-based strength classification.

|      Entropy | Classification |
| -----------: | -------------- |
|  `< 40` bits | Very weak      |
| `40–59` bits | Weak           |
| `60–79` bits | Moderate       |
| `80–99` bits | Strong         |
|  `100+` bits | Very strong    |

This is a simple classification rather than a formal security guarantee.

A high theoretical entropy value does not make an insecure PRNG
cryptographically secure.

For this reason, Zora explicitly identifies the generator as either:

```text
CSPRNG
```

or:

```text
PRNG
```

---

# Example commands

### Basic key

```bash
python zora.py 32
```

### Digits only

```bash
python zora.py 32 --charset @digits
```

### Lowercase only

```bash
python zora.py 32 --charset @lower
```

### Uppercase only

```bash
python zora.py 32 --charset @upper
```

### Alphanumeric

```bash
python zora.py 32 --charset @letters@digits
```

### Hexadecimal

```bash
python zora.py 32 --charset @hex
```

### Hexadecimal plus custom characters

```bash
python zora.py 32 --charset @hexXYZ
```

### Uppercase, lowercase and digits

```bash
python zora.py 32 --charset @upper@lower@digits
```

### Symbols

```bash
python zora.py 32 --charset @special
```

### Group the output

```bash
python zora.py 32 --group 4
```

### Custom separator

```bash
python zora.py 32 --group 4 --sep ":"
```

### Generate multiple keys

```bash
python zora.py 32 -n 10
```

### Save to a file

```bash
python zora.py 32 -n 100 -o keys.txt
```

### Prefix

```bash
python zora.py 32 --prefix "AUTH_"
```

### Secure generation

```bash
python zora.py 32
```

### Reproducible testing

```bash
python zora.py 32 --unsafe --seed test
```

### Quiet output

```bash
python zora.py 32 --quiet
```

---

# Security

Zora is designed to make secure random generation the default.

The default generator uses Python's `secrets` module rather than
Python's standard `random` module.

The `--unsafe` option deliberately switches to a normal pseudo-random
number generator.

This distinction is important:

```text
Default
    ↓
secrets
    ↓
CSPRNG
    ↓
Suitable for security-sensitive random values
```

versus:

```text
--unsafe
    ↓
random
    ↓
PRNG
    ↓
Not suitable for security-sensitive values
```

Do not use `--unsafe` generated values for:

* Authentication credentials
* Password reset tokens
* Session tokens
* API secrets
* Encryption keys
* Other security-sensitive secrets

unless you specifically understand the security implications.

---

# Important entropy note

The entropy reported by Zora describes the size of the theoretical
random output space.

For example, a 32-character key selected uniformly from 62 possible
characters has:

$32 \times log{_2}\space 62$

bits of theoretical entropy.

However, entropy alone does not prove that a generator is secure.

For example:

```bash
python zora.py 32 --unsafe
```

can still report a high entropy value because the theoretical output
space is large.

The generator is nevertheless explicitly marked:

```text
Generator: PRNG
```

and the entropy/strength display is visually marked when `--unsafe` is
used.

---

# Development

Clone the repository:

```bash
git clone https://github.com/zscopuv/Zora.git
cd Zora
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
python zora.py 32
```

---

# Project structure

A minimal installation currently looks like:

```text
Zora/
├── zora.py
├── zora.jpg
├── LICENSE
├── README.md
└── requirements.txt
```

Future versions may introduce a package structure and automated tests.

---

# Roadmap

Possible future improvements include:

* [ ] Automated test suite
* [ ] More charset presets
* [ ] Better charset parsing errors
* [ ] Configuration files
* [ ] Packaging with `pyproject.toml`
* [ ] Installation through `pip`
* [ ] Shell completion
* [ ] More output formats
* [ ] Benchmarking mode
* [ ] Improved documentation
* [ ] Cross-platform terminal improvements
* [ ] API/library usage
* [ ] More extensive security testing

The roadmap is subject to change.

---

# Versioning

Zora currently follows semantic versioning:

```text
MAJOR.MINOR.PATCH
```

For example:

```text
v0.1.0
```

The `0.x` versions indicate that the CLI and features may still change
before the first stable `1.0.0` release.

---

# Contributing

Contributions, bug reports, feature requests, and suggestions are
welcome.

Before submitting a change:

1. Make sure the program still runs.
2. Test the affected CLI options.
3. Avoid breaking existing behavior unless the change is intentional.
4. Update the documentation when adding or changing an option.

---

# License

This project is licensed under the MIT License.

See [`LICENSE`](LICENSE) for the full license text.

---

# Disclaimer

Zora is provided as-is.

While Zora uses a cryptographically secure random generator by default,
the security of a system depends on how generated values are stored,
transmitted, and used.

Always evaluate the complete security design of the application in which
a generated key or token is used.