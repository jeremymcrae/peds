
from peds import Family

def get_trios(family):
    """ get complete trios (child and parents) in a family
    
    Args:
        family: Family object (a graph with Persons as nodes)
    
    Returns:
        list of peds.Family objects, each for a unique trio
    """
    
    trios = []
    for x in family:
        mom = family.get_mother(x)
        dad = family.get_father(x)
        
        if mom is None or dad is None:
            continue
        
        trio = Family(x.family)
        trio.add_person(x)
        trio.add_person(mom)
        trio.add_person(dad)
        trio.set_mom(mom, x)
        trio.set_dad(dad, x)
        
        trios.append(trio)
    
    return trios

def get_probands(family):
    """ find probands within a Family
    
    Returns:
        list of probands (as peds.Person objects)
    """
    probands = []
    for x in family:
        # arbitrarily define probands as individuals who are affected, and do
        # not have any children in the family. This could be a bit looser,
        # to cope with multigenerational familes, but will do for now.
        if x.is_affected() and len(list(family.get_children(x))) == 0:
            probands.append(x)
    
    return probands
