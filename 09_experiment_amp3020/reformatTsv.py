import pandas as pd
import argparse

def reformat_data(input_file, output_file):
    """
    Reformats data from a TSV input file to a specified format and saves it to a TSV output file.

    Args:
        input_file (str): Path to the input TSV file.
        output_file (str): Path to the output TSV file.
    """

    try:
        df = pd.read_csv(input_file, sep='\t')

        df_melted = pd.melt(df, 
                            id_vars=['dose', 'repl'], 
                            var_name='time', 
                            value_name='od_value')

        df_melted['time'] = pd.to_numeric(df_melted['time'], errors='coerce')
        df_melted.dropna(inplace=True)
        df_melted['time'] = df_melted['time'].astype(int)

        df_melted.to_csv(output_file, sep='\t', index=False)

        print(f"Reformatted data saved to {output_file}")

    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reformat TSV data.")
    parser.add_argument("-i", "--input", required=True, help="Path to the input TSV file.")
    parser.add_argument("-o", "--output", required=True, help="Path to the output TSV file.")
    args = parser.parse_args()

    reformat_data(args.input, args.output)