# ![Logo](https://i.ibb.co/21JfnbBZ/zora.jpg)

> **Early release (`v0.2`)**

Zora is a command-line tool for generating random keys using Python's
cryptographically secure `secrets` module by default.

It supports customizable character sets, composable charset presets,
prefixes, suffixes, grouping, multiple output formats, file output,
entropy estimation, benchmarking, and an optional deterministic PRNG mode.

---

## Features

- 🔐 **Cryptographically secure** generation by default
- ⚠️ Optional insecure **PRNG mode** with `--unsafe`
- 🎲 **Deterministic generation** with `--seed` in unsafe mode
- 🔤 **Custom character sets**
- 🧩 **Composable charset presets** such as `@letters@digits`
- ⚡ **Fast charset shorthand** with `-x`
- 🔢 **28 built-in charset presets**
- ➕ Add **custom characters** to presets
- 📏 Configurable **key length**
- 📦 Generate **multiple keys** at once
- 🔗 Add **prefixes and suffixes**
- 📐 **Group keys with custom separators**
- 💾 Write generated **keys to a file**
- 📤 Multiple output formats: **Text, JSON, CSV, XML, YAML**
- 📊 Calculate **theoretical entropy**
- 💪 **Estimate key strength** from entropy
- ⏱️ Display **generation time**
- 🏁 **Benchmark key generation**
- 🤫 **Quiet mode** for scripting
- 📋 **Charset preset listing**
- 🔍 **Charset and argument validation**
- ℹ️ Display the installed version with `--version`

---

# Installation

## Requirements

Python 3.9 or newer is recommended.

Install Zora from PyPI:

```bash
pip install zora-cli
````

Run Zora:

```bash
zora 32
```

### Optional YAML support

YAML output requires PyYAML:

```bash
pip install pyyaml
```

---

# Usage

Basic usage:

```bash
zora LENGTH [OPTIONS]
```

For example:

```bash
zora 32
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
zora 32
```

The value must be greater than `0`.

---

## `--version`

Display the currently installed Zora version:

```bash
zora --version
```

Example:

```text
zora 0.2.0
```

---

## `--charset` / `-x`

Select the character set used to generate keys.

The default charset is:

```text
@letters
```

Long form:

```bash
zora 32 --charset @digits
```

Short form:

```bash
zora 32 -x @digits
```

The `-x` option is provided as a convenient shorthand for faster charset selection.

Zora supports both predefined charset presets and literal characters.

---

## Charset presets

Use:

```bash
zora --charset-list
```

to display all available presets.

## Basic

| Preset     | Characters              |
| ---------- | ----------------------- |
| `@digits`  | `0-9`                   |
| `@letters` | `a-zA-Z`                |
| `@lower`   | `a-z`                   |
| `@upper`   | `A-Z`                   |
| `@special` | Punctuation and symbols |

## Numeric

| Preset    | Characters               |
| --------- | ------------------------ |
| `@bin`    | `01`                     |
| `@oct`    | `01234567`               |
| `@hex`    | `0123456789ABCDEF`       |
| `@lhex`   | `0123456789abcdef`       |
| `@allhex` | `0123456789ABCDEFabcdef` |

## URL / filename friendly

| Preset      | Characters                       |
| ----------- | -------------------------------- |
| `@url`      | URL-friendly characters          |
| `@urlsafe`  | URL-safe alphanumeric characters |
| `@filename` | Filename-safe characters         |

## Human-friendly

These presets avoid characters that can easily be confused with one another.

| Preset        | Description                   |
| ------------- | ----------------------------- |
| `@lowersafe`     | Lowercase without `l`         |
| `@uppersafe`     | Uppercase without `I` and `O` |
| `@digitssafe` | Digits without `0` and `1`    |

## Base encodings

| Preset     | Description               |
| ---------- | ------------------------- |
| `@base32`  | Uppercase Base32 alphabet |
| `@base32x` | Lowercase Base32 alphabet |
| `@base36` | Uppercase Base36 alphabet |
| `@base36x`  | Lowercase Base36 alphabet |
| `@base62`  | Base62 alphabet           |

## Base64

| Preset       | Description              |
| ------------ | ------------------------ |
| `@base64`    | Standard Base64 alphabet |
| `@base64url` | URL-safe Base64 alphabet |

## Symbols

| Preset      | Characters                  |
| ----------- | --------------------------- |
| `@symbols`  | Punctuation and symbols     |
| `@brackets` | `()[]{}<>`                  |
| `@quotes`   | Quote characters            |
| `@math`     | Common mathematical symbols |

---

## Combining presets

Presets can be combined:

```bash
zora 32 --charset @letters@digits
```

This creates an alphanumeric character set.

Multiple presets can also be combined:

```bash
zora 32 --charset @upper@lower@digits
```

Duplicate characters are automatically removed.

For example:

```text
@letters@upper
```

does not contain uppercase characters twice.

The short `-x` form can be used as well:

```bash
zora 32 -x @upper@lower@digits
```

---

## Custom characters

Literal characters can be included alongside presets.

For example:

```bash
zora 32 --charset @hexXYZ
```

This means:

```text
@hex + X + Y + Z
```

Another example:

```bash
zora 32 --charset XYZ@hex
```

means:

```text
X + Y + Z + @hex
```

This allows arbitrary character sets without requiring a new preset.

---

## `--charset-list`

Display all available charset presets:

```bash
zora --charset-list
```

The output includes the preset name and its characters.

Example:

```text
Available charsets:
  @digits       = 0123456789
  @letters      = abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
  @lower        = abcdefghijklmnopqrstuvwxyz
  @upper        = ABCDEFGHIJKLMNOPQRSTUVWXYZ
  ...

