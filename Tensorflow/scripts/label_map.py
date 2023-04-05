import pandas as pd
import typing as Ty
import glob
import argparse


def csv_to_label(csv_path: Ty.AnyStr, pbtxt_path: Ty.AnyStr):
    """
    The following script aims to convert the csv informations to label *.pbtxt files.

    Args:
        csv_path (Ty.AnyStr): the name and the directory that contains the csv to be processed
        pbtxt_path (Ty.AnyStr): the name and the directory where is going to be saved the pbtxt generated

    Usage:
        # Create train data:
        python csv_to_labelmap.py --csv_path=data/train_labels.csv  --pbtxt_path=data/train.pbtxt

        # Create test data:
        python csv_to_labelmap.py --csv_path=data/test_labels.csv  --pbtxt_path=data/test.pbtxt
    """

    df = pd.read_csv(csv_path)

    # getting all the unique labels
    unique_labels = df["class"].unique()

    # generating the string to be saved in pbtxt format
    label_maps = ""
    for idx, labels in enumerate(unique_labels):

        label_maps += (
            """

            item {
                name: '"""
            + str(idx)
            + """'
                id: """
            + str(labels)
            + """
            }


        """
        )

    with open(pbtxt_path, "w") as pbfile:
        pbfile.write(label_maps)


def main():
    parser = argparse.ArgumentParser(
        description="Generating pbtxt from csv files",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "-c",
        "--csv_dir",
        help="Path and file name where the csv it is stored",
        type=str,
        default=None,
    )
    parser.add_argument(
        "-p",
        "--pbtxt_dir",
        help="Path and file name where the pbtxt_dir it is going to be stored",
        type=str,
        default=None,
    )

    args = parser.parse_args()

    # Now we are ready to start the iteration
    csv_to_label(args.csv_dir, args.pbtxt_dir)


if __name__ == "__main__":
    main()
