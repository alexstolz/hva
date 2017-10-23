#!/usr/bin/env python3

import csv
import re
from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef
from rdflib.namespace import XSD, RDFS, OWL, FOAF, DC, DCTERMS
import urllib

import time

start_total = time.time()

BASE_URI = "http://www.ebusiness-unibw.org/ontologies/hva/"

HVA = Namespace(BASE_URI+"ontology#")
#LEXINFO = Namespace("http://www.lexinfo.net/ontology/2.0/lexinfo#")
#LEMON = Namespace("http://lemon-model.net/lemon#")
GOLD = Namespace("http://purl.org/linguistics/gold/")
NIF = Namespace("http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#")

def triple(g, subject, predicate, object, datatype=None, language=None):
    if None in [subject, predicate, object]:
        return
    elif type(object) == Literal:
        if object.title() == "":
            return
        if language != None:
            object.language = language
        elif datatype != None:
            object.datatype = datatype
    elif type(object) == URIRef:
        if object.title() == "":
            return
    elif type(object) == BNode:
        pass
    else:
        print ("Warning: triple({}, {}, {}) not created - object type neither Literal, BNode nor URIRef".format(subject, predicate, object))
        return
    g.add((subject, predicate, object))

def asciify_url(url, force_quote=False):
   # from https://blog.elsdoerfer.name/2008/12/12/opening-iris-in-python/
   r"""Attempts to make a unicode url usuable with ``urllib/urllib2``.

   More specifically, it attempts to convert the unicode object ``url``,
   which is meant to represent a IRI, to an unicode object that,
   containing only ASCII characters, is a valid URI. This involves:

       * IDNA/Puny-encoding the domain name.
       * UTF8-quoting the path and querystring parts.

   See also RFC 3987.
   """
   parts = urllib.parse.urlsplit(url)
   if not parts.scheme or not parts.netloc:
       # apparently not an url
       return url

   # idna-encode domain
   hostname = parts.hostname.encode('idna')

   # UTF8-quote the other parts. We check each part individually if
   # if needs to be quoted - that should catch some additional user
   # errors, say for example an umlaut in the username even though
   # the path *is* already quoted.
   def quote(s, safe):
       s = s or ''
       # Triggers on non-ascii characters - another option would be:
       #     urllib.quote(s.replace('%', '')) != s.replace('%', '')
       # which would trigger on all %-characters, e.g. "&".
       if s.encode('ascii', 'replace') != s or force_quote:
           return urllib.parse.quote(s.encode('utf8'), safe=safe)
       return s
   username = quote(parts.username, '')
   password = quote(parts.password, safe='')
   path = quote(parts.path, safe='/')
   query = quote(parts.query, safe='&=')

   # put everything back together
   netloc = hostname
   if username or password:
       netloc = '@' + netloc
       if password:
           netloc = ':' + password + netloc
       netloc = username + netloc
   if parts.port:
       netloc += ':' + str(parts.port)
   return urllib.parse.urlunsplit([parts.scheme, netloc.decode("utf-8"), path, query, parts.fragment])
    
#----------
# Ontology
#----------

start = time.time()
print("writing ontology")

g = Graph()

g.bind("owl", OWL)
g.bind("foaf", FOAF)
g.bind("hva", HVA)
g.bind("dc", DC)
g.bind("dcterms", DCTERMS)

triple(g, HVA.Ontology, RDF.type, OWL.Ontology)
triple(g, HVA.Ontology, RDFS.label, Literal("Hartmann von Aue Ontology", lang="en"))
triple(g, HVA.Ontology, RDFS.comment, Literal("This ontology re-models the database schema of the Hartmann von Aue Portal in order to make it available as Linked Open Data.", lang="en"))
triple(g, HVA.Ontology, DC.creator, Literal("Alex Stolz", datatype=XSD.string))
triple(g, HVA.Ontology, DC.title, Literal("Hartmann von Aue Ontology", lang="en"))
triple(g, HVA.Ontology, DCTERMS.contributor, Literal("Martin Hepp and Roy Boggs", datatype=XSD.string))
triple(g, HVA.Ontology, DCTERMS.license, URIRef("http://creativecommons.org/licenses/by/3.0/"))
triple(g, HVA.Ontology, OWL.versionInfo, Literal("v1.0, release 28-03-2017", datatype=XSD.string))
triple(g, HVA.Ontology, FOAF.page, URIRef("http://www.hva.uni-trier.de/"))