Use as:
  zora --charset @digits
  zora --charset @letters@digits
  zora --charset @hexXYZ
```

This mode exits immediately after displaying the available presets.

---

# Multiple keys

Use `-n` or `--count` to generate multiple keys:

```bash
zora 32 --count 10
```

or:

```bash
zora 32 -n 10
```

Each key is generated independently.

When using the secure default generator, each key is generated using the
cryptographically secure random generator.

---

# Prefixes and suffixes

Add a prefix:

```bash
zora 32 --prefix "AUTH_"
```

Example:

```text
AUTH_GxKqTnJpYwRzLhBcVfQmNsXeUaPkTdWr
```

Add a suffix:

```bash
zora 32 --suffix "_KEY"
```

Both can be used together:

```bash
zora 32 --prefix "AUTH_" --suffix "_KEY"
```

> Prefixes and suffixes are not random and therefore do not contribute to
> the calculated entropy.

---

# Grouping

Use `--group` to insert a separator every N characters.

For example:

```bash
zora 32 --group 4
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
zora 32 --group 4 --sep ":"
```

Output:

```text
GxKq:TnJp:YwRz:LhBc:VfQm:NsXe:UaPk:TdWr
```

Grouping only changes the presentation of the key. It does not affect
entropy.

---

# Output formats

Zora supports multiple output formats through `--format`.

Available formats:

* `text`
* `json`
* `csv`
* `xml`
* `yml`

The default format is `text`.

## Text

```bash
zora 32 --format text
```

This is the default output format.

## JSON

```bash
zora 32 -n 3 --format json
```

Example:

```json
{
  "keys": [
    "GxKqTnJpYwRzLhBcVfQmNsXeUaPkTdWr",
    "...",
    "..."
  ]
}
```

## CSV

```bash
zora 32 -n 3 --format csv
```

The generated CSV contains a `key` column.

## XML

```bash
zora 32 -n 3 --format xml
```

## YAML

```bash
zora 32 -n 3 --format yml
```

YAML output requires PyYAML:

```bash
pip install pyyaml
```

---

# File output

Use `-o` or `--output` to write generated output to a file:

```bash
zora 32 -n 10 --output keys.txt
```

The output format can be selected independently:

```bash
zora 32 -n 10 --format json -o keys.json
```

```bash
zora 32 -n 10 --format csv -o keys.csv
```

Generated files use UTF-8 encoding.

Text-based CLI output uses a conventional final newline.

---

# Secure generation

Zora uses Python's `secrets` module by default.

This is the recommended mode when generating authentication tokens,
API keys, secrets, or other security-sensitive random values.

```bash
zora 32
```

The output will report:

```text
Generator: CSPRNG
```

---

# Unsafe / PRNG mode

Use:

```bash
zora 32 --unsafe
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
zora 32 --seed example
```

because Zora's secure generator should not be made deterministic through
the normal CLI.

Instead:

```bash
zora 32 --unsafe --seed example
```

A seed can be useful for testing reproducibility.

For example:

```bash
zora 32 --unsafe --seed test
```

will produce the same deterministic sequence when run with the same
configuration.

When generating multiple keys, the PRNG is seeded once before generation
rather than being reseeded for every key.

---

# Benchmarking

Use `--benchmark` to benchmark key generation:

```bash
zora 32 --benchmark
```

The benchmark reports:

* Generator
* Key length
* Number of keys
* Charset size
* Total characters generated
* Keys per second
* Characters per second

Example:

```text
Zora Benchmark
────────────────────────────────
Generator: CSPRNG
Length: 32
Count: 1
Charset: 52
Characters: 32
Keys/sec: ...
Characters/sec: ...
```

Benchmarking does not produce normal key output.

The benchmark respects `--unsafe`, `--seed`, `--count`, and the selected
charset.

---

# Quiet mode

Use `-q` or `--quiet` to suppress non-essential output:

```bash
zora 32 --quiet
```

This is useful when using Zora inside scripts or shell pipelines.

For example:

```bash
zora 32 --quiet > key.txt
```

Quiet mode suppresses the timer, entropy, strength, generator information,
and update notification.

---

# Entropy

Zora calculates the theoretical entropy of the random portion of the key.

The formula is:

```text
entropy = length × log₂(charset size)
```

For example, using 52 possible characters:

```text
32 × log₂(52)
```

produces approximately:

```text
182.41 bits
```

The entropy calculation only considers random characters.

Known prefixes, suffixes, and grouping separators do not increase the
entropy.

For example:

```bash
zora 32 --prefix "AUTH_"
```

has the same theoretical entropy as:

```bash
zora 32
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

