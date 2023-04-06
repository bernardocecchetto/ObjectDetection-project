import pandas as pd
import typing as Ty
import glob
import argparse
from object_detection.protos.string_int_label_map_pb2 import (
    StringIntLabelMap,
    StringIntLabelMapItem,
)
from google.protobuf import text_format


def convert_classes(classes, start=1):
    msg = StringIntLabelMap()
    for id, name in enumerate(classes, start=start):
        msg.item.append(StringIntLabelMapItem(id=id, name=name))

    text = str(text_format.MessageToBytes(msg, as_utf8=True), "utf-8")
    return text


def csv_to_label(input_dir: Ty.AnyStr, output_dir: Ty.AnyStr):
    """
    The following script aims to convert the csv informations to label *.pbtxt files.

    Args:
        input_dir (Ty.AnyStr): The directory that contains all the csvs to be processed (train/validation/test)
        output_dir (Ty.AnyStr): The the directory where is going to be saved the pbtxt generated

    Usage:
        python csv_to_labelmap.py --input_dir=data/  --output_dir=data/
    """
    csvs = glob.glob(f"{input_dir}/*csv")

    csv_list = []
    for csv in csvs:
        df = pd.read_csv(csv)
        csv_list.append(df)

    df = pd.concat(csv_list)

    # getting all the unique labels
    unique_labels = df["class"].unique()

    # generating the string to be saved in pbtxt format
    label_maps = convert_classes(unique_labels)

    with open(f"{output_dir}/label_map.pbtxt", "w") as pbfile:
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
