
import networkx as nx

class Family(nx.DiGraph):
    """ this is mostly a wrapper around networkx's DiGraph class
    
    Family members are stored as nodes, and children are linked to their parents
    by edges. More distant relatives must be identified by traversing the graph
    via child -> parent -> grandparent etc.
    """
    
    def __init__(self, id):
        self.id = id
        
        # properly initialise the networkx DiGraph class
        super(Family, self).__init__()
    
    def __repr__(self):
        return 'Family({})'.format(self.id)
    
    def __gt__(self, other):
        return self.id > other.id
    
    def get_parents(self, person):
        return self.predecessors(person)
    
    def get_father(self, person):
        # return the male parent, or None if father not present
        for x in self.get_parents(person):
            if x.is_male():
                return x
    
    def get_mother(self, person):
        # return the female parent, or None if mother not present
        for x in self.get_parents(person):
            if not x.is_male() and not x.unknown_sex():
                return x
    
    def get_children(self, person):
        return self.successors(person)
    
    def add_person(self, person):
        if person.family != self.id:
            raise ValueError("{} didn't match family ID: {}".format(person.id,
                self.id))
        
        self.add_node(person)
    
    def set_mom(self, mom, child):
        self.add_edge(mom, child)
        # get the actual node for the mom, which contains the sex
        nodes = list(self.nodes)
        if nodes[nodes.index(mom)].is_male():
            raise ValueError("mom is not female: {}".format(mom.id))
    
    def set_dad(self, dad, child):
        self.add_edge(dad, child)
        # get the actual node for the dad, which contains the sex
        nodes = list(self.nodes)
        dad = nodes[nodes.index(dad)]
        if not (dad.is_male() or dad.unknown_sex()):
            raise ValueError("dad is not male: {}".format(dad.id))
    
    def get_proband(self):
        for x in self.nodes():
            if x.is_affected():
                return x
