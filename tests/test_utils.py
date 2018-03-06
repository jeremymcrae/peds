
import unittest

from peds import Family, Person, get_probands, get_trios

class TestUtils(unittest.TestCase):
    """ test loading a pedigree file
    """
    
    def test_get_probands(self):
        """ check get_probands works
        """
        
        fam = Family('A')
        child = Person('A', 'B', 'C', 'D', '1', '2')
        dad = Person('A', 'C', '0', '0', '1', '1')
        fam.add_person(child)
        fam.add_person(dad)
        fam.set_dad(dad, child)
        
        self.assertEqual(get_probands(fam), [child])
        
        # TODO: Add additional test cases.
    
    def test_get_probands_missing(self):
        """ check get_probands works for family wihtout affected proband
        """
        
        fam = Family('A')
        child = Person('A', 'B', 'C', 'D', '1', '1')
        dad = Person('A', 'C', '0', '0', '1', '1')
        fam.add_person(child)
        fam.add_person(dad)
        fam.set_dad(dad, child)
        
        self.assertEqual(get_probands(fam), [])
    
    def test_get_trios(self):
        """ check get_trios works
        """
        
        fam = Family('A')
        child = Person('A', 'B', 'C', 'D', '1', '2')
        dad = Person('A', 'C', '0', '0', '1', '1')
        mom = Person('A', 'D', '0', '0', '2', '1')
        fam.add_person(child)
        fam.add_person(dad)
        fam.add_person(mom)
        fam.set_dad(dad, child)
        fam.set_mom(mom, child)
        
        self.assertEqual(set(get_trios(fam)[0]), set([child, dad, mom]))
        
        # TODO: Add additional test cases.
