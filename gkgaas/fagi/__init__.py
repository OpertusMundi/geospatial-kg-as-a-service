from enum import Enum


class SerializationFormat(Enum):
    NT = 'NT'
    TTL = 'TTL'
    RDF_XML = 'RDF'
    JSON_LD = 'JSONLD'
    RDF_JSON = 'RJ'
    TRIG = 'TRIG'
    N_QUADS = 'NQ'
    TRIX = 'TRIX'

    def __str__(self):
        return self.value


class Locale(Enum):
    EN = 'EN'
    EN_GB = 'EN-GB'
    EN_US = 'EN-US'
    DE = 'DE'
    DE_DE = 'DE-DE'
    DE_AT = 'DE-AT'
    EL = 'EL'

    def __str__(self):
        return self.value


class Similarity(Enum):
    SORTED_JARO_WINKLER = 'sortedjarowinkler'
    JARO_WINKLER = 'jarowinkler'
    COSINE = 'cosine'
    JARO = 'jaro'
    LEVENSHTEIN = 'levenshtein'
    TWOGRAM = '2Gram'
    LONGEST_COMMON_SUB_SEQUENCE = 'longestcommonsubsequence'

    def __str__(self):
        return self.value


class StatsLevelOfDetail(Enum):
    LIGHT = 'light'
    DETAILED = 'detailed'

    def __str__(self):
        return self.value


class LinksFormat(Enum):
    NT = 'nt'
    CSV = 'csv'
    CSV_UNIQUE_LINKS = 'csv-unique-links'
    CSV_ENSEMBLES = 'csv-ensembles'

    def __str__(self):
        return self.value


class FusionMode(Enum):
    # Only linked triples are handled: Fused triples replace the respective ones
    # of dataset A (the fusion output is exclusively written to A)
    AA = 'aa_mode'

    # Only linked triples are handled: Fused triples replace the respective ones
    # of dataset B (the fusion output is exclusively written to B)
    BB = 'bb_mode'

    # All triples are handled: Fused triples replace the respective ones of
    # dataset A; un-linked triples of dataset B are copied as-is into dataset A
    AB = 'ab_mode'

    # All triples are handled: Fused triples replace the respective ones of
    # dataset B; un-linked triples of dataset A are copied as-is into dataset B
    BA = 'ba_mode'

    # All triples are handled: Fused triples replace the respective ones of
    # dataset A. Fused triples are removed from dataset B, which only maintains
    # the remaining, unlinked triples
    A = 'a_mode'

    # All triples are handled: Fused triples replace the respective ones of
    # dataset B. Fused triples are removed from dataset A, which only maintains
    # the remaining, unlinked triples.
    B = 'b_mode'

    # Only linked triples are handled: Only fused triples are written to a
    # third dataset.
    L = 'l_mode'

    def __str__(self):
        return self.value
