#!/usr/bin/env python3
"""Tests for the gta6-meme-x-01 v2 repo.

1. meme.py twice -> identical sha256 (determinism).
2. meme.png is 1080x1080.
3. main.ts runs with the placeholder POST.json -> exit 0, and
   out/POST.json is byte-identical to POST.json.
Run from the repo root: python3 tests/test.py
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)


def run(cmd, **kw):
    return subprocess.run(cmd, cwd=REPO, capture_output=True, text=True,
                          **kw)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def main():
    failures = []

    # 1. determinism: run meme.py twice, compare sha256
    hashes = []
    for _ in range(2):
        r = run([sys.executable, "meme.py"])
        if r.returncode != 0:
            failures.append(f"meme.py failed: {r.stderr.strip()}")
            break
        hashes.append(sha256(os.path.join(REPO, "meme.png")))
    if len(hashes) == 2:
        print("meme.py sha256 run 1:", hashes[0])
        print("meme.py sha256 run 2:", hashes[1])
        if hashes[0] != hashes[1]:
            failures.append("meme.py is not deterministic")

    # 2. size 1080x1080
    from PIL import Image
    with Image.open(os.path.join(REPO, "meme.png")) as im:
        print("meme.png size:", im.size)
        if im.size != (1080, 1080):
            failures.append(f"meme.png is {im.size}, not 1080x1080")

    # 3. main.ts with placeholder POST.json -> exit 0
    outdir = os.path.join(REPO, "out-test")
    shutil.rmtree(outdir, ignore_errors=True)
    env = dict(os.environ, MAKEFUN_BOT_DIR=REPO,
               MAKEFUN_OUTPUT_DIR=outdir)
    r = run(["node", "main.ts"], env=env)
    print("main.ts exit code:", r.returncode, "| stdout:",
          repr(r.stdout), "| stderr:", repr(r.stderr))
    if r.returncode != 0:
        failures.append(f"main.ts exit {r.returncode}: {r.stderr.strip()}")
    else:
        with open(os.path.join(REPO, "POST.json"), "rb") as f:
            src = f.read()
        with open(os.path.join(outdir, "POST.json"), "rb") as f:
            dst = f.read()
        if src != dst:
            failures.append("out/POST.json differs from POST.json")
        else:
            print("out/POST.json byte-identical to POST.json")
    shutil.rmtree(outdir, ignore_errors=True)

    # 4. POST.json placeholder is valid JSON with the expected URL shape
    with open(os.path.join(REPO, "POST.json")) as f:
        data = json.load(f)
    assert data["url"] == "https://x.com/<handle>/status/<id>", data
    print("POST.json placeholder OK")

    if failures:
        print("FAILURES:")
        for f in failures:
            print(" -", f)
        return 1
    print("ALL TESTS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
