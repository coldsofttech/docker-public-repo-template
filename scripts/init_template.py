#!/usr/bin/env python3
"""Tailor a repository created from the template. Run by the Init workflow.

Reads IMAGE_NAME, REPO and WITH_PYTEST / WITH_MYPY ("true" or "false") from the environment, and
optionally DOCKERHUB_NAMESPACE. Removes TEMPLATE_CHANGELOG.md and this script when done.
"""
import os
import re
import shutil
import sys
from pathlib import Path


def read(path):
    return Path(path).read_text(encoding="utf-8")


def write(path, text):
    Path(path).write_text(text, encoding="utf-8", newline="\n")


def cut(text, start, end):
    """Remove the block that begins at `start` and runs up to (not including) `end`."""
    first = text.index(start) + 1
    return text[:first] + text[text.index(end, first):]


def drop_step(text, name):
    """Remove the workflow step called `name`."""
    return re.sub(rf"      - name: {re.escape(name)}\n(?:        .*\n)+", "", text, count=1)


def main():
    image = os.environ["IMAGE_NAME"].strip()
    namespace = os.environ.get("DOCKERHUB_NAMESPACE", "").strip()
    repo = os.environ["REPO"]
    pytest = os.environ.get("WITH_PYTEST") == "true"
    mypy = os.environ.get("WITH_MYPY") == "true"

    if not re.fullmatch(r"[a-z0-9][a-z0-9._-]*", image):
        sys.exit(f"Invalid image name {image!r}: use lowercase letters, digits, '.', '_' and '-'.")
    if namespace and not re.fullmatch(r"[a-z0-9][a-z0-9_-]*", namespace):
        sys.exit(f"Invalid Docker Hub namespace {namespace!r}: use lowercase letters, digits, '_' and '-'.")

    # Image name and namespace.
    dockerfile = read("Dockerfile")
    dockerfile = re.sub(r'(image\.title=)"[^"]*"', rf'\1"{image}"', dockerfile, count=1)
    dockerfile = dockerfile.replace("OWNER/REPOSITORY", repo)
    write("Dockerfile", dockerfile)

    # The README's image badge links to the package, which is named after the image.
    package = f"/pkgs/container/{repo.split('/')[1]}"
    write("README.md", read("README.md").replace(package, f"/pkgs/container/{image}"))

    release = read(".github/workflows/release.yml")
    release = re.sub(r"(IMAGE_NAME: ).*", rf"\g<1>{image}", release, count=1)
    release = re.sub(r"(DOCKERHUB_NAMESPACE: ).*", rf'\g<1>"{namespace}"', release, count=1)
    write(".github/workflows/release.yml", release)

    # pytest and mypy.
    workflow = read(".github/workflows/ci.yml")
    tools = [t for t, on in (("mypy", mypy), ("pytest", pytest)) if on]
    if not pytest:
        shutil.rmtree("tests", ignore_errors=True)
        Path("pytest.ini").unlink(missing_ok=True)
        workflow = drop_step(workflow, "Run unit tests")
        workflow = cut(workflow, "\n  int-tests:\n", "  build:")
    if not mypy:
        Path("mypy.ini").unlink(missing_ok=True)
        workflow = drop_step(workflow, "Type-check with mypy")
    elif not pytest:
        write("mypy.ini", read("mypy.ini").replace("files = app, tests", "files = app"))

    if tools:
        workflow = workflow.replace("pip install mypy pytest", "pip install " + " ".join(tools), 1)
    else:
        workflow = cut(workflow, "\n  tests:\n", "  build:")
    write(".github/workflows/ci.yml", workflow)

    # Required status checks follow the jobs that remain.
    ruleset = read(".github/rulesets/main.json")
    for job, kept in (("tests", bool(tools)), ("int-tests", pytest)):
        if not kept:
            ruleset = re.sub(rf'[ \t]*\{{ "context": "{job}" \}},\r?\n', "", ruleset)
    write(".github/rulesets/main.json", ruleset)

    # Docs and README follow the same choices.
    docs = read("docs/docker.md")
    lines = []
    for line in docs.splitlines():
        if (line.startswith("- `mypy.ini`") and not mypy) or (
            line.startswith("- `tests/`") and not pytest
        ):
            continue
        if line.startswith("pytest -m integration") and not pytest:
            continue
        if line.startswith("pip install mypy pytest"):
            if not tools:
                continue
            line = " && ".join(["pip install " + " ".join(tools), *tools])
        lines.append(line)
    docs = "\n".join(lines) + "\n"
    both = "runs the unit tests (`tests`) and the integration tests (`int-tests`)"
    if not pytest:
        docs = docs.replace("`app/` and `tests/`", "`app/`")
        if mypy:
            docs = docs.replace(both, "runs mypy")
        else:
            docs = docs.replace(f"hadolint, {both}, and builds", "hadolint and builds")
    write("docs/docker.md", docs)

    if not pytest:
        write("README.md", read("README.md").replace("linting, image tests and", "linting and"))

    # The template's own changelog does not belong in the new repository.
    Path("TEMPLATE_CHANGELOG.md").unlink(missing_ok=True)
    Path(__file__).unlink()


if __name__ == "__main__":
    main()
