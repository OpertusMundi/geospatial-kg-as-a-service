from unittest import TestCase

from gkgaas.triplegeo.mapping import MapProperties


class TestMapProperties(TestCase):
    def test_osm_shapefile_01(self):
        expected = \
            """
URI:
  entity: uri
  generateWith: getUUID(DATA_SOURCE,osm_id)
            """.strip()

        map_properties = MapProperties(
            name='URI',
            entity_type='uri',
            generator_function='getUUID',
            function_arguments=['DATA_SOURCE', 'osm_id'])

        self.assertEqual(expected, map_properties.to_yml_str().strip())

    def test_osm_shapefile_02(self):
        expected = \
            """
DATA_SOURCE:
  partOf: sourceInfo
  entity: source
  predicate: slipo:sourceRef
  generateWith: getDataSource
            """.strip()

        map_properties = MapProperties(
            name='DATA_SOURCE',
            part='sourceInfo',
            entity_type='source',
            predicate='slipo:sourceRef',
            generator_function='getDataSource'
        )

        self.assertEqual(expected, map_properties.to_yml_str().strip())

    def test_osm_shapefile_03(self):
        expected = \
            """
CATEGORY_URI:
  entity: category
  predicate: slipo:category
  datatype: uri
            """.strip()

        map_properties = MapProperties(
            name='CATEGORY_URI',
            entity_type='category',
            predicate='slipo:category',
            datatype='uri'
        )

        self.assertEqual(expected, map_properties.to_yml_str().strip())

    def test_osm_shapefile_04(self):
        expected = \
            """
ASSIGNED_CATEGORY:
  entity: assignedCategory
  predicate: slipo:assignedCategory
  generateWith: getEmbeddedCategory
            """.strip()

        map_properties = MapProperties(
            name='ASSIGNED_CATEGORY',
            entity_type='assignedCategory',
            predicate='slipo:assignedCategory',
            generator_function='getEmbeddedCategory'
        )

        self.assertEqual(expected, map_properties.to_yml_str().strip())

    def test_osm_shapefile_05(self):
        expected = \
            """
osm_id:
  partOf: sourceInfo
  entity: source
  predicate: slipo:poiRef
            """.strip()

        map_properties = MapProperties(
            name='osm_id',
            part='sourceInfo',
            entity_type='source',
            predicate='slipo:poiRef'
        )

        self.assertEqual(expected, map_properties.to_yml_str().strip())

    def test_osm_shapefile_06(self):
        expected = \
            """
last_update:
  entity: lastUpdated
  predicate: slipo:lastUpdated
  datatype: datetime
            """.strip()

        map_properties = MapProperties(
            name='last_update',
            entity_type='lastUpdated',
            predicate='slipo:lastUpdated',
            datatype='datetime'
        )

        self.assertEqual(expected, map_properties.to_yml_str().strip())

    def test_osm_shapefile_07(self):
        expected = \
            """
phone:
  instanceOf: contact
  entity: phone
  predicate: slipo:phone
  type: phone
            """.strip()

        map_properties = MapProperties(
            name='phone',
            instance='contact',
            entity_type='phone',
            predicate='slipo:phone',
            resource_type='phone'
        )

        self.assertEqual(expected, map_properties.to_yml_str().strip())

    def test_osm_shapefile_08(self):
        expected = \
            """
email:
  instanceOf: contact
  entity: email
  predicate: slipo:email
  type: email
            """.strip()

        map_properties = MapProperties(
            name='email',
            instance='contact',
            entity_type='email',
            predicate='slipo:email',
            resource_type='email'
        )

        self.assertEqual(expected, map_properties.to_yml_str().strip())

    def test_osm_shapefile_09(self):
        expected = \
            """
fax:
  instanceOf: contact
  entity: fax
  predicate: slipo:fax
  type: fax
            """.strip()

        map_properties = MapProperties(
            name='fax',
            instance='contact',
            entity_type='fax',
            predicate='slipo:fax',
            resource_type='fax'
        )

        self.assertEqual(expected, map_properties.to_yml_str().strip())

    def test_osm_shapefile_10(self):
        expected = \
            """
website:
  entity: homepage
  predicate: slipo:homepage
  datatype: string
            """.strip()

        map_properties = MapProperties(
            name='website',
            entity_type='homepage',
            predicate='slipo:homepage',
            datatype='string'
        )

        self.assertEqual(expected, map_properties.to_yml_str().strip())

    def test_osm_shapefile_11(self):
        expected = \
            """
wikipedia:
  entity: wikipedia
  predicate: slipo:otherLink
  datatype: string
            """.strip()

        map_properties = MapProperties(
            name='wikipedia',
            entity_type='wikipedia',
            predicate='slipo:otherLink',
            datatype='string'
        )

        self.assertEqual(expected, map_properties.to_yml_str().strip())

    def test_osm_shapefile_12(self):
        expected = \
            """
opening_hours:
  partOf: timeSlot
  entity: openingHours
  predicate: slipo:concat
            """.strip()

        map_properties = MapProperties(
            name='opening_hours',
            part='timeSlot',
            entity_type='openingHours',
            predicate='slipo:concat'
        )

        self.assertEqual(expected, map_properties.to_yml_str().strip())

    def test_osm_shapefile_13(self):
        expected = \
            """
name:
  instanceOf: name
  entity: name
  predicate: slipo:name
  type: official
            """.strip()

        map_properties = MapProperties(
            name='name',
            instance='name',
            entity_type='name',
            predicate='slipo:name',
            resource_type='official'
        )

        self.assertEqual(expected, map_properties.to_yml_str().strip())

    def test_osm_shapefile_14(self):
        expected = \
            """
name:
  instanceOf: name
  entity: name
  predicate: slipo:name
  type: official
            """.strip()

        map_properties = MapProperties(
            name='name',
            instance='name',
            entity_type='name',
            predicate='slipo:name',
            resource_type='official'
        )

        self.assertEqual(expected, map_properties.to_yml_str().strip())

    def test_osm_shapefile_15(self):
        expected = \
            """
TRANSLIT:
  instanceOf: name
  entity: translit_name
  predicate: slipo:name
  type: transliterated
  language: en
  generateWith: getTransliteration(name)
            """.strip()

        map_properties = MapProperties(
            name='TRANSLIT',
            instance='name',
            entity_type='translit_name',
            predicate='slipo:name',
            resource_type='transliterated',
            language='en',
            generator_function='getTransliteration',
            function_arguments=['name']
        )

        self.assertEqual(expected, map_properties.to_yml_str().strip())

    def test_osm_shapefile_16(self):
        expected = \
            """
name_%LANG:
  instanceOf: name
  entity: name
  predicate: slipo:name
  type: NONE
  language: getLanguage
            """.strip()

        map_properties = MapProperties(
            name='name_%LANG',
            instance='name',
            entity_type='name',
            predicate='slipo:name',
            resource_type='NONE',
            language='getLanguage'
        )

        self.assertEqual(expected, map_properties.to_yml_str().strip())

    def test_osm_shapefile_17(self):
        expected = \
            """
int_name:
  instanceOf: name
  entity: int_name
  predicate: slipo:name
  type: international
            """.strip()

        map_properties = MapProperties(
            name='int_name',
            instance='name',
            entity_type='int_name',
            predicate='slipo:name',
            resource_type='international'
        )

        self.assertEqual(expected, map_properties.to_yml_str().strip())

    def test_osm_shapefile_18(self):
        expected = \
            """
alt_name:
  instanceOf: name
  entity: alt_name
  predicate: slipo:name
  type: alternate
            """.strip()

        map_properties = MapProperties(
            name='alt_name',
            instance='name',
            entity_type='alt_name',
            predicate='slipo:name',
            resource_type='alternate'
        )

        self.assertEqual(expected, map_properties.to_yml_str().strip())

    def test_osm_shapefile_19(self):
        expected = \
            """
street:
  partOf: address
  entity: address
  predicate: slipo:street
            """.strip()

        map_properties = MapProperties(
            name='street',
            part='address',
            entity_type='address',
            predicate='slipo:street'
        )

        self.assertEqual(expected, map_properties.to_yml_str().strip())

    def test_osm_shapefile_20(self):
        expected = \
            """
housenumber:
  partOf: address
  entity: address
  predicate: slipo:number
            """.strip()

        map_properties = MapProperties(
            name='housenumber',
            part='address',
            entity_type='address',
            predicate='slipo:number'
        )

        self.assertEqual(expected, map_properties.to_yml_str().strip())

    def test_osm_shapefile_21(self):
        expected = \
            """
city:
  partOf: address
  entity: address
  predicate: slipo:locality
            """.strip()

        map_properties = MapProperties(
            name='city',
            part='address',
            entity_type='address',
            predicate='slipo:locality'
        )

        self.assertEqual(expected, map_properties.to_yml_str().strip())

    def test_osm_shapefile_22(self):
        expected = \
            """
country:
  partOf: address
  entity: address
  predicate: slipo:country
            """.strip()

        map_properties = MapProperties(
            name='country',
            part='address',
            entity_type='address',
            predicate='slipo:country'
        )

        self.assertEqual(expected, map_properties.to_yml_str().strip())

    def test_osm_shapefile_23(self):
        expected = \
            """
postcode:
  partOf: address
  entity: address
  predicate: slipo:postcode
            """.strip()

        map_properties = MapProperties(
            name='postcode',
            part='address',
            entity_type='address',
            predicate='slipo:postcode'
        )

        self.assertEqual(expected, map_properties.to_yml_str().strip())

    def test_osm_shapefile_24(self):
        expected = \
            """
image:
  partOf: media
  entity: media
  predicate: slipo:url
  type: image
  datatype: uri
            """.strip()

        map_properties = MapProperties(
            name='image',
            part='media',
            entity_type='media',
            predicate='slipo:url',
            resource_type='image',
            datatype='uri'
        )

        self.assertEqual(expected, map_properties.to_yml_str().strip())

    def test_osm_shapefile_25(self):
        expected = \
            """
description:
  entity: description
  predicate: slipo:description
            """.strip()

        map_properties = MapProperties(
            name='description',
            entity_type='description',
            predicate='slipo:description'
        )

        self.assertEqual(expected, map_properties.to_yml_str().strip())

    def test_osm_shapefile_26(self):
        expected = \
            """
LONGITUDE:
  entity: lon
  predicate: wgs84_pos:long
  datatype: float
  generateWith: geometry.getLongitude
            """.strip()

        map_properties = MapProperties(
            name='LONGITUDE',
            entity_type='lon',
            predicate='wgs84_pos:long',
            datatype='float',
            generator_function='geometry.getLongitude'
        )

        self.assertEqual(expected, map_properties.to_yml_str().strip())

    def test_osm_shapefile_27(self):
        expected = \
            """
LATITUDE:
  entity: lat
  predicate: wgs84_pos:lat
  datatype: float
  generateWith: geometry.getLatitude
            """.strip()

        map_properties = MapProperties(
            name='LATITUDE',
            entity_type='lat',
            predicate='wgs84_pos:lat',
            datatype='float',
            generator_function='geometry.getLatitude'
        )

        self.assertEqual(expected, map_properties.to_yml_str().strip())

    def test_osm_shapefile_28(self):
        expected = \
            """
AREA:
  entity: area
  predicate: slipo:area
  datatype: float
  generateWith: geometry.getArea
            """.strip()

        map_properties = MapProperties(
            name='AREA',
            entity_type='area',
            predicate='slipo:area',
            datatype='float',
            generator_function='geometry.getArea'
        )

        self.assertEqual(expected, map_properties.to_yml_str().strip())

    def test_osm_shapefile_29(self):
        expected = \
            """
LENGTH:
  entity: length
  predicate: slipo:length
  datatype: float
  generateWith: geometry.getLength
            """.strip()

        map_properties = MapProperties(
            name='LENGTH',
            entity_type='length',
            predicate='slipo:length',
            datatype='float',
            generator_function='geometry.getLength'
        )

        self.assertEqual(expected, map_properties.to_yml_str().strip())
