from pipeline import *

class SentenceLimiter:
    """
    Limit the text, word boundaries and 
    sentence boundaries of a given document
    to the number of sentences given
    Important: number_sentences starts with 0 for the fist sentence
    """
    def run(self, document, number_sentences):
        boundaries = (document.sentences_boundaries[0][0], document.sentences_boundaries[:number_sentences+1][-1][1])
        document.text = document.text[boundaries[0]:boundaries[1]]
        document.sentences_boundaries = self.limitSenteceBoundaries(document.sentences_boundaries, boundaries[1])
        document.words_boundaries = self.limitWordBoundaries(document.words_boundaries, boundaries[1]) 
        document.entities = self.limitEntities(document.entities, boundaries[1])
        document.triples = self.limitTriples(document.triples, boundaries[1])
        return document

    def limitSenteceBoundaries(self, sentences_boundaries, maxi):
        sentences_boundaries_new = []
        for sent in sentences_boundaries:
            if sent[1] <= maxi:
                sentences_boundaries_new.append(sent) 
        return sentences_boundaries_new

    def limitEntities(self, entities, maxi):
        entities_new = []
        for e in entities:
            if e.boundaries[1] <= maxi:
                entities_new.append(e)
        return entities_new

    def limitTriples(self, triples, maxi):
        triples_new = []
        for t in triples:
            if t.sentence_id == 0:
                triples_new.append(t)
        return triples_new

    def limitWordBoundaries(self, words_boundaries, maxi):
        words_boundaries_new = []
        for word in words_boundaries:
            if word[1] <= maxi:
                words_boundaries_new.append(word) 
        return words_boundaries_new

class MainEntityLimiter:
    """
    Remove a document's content if the main entity is not aligned
    """
    def run(self, document):
        if not document.docid in [i.uri for i in document.entities]:
            document = None
        return document

class RemoveDisambiguationPagesLimiter:
    """
    Remove all entites that are disambiguation pages
    """
    def __init__(self, all_triples):
        """
        :param: input document containing the triples (two entities and
        the property that bind them together)
        """
        self.wikidata_triples = all_triples

    def run(self, document):
        # P31: instance of
        prop_id = 'http://www.wikidata.org/prop/direct/P31'
        # Q4167410: Wikimedia disambiguation page
        dis_id = 'http://www.wikidata.org/entity/Q4167410'
        if any([i for i in self.wikidata_triples.get(document.docid) if i[1] == prop_id and i[2] == dis_id ]):
            document = None
        return document
