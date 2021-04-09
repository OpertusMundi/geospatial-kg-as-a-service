from gkgaas.limes.limesprofile import LIMESProfile, Prefix, LIMESSource, \
    DatasetType, LIMESTarget, LIMESAcceptanceCondition, LIMESReviewCondition, \
    LIMESExecution, LIMESEngine, LIMESPlanner, LIMESRewriter, LIMESOutputFormat

slipo_default_match = LIMESProfile(
    prefixes=[
        Prefix(
            namespace='http://slipo.eu/def#',
            label='slipo'),
        Prefix(
            namespace='http://www.w3.org/2002/07/owl#',
            label='owl'),
        Prefix(
            namespace='http://www.opengis.net/ont/geosparql#',
            label='geo'),
        Prefix(
            namespace='http://www.w3.org/2003/01/geo/wgs84_pos#',
            label='wgs84')],
    source=LIMESSource(
        id='a',
        var='?x',
        properties=[
            'geo:hasGeometry/geo:asWKT RENAME wkt',
            'slipo:name/slipo:nameValue AS nolang->lowercase RENAME label'],
        restrictions=[],  # TODO: check whether this will be set later
        page_size=-1,
        dataset_type=DatasetType.N_TRIPLES),
    target=LIMESTarget(
        id='b',
        var='?y',
        properties=[
            'geo:hasGeometry/geo:asWKT RENAME wkt',
            'slipo:name/slipo:nameValue AS nolang->lowercase RENAME label'],
        restrictions=[],  # TODO: check whether this is set later
        page_size=-1,
        dataset_type=DatasetType.N_TRIPLES),
    metric='AND (trigrams(x.label, y.label)|0.3, '
           'Geo_Hausdorff(x.wkt,y.wkt)|0.5)',
    acceptance_condition=LIMESAcceptanceCondition(
        file_path='accepted.csv',
        relation='owl:sameAs',
        threshold=0.50),
    review_condition=LIMESReviewCondition(
        file_path='review.csv',
        relation='owl:sameAs',
        threshold=0.30),
    execution=LIMESExecution(
        engine=LIMESEngine.DEFAULT,
        planner=LIMESPlanner.DEFAULT,
        rewriter=LIMESRewriter.DEFAULT),
    output_format=LIMESOutputFormat.TAB)


slipo_dinuc_a1 = LIMESProfile(
    execution=LIMESExecution(
        engine=LIMESEngine.DEFAULT,
        planner=LIMESPlanner.HELIOS,
        rewriter=LIMESRewriter.ALGEBRAIC),
    metric='\n\t\tAND(\n\t\t\tGeo_Mean(x.wkt,y.wkt)|0.975601,'
           '\n\t\t\tOR(\n\t\t\t\ttrigrams(x.label,y.label)|0.35,'
           '\n\t\t\t\tAND(\n\t\t\t\t\ttrigrams(x.label,y.label)|0.2,'
           '\n\t\t\t\t\texactmatch(x.category,y.category)|1.0\n\t\t\t\t)'
           '|0.1\n\t\t\t)|0.1\n\t\t)\n\t',
    prefixes=[
        Prefix(
            label='slipo',
            namespace='http://slipo.eu/def#'),
        Prefix(
            label='geo',
            namespace='http://www.opengis.net/ont/geosparql#'),
        Prefix(
            label='owl',
            namespace='http://www.w3.org/2002/07/owl#'),
        Prefix(
            label='wgs84',
            namespace='http://www.w3.org/2003/01/geo/wgs84_pos#')],
    review_condition=LIMESReviewCondition(
            file_path='review.csv',
            relation='owl:sameAs',
            threshold=0.1),
    acceptance_condition=LIMESAcceptanceCondition(
            file_path='accepted.csv',
            relation='owl:sameAS',
            threshold=0.2),
    source=LIMESSource(
        dataset_type=DatasetType.N_TRIPLES,
        id='a',
        page_size=-1,
        properties=[
            'geo:hasGeometry/geo:asWKT AS regexreplace('
            '&lt;http:\\/\\/www\\.opengis\\.net\\/def\\/crs(\\/.+)*&gt;, ) '
            'RENAME wkt',
            'slipo:name/slipo:nameValue AS nolang->lowercase RENAME label',
            'slipo:assignedCategory AS lowercase RENAME category'],
        restrictions=[
            '?w2 slipo:nameType ?t1. FILTER (regex(str(?t1), '
            '"transliterated"))'],
        var='?x'),
    target=LIMESTarget(
        dataset_type=DatasetType.N_TRIPLES,
        id='b',
        page_size=-1,
        properties=[
            'geo:hasGeometry/geo:asWKT AS regexreplace('
            '&lt;http:\\/\\/www\\.opengis\\.net\\/def\\/crs(\\/.+)*&gt;, ) '
            'RENAME wkt',
            'slipo:name/slipo:nameValue AS nolang->lowercase RENAME label',
            'slipo:assignedCategory AS lowercase RENAME category'],
        restrictions=[
            '?w2 slipo:nameType ?t1. FILTER (regex(str(?t1), '
            '"transliterated"))'],
        var='?y'),
    output_format=LIMESOutputFormat.TAB)