# Classes
triple(g, HVA.Verse, RDF.type, OWL.Class)
triple(g, HVA.Verse, RDFS.isDefinedBy, HVA.Ontology)
triple(g, HVA.Verse, RDFS.label, Literal("Verse", lang="en"))
triple(g, HVA.Verse, RDFS.comment, Literal("A verse is a single metrical line in a poetic composition. (Source: Wikipedia)", lang="en"))
triple(g, HVA.Word, RDF.type, OWL.Class)
triple(g, HVA.Word, RDFS.isDefinedBy, HVA.Ontology)
triple(g, HVA.Word, RDFS.label, Literal("Word", lang="en"))
triple(g, HVA.Word, RDFS.comment, Literal("In linguistics, a word is the smallest element that can be uttered in isolation with semantic and pragmatic content. (Source: Wikipedia)", lang="en"))
triple(g, HVA.Note, RDF.type, OWL.Class)
triple(g, HVA.Note, RDFS.isDefinedBy, HVA.Ontology)
triple(g, HVA.Note, RDFS.label, Literal("Note", lang="en"))
triple(g, HVA.Note, RDFS.comment, Literal("A note is a string of text placed at the bottom of a page in a book or document or at the end of a chapter, volume or the whole text. (Source: Wikipedia)", lang="en"))
triple(g, HVA.DictEntry, RDF.type, OWL.Class)
triple(g, HVA.DictEntry, RDFS.isDefinedBy, HVA.Ontology)
triple(g, HVA.DictEntry, RDFS.label, Literal("Dictionary Entry", lang="en"))
triple(g, HVA.DictEntry, RDFS.comment, Literal("A lexicon entry used to explain a concept.", lang="en"))
# Properties
# - object
triple(g, HVA.partOfVerse, RDF.type, OWL.ObjectProperty)
triple(g, HVA.partOfVerse, RDFS.domain, HVA.Word)
triple(g, HVA.partOfVerse, RDFS.range, HVA.Verse)
triple(g, HVA.partOfVerse, RDFS.isDefinedBy, HVA.Ontology)
triple(g, HVA.partOfVerse, RDFS.label, Literal("Part of Verse", lang="en"))
triple(g, HVA.partOfVerse, RDFS.comment, Literal("A property to indicate the parthood of a Word to a Verse.", lang="en"))
triple(g, HVA.note, RDF.type, OWL.ObjectProperty)
triple(g, HVA.note, RDFS.domain, HVA.Verse)
triple(g, HVA.note, RDFS.range, HVA.Note)
triple(g, HVA.note, RDFS.isDefinedBy, HVA.Ontology)
triple(g, HVA.note, RDFS.label, Literal("Attach Note to Verse", lang="en"))
triple(g, HVA.note, RDFS.comment, Literal("Property to attach a Note to a Verse.", lang="en"))
triple(g, HVA.entry, RDF.type, OWL.ObjectProperty)
triple(g, HVA.entry, RDFS.domain, HVA.Word)
triple(g, HVA.entry, RDFS.range, HVA.DictEntry)
triple(g, HVA.entry, RDFS.isDefinedBy, HVA.Ontology)
triple(g, HVA.entry, RDFS.label, Literal("Attach DictEntry to Word", lang="en"))
triple(g, HVA.entry, RDFS.comment, Literal("Property to attach a DictEntry to a Word.", lang="en"))
# - data type (tbd: domain and range)
triple(g, HVA.verseNumber, RDF.type, OWL.DatatypeProperty)
triple(g, HVA.verseNumber, RDFS.domain, HVA.Verse)
triple(g, HVA.verseNumber, RDFS.range, XSD.int)
triple(g, HVA.verseNumber, RDFS.isDefinedBy, HVA.Ontology)
triple(g, HVA.verseNumber, RDFS.label, Literal("Verse Number", lang="en"))
triple(g, HVA.verseNumber, RDFS.comment, Literal("Verse number of a verse in a poem.", lang="en"))
triple(g, HVA.lineInText, RDF.type, OWL.DatatypeProperty)
triple(g, HVA.lineInText, RDFS.domain, HVA.Verse)
triple(g, HVA.lineInText, RDFS.range, XSD.int)
triple(g, HVA.lineInText, RDFS.isDefinedBy, HVA.Ontology)
triple(g, HVA.lineInText, RDFS.label, Literal("Line in Text", lang="en"))
triple(g, HVA.lineInText, RDFS.comment, Literal("Line number of a verse in a poem (is not necessarily the same as the verse number).", lang="en"))
triple(g, HVA.positionInVerse, RDF.type, OWL.DatatypeProperty)
triple(g, HVA.positionInVerse, RDFS.domain, HVA.Word)
triple(g, HVA.positionInVerse, RDFS.range, XSD.int)
triple(g, HVA.positionInVerse, RDFS.isDefinedBy, HVA.Ontology)
triple(g, HVA.positionInVerse, RDFS.label, Literal("Position in Verse", lang="en"))
triple(g, HVA.positionInVerse, RDFS.comment, Literal("Position of the word in a verse.", lang="en"))
triple(g, HVA.text, RDF.type, OWL.DatatypeProperty)
triple(g, HVA.text, RDFS.domain, OWL.Thing)
triple(g, HVA.text, RDFS.range, RDFS.Literal)
triple(g, HVA.text, RDFS.isDefinedBy, HVA.Ontology)
triple(g, HVA.text, RDFS.label, Literal("Text", lang="en"))
triple(g, HVA.text, RDFS.comment, Literal("Textual description.", lang="en"))
triple(g, HVA.word, RDF.type, OWL.DatatypeProperty)
triple(g, HVA.word, RDFS.domain, OWL.Thing)
triple(g, HVA.word, RDFS.range, RDFS.Literal)
triple(g, HVA.word, RDFS.isDefinedBy, HVA.Ontology)
triple(g, HVA.word, RDFS.label, Literal("Word", lang="en"))
triple(g, HVA.word, RDFS.comment, Literal("Textual description of a word.", lang="en"))
triple(g, HVA.lemma, RDF.type, OWL.DatatypeProperty)
triple(g, HVA.lemma, RDFS.domain, OWL.Thing)
triple(g, HVA.lemma, RDFS.range, RDFS.Literal)
triple(g, HVA.lemma, RDFS.isDefinedBy, HVA.Ontology)
triple(g, HVA.lemma, RDFS.label, Literal("Lemma", lang="en"))
triple(g, HVA.lemma, RDFS.comment, Literal("Lemma of a word.", lang="en"))
triple(g, HVA.grammar, RDF.type, OWL.DatatypeProperty)
triple(g, HVA.grammar, RDFS.domain, OWL.Thing)
triple(g, HVA.grammar, RDFS.range, XSD.string)
triple(g, HVA.grammar, RDFS.isDefinedBy, HVA.Ontology)
triple(g, HVA.grammar, RDFS.label, Literal("Grammar", lang="en"))
triple(g, HVA.grammar, RDFS.comment, Literal("Grammar of a word.", lang="en"))
triple(g, HVA.translation, RDF.type, OWL.DatatypeProperty)
triple(g, HVA.translation, RDFS.domain, OWL.Thing)
triple(g, HVA.translation, RDFS.range, RDFS.Literal)
triple(g, HVA.translation, RDFS.isDefinedBy, HVA.Ontology)
triple(g, HVA.translation, RDFS.label, Literal("Translation", lang="en"))
triple(g, HVA.translation, RDFS.comment, Literal("Translation of a word or text into another language.", lang="en"))
triple(g, HVA.msA, RDF.type, OWL.DatatypeProperty)
triple(g, HVA.msA, RDFS.domain, HVA.Verse)
triple(g, HVA.msA, RDFS.range, XSD.string)
triple(g, HVA.msA, RDFS.isDefinedBy, HVA.Ontology)
triple(g, HVA.msA, RDFS.label, Literal("Manuscript A", lang="en"))
triple(g, HVA.msA, RDFS.comment, Literal("Manuscript identifier type A.", lang="en"))
triple(g, HVA.msB, RDF.type, OWL.DatatypeProperty)
triple(g, HVA.msB, RDFS.domain, HVA.Verse)
triple(g, HVA.msB, RDFS.range, XSD.string)
triple(g, HVA.msB, RDFS.isDefinedBy, HVA.Ontology)
triple(g, HVA.msB, RDFS.label, Literal("Manuscript B", lang="en"))
triple(g, HVA.msB, RDFS.comment, Literal("Manuscript identifier type B.", lang="en"))
triple(g, HVA.msBa, RDF.type, OWL.DatatypeProperty)
triple(g, HVA.msBa, RDFS.domain, HVA.Verse)
triple(g, HVA.msBa, RDFS.range, XSD.string)
triple(g, HVA.msBa, RDFS.isDefinedBy, HVA.Ontology)
triple(g, HVA.msBa, RDFS.label, Literal("Manuscript Ba", lang="en"))
triple(g, HVA.msBa, RDFS.comment, Literal("Manuscript identifier type Ba.", lang="en"))
triple(g, HVA.msBb, RDF.type, OWL.DatatypeProperty)
triple(g, HVA.msBb, RDFS.domain, HVA.Verse)
triple(g, HVA.msBb, RDFS.range, XSD.string)
triple(g, HVA.msBb, RDFS.isDefinedBy, HVA.Ontology)
triple(g, HVA.msBb, RDFS.label, Literal("Manuscript Bb", lang="en"))
triple(g, HVA.msBb, RDFS.comment, Literal("Manuscript identifier type Bb.", lang="en"))
triple(g, HVA.msC, RDF.type, OWL.DatatypeProperty)
triple(g, HVA.msC, RDFS.domain, HVA.Verse)
triple(g, HVA.msC, RDFS.range, XSD.string)
triple(g, HVA.msC, RDFS.isDefinedBy, HVA.Ontology)
triple(g, HVA.msC, RDFS.label, Literal("Manuscript C", lang="en"))
triple(g, HVA.msC, RDFS.comment, Literal("Manuscript identifier type C.", lang="en"))
triple(g, HVA.msD, RDF.type, OWL.DatatypeProperty)
triple(g, HVA.msD, RDFS.domain, HVA.Verse)
triple(g, HVA.msD, RDFS.range, XSD.string)
triple(g, HVA.msD, RDFS.isDefinedBy, HVA.Ontology)
triple(g, HVA.msD, RDFS.label, Literal("Manuscript D", lang="en"))
triple(g, HVA.msD, RDFS.comment, Literal("Manuscript identifier type D.", lang="en"))
triple(g, HVA.msE, RDF.type, OWL.DatatypeProperty)
triple(g, HVA.msE, RDFS.domain, HVA.Verse)
triple(g, HVA.msE, RDFS.range, XSD.string)
triple(g, HVA.msE, RDFS.isDefinedBy, HVA.Ontology)
triple(g, HVA.msE, RDFS.label, Literal("Manuscript E", lang="en"))
triple(g, HVA.msE, RDFS.comment, Literal("Manuscript identifier type E.", lang="en"))
triple(g, HVA.msF, RDF.type, OWL.DatatypeProperty)
triple(g, HVA.msF, RDFS.domain, HVA.Verse)
triple(g, HVA.msF, RDFS.range, XSD.string)
triple(g, HVA.msF, RDFS.isDefinedBy, HVA.Ontology)
triple(g, HVA.msF, RDFS.label, Literal("Manuscript F", lang="en"))
triple(g, HVA.msF, RDFS.comment, Literal("Manuscript identifier type F.", lang="en"))
triple(g, HVA.msFvS, RDF.type, OWL.DatatypeProperty)
triple(g, HVA.msFvS, RDFS.domain, HVA.Verse)
triple(g, HVA.msFvS, RDFS.range, XSD.string)
triple(g, HVA.msFvS, RDFS.isDefinedBy, HVA.Ontology)
triple(g, HVA.msFvS, RDFS.label, Literal("Manuscript FvS", lang="en"))
triple(g, HVA.msFvS, RDFS.comment, Literal("Manuscript identifier type FvS.", lang="en"))
triple(g, HVA.msG, RDF.type, OWL.DatatypeProperty)
triple(g, HVA.msG, RDFS.domain, HVA.Verse)
triple(g, HVA.msG, RDFS.range, XSD.string)
triple(g, HVA.msG, RDFS.isDefinedBy, HVA.Ontology)
triple(g, HVA.msG, RDFS.label, Literal("Manuscript G", lang="en"))
triple(g, HVA.msG, RDFS.comment, Literal("Manuscript identifier type G.", lang="en"))
triple(g, HVA.msK, RDF.type, OWL.DatatypeProperty)
triple(g, HVA.msK, RDFS.domain, HVA.Verse)
triple(g, HVA.msK, RDFS.range, XSD.string)
triple(g, HVA.msK, RDFS.isDefinedBy, HVA.Ontology)
triple(g, HVA.msK, RDFS.label, Literal("Manuscript K", lang="en"))
triple(g, HVA.msK, RDFS.comment, Literal("Manuscript identifier type K.", lang="en"))
triple(g, HVA.msV, RDF.type, OWL.DatatypeProperty)
triple(g, HVA.msV, RDFS.domain, HVA.Verse)
triple(g, HVA.msV, RDFS.range, XSD.string)
triple(g, HVA.msV, RDFS.isDefinedBy, HVA.Ontology)
triple(g, HVA.msV, RDFS.label, Literal("Manuscript V", lang="en"))
triple(g, HVA.msV, RDFS.comment, Literal("Manuscript identifier type V.", lang="en"))
triple(g, HVA.msW, RDF.type, OWL.DatatypeProperty)
triple(g, HVA.msW, RDFS.domain, HVA.Verse)
triple(g, HVA.msW, RDFS.range, XSD.string)
triple(g, HVA.msW, RDFS.isDefinedBy, HVA.Ontology)
triple(g, HVA.msW, RDFS.label, Literal("Manuscript W", lang="en"))
triple(g, HVA.msW, RDFS.comment, Literal("Manuscript identifier type W.", lang="en"))
triple(g, HVA.msZ, RDF.type, OWL.DatatypeProperty)
triple(g, HVA.msZ, RDFS.domain, HVA.Verse)
triple(g, HVA.msZ, RDFS.range, XSD.string)
triple(g, HVA.msZ, RDFS.isDefinedBy, HVA.Ontology)
triple(g, HVA.msZ, RDFS.label, Literal("Manuscript Z", lang="en"))
triple(g, HVA.msZ, RDFS.comment, Literal("Manuscript identifier type Z.", lang="en"))
triple(g, HVA.char, RDF.type, OWL.DatatypeProperty)
triple(g, HVA.char, RDFS.domain, HVA.DictEntry)
triple(g, HVA.char, RDFS.range, XSD.string)
triple(g, HVA.char, RDFS.isDefinedBy, HVA.Ontology)
triple(g, HVA.char, RDFS.label, Literal("Single character or letter", lang="en"))
triple(g, HVA.char, RDFS.comment, Literal("Single character (or letter) from an alphabet for indexing and sorting purposes.", lang="en"))

