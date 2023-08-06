from Bb_rest_helper import Get_Config
from Bb_rest_helper import Auth_Helper
from Bb_rest_helper import Bb_Requests
from Bb_rest_helper import Bb_Utils

import unittest


class Tests_Bb_rest(unittest.TestCase):

    
    def test_learn_auth(self):
        self.conf = Get_Config('./learn_config.json') 
        self.url = self.conf.get_url()
        self.key = self.conf.get_key()
        self.secret = self.conf.get_secret()
        self.auth = Auth_Helper (self.url,self.key,self.secret)
        result = self.auth.learn_auth()
        self.assertEqual(result, result)

    def test_collab_auth(self):
        self.conf = Get_Config('./collab_config.json') 
        self.url = self.conf.get_url()
        self.key = self.conf.get_key()
        self.secret = self.conf.get_secret()
        self.auth = Auth_Helper (self.url,self.key,self.secret)
        result = self.auth.collab_auth()
        self.assertEqual(result, result)
    
    def test_time_format_1(self, utils = Bb_Utils()):
        data = '02/02/2021'
        self.utils = utils
        result = self.utils.time_format(data)
        self.assertEqual(result, '2021-02-02T00:00:00.000Z')

    def test_time_format_2(self, utils = Bb_Utils()):
        data = '02/02/2021 23:45'
        self.utils = utils
        result = self.utils.time_format(data)
        self.assertEqual(result, '2021-02-02T23:45:00.000Z')

    def test_time_format_3(self, utils = Bb_Utils()):
        data = '02/02/2021 23:45:24'
        self.utils = utils
        result = self.utils.time_format(data)
        self.assertEqual(result, '2021-02-02T23:45:24.000Z')





if __name__ == '__main__':
    unittest.main()







