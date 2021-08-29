  "css": {
    "relevantWords": [
      { "css2": "" },
      { "stylsheets": "" },
      { "stylesheets": "" },
      { "css code": "" },
      { "bootstrap responsive": "" },
      { "css 2": "" }
    ],
    "wikiLink": [
      "http://stackoverflow.com/tags/css/info",
      "http://en.wikipedia.org/wiki/CSS"
    ]
  }

    "cast": {
    "relevantWords": [
      { "casting": "" },
      { "typecast": "" },
      { "typecasted": "" },
      {
        "implicit conversions": "http://en.wikipedia.org/wiki/Implicit_conversion"
      },
      { "type casting": "" },
      { "boxing unboxing": "" }
    ],
    "wikiLink": []
  },

(u'name value pairs', {u'wikiLink': [], u'relevantWords': [{u'serlialized': u''}, {u'form encoding': u''}, {u'value pairs': u''}, {u'specifically formatted': u''}, {u'json esque': u''}, {u'key value': u'http://stackoverflow.com/tags/key-value/info'}]})
(u'name value pairs', {u'wikiLink': [], u'relevantWords': [{u'serlialized': u''}, {u'form encoding': u''}, {u'value pairs': u''}, {u'specifically formatted': u''}, {u'json esque': u''}, {u'key value': u'http://stackoverflow.com/tags/key-value/info'}]})
(u'mdbg', {u'wikiLink': [], u'relevantWords': [{u'redgate reflector': u''}, {u'psscor': u''}, {u'winddbg': u'http://stackoverflow.com/tags/windbg/info'}, {u'windbg cdb': u''}, {u'ollydebug': u'http://en.wikipedia.org/wiki/Ollydbg'}]})
(u'mdbg', {u'wikiLink': [], u'relevantWords': [{u'redgate reflector': u''}, {u'psscor': u''}, {u'winddbg': u'http://stackoverflow.com/tags/windbg/info'}, {u'windbg cdb': u''}, {u'ollydebug': u'http://en.wikipedia.org/wiki/Ollydbg'}]})

match(w:SEWord)-[:has_member]->(s:Synset) return w,s
match(w:SEWord) where w.term = 'css' return w
match(n) return n
match(n) delete n

MATCH (n) DETACH DELETE n

CREATE (w:SEWord {term: 'cast'})-[:has_synonym]->(s:Synset {name: 'Synset'})-[:has_member]->(w2:SEWord {term: 'typecast'})

match(w:SEWord)-[:has_synonym]-(s:s) where w.term = 'css' 

MATCH(s:Synset) where id(s) = 1 
MERGE 


CREATE(cast:SEWord {term: 'cast'})-[:has_synonym]->(cssSynset:Synset {name: "Synonym"})-[:has_member]->(typecast:SEWord {term:'typecast'})