g.serialize(destination="rdf/ontology.n3", format="n3")
print ("execution time:", time.time()-start)


#----------
# Dataset
#----------

lexer_mapping = {}
with open("data/csv/HvALexerKeys.csv", "r") as csvfile:
    lexer_mapping = dict(csv.reader(csvfile))
    lexer_mapping =  {k.lower(): v for k, v in lexer_mapping.items()}

namespaces = {
    "ah": ("ah#", "Der arme Heinrich", "http://www.hva.uni-trier.de/kb_armer.php"),
    "er": ("er#", "Erec", "http://www.hva.uni-trier.de/kb_erec.php"),
    "gr": ("gr#", "Gregorius", "http://www.hva.uni-trier.de/kb_gregorius.php"),
    "iw": ("iw#", "Iwein", "http://www.hva.uni-trier.de/kb_iwein.php"),
    "kl": ("kl#", "Die Klage", "http://www.hva.uni-trier.de/kb_klage.php"),
    "ly": ("ly#", "Lyrik", "http://www.hva.uni-trier.de/kb_lyrics.php")
}

def gen_manuscript_link(g, namespace, folder, uri, ms):
    manuscript_search = re.search("([a-z]+)([0-9]*)([a-z]*)", ms, re.IGNORECASE)
    if manuscript_search:
        ms_prefix = manuscript_search.group(1)
        ms_id = manuscript_search.group(2)
        ms_postfix = manuscript_search.group(3)
        if ms_postfix and len(ms_postfix) > 1:
            ms_id = ms_id + ms_postfix[:-1]
        ms_uri_pdf = "http://hvauep.uni-trier.de/resources/{0}/manuscripts/{1}_{2}/{1}_{3}_{4}.pdf".format(folder, namespace.capitalize(), ms_prefix.capitalize(), ms_prefix, ms_id)
        triple(g, uri, FOAF.page, URIRef(ms_uri_pdf))
        ms_uri_img = "http://hvauep.uni-trier.de/resources/{0}/manuscripts/{1}_{2}/{1}_{3}_{4}".format(folder, namespace.capitalize(), ms_prefix.capitalize(), ms_prefix, ms_id) # omit file extension, because can be any of .jpg, .gif, maybe additional ones as well
        triple(g, uri, FOAF.img, URIRef(ms_uri_img))

