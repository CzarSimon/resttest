# Standard library
import json
from abc import ABCMeta, abstractmethod
from os import listdir
from os.path import join, isfile
from typing import Any, Dict, List
from collections import namedtuple

# Internal modules
from resttest.models import Env, TestCase


NumberedFilename = namedtuple("NumberedFilename", ["number", "name"])


class Reader(metaclass=ABCMeta):
    @abstractmethod
    def read_env(self, port: int) -> Env:
        raise NotImplementedError

    @abstractmethod
    def read_test_case(self, name: str) -> TestCase:
        raise NotImplementedError

    @abstractmethod
    def read_test_cases(self) -> List[TestCase]:
        raise NotImplementedError


class FileReader(Reader):
    def __init__(self, test_dir: str) -> None:
        self.test_dir = test_dir

    def read_env(self, port: int) -> Env:
        raw = self._read_file("env.json")
        return Env.fromdict(port, raw)

    def read_test_case(self, name: str) -> TestCase:
        filename = self._append_suffix(name)
        raw = self._read_file(filename)
        return TestCase.fromdict(raw)

    def read_test_cases(self) -> List[TestCase]:
        filenames = self._get_test_case_names()
        return [self.read_test_case(fname) for fname in filenames]

    def _read_file(self, name: str) -> Dict[str, Any]:
        filename = f"{self.test_dir}/{name}"
        with open(filename, "r") as f:
            return json.load(f)

    def _append_suffix(self, name: str) -> str:
        if name.endswith(".json"):
            return name
        return name + ".json"

    def _get_test_case_names(self) -> List[str]:
        unsorted_names = [
            fname
            for fname in listdir(self.test_dir)
            if isfile(join(self.test_dir, fname)) and fname != "env.json"
        ]
        return self._sort_filenames(unsorted_names)

    def _sort_filenames(self, filenames: List[str]) -> List[str]:
        numbered = self._number_filenames(filenames)
        sorted_names = sorted(numbered, key=lambda nf: nf.number)
        return [nf.name for nf in sorted_names]

    def _number_filenames(self, filenames: List[str]) -> List[NumberedFilename]:
        return [
            NumberedFilename(number=int(fname.split("-")[0]), name=fname)
            for fname in filenames
        ]
