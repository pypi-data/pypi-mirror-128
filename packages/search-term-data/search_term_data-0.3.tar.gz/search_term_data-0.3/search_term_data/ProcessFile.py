import time
import os
import datetime
import logging
import csv


class ProcessFile:
    def __init__(self, filename: str, working_dir: str):
        self.filename: str = filename
        self.working_dir: str = working_dir
        self.logger = logging.getLogger()

    async def computation(self) -> None:
        """
        Computes
        """
        try:
            time.sleep(1)
            csv_file_data = self.process_new_file()
            self.save_to_csv_file(csv_file_data)
            self.logger.info(f"Done processing file: {self.filename}")
        except:
            self.logger.error(f"Error occurred while processing {self.filename}")

    def get_field(self, name: str, value: str) -> int:
        """
        checks if the data is of integer type
        """
        try:
            float(value.replace(",", ""))
            return value
        except ValueError:
            self.logger.error(
                f"Error occurred while processing {self.filename}, Could not convert {name} to an integer")
            raise Exception(f"Could not convert {name} to an integer")

    def process_new_file(self):
        """
        process the newly added file and calculates the roas
        returns a csv file data
        """
        self.logger.info(f"Processing file: {self.filename}")
        with open(
                self.get_working_dir() + "/" + self.get_filename(),
                encoding="utf8",
                errors="ignore",
        ) as file:
            try:
                currency_terms = {}
                skip_first_line = 0
                for line in file:
                    if skip_first_line != 0:
                        file_data = line.strip().split(";")
                        search_term = file_data[0]
                        clicks = self.get_field("clicks", file_data[5])
                        impressions = self.get_field("impressions", file_data[8])
                        con_value = self.get_field("conversion value", file_data[10])
                        cost = self.get_field("cost", file_data[7])
                        currency = file_data[6]
                        roas = self.weird_division(
                            con_value.replace(",", ""), cost.replace(",", "")
                        )
                        if currency not in currency_terms:
                            currency_terms[currency] = [
                                [search_term, clicks, cost, impressions, con_value, roas]
                            ]
                        else:
                            currency_terms[currency].append(
                                [search_term, clicks, cost, impressions, con_value, roas]
                            )

                    skip_first_line += 1
                return currency_terms
            except IndexError:
                self.logger.error(f" list index out of range while processing file: {self.filename}")
                raise Exception(f" list index out of range while processing file: {self.filename}")

    def save_to_csv_file(self, currency_terms) -> None:
        """
        saves the csv file data to a csv file
        :param currency_terms: csv file data
        """
        current_dir = self.get_working_dir()
        for currency in currency_terms:
            path = current_dir + "/processed/{}/search_terms/".format(currency)
            if not os.path.exists(path):
                os.makedirs(path)
            ct = datetime.datetime.now()
            filename = str(ct.timestamp()) + ".csv"
            with open(os.path.join(path, filename), "w", encoding="UTF8") as fp:
                header = [
                    "search_term",
                    "clicks",
                    "cost",
                    "impressions",
                    "conversion_value",
                    "roas",
                ]
                writer = csv.writer(fp)
                # write the header
                writer.writerow(header)
                # write multiple rows
                writer.writerows(currency_terms[currency])

    def weird_division(self, con_value, cost):
        return float(con_value) / float(cost) if float(cost) else 0

    def get_filename(self) -> str:
        """
        returns the filename
        """
        return self.filename

    def get_working_dir(self) -> str:
        """
        return the working directory
        """
        return self.working_dir