slipo_dinuc_a2 = LIMESProfile(
    execution=LIMESExecution(
        engine=LIMESEngine.DEFAULT,
        planner=LIMESPlanner.HELIOS,
        rewriter=LIMESRewriter.ALGEBRAIC),
    metric='\n\t\tAND(\n\t\t\tGeo_Mean(x.wkt,y.wkt)|0.966,'
           '\n\t\t\tOR(\n\t\t\t\ttrigrams(x.label,y.label)|0.5,'
           '\n\t\t\t\tAND(\n\t\t\t\t\ttrigrams(x.label,y.label)|0.2,'
           '\n\t\t\t\t\texactmatch(x.category,y.category)|1.0\n\t\t\t\t)|'
           '0.1\n\t\t\t)|0.1\n\t\t)\n\t',
    prefixes=[
        Prefix(
            label='slipo',
            namespace='http://slipo.eu/def#'),
        Prefix(
            label='geo',
            namespace='http://www.opengis.net/ont/geosparql#'),
        Prefix(
            label='owl',
            namespace='http://www.w3.org/2002/07/owl#'),
        Prefix(
            label='wgs84',
            namespace='http://www.w3.org/2003/01/geo/wgs84_pos#')
    ],
    review_condition=LIMESReviewCondition(
        file_path='review.csv',
        relation='owl:sameAs',
        threshold=0.1),
    acceptance_condition=LIMESAcceptanceCondition(
        file_path='accepted.csv',
        relation='owl:sameAS',
        threshold=0.2),
    source=LIMESSource(
        dataset_type=DatasetType.N_TRIPLES,
        id='a',
        page_size=-1,
        properties=[
            'geo:hasGeometry/geo:asWKT AS regexreplace('
            '&lt;http:\\/\\/www\\.opengis\\.net\\/def\\/crs(\\/.+)*&gt;, ) '
            'RENAME wkt',
            'slipo:name/slipo:nameValue AS nolang->lowercase RENAME label',
            # 'slipo:assignedCategory AS lowercase RENAME category'
        ],
        restrictions=[
            '?w2 slipo:nameType ?t1 . FILTER (regex(str(?t1), "translit"))'
        ],
        var='?x'),
    target=LIMESTarget(
        dataset_type=DatasetType.N_TRIPLES,
        id='b',
        page_size=-1,
        properties=[
            'geo:hasGeometry/geo:asWKT AS regexreplace('
            '&lt;http:\\/\\/www\\.opengis\\.net\\/def\\/crs(\\/.+)*&gt;, ) '
            'RENAME wkt',
            'slipo:name/slipo:nameValue AS nolang->lowercase RENAME label',
            # 'slipo:assignedCategory AS lowercase RENAME category'
        ],
        restrictions=[
            '?w2 slipo:nameType ?t1 . FILTER (regex(str(?t1), "translit"))'],
        var='?y'),
    output_format=LIMESOutputFormat.TAB)

