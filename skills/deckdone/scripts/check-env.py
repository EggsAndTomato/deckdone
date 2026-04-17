#!/usr/bin/env python3
"""Checks DeckDone dependencies and optionally installs missing ones."""

import argparse
import importlib.util
import json
import os
import platform
import shutil
import subprocess
import sys


CHECKS = [
    {
        "id": "python",
        "category": "Python",
        "name": "Python 3.8+",
        "check": "check_python",
        "install_cmd": None,
        "install_hint": "Install Python 3.8+ from https://python.org",
    },
    {
        "id": "pypdf",
        "category": "Python",
        "name": "pypdf",
        "check": "check_pypdf",
        "install_cmd": "pip install pypdf",
    },
    {
        "id": "pypdfium2",
        "category": "Python",
        "name": "pypdfium2",
        "check": "check_pypdfium2",
        "install_cmd": "pip install pypdfium2",
    },
    {
        "id": "pdfplumber",
        "category": "Python",
        "name": "pdfplumber",
        "check": "check_pdfplumber",
        "install_cmd": "pip install pdfplumber",
        "optional": True,
    },
    {
        "id": "node",
        "category": "Node.js",
        "name": "Node.js 18+",
        "check": "check_node",
        "install_cmd": None,
        "install_hint": "Install Node.js 18+ from https://nodejs.org",
    },
    {
        "id": "pptxgenjs",
        "category": "Node.js",
        "name": "pptxgenjs (global)",
        "check": "check_pptxgenjs",
        "install_cmd": "npm install -g pptxgenjs",
    },
    {
        "id": "playwright",
        "category": "Node.js",
        "name": "playwright (global)",
        "check": "check_playwright",
        "install_cmd": "npm install -g playwright",
    },
    {
        "id": "sharp",
        "category": "Node.js",
        "name": "sharp (global)",
        "check": "check_sharp",
        "install_cmd": "npm install -g sharp",
    },
    {
        "id": "pw_browsers",
        "category": "Node.js",
        "name": "Playwright browsers",
        "check": "check_pw_browsers",
        "install_cmd": "npx playwright install",
    },
    {
        "id": "libreoffice",
        "category": "System",
        "name": "LibreOffice",
        "check": "check_libreoffice",
        "install_cmd": None,
        "install_hint": "Install LibreOffice: winget install TheDocumentFoundation.LibreOffice (Win) / brew install --cask libreoffice (macOS) / apt install libreoffice (Linux)",
        "optional": True,
    },
]


def check_python():
    return sys.version_info >= (3, 8)


def check_pypdf():
    return importlib.util.find_spec("pypdf") is not None


def check_pypdfium2():
    return importlib.util.find_spec("pypdfium2") is not None


def check_pdfplumber():
    return importlib.util.find_spec("pdfplumber") is not None


