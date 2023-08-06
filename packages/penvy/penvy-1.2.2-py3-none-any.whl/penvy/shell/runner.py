import io
import os
import sys
import subprocess


def run_and_read_line(command: str, cwd: str = os.getcwd(), shell=False):
    proc = subprocess.Popen(command, cwd=cwd, stdout=subprocess.PIPE, shell=shell)
    line = io.TextIOWrapper(proc.stdout, encoding="utf-8").read().rstrip()

    if not line:
        raise Exception(f"No output returned to stdout for: {command}")

    return line


def run_shell_command(command: str, cwd: str = os.getcwd(), shell=False):
    proc = subprocess.Popen(command, cwd=cwd, shell=shell)
    proc.communicate()

    if proc.returncode != 0:
        raise Exception(f"Shell command failed with code: {proc.returncode}")


def run_with_live_output(command: str, cwd: str = os.getcwd(), shell=False):
    proc = subprocess.Popen(command, cwd=cwd, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    for line in iter(proc.stdout.readline, b""):
        sys.stdout.write(line)

    proc.communicate()

    if proc.returncode != 0:
        raise Exception(f"Shell command failed with code: {proc.returncode}")
