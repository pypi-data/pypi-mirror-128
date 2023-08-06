import time
import os
import datetime
import csv


class ProcessFile:
    def __init__(self, filename: str, working_dir: str):
        self.filename: str = filename
        self.working_dir: str = working_dir

    async def computation(self) -> None:
        """
        Computes
        """
        time.sleep(1)
        csv_file_data = self.process_new_file()
        self.save_to_csv_file(csv_file_data)

    def process_new_file(self):
        """
        process the newly added file and calculates the roas
        returns a csv file data
        """
        with open(self.get_working_dir() + "/" + self.get_filename(), encoding="utf8", errors="ignore") as file:
            currency_terms = {}
            skip_first_line = 0
            for line in file:
                if skip_first_line != 0:
                    remove_whitespace = line.strip().split(";")
                    search_term = remove_whitespace[0]
                    clicks = remove_whitespace[5]
                    impressions = remove_whitespace[8]
                    con_value = remove_whitespace[10]
                    cost = remove_whitespace[7]
                    currency = remove_whitespace[6]
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
