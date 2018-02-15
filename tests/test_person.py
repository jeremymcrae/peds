

import unittest

from peds import Person

class TestPerson(unittest.TestCase):
    """ test Person methods
    """
    
    def test_initialize_person(self):
        """ check Person() initializes correctly
        """
        
        i = Person('A', 'B', '0', '0', '1', '0')
        
        self.assertEqual(i.id, 'B')
        self.assertEqual(i.family, 'A')
        self.assertEqual(i.mom, '0')
        self.assertEqual(i.dad, '0')
    
    def test_initialize_person_data(self):
        """
        """
        
        i = Person('A', 'B', '0', '0', '1', '0')
        self.assertEqual(i.data, ())
        
        i = Person('A', 'B', '0', '0', '1', '0', 'PATH_TO_VCF')
        self.assertEqual(i.data, ('PATH_TO_VCF', ))
        
        i = Person('A', 'B', '0', '0', '1', '0', 'PATH_TO_VCF', 'SOMETHING_ELSE')
        self.assertEqual(i.data, ('PATH_TO_VCF', 'SOMETHING_ELSE'))
    
    def test_person_odd_sex(self):
        """ check that we can handle different sex codes
        """
        
        # go through all the possible male codes
        Person('A', 'B', '0', '0', '1', '0')
        Person('A', 'B', '0', '0', 'm', '0')
        Person('A', 'B', '0', '0', 'M', '0')
        Person('A', 'B', '0', '0', 'male', '0')
        
        # go through all the possible female codes
        Person('A', 'B', '0', '0', '2', '0')
        Person('A', 'B', '0', '0', 'f', '0')
        Person('A', 'B', '0', '0', 'F', '0')
        Person('A', 'B', '0', '0', 'female', '0')
        
        # go through all the possible unknown sex codes
        Person('A', 'B', '0', '0', '0', '0')
        Person('A', 'B', '0', '0', 'NA', '0')
        Person('A', 'B', '0', '0', 'unknown', '0')
        Person('A', 'B', '0', '0', '.', '0')
        Person('A', 'B', '0', '0', '-9', '0')
        
        with self.assertRaises(ValueError):
            Person('A', 'B', '0', '0', 'z', '0')
    
    def test_person_odd_phenotype(self):
        """ check that we can handle different phenotype codes
        """
        
        Person('A', 'B', '0', '0', '1', '1')
        Person('A', 'B', '0', '0', '1', '2')
        Person('A', 'B', '0', '0', '1', '0')
        Person('A', 'B', '0', '0', '1', 'NA')
        Person('A', 'B', '0', '0', '1', 'unknown')
        Person('A', 'B', '0', '0', '1', '-9')
        
        # raise an error for a nonstandard phenotype
        # TODO: allow for non-binary phenotypes!
        with self.assertRaises(ValueError):
            Person('A', 'B', '0', '0', '1', '5')
    
    def test_equality(self):
        """ check that we can compare two individuals
        """
        
        # two Persons with the same family ID and individual ID are equivalent
        a = Person('A', 'B', '0', '0', '1', '1')
        b = Person('A', 'B', '1', '1', '1', '1')
        self.assertEqual(a, b)
        
        # different individual IDs don't match
        c = Person('A', 'C', '1', '1', '1', '1')
        self.assertNotEqual(a, c)
        
        # different family IDs don't match
        d = Person('D', 'B', '1', '1', '1', '1')
        self.assertNotEqual(a, d)
    
    def test_is_affected(self):
        """ check that is_affected works correctly
        """
        
        a = Person('A', 'B', '0', '0', '1', '1')
        self.assertFalse(a.is_affected())
        
        a = Person('A', 'B', '0', '0', '1', '2')
        self.assertTrue(a.is_affected())
    
    def test_is_male(self):
        """ check that is_male works correctly
        """
        
        a = Person('A', 'B', '0', '0', '1', '1')
        self.assertTrue(a.is_male())
        
        a = Person('A', 'B', '0', '0', '2', '1')
        self.assertFalse(a.is_male())
        
        a = Person('A', 'B', '0', '0', '0', '1')
        self.assertFalse(a.is_male())
        self.assertTrue(a.unknown_sex())
    
