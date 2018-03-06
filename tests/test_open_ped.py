
import shutil
import tempfile
import unittest

from peds import open_ped, Family, Person

class TestOpenPed(unittest.TestCase):
    """ test loading a pedigree file
    """
    
    @classmethod
    def setUpClass(cls):
        cls.tempdir = tempfile.mkdtemp()
    
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tempdir)
    
    def setUp(self):
        self.temp = tempfile.NamedTemporaryFile(dir=self.tempdir, delete=False,
            mode='wt')
    
    def test_open_ped(self):
        """ check open_ped works with a ped file with spaces
        """
        
        self.temp.write('A B 0 0 1 1\n')
        self.temp.flush()
        families = open_ped(self.temp.name)
        
        fam = Family('A')
        fam.add_person(Person('A', 'B', '0', '0', '1', '1'))
        
        self.assertEqual(families[0].nodes, fam.nodes)
    
    def test_open_ped_mismatch(self):
        """ check open_ped doesn't give match for different families
        """
        
        self.temp.write('A B 0 0 1 1\n')
        self.temp.flush()
        families = open_ped(self.temp.name)
        
        fam = Family('A')
        fam.add_person(Person('A', 'B', '0', '0', '1', '1'))
        fam.add_person(Person('A', 'C', '0', '0', '1', '1'))
        
        self.assertNotEqual(families[0].nodes, fam.nodes)
    
    def test_open_ped_tabs(self):
        """ check open_ped works when the file has tabs
        """
        
        self.temp.write('A\tB\t0\t0\t1\t1\n')
        self.temp.flush()
        families = open_ped(self.temp.name)
        
        fam = Family('A')
        fam.add_person(Person('A', 'B', '0', '0', '1', '1'))
        
        self.assertEqual(families[0].nodes, fam.nodes)
    
    def test_open_ped_header(self):
        """ check open_ped works when we have a header
        """
        
        self.temp.write('family_id person_id dad mom sex phenotype\n')
        self.temp.write('A B 0 0 1 1\n')
        self.temp.flush()
        families = open_ped(self.temp.name)
        
        fam = Family('A')
        fam.add_person(Person('A', 'B', '0', '0', '1', '1'))
        
        self.assertEqual(families[0].nodes, fam.nodes)
    
    def test_open_ped_comment_line(self):
        """ check open_ped works when we have a comment line
        """
        
        self.temp.write('A B 0 0 1 1\n')
        self.temp.write('#anything can go here\n')
        self.temp.flush()
        families = open_ped(self.temp.name)
        
        fam = Family('A')
        fam.add_person(Person('A', 'B', '0', '0', '1', '1'))
        
        self.assertEqual(families[0].nodes, fam.nodes)
    
    def test_open_ped_duplicate_person(self):
        """ check open_ped raises an error for duplicate people
        """
        
        self.temp.write('A B 0 0 1 1\n')
        self.temp.write('A B 0 0 1 1\n')
        self.temp.flush()
        
        with self.assertRaises(ValueError):
            open_ped(self.temp.name)
    
    def test_open_ped_with_parent(self):
        """ check open_ped correctly identifies parental relationships
        """
        
        self.temp.write('A B C 0 1 1\n')
        self.temp.write('A C 0 0 1 1\n')
        self.temp.flush()
        
        families = open_ped(self.temp.name)
        
        fam = Family('A')
        child = Person('A', 'B', 'C', '0', '1', '1')
        dad = Person('A', 'C', '0', '0', '1', '1')
        fam.add_person(child)
        fam.add_person(dad)
        fam.set_dad(dad, child)
        
        self.assertEqual(families[0].nodes, fam.nodes)
        self.assertEqual(families[0].edges, fam.edges)
    
    def test_open_ped_multigenerational(self):
        """ test that open_ped works with multigenerational families
        """
        
        self.temp.write('A B C D 1 1\n')
        self.temp.write('A C E F 1 1\n')
        self.temp.write('A D G H 2 1\n')
        self.temp.write('A E 0 0 1 1\n')
        self.temp.write('A F 0 0 2 1\n')
        self.temp.write('A G 0 0 1 1\n')
        self.temp.write('A H 0 0 2 1\n')
        self.temp.flush()
        
        families = open_ped(self.temp.name)
        
        fam = Family('A')
        child = Person('A', 'B', 'C', 'D', '1', '1')
        dad = Person('A', 'C', 'E', 'F', '1', '1')
        mom = Person('A', 'D', 'G', 'H', '2', '1')
        pat_gnddad = Person('A', 'E', '0', '0', '1', '1')
        pat_gndmom = Person('A', 'F', '0', '0', 'F', '1')
        mat_gnddad = Person('A', 'G', '0', '0', '1', '1')
        mat_gndmom = Person('A', 'H', '0', '0', 'F', '1')
        for x in [child, dad, mom, pat_gnddad, pat_gndmom, mat_gnddad, mat_gndmom]:
            fam.add_person(x)
        
        # and define relationships
        fam.set_dad(dad, child)
        fam.set_mom(mom, child)
        fam.set_dad(pat_gnddad, dad)
        fam.set_mom(pat_gndmom, dad)
        fam.set_dad(mat_gnddad, mom)
        fam.set_mom(mat_gndmom, mom)
        
        self.assertEqual(families[0].nodes, fam.nodes)
        self.assertEqual(families[0].edges, fam.edges)
    
    def test_open_ped_multifamily(self):
        """ test that open_ped works with multiple families
        """
        
        self.temp.write('A B 0 0 1 1\n')
        self.temp.write('C D 0 0 1 1\n')
        self.temp.flush()
        
        families = open_ped(self.temp.name)
        
        fam1 = Family('A')
        fam1.add_person(Person('A', 'B', '0', '0', '1', '1'))
        fam2 = Family('C')
        fam2.add_person(Person('C', 'D', '0', '0', '1', '1'))
        
        expected = [fam1, fam2]
        
        # the
        self.assertEqual(len(families), len(expected))
        
        for a, b in zip(sorted(families), sorted(expected)):
            self.assertEqual(a.nodes, b.nodes)
            self.assertEqual(a.edges, b.edges)
    
    def test_open_ped_partial_parents(self):
        """ test that open_ped identifies sibs, even when parents aren't present
        """
        
        # define a ped file where the parents are referred to only within the
        # child lines. We have to spot siblings from these.
        self.temp.write('A B C D 1 1\n')
        self.temp.write('A E C D 1 1\n')
        self.temp.flush()
        
        families = open_ped(self.temp.name)
        
        child1 = Person('A', 'B', 'C', 'D', '1', '1')
        child2 = Person('A', 'E', 'C', 'D', '1', '1')
        dad = Person('A', 'C', 'NA', 'NA', 'NA', 'NA')
        mom = Person('A', 'D', 'NA', 'NA', 'NA', 'NA')
        fam = Family('A')
        fam.add_person(child1)
        fam.add_person(child2)
        fam.add_person(mom)
        fam.add_person(dad)
        
        fam.set_mom(mom, child1)
        fam.set_mom(mom, child2)
        fam.set_dad(dad, child1)
        fam.set_dad(dad, child2)
        
        self.assertEqual(families[0].nodes, fam.nodes)
        self.assertEqual(families[0].edges, fam.edges)
