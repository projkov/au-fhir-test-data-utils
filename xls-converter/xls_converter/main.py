import pandas as pd
import os
import argparse
from constants import SHEETS
from processing_utils import process_sheet, post_process_sheet

parser = argparse.ArgumentParser(
    prog="Test Data converter",
    description="Load XLSX file with test data and convert it to csvs",
)
parser.add_argument("filename")
parser.add_argument("destination")


if __name__ == "__main__":
    args = parser.parse_args()
    xlsx = pd.ExcelFile(args.filename)
    for sheet in SHEETS:
        file_name = f"AU Core Sample Data - {sheet}.csv"
        file_path = os.path.join(args.destination, file_name)

        df = xlsx.parse(sheet, dtype=str, keep_default_na=False)

        process_sheet(sheet, df)

        df.to_csv(file_path, index=None, header=True, encoding="utf-8-sig", lineterminator="\r\n" if sheet == 'MedicationRequest' else "\n")

        post_process_sheet(sheet, file_path)
