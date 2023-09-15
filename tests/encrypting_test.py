import sys
sys.path.append("..")
from encrypting import *
import unittest
from pathlib import Path
import os

class TestClass(unittest.TestCase):
    def test_hash256(self):
        hash1 = hash256(b"car")
        hash2 = hash256(b"dog")
        self.assertNotEqual(hash1, hash2, msg="Same hash for two different strings")
        self.assertIsInstance(hash1, str, msg="hash function doesn't return type string")
    
    def test_kdf(self):
        kdf1 = kdf(b"test")
        kdf2 = kdf(b"test")
        kdf3 = kdf(b"testing")
        salt_path = Path(".salt")

        self.assertTrue(salt_path.exists(), msg=".salt was not created")
        os.remove(salt_path.resolve())

        self.assertEqual(kdf1, kdf2, msg="Same password didn't produce the same key")
        self.assertNotEqual(kdf1, kdf3, msg="Different password resulted in same key")