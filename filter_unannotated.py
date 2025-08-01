import json, argparse, os

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input")
parser.add_argument("-a", "--annotation")
parser.add_argument("-d", "--dry-run", action="store_true", default=False)

args = parser.parse_args()

assert os.path.isdir(args.input)
assert os.path.isfile(args.annotation)

abs_path = os.path.abspath(args.input)

with open(args.annotation, "r") as file:
    annotations = json.loads(file.read())

filtered_anno = set(dict(filter(lambda x: x[1] != [], annotations.items())).keys())

all_input = os.listdir(args.input)
pics = set(
    [f for f in all_input if os.path.isfile(abs_path + "/" + f) and f.endswith(".jpg")]
)

not_annotated = pics - filtered_anno

if args.dry_run:
    cwd = os.getcwd()

    not_annotated_paths = [
        (abs_path + "/" + not_anno, cwd + "/Unannotated/" + not_anno)
        for not_anno in not_annotated
    ]

    if not os.path.isdir("Unannotated"):
        os.mkdir("Unannotated")

    for file in not_annotated_paths:
        os.rename(file[0], file[1])
else:
    not_annotated_paths = [abs_path + "/" + not_anno for not_anno in not_annotated]

    for file in not_annotated_paths:
        os.remove(file)