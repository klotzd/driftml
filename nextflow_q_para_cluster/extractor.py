import argparse
import pandas as pd
import yaml
import json


parser = argparse.ArgumentParser()

parser.add_argument("--run", action="store", nargs="?")
parser.add_argument("fname")

# validation
args = parser.parse_args()
fname = args.fname

df = pd.read_csv(fname)

if args.run is not None:
    run = args.run

    df.run = df.run.astype(str)
    params = df[df.run == run].squeeze().to_json(double_precision=15)
    params = json.loads(params)

    print(yaml.dump(params, default_flow_style=False))

