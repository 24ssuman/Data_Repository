import pandas as pd
from functools import reduce


def merge_and_sum_y(output_file):
    # Read the files assuming two columns: x and y
    fs = []
    for i in range(0, 10):
        fname = 'spectrum_' + str(i + 1) + '.dat'
        fs.append(pd.read_csv(fname, delim_whitespace=True, header=None, names=["x", f"y_{i+1}"]))

    # Merge the dataframes on 'x' with outer join and sum the 'y' values
    df_merged = reduce(
        lambda left, right: pd.merge(left, right, on="x", how="outer"),
        fs
    )

    # Replace NaNs with 0 and sum all y columns
    y_columns = [col for col in df_merged.columns if col != "x"]
    df_merged[y_columns] = df_merged[y_columns].fillna(0)
    df_merged["y"] = df_merged[y_columns].mean(axis=1)

    # Keep only 'x' and final 'y' and sort by 'x'
    df_final = df_merged[["x", "y"]].sort_values(by="x")

    # Save to output file
    df_final.to_csv(output_file, sep="\t", index=False, header=False)



merge_and_sum_y("averaged_ir.dat")
