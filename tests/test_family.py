

import unittest

from peds import Family, Person

class TestFamily(unittest.TestCase):
    """ test creating a Family
    """
    
    def test_family_initialize(self):
        """ check Family() initializes correctly
        """
        
        fam = Family('A')
        
        self.assertEqual(fam.id, 'A')
        self.assertEqual(len(fam), 0)
    
    def test_get_parents(self):
        """ test that get_parents works correctly
        """
        
        fam = Family('A')
        child = Person('A', 'B', 'C', 'D', '1', '1')
        fam.add_person(child)
        
        # check when no parent available
        self.assertEqual(list(fam.get_parents(child)), [])
        
        mother = Person('A', 'D', '0', '0', '2', '1')
        father = Person('A', 'C', '0', '0', '1', '1')
        
        fam.add_person(mother)
        fam.add_person(father)
        fam.set_mom(mother, child)
        fam.set_dad(father, child)
        
        self.assertEqual(set(fam.get_parents(child)), set([mother, father]))
    
    def test_get_mother(self):
        """ test getting a mother
        """
        
        fam = Family('A')
        child = Person('A', 'B', '0', 'C', '1', '1')
        fam.add_person(child)
        
        # check when no parent available
        self.assertIsNone(fam.get_mother(child))
        
        mother = Person('A', 'C', '0', '0', '2', '1')
        fam.add_person(mother)
        fam.set_mom(mother, child)
        self.assertEqual(fam.get_mother(child), mother)
        
        # despite a mother being present, there is still not father
        self.assertIsNone(fam.get_father(child))
    
    def test_set_mother_placeholder(self):
        """ check the mother when set with a placeholder mother
        """
        
        fam = Family('A')
        child = Person('A', 'B', '0', 'C', '1', '1')
        mother = Person('A', 'C', '0', '0', '2', '1')
        placeholder = Person('A', 'C', 'NA', 'NA', 'NA', 'NA')
        fam.add_person(child)
        fam.add_person(mother)
        
        fam.set_mom(placeholder, child)
        
        # and check we can still pick up the parent.
        self.assertIsNotNone(fam.get_mother(child))
    
    def test_get_father(self):
        """ test getting a father
        """
        
        fam = Family('A')
        child = Person('A', 'B', 'C', '0', '1', '1')
        fam.add_person(child)
        
        # check when no parent available
        self.assertIsNone(fam.get_father(child))
        
        father = Person('A', 'C', '0', '0', '1', '1')
        fam.add_person(father)
        fam.set_dad(father, child)
        self.assertEqual(fam.get_father(child), father)
        
        # despite a father being present, there is still not mother
        self.assertIsNone(fam.get_mother(child))
    
    def test_set_father_placeholder(self):
        """ check the father when set with a placeholder father
        """
        
        fam = Family('A')
        child = Person('A', 'B', 'C', '0', '1', '1')
        father = Person('A', 'C', '0', '0', '1', '1')
        placeholder = Person('A', 'C', 'NA', 'NA', 'NA', 'NA')
        fam.add_person(child)
        fam.add_person(father)
        
        fam.set_dad(placeholder, child)
        
        # and check we can still pick up the parent.
        self.assertIsNotNone(fam.get_father(child))
    
    def test_get_children(self):
        """ test getting children
        """
        
        fam = Family('A')
        child1 = Person('A', 'B', 'C', '0', '1', '1')
        fam.add_person(child1)
        
        self.assertEqual(list(fam.get_children(child1)), [])
        
        father = Person('A', 'C', '0', '0', '1', '1')
        fam.add_person(father)
        fam.set_dad(father, child1)
        
        self.assertEqual(list(fam.get_children(father)), [child1])
        
        child2 = Person('A', 'D', 'C', '0', '1', '1')
        fam.add_person(child2)
        fam.set_dad(father, child2)
        self.assertEqual(set(fam.get_children(father)), set([child1, child2]))
    
    def test_add_person(self):
        """ test adding a person
        """
        fam = Family('A')
        person = Person('A', 'B', '0', '0', '1', '1')
        fam.add_person(person)
        self.assertTrue(person in fam)
        
        # check for an error if the family ID doesn't match
        person = Person('NOT_A', 'B', '0', '0', '1', '1')
        with self.assertRaises(ValueError):
            fam.add_person(person)
    
    def test_set_mom(self):
        """
        """
        
        fam = Family('A')
        child = Person('A', 'B', '0', 'C', '1', '1')
        mom = Person('A', 'C', '0', '0', '2', '1')
        fam.add_person(child)
        fam.add_person(mom)
        fam.set_mom(mom, child)
        self.assertEqual(fam.get_mother(child), mom)
        
        # make sure we can't add a second, different, mother
        mom2 = Person('A', 'D', '0', '0', '2', '1')
        fam.add_person(mom)
        with self.assertRaises(ValueError):
            fam.set_mom(mom2, child)
        
        # but we can set the original mother again
        fam.set_mom(mom, child)
    
    def test_set_mom_missing_members(self):
        """ test that if we link parent to child, both must be present
        """
        
        child = Person('A', 'B', '0', 'C', '1', '1')
        mom = Person('A', 'C', '0', '0', '2', '1')
        
        fam = Family('A')
        fam.add_person(child)
        
        # the mother must be in the family to set the parent
        with self.assertRaises(ValueError):
            fam.set_mom(mom, child)
        
        # the child must be in the family to set the parent
        fam = Family('A')
        fam.add_person(mom)
        with self.assertRaises(ValueError):
            fam.set_mom(mom, child)
    
    def test_set_mom_mismatching_id(self):
        """ if we set a mother, the mothers ID must be expected in child
        """
        fam = Family('A')
        child = Person('A', 'B', '0', 'D', '1', '1')
        mom = Person('A', 'C', '0', '0', '2', '1')
        
        fam.add_person(child)
        fam.add_person(mom)
        
        with self.assertRaises(ValueError):
            fam.set_mom(mom, child)
    
    def test_set_mom_male(self):
        """ check we raise an error if we try to add a male mother
        """
        fam = Family('A')
        child = Person('A', 'B', '0', 'C', '1', '1')
        mom = Person('A', 'C', '0', '0', '1', '1')
        fam.add_person(child)
        fam.add_person(mom)
        with self.assertRaises(ValueError):
            fam.set_mom(mom, child)
        
    def test_set_dad(self):
        """
        """
        
        fam = Family('A')
        child = Person('A', 'B', 'C', '0', '1', '1')
        dad = Person('A', 'C', '0', '0', '1', '1')
        fam.add_person(child)
        fam.add_person(dad)
        fam.set_dad(dad, child)
        self.assertEqual(fam.get_father(child), dad)
        
        # make sure we can't add a second, different, father
        dad2 = Person('A', 'D', '0', '0', '2', '1')
        fam.add_person(dad)
        with self.assertRaises(ValueError):
            fam.set_dad(dad2, child)
        
        # but we can set the original father again
        fam.set_dad(dad, child)
    
    def test_set_dad_missing_members(self):
        """ test that if we link parent to child, both must be present
        """
        
        child = Person('A', 'B', 'C', '0', '1', '1')
        dad = Person('A', 'C', '0', '0', '1', '1')
        
        fam = Family('A')
        fam.add_person(child)
        
        # the father must be in the family to set the parent
        with self.assertRaises(ValueError):
            fam.set_dad(dad, child)
        
        # the child must be in the family to set the parent
        fam = Family('A')
        fam.add_person(dad)
        with self.assertRaises(ValueError):
            fam.set_dad(dad, child)
    
    def test_set_dad_mismatching_id(self):
        """ if we set a father, the fathers ID must be expected in child
        """
        fam = Family('A')
        child = Person('A', 'B', 'D', '0', '1', '1')
        dad = Person('A', 'C', '0', '0', '1', '1')
        
        fam.add_person(child)
        fam.add_person(dad)
        
        with self.assertRaises(ValueError):
            fam.set_dad(dad, child)
    
    def test_set_dad_male(self):
        """ check we raise an error if we try to add a female father
        """
        fam = Family('A')
        child = Person('A', 'B', 'C', '0', '1', '1')
        dad = Person('A', 'C', '0', '0', '2', '1')
        fam.add_person(child)
        fam.add_person(dad)
        with self.assertRaises(ValueError):
            fam.set_dad(dad, child)
        
