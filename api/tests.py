# Set the path
import os
import sys
import unittest
from api.app.tests import AppTest
from api.user.tests import UserTest
from api.bucketlist.tests import BucketlistTest


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


if __name__ == '__main__':
    unittest.main()
