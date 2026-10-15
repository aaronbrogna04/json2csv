# Security Policy

## Reporting a Vulnerability

If you find a security vulnerability in json2csv, please report it through [GitHub's private vulnerability reporting](https://github.com/aaronbrogna04/json2csv/security/advisories/new). This keeps the details private while we work on a fix.

Please include:

- What you found and how to reproduce it
- Which version you're using
- Any relevant logs or output (redact secrets)

## Security Measures

This project includes the following security measures:

- **Bandit** runs in the GitHub Actions CI workflow on every push to `main` and every pull request, scanning `src` for common security issues
- **Dependabot** checks weekly for updates to pip dependencies and GitHub Actions
- **Minimal workflow permissions** (`permissions: contents: read`)

## Response Times

This is a volunteer-maintained open source project. Security reports are taken seriously, but there are no guaranteed response times.

**Enterprise support** is available, with priority response SLAs. Contact aaronbrogna46@gmail.com for details.

## Supported Versions

Security fixes are applied to the latest release on the `main` branch. There is no backport policy for older versions.
