import unittest
from app.models import Pitch

class PitchTest(unittest.TestCase):
    '''
    Test Class to test the behaviour of the pitch class
    '''

    def setUp(self):
        '''
        Set up method that will run before every Test
        '''
        self.new_pitch = Pitch(1,'Ransom','products','07/12/2022', 'product')

    def test_instance(self):
        self.assertTrue(isinstance(self.new_pitch,Pitch))
