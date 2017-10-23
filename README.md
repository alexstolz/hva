# Hartmann von Aue-Portal as Linked Open Data

This project features a conversion tool that was used to generate the Linked Open Data deployment of the works by Hartmann von Aue. The official deployment is available at http://www.ebusiness-unibw.org/ontologies/hva/, whereas the original Hartmann von Aue-portal can be found at http://www.hva.uni-trier.de/.

The current tool is able to generate RDF data together with a human-readable documentation.

## Conversion

The converter expects a set of CSV files as input files. They need to be located in the folder data/csv/, but are currently not delivered with the source code repository.

The conversion starts with the following command:

> python3 hva.py

When finished, the conversion tool will have produced a set of RDF/N3 files together with a human-readable documentation in HTML.


---

Please cite this work as:

A. Stolz, M. Hepp, R. Boggs: **Linked Open Data for Linguists: Publishing the Hartmann von Aue-Portal in RDF**, in: Proceedings of the *16th International Conference on Ontologies, DataBases, and Applications of Semantics (ODBASE‘17)*, October 24-25, 2017, Rhodes, Greece.