slipo_dinuc_a3 = LIMESProfile(
    execution=LIMESExecution(
        engine=LIMESEngine.DEFAULT,
        planner=LIMESPlanner.HELIOS,
        rewriter=LIMESRewriter.ALGEBRAIC),
    metric='AND(Geo_Mean(x.wkt,y.wkt)|0.98, trigrams(x.label,y.label)|0.6)',
    prefixes=[
        Prefix(
            label='slipo',
            namespace='http://slipo.eu/def#'),
        Prefix(
            label='geo',
            namespace='http://www.opengis.net/ont/geosparql#'),
        Prefix(
            label='owl',
            namespace='http://www.w3.org/2002/07/owl#'),
        Prefix(
            label='wgs84',
            namespace='http://www.w3.org/2003/01/geo/wgs84_pos#')],
    review_condition=LIMESReviewCondition(
        file_path='review.csv',
        relation='owl:sameAs',
        threshold=0.1),
    acceptance_condition=LIMESAcceptanceCondition(
        file_path='accepted.csv',
        relation='owl:sameAS',
        threshold=0.2),
    source=LIMESSource(
        dataset_type=DatasetType.N_TRIPLES,
        id='a',
        page_size=-1,
        properties=[
            'geo:hasGeometry/geo:asWKT AS regexreplace('
            '&lt;http:\\/\\/www\\.opengis\\.net\\/def\\/crs(\\/.+)*&gt;, ) '
            'RENAME wkt',
            'slipo:name/slipo:nameValue AS nolang->lowercase RENAME label'],
        restrictions=[
            '?x slipo:name ?someName .'],
        var='?x'),
    target=LIMESTarget(
        dataset_type=DatasetType.N_TRIPLES,
        id='b',
        page_size=-1,
        properties=[
            'geo:hasGeometry/geo:asWKT AS regexreplace('
            '&lt;http:\\/\\/www\\.opengis\\.net\\/def\\/crs(\\/.+)*&gt;, ) '
            'RENAME wkt',
            'slipo:name/slipo:nameValue AS nolang->lowercase RENAME label',
            '?y slipo:name ?someName .'],
        var='?y'),
    output_format=LIMESOutputFormat.TAB)

slipo_dinuc_b1 = LIMESProfile(
    execution=LIMESExecution(
        engine=LIMESEngine.DEFAULT,
        planner=LIMESPlanner.HELIOS,
        rewriter=LIMESRewriter.ALGEBRAIC),
    metric='\n\t\tAND(\n\t\t\tGeo_Mean(x.wkt,y.wkt)|0.95,\n\t\t\tAND('
           '\n\t\t\t\ttrigrams(x.label,y.label)|0.2,\n\t\t\t\t'
           'ExactMatch(x.category, y.category)|0.5\n\t\t\t)|0.2\n\t\t)\n\t',
    prefixes=[
        Prefix(
            label='slipo',
            namespace='http://slipo.eu/def#'),
        Prefix(
            label='geo',
            namespace='http://www.opengis.net/ont/geosparql#'),
        Prefix(
            label='owl',
            namespace='http://www.w3.org/2002/07/owl#'),
        Prefix(
            label='wgs84',
            namespace='http://www.w3.org/2003/01/geo/wgs84_pos#')],
    review_condition=LIMESReviewCondition(
        file_path='review.csv',
        relation='owl:sameAs',
        threshold=0.1),
    acceptance_condition=LIMESAcceptanceCondition(
        file_path='accepted.csv',
        relation='owl:sameAS',
        threshold=0.2
    ),
    source=LIMESSource(
        dataset_type=DatasetType.N_TRIPLES,
        id='a',
        page_size=-1,
        properties=[
            'geo:hasGeometry/geo:asWKT AS regexreplace('
            '&lt;http:\\/\\/www\\.opengis\\.net\\/def\\/crs(\\/.+)*&gt;, ) '
            'RENAME wkt',
            'slipo:name/slipo:nameValue AS nolang->lowercase RENAME label',
            'slipo:assignedCategory AS lowercase RENAME category'],
        restrictions=[
            '?w2 slipo:nameType ?t1 . FILTER (regex(str(?t1), "translit"))'],
        var='?x'),
    target=LIMESTarget(
        dataset_type=DatasetType.N_TRIPLES,
        id='b',
        page_size=-1,
        properties=[
            'geo:hasGeometry/geo:asWKT AS regexreplace('
            '&lt;http:\\/\\/www\\.opengis\\.net\\/def\\/crs(\\/.+)*&gt;, ) '
            'RENAME wkt',
            'slipo:name/slipo:nameValue AS nolang->lowercase RENAME label',
            'slipo:assignedCategory AS lowercase RENAME category'],
        restrictions=[
            '?w2 slipo:nameType ?t1 . FILTER (regex(str(?t1), "translit"))'],
        var='?y'),
    output_format=LIMESOutputFormat.TAB)

