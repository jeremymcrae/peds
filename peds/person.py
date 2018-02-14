
class Person(object):
    
    male_codes = set(['1', 'm', 'M', 'male'])
    female_codes = set(['2', 'f', 'F', 'female'])
    unknown_codes = set(['0', 'NA', 'unknown', '.', '-9'])
    
    def __init__(self, family, id, dad, mom, sex, phenotype):
        
        self.family = family
        self.id = id
        self.mom = mom
        self.dad = dad
        self.sex = sex
        self.phenotype = phenotype
        
        if self.sex not in self.male_codes | self.female_codes | self.unknown_codes:
            raise ValueError('unknown sex code: {}'.format(self.sex))
        
        if self.phenotype not in set(['1', '2']) | self.unknown_codes:
            raise ValueError('unknown phenotype: {}'.format(self.phenotype))
    
    def __repr__(self):
        return 'Person(family="{}", person="{}", mom="{}", dad="{}", sex="{}", ' \
            'phenotype="{}")'.format(self.family, self.id, self.mom,
            self.dad, self.sex, self.phenotype)
    
    def __str__(self):
        return self.id
    
    def __hash__(self):
        return hash((self.family, self.id))
    
    def __eq__(self, other):
        return hash(self) == hash(other)
    
    def is_affected(self):
        return self.phenotype == "2"
    
    def is_male(self):
        return self.sex in self.male_codes
    
    def unknown_sex(self):
        return self.sex in self.unknown_codes
