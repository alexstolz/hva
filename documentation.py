#!/usr/bin/env python3

from chameleon import PageTemplateFile

BASE = "http://www.ebusiness-unibw.org/ontologies/hva/"

namespaces = {
    "ontology": ("ontology#", "HvA Ontology", "ontology#"),
    "ah": ("ah#", "Der arme Heinrich", "http://www.hva.uni-trier.de/kb_armer.php"),
    "er": ("er#", "Erec", "http://www.hva.uni-trier.de/kb_erec.php"),
    "gr": ("gr#", "Gregorius", "http://www.hva.uni-trier.de/kb_gregorius.php"),
    "iw": ("iw#", "Iwein", "http://www.hva.uni-trier.de/kb_iwein.php"),
    "kl": ("kl#", "Die Klage", "http://www.hva.uni-trier.de/kb_klage.php"),
    "ly": ("ly#", "Lyrik", "http://www.hva.uni-trier.de/kb_lyrics.php"),
    "dict": ("dict#", "Context Dictionary", "dict#")
}

def gen_poem_docs(me, data=namespaces):
    template = PageTemplateFile("html/documentation.template.html")
    documentation = template(data=data, me=me, base=BASE)
    with open("html/generated/{}.html".format(me), "w+") as f:
        f.write(documentation)

for ns in namespaces.keys()-["ontology", "dict"]:
    gen_poem_docs(me=ns)