slipo_dinuc_c1 = LIMESProfile(
    execution=LIMESExecution(
        engine=LIMESEngine.DEFAULT,
        planner=LIMESPlanner.HELIOS,
        rewriter=LIMESRewriter.ALGEBRAIC),
    metric='Geo_Mean(x.wkt,y.wkt)',
    prefixes=[
        Prefix(
            label='slipo',
            namespace='http://slipo.eu/def#'),
        Prefix(
            label='geo',
            namespace='http://www.opengis.net/ont/geosparql#'),
        Prefix(
            label='owl',
            namespace='http://www.w3.org/2002/07/owl#'),
        Prefix(
            label='wgs84',
            namespace='http://www.w3.org/2003/01/geo/wgs84_pos#')],
    review_condition=LIMESReviewCondition(
        file_path='review.csv',
        relation='owl:sameAs',
        threshold=0.8),
    acceptance_condition=LIMESAcceptanceCondition(
        file_path='accepted.csv',
        relation='owl:sameAS',
        threshold=0.8),
    source=LIMESSource(
        dataset_type=DatasetType.N_TRIPLES,
        id='a',
        page_size=-1,
        properties=[
            'geo:hasGeometry/geo:asWKT AS regexreplace('
            '&lt;http:\\/\\/www\\.opengis\\.net\\/def\\/crs(\\/.+)*&gt;, ) '
            'RENAME wkt'],
        restrictions=['?x geo:hasGeometry ?somegeo'],
        var='?x'),
    target=LIMESTarget(
        dataset_type=DatasetType.N_TRIPLES,
        id='b',
        page_size=-1,
        properties=[
            'geo:hasGeometry/geo:asWKT AS regexreplace('
            '&lt;http:\\/\\/www\\.opengis\\.net\\/def\\/crs(\\/.+)*&gt;, ) '
            'RENAME wkt'],
        restrictions=['?x geo:hasGeometry ?somegeo'],
        var='?y'),
    output_format=LIMESOutputFormat.TAB)

slipo_equi_match_by_name_and_distance = LIMESProfile(
    prefixes=[
        Prefix(
            namespace='http://slipo.eu/def#',
            label='slipo'),
        Prefix(
            namespace='http://www.w3.org/2002/07/owl#',
            label='owl'),
        Prefix(
            namespace='http://www.opengis.net/ont/geosparql#',
            label='geo'),
        Prefix(
            namespace='http://www.w3.org/2003/01/geo/wgs84_pos#',
            label='wgs84')],
    source=LIMESSource(
        id='a',
        var='?x',
        properties=[
            'geo:hasGeometry/geo:asWKT RENAME wkt',
            'slipo:name/slipo:nameValue AS nolang->lowercase RENAME label'],
        restrictions=[],
        page_size=-1,
        dataset_type=DatasetType.N_TRIPLES),
    target=LIMESTarget(
        id='b',
        var='?y',
        properties=[
            'wgs84:long RENAME long',
            'wgs84:lat RENAME lat',
            'geo:hasGeometry/geo:asWKT RENAME wkt',
            'slipo:name/slipo:nameValue AS nolang->lowercase RENAME label'],
        restrictions=[],
        page_size=-1,
        dataset_type=DatasetType.N_TRIPLES),
    metric='AND (trigrams(x.label, y.label)|0.8, '
           'Geo_Hausdorff(x.wkt,y.wkt)|0.8)',
    acceptance_condition=LIMESAcceptanceCondition(
        file_path='accepted.csv',
        relation='owl:sameAs',
        threshold=0.95),
    review_condition=LIMESReviewCondition(
        file_path='review.csv',
        relation='owl:sameAs',
        threshold=0.80),
    execution=LIMESExecution(
        engine=LIMESEngine.DEFAULT,
        planner=LIMESPlanner.DEFAULT,
        rewriter=LIMESRewriter.DEFAULT),
    output_format=LIMESOutputFormat.TAB)

slipo_match_by_geometry = LIMESProfile(
    execution=LIMESExecution(
        engine=LIMESEngine.DEFAULT,
        planner=LIMESPlanner.HELIOS,
        rewriter=LIMESRewriter.ALGEBRAIC),
    metric='Geo_Mean(x.wkt,y.wkt)',
    prefixes=[
        Prefix(
            label='slipo',
            namespace='http://slipo.eu/def#'),
        Prefix(
            label='geo',
            namespace='http://www.opengis.net/ont/geosparql#'),
        Prefix(
            label='owl',
            namespace='http://www.w3.org/2002/07/owl#'),
        Prefix(
            label='wgs84',
            namespace='http://www.w3.org/2003/01/geo/wgs84_pos#')],
    review_condition=LIMESReviewCondition(
        file_path='review.csv',
        relation='owl:sameAs',
        threshold=0.95),
    acceptance_condition=LIMESAcceptanceCondition(
        file_path='accepted.csv',
        relation='owl:sameAS',
        threshold=0.9995),
    source=LIMESSource(
        dataset_type=DatasetType.N_TRIPLES,
        id='a',
        page_size=-1,
        properties=[
            'geo:hasGeometry/geo:asWKT AS regexreplace('
            '&lt;http:\\/\\/www\\.opengis\\.net\\/def\\/crs(\\/.+)*&gt;, ) '
            'RENAME wkt'],
        restrictions=[],
        var='?x'),
    target=LIMESTarget(
        dataset_type=DatasetType.N_TRIPLES,
        id='b',
        page_size=-1,
        properties=[
            'geo:hasGeometry/geo:asWKT AS regexreplace('
            '&lt;http:\\/\\/www\\.opengis\\.net\\/def\\/crs(\\/.+)*&gt;, ) '
            'RENAME wkt'],
        restrictions=[],
        var='?y'),
    output_format=LIMESOutputFormat.TAB
)