def check_node():
    try:
        result = subprocess.run(
            ["node", "--version"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode != 0:
            return False
        version_str = result.stdout.strip().lstrip("v")
        major = int(version_str.split(".")[0])
        return major >= 18
    except (FileNotFoundError, subprocess.TimeoutExpired, ValueError):
        return False


def _check_npm_global(package):
    try:
        result = subprocess.run(
            ["npm", "list", "-g", package],
            capture_output=True,
            text=True,
            timeout=15,
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def check_pptxgenjs():
    return _check_npm_global("pptxgenjs")


def check_playwright():
    return _check_npm_global("playwright")


def check_sharp():
    return _check_npm_global("sharp")


def check_pw_browsers():
    if platform.system() == "Windows":
        base = os.environ.get("LOCALAPPDATA", "")
        pw_dir = os.path.join(base, "ms-playwright") if base else ""
    else:
        pw_dir = os.path.expanduser("~/.cache/ms-playwright")
    if not pw_dir or not os.path.isdir(pw_dir):
        return False
    entries = os.listdir(pw_dir)
    return len(entries) > 0


def check_libreoffice():
    candidates = ["soffice", "libreoffice"]
    if platform.system() == "Windows":
        candidates.append(
            os.path.join(
                os.environ.get("ProgramFiles", r"C:\Program Files"),
                "LibreOffice",
                "program",
                "soffice.exe",
            )
        )
    for cmd in candidates:
        if shutil.which(cmd):
            return True
        if os.path.isfile(cmd):
            return True
    return False


CHECK_FUNCS = {
    "python": check_python,
    "pypdf": check_pypdf,
    "pypdfium2": check_pypdfium2,
    "pdfplumber": check_pdfplumber,
    "node": check_node,
    "pptxgenjs": check_pptxgenjs,
    "playwright": check_playwright,
    "sharp": check_sharp,
    "pw_browsers": check_pw_browsers,
    "libreoffice": check_libreoffice,
}


def run_checks():
    results = []
    for check in CHECKS:
        func = CHECK_FUNCS[check["id"]]
        passed = func()
        results.append({**check, "passed": passed})
    return results


def print_report(results):
    current_cat = None
    for r in results:
        if r["category"] != current_cat:
            current_cat = r["category"]
            print(f"\n{current_cat}:")
        status = "PASS" if r["passed"] else ("SKIP" if r.get("optional") else "FAIL")
        suffix = " (optional)" if r.get("optional") else ""
        print(f"  [{status}] {r['name']}{suffix}")

    required_fails = [r for r in results if not r["passed"] and not r.get("optional")]
    optional_fails = [r for r in results if not r["passed"] and r.get("optional")]
    print()

    if not required_fails and not optional_fails:
        print("All dependencies satisfied.")
    elif not required_fails:
        print(f"Core dependencies OK. {len(optional_fails)} optional item(s) missing.")
    else:
        print(f"FAIL: {len(required_fails)} required item(s) missing.")
        for r in required_fails:
            print(f"  - {r['name']}")
            if r.get("install_cmd"):
                print(f"    Install: {r['install_cmd']}")
            elif r.get("install_hint"):
                print(f"    {r['install_hint']}")


def print_json_report(results):
    output = []
    for r in results:
        output.append(
            {
                "id": r["id"],
                "name": r["name"],
                "category": r["category"],
                "passed": r["passed"],
                "optional": r.get("optional", False),
                "install_cmd": r.get("install_cmd"),
            }
        )
    print(json.dumps(output, indent=2))


def install_missing(results, auto_yes=False):
    missing = [r for r in results if not r["passed"] and r.get("install_cmd")]
    if not missing:
        print("Nothing to install.")
        return

    print(f"\n{len(missing)} item(s) to install:\n")
    for r in missing:
        print(f"  {r['name']}: {r['install_cmd']}")
    print()

    for r in missing:
        if auto_yes:
            print(f"Installing {r['name']}...")
            _run_install(r["install_cmd"])
        else:
            answer = (
                input(f"Install {r['name']}? ({r['install_cmd']}) [y/N]: ")
                .strip()
                .lower()
            )
            if answer == "y":
                _run_install(r["install_cmd"])
            else:
                print(f"  Skipped {r['name']}.")


def _run_install(cmd):
    try:
        result = subprocess.run(cmd, shell=True, timeout=120)
        if result.returncode == 0:
            print(f"  OK")
        else:
            print(f"  FAILED (exit code {result.returncode})")
    except subprocess.TimeoutExpired:
        print(f"  FAILED (timeout)")


def main():
    parser = argparse.ArgumentParser(description="Check DeckDone dependencies")
    parser.add_argument(
        "--install",
        action="store_true",
        help="Install missing dependencies (prompts for confirmation)",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="Auto-confirm all installs (use with --install for non-interactive mode)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON",
    )
    args = parser.parse_args()

    if args.json and args.install:
        print("Error: --json and --install are mutually exclusive", file=sys.stderr)
        sys.exit(2)

    results = run_checks()

    if args.json:
        print_json_report(results)
        required_fails = [
            r for r in results if not r["passed"] and not r.get("optional")
        ]
        sys.exit(1 if required_fails else 0)

    print_report(results)

    if args.install:
        install_missing(results, auto_yes=args.yes)
        print("\n--- Re-checking ---")
        results = run_checks()
        print_report(results)

    required_fails = [r for r in results if not r["passed"] and not r.get("optional")]
    sys.exit(1 if required_fails else 0)


if __name__ == "__main__":
    main()
