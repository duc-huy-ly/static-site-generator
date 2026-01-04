import unittest

from main import extract_title

class TestExtractTitle(unittest.TestCase):
    def testNormalExtraction(self):
        md = "# Big name"
        extracted = extract_title(md)
        expected = "Big name"
        self.assertEqual(extracted, expected)
    
    def testWithSpaceInfrontOfHash(self):
        md = "      # Big name"
        extracted = extract_title(md)
        expected = "Big name"
        self.assertEqual(extracted, expected)
    
    def testWithLineReturnsFirst(self):
        md = "\n\n   # Header"
        self.assertEqual(extract_title(md), "Header")
    
    def testWithLineInBetween(self):
        md = "First Line\n\n # Header"
        self.assertEqual(extract_title(md), "Header")
        
    def testTitleGluedToHash(self):
        md = "#Header"
        self.assertEqual(extract_title(md), None)
    
    def testMultipleHashes(self):
        md = "## Header"
        self.assertEqual(extract_title(md), None)
    