
|Travis|

peds: basic pedigree parsing
----------------------------

All this does is parse [pedigree files](http://zzz.bwh.harvard.edu/plink/data.shtml#ped)
and group individuals within families. Only performs minimal validation.

Install
-------

.. code:: bash

    pip install peds

Usage
-----

.. code:: python

    from peds import open_ped

    families = open_ped(PATH)

    family = families[0]

    # find affected family members
    affected = [ x for x in family is x.is_affected()]

    # find parents
    for person in family:
        father = family.get_father(person)
        mother = family.get_mother(person)

.. |Travis| image:: https://travis-ci.org/jeremymcrae/peds.svg?branch=master
    :target: https://travis-ci.org/jeremymcrae/peds