# Argument validation

Zora validates command-line arguments before generating keys.

Examples of invalid arguments include:

* A key length of `0` or less
* A key length missing when generation is requested
* A `--group` value greater than the key length
* Using `--seed` without `--unsafe`
* An unknown charset preset
* An empty final charset
* A charset containing fewer than two unique characters

Invalid arguments result in a clear command-line error instead of
attempting to generate invalid output.

---

# Example commands

### Basic key

```bash
zora 32
```

### Digits only

```bash
zora 32 -x @digits
```

### Lowercase only

```bash
zora 32 -x @lower
```

### Uppercase only

```bash
zora 32 -x @upper
```

### Alphanumeric

```bash
zora 32 -x @letters@digits
```

### Hexadecimal

```bash
zora 32 -x @hex
```

### Hexadecimal plus custom characters

```bash
zora 32 -x @hexXYZ
```

### Uppercase, lowercase and digits

```bash
zora 32 -x @upper@lower@digits
```

### Human-friendly digits

```bash
zora 32 -x @digitssafe
```

### Symbols

```bash
zora 32 -x @symbols
```

### Group the output

```bash
zora 32 --group 4
```

### Custom separator

```bash
zora 32 --group 4 --sep ":"
```

### Generate multiple keys

```bash
zora 32 -n 10
```

### Save to a file

```bash
zora 32 -n 100 -o keys.txt
```

### JSON output

```bash
zora 32 -n 10 --format json
```

### Benchmark

```bash
zora 32 --benchmark
```

### Show available charsets

```bash
zora --charset-list
```

### Show version

```bash
zora --version
```

### Prefix

```bash
zora 32 --prefix "AUTH_"
```

### Secure generation

```bash
zora 32
```

### Reproducible testing

```bash
zora 32 --unsafe --seed test
```

### Quiet output

```bash
zora 32 --quiet
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

```text
32 × log₂(62)
```

bits of theoretical entropy.

However, entropy alone does not prove that a generator is secure.

For example:

```bash
zora 32 --unsafe
```

can still report a high entropy value because the theoretical output
space is large.

The generator is nevertheless explicitly marked:

```text
Generator: PRNG
```

and the entropy and strength display is visually marked when `--unsafe`
is used.

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
zora 32
```

For YAML output, install PyYAML:

```bash
pip install pyyaml
```

---

# Roadmap

Possible future improvements include:

* [x] More charset presets
* [x] Improved documentation
* [x] Installation through `pip`
* [x] Packaging with `pyproject.toml`
* [x] Better charset parsing errors
* [x] Multiple output formats
* [x] Benchmarking mode
* [x] Version information
* [x] Argument validation
* [x] Automated test suite
* [ ] Configuration files
* [ ] Shell completion
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
v0.2.0
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