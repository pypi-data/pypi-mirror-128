from __future__ import annotations

from typing import List, Union, Dict

import pandas as pd


class BotCSVPlugin:
    def __init__(self, has_header: bool = True, separator: str = ',') -> None:
        """
        This class stores the data in a CSV-like format.

        Args:
            has_header: True if the CSV's first row is supposed to be the header. Defaults to True.
            separator: The expected separator between each field.

        Attributes:
            has_header (bool, Optional): A list representing the header of the CSV, if it has one.
                Defaults to True.
            separator (str, Optional): The expected separator between each field. Defaults to ','.
        """
        self.has_header = has_header
        self._rows = pd.DataFrame()
        self.separator = separator
        ...

    def set_separator(self, separator: str) -> BotCSVPlugin:
        self.separator = separator
        return self

    def set_header(self, headers: List[str]) -> BotCSVPlugin:
        self.header = headers
        return self

    @property
    def header(self) -> List[str]:
        """
        Returns this CSV's header.

        Returns:
            List of header elements in str format.
        """
        return self._rows.columns.tolist()

    @header.setter
    def header(self, headers: List[str]):
        self._rows.columns = headers

    def add_row(self, row: Union[List[object], Dict[str, object]]) -> BotCSVPlugin:
        """
        Adds a new row to the CSV.

        If the input contains a new column, then a new column will be created in the CSV as well, with blank fields
        for the previously inserted lines.

        Args: row: A list of csv elements in string format, or a dict. If a list of rows is passed, it'll make a
        best-effort attempt to use add_rows() instead.

        Returns:
            self (allows Method Chaining).
        """
        # List Treatment
        if isinstance(row, list):
            # Empty List
            if not row:
                return self

            # List of Lists or list of
            if isinstance(row[0], list) or isinstance(row[0], dict):
                self.add_rows(row)
                return self

            # Zips this list with the header to form a dict
            row = dict(zip(self.header, row))

        # Appends the row and return
        self._rows = self._rows.append(row, ignore_index=True)
        return self

    def add_rows(self, rows: List[Union[List[object], Dict[str, object]]]) -> BotCSVPlugin:
        """
        Adds new rows to the CSV.

        If the input contains a new column, then a new column will be created in the CSV as well, with blank fields
        for the previously inserted lines.

        Args:
            rows: A list of rows. Each row is a list of str.

        Returns:
            self (allows Method Chaining).
        """
        self._rows = self._rows.append(rows)
        return self

    def remove_row(self, row: int) -> BotCSVPlugin:
        """
        Removes a single row from the CSV

        Args:
            row: 0-indexed row number

        Returns:
            self (allows Method Chaining).
        """
        self._rows = self._rows.drop(index=row)
        return self

    def remove_rows(self, rows: List[int]) -> BotCSVPlugin:
        """
        Removes either a single row or a list of rows from the CSV.

        Args:
            rows: List of 0-indexed row numbers.

        Returns:
            self (allows Method Chaining).
        """
        self._rows = self._rows.drop(index=rows)
        return self

    def remove_column(self, columns: Union[int, str]) -> BotCSVPlugin:
        """
        Removes single column from the CSV.

        Args:
            columns: A column's header or it's 0-indexed column number

        Returns:
            self (allows Method Chaining).
        """
        self._rows = self._rows.drop(columns=columns)
        return self

    def remove_columns(self, columns: Union[int, str, List[Union[int, str]]]) -> BotCSVPlugin:
        """
        Removes a list of columns from the CSV.

        Args:
            columns: A list of column's headers or their 0-indexed column numbers.

        Returns:
            self (allows Method Chaining).
        """
        self._rows = self._rows.drop(columns=columns)
        return self

    # noinspection PyTypeChecker
    def as_list(self, include_header: bool = False) -> List:
        """
        Returns the contents of this CSV in a list of lists format.

        Args:
            include_header: If True, the first inner-list will receive the CSV's header.

        Returns:
            A list of rows. Each is a list of row elements.
        """
        # Includes Header if needed
        data = self._rows.values.tolist()
        if include_header:
            data.insert(0, self.header)

        return data

    def as_dict(self) -> List[Dict[str, object]]:
        """
        Returns the contents of this CSV in a list of dicts format.

        Returns:
            A list of rows. Each row is a dict.
        """

        return self._rows.to_dict('list')

    def as_dataframe(self) -> pd.DataFrame:
        """
        Returns the contents of this CSV in a Pandas DataFrame format.

        Returns:
            A Pandas DataFrame object.
        """
        return self._rows

    def read(self, file_or_path):
        """
        Reads a CSV file using the delimiter and has_header attributes of thi class.

        Args:
            file_or_path: Either a buffered CSV file or a path to it.

        Returns:
            self (allows Method Chaining).
        """
        self._rows = pd.read_csv(file_or_path, sep=self.separator, header=0 if self.has_header else None)
        return self

    def write(self, file_or_path) -> BotCSVPlugin:
        """
        Writes this class's CSV content to a file using it's delimiter and has_header attributes.

        Args:
            file_or_path: Either a buffered CSV file or a path to it.

        Returns:
            self (allows Method Chaining).
        """
        self._rows.to_csv(file_or_path, sep=self.separator, header=True if self.has_header else False)
        return self

    def sort(self, by_columns: Union[int, str, List[Union[int, str]]], ascending: bool = True) -> BotCSVPlugin:
        """
        Sorts the CSV rows using the first column of the by_columns parameter as a reference. In case of a tie,
        the second column provided is used, and so on.

        Args:
            by_columns: A column's headers or their 0-indexed column number, or a list of these.
            ascending: Set to False if you want to use descending order. Defaults to True.

        Returns:
            self (allows Method Chaining)
        """
        self._rows = self._rows.sort_values(by_columns, ascending=ascending)
        return self
