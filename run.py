from argparse import ArgumentParser
import json
from os import listdir, makedirs
from os.path import isfile, join, splitext, isdir, abspath
import subprocess
import itertools
import sys

dir = "./tests/"
passed = []
failed = []

WHITE = "\033[0m"
GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"


def pcolor(txt, color):
    print("%s%s%s" % (color, txt, "\033[0m"))


def pcolor_json(j, color, prefix=""):
    if j:
        pcolor(prefix + json.dumps(j, sort_keys=True).replace('"', ""), color)


def read_clues(filename):
    with open(dir + filename, encoding="utf8") as f:
        return "\n".join([line for line in f.readlines() if line.startswith("##")])


def read_json_lines_file(filename):
    with open(dir + filename, encoding="utf8") as f:
        result = []
        for i, line in enumerate(f.readlines(), start=1):
            if not line.startswith("#"):
                try:
                    result.append(json.loads(line))
                except e:
                    print("invalid json\nfile: %s\nline %d: %s" % (filename, i, line))
                    sys.exit()
        return result

def main(solution_dir: str, restrict_tests_to: set):
    tests = sorted({splitext(f)[0] for f in listdir(dir) if isfile(join(dir, f))})

    for prefix in tests:
        if restrict_tests_to != set():
            omit = True
            for r in restrict_tests_to:
                if r in prefix:
                    omit = False
            if omit:
                continue
        input = "".join(
            [json.dumps(j) + "\n" for j in read_json_lines_file(prefix + ".in")]
        )
        expected = read_json_lines_file(prefix + ".out")

        process = subprocess.Popen(
            ["docker", "run", "-i", "-v", f"{solution_dir}:/order-book", "python:3.11.2-alpine", "/order-book/run.sh"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            encoding="utf8",
        )
        process.stdin.write(input)
        process.stdin.close()
        actual = []
        makedirs("tests_out_tmp/", exist_ok=True)
        with open("tests_out_tmp/" + prefix + ".out", "w") as tmp_out:
            for line in process.stdout.read().splitlines(True):
                tmp_out.write(line)
                line = line.replace("\n", "").replace("'", '"')
                if line:
                    try:
                        j = json.loads(line)
                    except e:
                        j = line
                    actual.append(j)

        if expected != actual:
            failed.append(prefix)
            pcolor(prefix + " " + read_clues(prefix + ".out"), BLUE)
            for i, (e, a) in enumerate(itertools.zip_longest(expected, actual), start=1):
                if json.dumps(a, sort_keys=True) == json.dumps(e, sort_keys=True):
                    pcolor_json(a, GREEN)  # , prefix="ok(%d):       " % i)
                else:
                    pcolor_json(a, RED, prefix="%d: " % i)
                    pcolor_json(e, WHITE, prefix="%d: " % i)
            print()
        else:
            passed.append(prefix)

    pcolor("passed:\n" + "\n".join(passed), GREEN)
    pcolor("failed:\n" + "\n".join(failed), RED)

if __name__ == "__main__":
    p = ArgumentParser()
    p.add_argument("solution_dir", help="path to solution directory")
    p.add_argument("tests", nargs="*", help="tests to run, all if not specified")
    args = p.parse_args()

    if not isdir(args.solution_dir):
        p.error(f"{args.solution_dir} is not a directory")
    
    main(abspath(args.solution_dir), set(args.tests))