slipo_match_by_name = LIMESProfile(
    prefixes=[
        Prefix(
            namespace='http://slipo.eu/def#',
            label='slipo'),
        Prefix(
            namespace='http://www.w3.org/2002/07/owl#',
            label='owl')],
    source=LIMESSource(
        id='a',
        var='?x',
        properties=['slipo:name/slipo:nameValue RENAME label'],
        restrictions=[],
        page_size=-1,
        dataset_type=DatasetType.N_TRIPLES),
    target=LIMESTarget(
        id='b',
        var='?y',
        properties=['slipo:name/slipo:nameValue RENAME label'],
        restrictions=[],
        page_size=-1,
        dataset_type=DatasetType.N_TRIPLES),
    metric='trigrams(x.label, y.label)',
    acceptance_condition=LIMESAcceptanceCondition(
        file_path='accepted.csv',
        relation='owl:sameAs',
        threshold=0.90),
    review_condition=LIMESReviewCondition(
        file_path='review.csv',
        relation='owl:sameAs',
        threshold=0.80),
    execution=LIMESExecution(
        engine=LIMESEngine.DEFAULT,
        planner=LIMESPlanner.DEFAULT,
        rewriter=LIMESRewriter.DEFAULT),
    output_format=LIMESOutputFormat.TAB)


slipo_osm_generic = LIMESProfile(
    prefixes=[
        Prefix(
            namespace='http://slipo.eu/def#',
            label='slipo'),
        Prefix(
            namespace='http://www.opengis.net/ont/geosparql#',
            label='geosparql'),
        Prefix(
            namespace='http://www.w3.org/2001/XMLSchema#',
            label='xsd'),
        Prefix(
            namespace='http://www.w3.org/1999/02/22-rdf-syntax-ns#',
            label='rdfs'),
        Prefix(
            namespace='http://www.w3.org/2003/01/geo/wgs84_pos#',
            label='wgs'),
        Prefix(
            label='owl',
            namespace='http://www.w3.org/2002/07/owl#'),
        Prefix(
            namespace='http://www.geonames.org/ontology#',
            label='geonames')],
    source=LIMESSource(
        id='a',
        var='?x',
        properties=[
            'slipo:name/slipo:nameValue RENAME label',
            'wgs:lat RENAME lat',
            'wgs:long RENAME long'],
        restrictions=['?x a geosparql:Feature'],
        page_size=-1,
        dataset_type=DatasetType.N_TRIPLES),
    target=LIMESTarget(
        id='b',
        var='?y',
        properties=[
            'geonames:name RENAME label',
            'geonames:alternateName RENAME label',
            'geonames:officialName RENAME label',
            'wgs:lat RENAME lat',
            'wgs:long RENAME long'],
        restrictions=['?y a geonames:Feature'],
        page_size=-1,
        dataset_type=DatasetType.N_TRIPLES),
    metric='AND ('
           'trigrams(x.label,y.label)|0.8,'
           'euclidean(x.lat|x.long, y.lat|y.long)|0.8)',
    # metric='euclidean(x.lat|long, y.lat|long)|0.8',
    acceptance_condition=LIMESAcceptanceCondition(
        file_path='accepted.csv',
        relation='owl:sameAs',
        threshold=0.90),
    review_condition=LIMESReviewCondition(
        file_path='review.csv',
        relation='owl:sameAs',
        threshold=0.80),
    execution=LIMESExecution(
        engine=LIMESEngine.DEFAULT,
        planner=LIMESPlanner.DEFAULT,
        rewriter=LIMESRewriter.DEFAULT),
    output_format=LIMESOutputFormat.TAB)
