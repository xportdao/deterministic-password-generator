# Deterministic Password Generator

A small Python script that derives a password from a secret phrase and a service domain using scrypt. It runs locally using the Python standard library.

## Run

```sh
python3 generate.py
```

Enter your secret phrase at `Secret phrase:` and a domain such as `example.com` at `Service:`. The script hides the phrase as you type and prints the generated password.

Use the same phrase and domain to reproduce a password. The script trims spaces around the domain and converts it to lowercase. Enter the domain in the same form each time, without a protocol, path, or trailing slash.

Choose a strong, unique secret phrase and keep it private. Anyone who knows it can regenerate your passwords.
