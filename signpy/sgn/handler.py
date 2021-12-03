# from signpy import sgn

import csv


class HandlerCSV:
    """Class for handling imports and exports with .csv files."""
    @staticmethod
    def export_signal1(filename: str, signal1):
        """Exports the given one dimensional signal to the .csv file."""
        with open(filename, "w+") as file:
            writer = csv.writer(file)
            writer.writerows(*signal1.unpack())


class HandlerJSON:
    """Class for handling imports and exports with .json files."""
    @staticmethod
    def export_signal1(filename: str, signal1):
        """Exports the given one dimensional signal to the .json file."""
        with open(filename, "w+") as file:
            pass
