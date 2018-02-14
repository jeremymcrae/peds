
from peds.person import Person
from peds.family import Family

def open_ped(path):
    """ open a ped file and return a list of Family objects
    """
    
    # split file into lists of lines for each family, indexed by family ID
    fams = {}
    with open(path) as handle:
        sep = get_separator(handle)
        for line in handle:
            # ignore header and comment lines
            if line.startswith('family_id\t') or line.startswith('#'):
                continue
            
            fam_id = line.split('\t', 1)[0]
            if fam_id not in fams:
                fams[fam_id] = Family(fam_id)
            
            person = Person(*line.strip().split('\t'))
            if person in fams[fam_id]:
                raise ValueError('already family: {}'.format(person))
            
            fams[fam_id].add_person(person)
    
    return [ link_members(x) for x in list(fams.values()) ]

def get_separator(handle):
    """ get the column separator (assumes same on all lines)
    """
    current = handle.tell()
    line = handle.readline()
    handle.seek(current)
    
    if line.count('\t') > line.count(' '):
        return '\t'
    else:
        return ' '

def link_members(family):
    """ links family members, i.e. parents to children
    """
    
    # link parents to their children
    for person in family:
        # make placeholder parents, to match on family and individual IDs
        mom = Person(family.id, person.mom, 'NA', 'NA', 'NA', 'NA')
        dad = Person(family.id, person.dad, 'NA', 'NA', 'NA', 'NA')
        
        if mom.id != '0' and mom in family:
            family.set_mom(mom, person)
        
        if dad.id != '0' and dad in family:
            family.set_dad(dad, person)
    
    return family
