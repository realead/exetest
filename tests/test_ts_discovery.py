import unittest
import os

import exetest.ts_discovery as ds
import exetest as ex

 
 
class DiscoveryTester(unittest.TestCase):  

    def test_stem1(self):
       self.assertEquals(ds.stem("AAA/BBB.txt"), "BBB")

    def test_stem2(self):
       self.assertEquals(ds.stem("AAA.txt"), "AAA")

    def test_extension1(self):
       self.assertEquals(ds.extension("AAA/BBB.txt"), ".txt")

    def test_extension2(self):
       self.assertEquals(ds.extension("AAA.txt"), ".txt")

    def test_filter_test_casesA(self):
        tcases=ds.filter_test_cases(["A.in", "A.out"], ds.DEFAULT_ENDINGS, ds.DEFAULT_NEEDED_FILES)
        self.assertEquals(len(tcases), 1)
        self.assertEquals(tcases["A"], {ex.INPUT_FILE : "A.in", 
                                        ex.STDOUT_FILE: "A.out"})
 

    def test_filter_test_casesB(self):
        tcases=ds.filter_test_cases(["B.in", "B.out", "B.err"], ds.DEFAULT_ENDINGS, ds.DEFAULT_NEEDED_FILES)
        self.assertEquals(len(tcases), 1)
        self.assertEquals(tcases["B"], {ex.INPUT_FILE : "B.in", 
                                        ex.STDOUT_FILE: "B.out",
                                        ex.STDERR_FILE: "B.err"})

    def test_filter_test_casesNoC(self):
        tcases=ds.filter_test_cases(["C.in",  "C.err"], ds.DEFAULT_ENDINGS, ds.DEFAULT_NEEDED_FILES)
        self.assertEquals(len(tcases), 0)


    def test_filter_test_casesABNoC(self):
        tcases=ds.filter_test_cases(["C.in", "B.in", "A.in", "A.out", "B.out", "B.err", "C.err"], ds.DEFAULT_ENDINGS, ds.DEFAULT_NEEDED_FILES)
        self.assertEquals(len(tcases), 2)
        self.assertEquals(tcases["B"], {ex.INPUT_FILE : "B.in", 
                                        ex.STDOUT_FILE: "B.out",
                                        ex.STDERR_FILE: "B.err"})
        self.assertEquals(tcases["A"], {ex.INPUT_FILE : "A.in", 
                                        ex.STDOUT_FILE: "A.out"})


    def test_discover_test_casesABNoC(self):
        folder="test_data/dummy_ts_set"
        tcases=ds.discover_test_cases(folder)
        self.assertEquals(len(tcases), 2)
        self.assertEquals(tcases["B"], {ex.INPUT_FILE : os.path.join(folder, "B.in"), 
                                        ex.STDOUT_FILE: os.path.join(folder, "B.out"),
                                        ex.STDERR_FILE: os.path.join(folder, "B.err")})
        self.assertEquals(tcases["A"], {ex.INPUT_FILE : os.path.join(folder, "A.in"), 
                                        ex.STDOUT_FILE: os.path.join(folder, "A.out")})


