import os
import daemon
from typing import List
import asyncio

from search_term_data.ProcessFile import ProcessFile


class BackgroundProcess:
    def __init__(self):
        self.new_files: List[str] = []
        self.working_dir: str = os.getcwd()

    def listening_for_new_files(self) -> None:
        """
        Daemon part that listens for newly added files and class ProcessFile
        """
        before = dict([(f, None) for f in self.filter_by_csv()])
        while True:
            after = dict([(f, None) for f in self.filter_by_csv()])
            added = [f for f in after if not f in before]
            if added:
                print(added)
                for file in added:
                    process_file = ProcessFile(file, self.get_working_dir())
                    asyncio.run(process_file.computation())
            before = after

    def filter_by_csv(self) -> List[str]:
        """
        Filters the folder to just return the csv files only
        :return: List of csv files
        """
        filenames = os.listdir(self.get_working_dir())
        return [filename for filename in filenames if filename.endswith(".csv")]

    def start_daemon(self) -> None:
        """
        Start the daemon
        """
        with daemon.DaemonContext():
            self.listening_for_new_files()

    def get_working_dir(self) -> str:
        """
        returns the directory that the daemon is listening to
        """
        return self.working_dir