def gen_kb_rdf(namespace, ubound=0):
    print("writing {} ({}) knowledge base".format(namespace, namespaces[namespace][1]))
    
    g = Graph()

    g.bind("owl", OWL)
    g.bind("foaf", FOAF)
    g.bind("hva", HVA)
    g.bind("dc", DC)
    g.bind("dcterms", DCTERMS)
    #g.bind("lemon", LEMON)
    #g.bind("lexinfo", LEXINFO)
    #g.bind("gold", GOLD)
    #g.bind("nif", NIF)
    
    BASE = Namespace(BASE_URI+namespaces[namespace][0])

    g.bind("data", BASE)

    triple(g, BASE.Ontology, RDF.type, OWL.Ontology)
    triple(g, BASE.Ontology, RDFS.label, Literal(namespaces[namespace][1], lang="de"))
    triple(g, BASE.Ontology, FOAF.page, URIRef(namespaces[namespace][2]))
    triple(g, BASE.Ontology, RDFS.comment, Literal(namespaces[namespace][1], lang="de"))
    triple(g, BASE.Ontology, DC.creator, Literal("Alex Stolz", datatype=XSD.string))
    triple(g, BASE.Ontology, DC.title, Literal(namespaces[namespace][1], lang="de"))
    triple(g, BASE.Ontology, DCTERMS.contributor, Literal("Martin Hepp and Roy Boggs", datatype=XSD.string))
    triple(g, BASE.Ontology, DCTERMS.license, URIRef("http://creativecommons.org/licenses/by/3.0/"))
    triple(g, BASE.Ontology, OWL.versionInfo, Literal("v1.0, release 28-03-2017", datatype=XSD.string))

    i = 0
    with open("data/csv/{0}DataSet.{0}Text.csv".format(namespace.capitalize()), "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            if i == 0:
                i += 1
                continue
            # AhTextNum,AhTextVerse,AhMSARef,AhMsBaRef,AhMsBbRef,AhMsCRef,AhMsDRef,AhMsERef,AhMsFRef,AhTextPos
            # ErTextNum,ErTextIndex,ErTextVerse,ErTextPos,ErTextMsA,ErTextMsK,ErTextMsV,ErTextMsW,ErTextMsFvS,ErTextMsZ
            # GrTextNumber,GrTextVerse,GrTextMsA,GrTextMsG
            # IwTextNumber,IwTextVerse,IwTextMsA,IwTextMsB,IwTextMsd
            # klTextNumber,klTextVerse,KlMsA
            # lyNum,lyText,lyMsA,lyMsB,lyMsC,lyMsE,lyMsm,lyMss,lyTextPos
            msA, msB, msBa, msBb, msC, msD, msE, msF, msFvS, msG, msK, msV, msW, msZ = [""]*14
            folder = ""
            if namespace == "ah":
                verse_num, text, msA, msBa, msBb, msC, msD, msE, msF, text_pos = row
                folder = "armer"
            elif namespace == "er":
                verse_num, _, text, text_pos, msA, msK, msV, msW, msFvS, msZ = row
                folder = "erec"
            elif namespace == "gr":
                verse_num, text, msA, msG = row
                text_pos = verse_num
                folder = "gregorius"
            elif namespace == "iw":
                verse_num, text, msA, msB, msD = row
                text_pos = verse_num
                folder = "iwein"
            elif namespace == "kl":
                verse_num, text, msA = row
                text_pos = verse_num
                folder = "klage"
            elif namespace == "ly":
                verse_num, text, msA, msB, msC, msE, msM, msS, text_pos = row
                folder = "lyrics"
                
            verse_num = verse_num.strip()
            text_pos = text_pos.strip()
            uri = BASE["Verse-{}".format(verse_num)]
            # Phrase subclassof LexicalEntry
            triple(g, uri, RDF.type, HVA.Verse)
            triple(g, uri, RDFS.isDefinedBy, BASE.Ontology)
            #triple(g, uri, RDF.type, LEMON.Phrase) # A phrase in lemon is defined in the looser sense of a sequence of words, it does not have to a fully grammatical phrase
            triple(g, uri, HVA.verseNumber, Literal(verse_num, datatype=XSD.int))
            triple(g, uri, HVA.lineInText, Literal(text_pos, datatype=XSD.int))
            triple(g, uri, HVA.text, Literal(text, lang="gmh"))
            triple(g, uri, RDFS.comment, Literal(text, lang="gmh"))
            if msA:
                triple(g, uri, HVA.msA, Literal(msA, datatype=XSD.string))
                gen_manuscript_link(g, namespace, folder, uri, msA)
            if msBa:
                triple(g, uri, HVA.msBa, Literal(msBa, datatype=XSD.string))
                gen_manuscript_link(g, namespace, folder, uri, msBa)
            if msBb:
                triple(g, uri, HVA.msBb, Literal(msBb, datatype=XSD.string))
                gen_manuscript_link(g, namespace, folder, uri, msBb)
            if msC:
                triple(g, uri, HVA.msC, Literal(msC, datatype=XSD.string))
                gen_manuscript_link(g, namespace, folder, uri, msC)
            if msD:
                triple(g, uri, HVA.msD, Literal(msD, datatype=XSD.string))
                gen_manuscript_link(g, namespace, folder, uri, msD)
            if msE:
                triple(g, uri, HVA.msE, Literal(msE, datatype=XSD.string))
                gen_manuscript_link(g, namespace, folder, uri, msE)
            if msF:
                triple(g, uri, HVA.msF, Literal(msF, datatype=XSD.string))
                gen_manuscript_link(g, namespace, folder, uri, msF)
            if msFvS:
                triple(g, uri, HVA.msFvS, Literal(msFvS, datatype=XSD.string))
                gen_manuscript_link(g, namespace, folder, uri, msFvS)
            if msG:
                triple(g, uri, HVA.msG, Literal(msG, datatype=XSD.string))
                gen_manuscript_link(g, namespace, folder, uri, msG)
            if msK:
                triple(g, uri, HVA.msK, Literal(msK, datatype=XSD.string))
                gen_manuscript_link(g, namespace, folder, uri, msK)
            if msV:
                triple(g, uri, HVA.msV, Literal(msV, datatype=XSD.string))
                gen_manuscript_link(g, namespace, folder, uri, msV)
            if msW:
                triple(g, uri, HVA.msW, Literal(msW, datatype=XSD.string))
                gen_manuscript_link(g, namespace, folder, uri, msW)
            if msZ:
                triple(g, uri, HVA.msZ, Literal(msZ, datatype=XSD.string))
                gen_manuscript_link(g, namespace, folder, uri, msZ)
            i += 1
            if ubound and i > ubound:
                break

    i = 0
    with open("data/csv/{0}DataSet.{0}Data.csv".format(namespace.capitalize()), "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            if i == 0:
                i += 1
                continue
            # AhDataNum,AhDataPos,AhDataWord,AhDataLemma,AhDataGrammar,AhDataGerman,AhDataEnglish
            # ErDataNum,ERDataIndex,ERDataPos,ErDataWord,ErDataLemma,ErDataGrammar,ErDataGerman,ErDataEnglish
            # GrDataNum,GrDataPos,GrDataWord,GrDataLemma,GrDataGrammar,GrDataGerman,GrDataEnglish
            # IwDataNum,IwDataPos,IwDataWord,IwDataLemma,IwDataGrammar,IwDataGerman,IwDataEnglish
            # KlDataNum,KlDataPos,KlDataWord,KlDataLemma,KlDataGrammar,KlDataGerman,KlDataEnglish
            # lyNum,lyPosition,lyWordform,lyLemma,lyGrammar,lyGerman,lyEnglish
            if namespace == "er":
                verse_num, _, word_pos, word, lemma, grammar, word_ger, word_eng = row
            else:
                verse_num, word_pos, word, lemma, grammar, word_ger, word_eng = row
            verse_num = verse_num.strip() # verse number
            word_pos = word_pos.strip()
            uri = BASE["Word-{}-{}".format(verse_num, word_pos)]
            uri_verse = BASE["Verse-{}".format(verse_num)]
            # Word subclassof LexicalEntry
            triple(g, uri, RDF.type, HVA.Word)
            triple(g, uri, RDFS.isDefinedBy, BASE.Ontology)
            #triple(g, uri, RDF.type, LEMON.Word) # A word is a single unit of writing or speech. In languages written in Latin, Cyrillic, Greek, Arabic scripts etc. these are assumed to be separated by white-space characters. For Chinese, Japanese, Korean this should correspond to some agreed segmentation scheme.
            #triple(g, uri, HVA.verseNumber, Literal(verse_num, datatype=XSD.int)) # not defined at word level
            triple(g, uri, HVA.positionInVerse, Literal(word_pos, datatype=XSD.int))
            triple(g, uri, HVA.word, Literal(word, lang="gmh")) # lang tag Mittelhochdeutsch ("gmh")
            triple(g, uri, HVA.lemma, Literal(lemma, lang="gmh"))
            triple(g, uri, RDFS.label, Literal(lemma, lang="gmh"))
            #triple(g, uri, NIF.lemma, Literal(lemma, lang="gmh"))
            triple(g, uri, HVA.grammar, Literal(grammar, datatype=XSD.string))
            triple(g, uri, HVA.translation, Literal(word_ger, lang="de"))
            triple(g, uri, RDFS.label, Literal(word_ger, lang="de"))
            triple(g, uri, HVA.translation, Literal(word_eng, lang="en"))
            triple(g, uri, RDFS.label, Literal(word_eng, lang="en"))
            triple(g, uri, HVA.partOfVerse, uri_verse)
            if lemma.lower() in lexer_mapping:
                triple(g, uri, FOAF.page, URIRef("http://woerterbuchnetz.de/Lexer/?lemid=" + lexer_mapping[lemma.lower()]))
            i += 1
            if ubound and i > ubound:
                break

    i = 0                                   
    with open("data/csv/{0}DataSet.{0}Notes.csv".format(namespace.capitalize()), "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            if i == 0:
                i += 1
                continue
            # AhNotesNum,AhNotesLemma,AhNotesGrammar,AhNotesNote
            # ErNotesNum,ErNotesIndex,ErNotesWord,ErNotesGrammar,ErNotesNote
            # GrNotesNum,GrNotesLemma,GrNotesGrammar,GrNotesNote
            # IwNotesNum,IwNotesLemma,IwNotesGrammar,IwNotesNote
            # KlNotesNum,KlNotesLemma,KlNotesGrammar,KLNotesNote
            # lyNum,lyWord,lyGrammar,LyNote
            if namespace == "er":
                verse_num, _, lemma, _, note = row
            else:
                verse_num, lemma, _, note = row
            verse_num = verse_num.strip()
            uri_verse = BASE["Verse-{}".format(verse_num)]
            text = Literal(note, lang="de")
            noteNode = BNode()
            triple(g, uri_verse, HVA.note, noteNode)
            triple(g, noteNode, RDF.type, HVA.Note)
            triple(g, noteNode, HVA.text, text)
            triple(g, noteNode, RDFS.comment, text)
            triple(g, noteNode, HVA.lemma, Literal(lemma, lang="gmh"))
            triple(g, noteNode, RDFS.label, Literal(lemma, lang="gmh"))
            i += 1
            if ubound and i > ubound:
                break
                
    g.serialize(destination="rdf/{}.n3".format(namespace), format="n3")
    
                
ubound = 0

for k in namespaces.keys():
    start = time.time()
    gen_kb_rdf(namespace=k, ubound=ubound)
    print("execution time:", time.time()-start)
    


#----------
# Dictionary
#----------

start = time.time()
print("writing dictionary")

DICT = Namespace(BASE_URI+"dict#")

g = Graph()

g.bind("owl", OWL)
g.bind("foaf", FOAF)
g.bind("hva", HVA)
g.bind("dict", DICT)
g.bind("dc", DC)
g.bind("dcterms", DCTERMS)
for k in namespaces.keys():
    g.bind("data{}".format(k), Namespace(namespaces[k][0]))
    
triple(g, DICT.Ontology, RDF.type, OWL.Ontology)
triple(g, DICT.Ontology, RDFS.label, Literal("Context Dictionary", lang="de"))
triple(g, DICT.Ontology, FOAF.page, URIRef("http://hvauep.uni-trier.de/dictionary.php?q=context"))
triple(g, DICT.Ontology, RDFS.comment, Literal("Context Dictionary of the Hartmann von Aue Portal.", lang="de"))
triple(g, DICT.Ontology, DC.creator, Literal("Alex Stolz", datatype=XSD.string))
triple(g, DICT.Ontology, DC.title, Literal("Context Dictionary", lang="de"))
triple(g, DICT.Ontology, DCTERMS.contributor, Literal("Martin Hepp and Roy Boggs", datatype=XSD.string))
triple(g, DICT.Ontology, DCTERMS.license, URIRef("http://creativecommons.org/licenses/by/3.0/"))
triple(g, DICT.Ontology, OWL.versionInfo, Literal("v1.0, release 28-03-2017", datatype=XSD.string))

i = 0
with open("data/csv/DictData.csv", "r") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    for row in reader:
        if i == 0:
            i += 1
            continue
        char, lemma, grammar, levels, special, german, english, verse, sortlemma, sortcode = row
        # h, e, g, i, k, l
        arr = [v.strip() for v in verse.split(",")]
        verses = []
        for v in arr:
            verse_search = re.search("([hegikl]\d{1,5})(.*)", v, re.IGNORECASE)
            if verse_search:
                verses.append([verse_search.group(1), verse_search.group(2).strip()])
            elif len(verses) > 0:
                verses[-1][1] = verses[-1][1] + ", " + v
        sortlemma = sortlemma.strip()
        levels = levels.strip()
        raw_lemma = sortlemma.replace(",", "").replace(" ", "-").replace("ô", "o")
        uri = URIRef(asciify_url(str(DICT["Lemma-{}".format(raw_lemma)]), force_quote=True))
        triple(g, uri, HVA.lemma, Literal(lemma, lang="gmh"))
        uri_entry = URIRef(asciify_url(str(DICT["Entry-{}-{}".format(raw_lemma, levels)]), force_quote=True))
        triple(g, uri, RDF.type, HVA.Word)
        triple(g, uri, RDFS.isDefinedBy, DICT.Ontology)
        triple(g, uri, HVA.entry, uri_entry)
        triple(g, uri_entry, RDF.type, HVA.DictEntry)
        triple(g, uri_entry, RDFS.isDefinedBy, DICT.Ontology)
        triple(g, uri_entry, HVA.char, Literal(char, datatype=XSD.string))
        triple(g, uri_entry, HVA.lemma, Literal(lemma, lang="gmh"))
        triple(g, uri_entry, RDFS.label, Literal(lemma, lang="gmh"))
        triple(g, uri_entry, HVA.grammar, Literal(grammar, datatype=XSD.string))
        triple(g, uri_entry, HVA.translation, Literal(german, lang="de"))
        triple(g, uri_entry, RDFS.label, Literal(german, lang="de"))
        triple(g, uri_entry, HVA.translation, Literal(english, lang="en"))
        triple(g, uri_entry, RDFS.label, Literal(english, lang="en"))
        #triple(g, uri_entry, HVA.text, Literal(verse, lang="gmh"))
        for vnum, v in verses:
            t = vnum[0] # first character
            num = vnum[1:]
            if t == "h":
                triple(g, uri, HVA.partOfVerse, URIRef(namespaces["ah"][0]+"Verse-{}".format(num)))
            elif t == "e":
                triple(g, uri, HVA.partOfVerse, URIRef(namespaces["er"][0]+"Verse-{}".format(num)))
            elif t == "g":
                triple(g, uri, HVA.partOfVerse, URIRef(namespaces["gr"][0]+"Verse-{}".format(num)))
            elif t == "i":
                triple(g, uri, HVA.partOfVerse, URIRef(namespaces["iw"][0]+"Verse-{}".format(num)))
            elif t == "k":
                triple(g, uri, HVA.partOfVerse, URIRef(namespaces["kl"][0]+"Verse-{}".format(num)))
            elif t == "l":
                triple(g, uri, HVA.partOfVerse, URIRef(namespaces["ly"][0]+"Verse-{}".format(num)))
            #triple(g, uri_entry, HVA.text, Literal(v, lang="gmh"))
        i += 1
        if ubound and i > ubound:
            break
        
    g.serialize(destination="rdf/dict.n3", format="n3")

print("execution time:", time.time()-start)

print("total execution time:", time.time()-start_total)