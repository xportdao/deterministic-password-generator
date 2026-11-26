# KEY. — Deterministic Password Generator

A small, open-source tool that derives a service-specific password from a master phrase and a service domain. The same inputs reproduce the same password without a password database.

> **Security status: v1 / experimental.** This project has not undergone an independent security audit. Review the risks below before using it with real accounts. For high-value accounts, prefer a well-established password manager and passkeys or multifactor authentication.

## Usage

### Python

Requires Python 3 with scrypt support in the standard library.

```sh
python3 generate.py
```

Enter a master phrase at `Secret phrase:` and a domain such as `example.com` at `Service:`. The phrase is hidden while typing; the generated password is printed to the terminal.

### Browser

Open `index.html` in a compatible browser using a trusted local copy or a trusted HTTPS origin. Enter your master phrase and service domain, then select **Generate password**.

The browser implementation uses a temporary Web Worker and Web Crypto. It does not intentionally store credentials or make network requests during generation. The displayed password is cleared after 60 seconds; system clipboard contents may remain.

Use exactly the same master phrase and normalized service identifier every time. Enter a bare domain, without a protocol, path or trailing slash. The browser accepts ASCII domains (use Punycode for internationalized domains). Spaces and case in the master phrase are significant.

## Algorithm specification — v1

| Parameter | Value |
| --- | --- |
| KDF | scrypt |
| Secret input | Master phrase encoded as UTF-8 |
| Salt | Trimmed, lowercased service identifier encoded as UTF-8 |
| N | 131072 (2^17) |
| r | 8 |
| p | 1 |
| Derived key length | 15 bytes (120 bits) |
| Output | URL-safe Base64 of the derived key, followed by the literal suffix `aA1!` |
| Password length | 24 characters |
| Approximate scrypt memory requirement | 128 MiB, excluding implementation overhead |

The Python and browser implementations are intended to reproduce the same output for supported identical inputs. The browser applies stricter domain validation than the Python script.

## Known risks and limitations of v1

| Risk | Impact |
| --- | --- |
| Master phrase compromise | Anyone who obtains the master phrase can regenerate passwords for known or guessed service identifiers. There is no independent per-account secret to limit the impact. |
| Offline guessing | A leaked generated password and its service identifier allow an attacker to test candidate master phrases offline. Scrypt raises the cost of guessing but does not protect a weak or reused phrase. The domain salt is public and predictable. |
| No per-service password rotation | There is no version counter or rotation mechanism. With identical inputs the password never changes, even after a service breach. |
| No account separation | Multiple accounts using the same master phrase and service identifier receive the same password. v1 has no dedicated account identifier. |
| Fixed password format | The fixed suffix adds no entropy. The 120-bit derived key sets an upper bound on derived-output entropy, and actual resistance to guessing can be much lower depending on the master phrase. Some websites may reject the fixed length or character set. |
| Input and recovery errors | Different subdomains, spelling, Unicode representations or master-phrase whitespace can produce different passwords. The tool does not retain account metadata or offer password recovery. Losing the exact inputs can make accounts inaccessible. |
| Unreviewed browser cryptography | The browser contains a custom JavaScript scrypt implementation. It has not been independently audited; implementation defects and cross-browser compatibility issues remain possible. |
| Web delivery and device trust | A modified HTML file, compromised hosting origin, malicious extension, keyboard software or infected device may capture secrets. CSP and local computation do not establish the integrity of delivered code or protect against a compromised device. |
| Residual secrets | Clearing inputs, terminating the worker and overwriting some buffers are best-effort measures, not guaranteed memory erasure. Passwords may persist in the clipboard, terminal scrollback or other system components. |
| Resource constraints | Scrypt requires significant memory and CPU time. Generation may be slow or fail on low-memory devices and mobile browsers. |
| Testing and audit coverage | There is currently no automated regression suite in the repository and no independent security audit. Browser and mobile compatibility should not be assumed. |

## Safer use

- Use a high-entropy, unique master phrase, preferably made from randomly selected words. Never reuse a password from another account as the master phrase.
- Keep a secure offline recovery copy of the master phrase and any service identifiers needed to reproduce your passwords.
- Use a trusted, verified copy of the application on a trusted device. Avoid entering the master phrase into unfamiliar hosted copies.
- Enable passkeys or multifactor authentication wherever available.
- If a generated password is exposed, replace it with a new independent password. If the master phrase may be compromised, rotate all affected credentials.
- Do not treat automatic clearing or the absence of a password database as a guarantee of security.

## Compatibility policy

The existing derivation algorithm is designated **v1**. Future changes to the KDF, parameters, input encoding, normalization or output formatting must be explicitly versioned. Preserve the v1 derivation path for existing users so that upgrades do not silently change previously generated passwords.

This designation documents the current algorithm; it does not imply that v1 is audited, certified or production-ready.
