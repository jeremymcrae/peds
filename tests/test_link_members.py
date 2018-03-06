
import unittest

from peds import Family, Person
from peds.ped import link_members

class TestLinkMembers(unittest.TestCase):
    """ test linking family members
    """
    
    def test_link_members(self):
        """ test that link_members works correctly
        """
        
        child1 = Person('A', 'B', 'C', 'D', '1', '1')
        child2 = Person('A', 'E', 'C', 'D', '1', '1')
        fam = Family('A')
        fam.add_person(child1)
        fam.add_person(child2)
        
        fam = link_members(fam)
        
        dad = Person('A', 'C', 'NA', 'NA', 'NA', 'NA')
        mom = Person('A', 'D', 'NA', 'NA', 'NA', 'NA')
        expected = Family('A')
        expected.add_person(child1)
        expected.add_person(child2)
        expected.add_person(mom)
        expected.add_person(dad)
        
        expected.set_mom(mom, child1)
        expected.set_mom(mom, child2)
        expected.set_dad(dad, child1)
        expected.set_dad(dad, child2)
        
        self.assertEqual(expected.nodes, fam.nodes)
        self.assertEqual(expected.edges, fam.edges)
    
    def test_link_members_inferred(self):
        """ test that link_members works with parents from child lines
        """
        
        child1 = Person('A', 'B', 'C', 'D', '1', '1')
        child2 = Person('A', 'E', 'C', 'D', '1', '1')
        fam = Family('A')
        fam.add_person(child1)
        fam.add_person(child2)
        
        fam = link_members(fam)
        
        # getting a list or iterator of family members doesn't include parents
        # only described in child lines
        self.assertEqual(list(fam), [child1, child2])
        
        # still identify parents, even though we don't iterate through them
        self.assertEqual(fam.get_mother(child1), Person('A', 'D', 'NA', 'NA', 'female', 'NA'))
        self.assertEqual(fam.get_father(child1), Person('A', 'C', 'NA', 'NA', 'male', 'NA'))
        self.assertEqual(fam.get_mother(child2), Person('A', 'D', 'NA', 'NA', 'female', 'NA'))
        self.assertEqual(fam.get_father(child2), Person('A', 'C', 'NA', 'NA', 'male', 'NA'))
