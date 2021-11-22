import unittest
import os
from dataRetrieval import retrieveDatafromHtmlFiles, retrieveDatafromErrorFiles, retrieveDatafromVisitFiles
from config import HTML_FILE_DIR, ERROR_FILE_DIR, VISIT_FILE_DIR


class TestRetrieval(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.schema = 'Test'
        cls.HtmlFilepath = HTML_FILE_DIR.format(hospital=cls.schema)
        cls.ErrorFilepath = ERROR_FILE_DIR.format(hospital=cls.schema)
        cls.VisitFilepath = VISIT_FILE_DIR.format(hospital=cls.schema)

    @classmethod
    def tearDownClass(cls):
        filePaths = cls.HtmlFilepath, cls.ErrorFilepath, cls.VisitFilepath
        for filePath in filePaths:
            for _, _, files in os.walk(filePath):
                for fileName in files:
                    os.rename(filePath + "Processed\\" + fileName, filePath + fileName)

    def testRetrieveDatafromHtmlFiles(self):
        retrieveDatafromHtmlFiles(schema=self.schema)
        self.assertTrue(os.listdir(self.HtmlFilepath + "Processed\\"))
        self.assertFalse(os.listdir(self.HtmlFilepath + "Errored\\"))

    def testRetrieveDatafromErrorFiles(self):
        retrieveDatafromErrorFiles(schema=self.schema)
        self.assertTrue(os.listdir(self.ErrorFilepath + "Processed\\"))
        self.assertFalse(os.listdir(self.ErrorFilepath + "Errored\\"))

    def testRetrieveDatafromVisitFiles(self):
        retrieveDatafromVisitFiles(schema=self.schema)
        self.assertTrue(os.listdir(self.VisitFilepath + "Processed\\"))
        self.assertFalse(os.listdir(self.VisitFilepath + "Errored\\"))


if __name__ == '__main__':
    import xmlrunner
    runner = xmlrunner.XMLTestRunner(output='test-reports')
    unittest.main(testRunner=runner)