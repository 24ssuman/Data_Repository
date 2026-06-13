import pandas as pd
import numpy as np
from functools import reduce
import glob
import os


def merge_and_sum_y(files, output_file):
    # Read the files assuming two columns: x and y
    dfs = [pd.read_csv(f, delim_whitespace=True, header=None, names=["x", f"y_{i}"])
           for i, f in enumerate(files)]

    # Merge all dataframes on 'x' with outer join
    df_merged = reduce(
        lambda left, right: pd.merge(left, right, on="x", how="outer"),
        dfs
    )

    # Replace NaNs with 0 and sum all y columns
    y_columns = [col for col in df_merged.columns if col != "x"]
    df_merged[y_columns] = df_merged[y_columns].fillna(0)
    df_merged["y"] = df_merged[y_columns].sum(axis=1)

    # Keep only 'x' and final 'y' and sort by 'x'
    df_final = df_merged[["x", "y"]].sort_values(by="x")

    # Save to output file
    df_final.to_csv(output_file, sep="\t", index=False, header=False)


def weight(fnames, p):
    fnames2 = []
    for fname in fnames:
        # figure out weight index from filename (assumes isomer-<N>.dat)
        base = os.path.basename(fname)
        idx = fnames.index(fname)
        w = float(p[idx])

        # output file
        fout = base.replace(".dat", "-weighted.dat")
        fnames2.append(fout)

        # read + scale y values
        with open(fname, "r") as f:
            lines = f.readlines()
        new_lines = []
        for line in lines:
            parts = line.split()
            #parts[1] = str(float(parts[1]) * w / total_areas[idx + 1])
            parts[1] = str(float(parts[1]) * w)
            new_lines.append("\t".join(parts))
        with open(fout, "w") as f:
            f.write("\n".join(new_lines) + "\n")

    return fnames2


# --- main workflow ---
with open("../weights.dat", "r") as f:
    p = f.readline().split()

# all input isomer files
input_files = sorted(glob.glob("new_ir*.dat"))

# weight them
weighted_files = weight(input_files, p)

# merge + sum
#merge_and_sum_y(weighted_files, "all_by_area.dat")

