from unittest import TestCase

from gkgaas.triplegeo.classification import Category


class TestClassification(TestCase):
    def test_str_serialization(self):
        target = \
            """
ACCOMMODATION #Z
  ALPINEHUT #23
  CAMPING #24
  CARAVAN #25
  CHALET #26
  GUESTHOUSE #27
  HOSTEL #28
  HOTEL #29
  MOTEL #30
            """.strip()

        test_category = Category(
            name='ACCOMMODATION',
            category_id='Z',
            sub_classes=[
                ('ALPINEHUT', '23'),
                ('CAMPING', '24'),
                ('CARAVAN', '25'),
                ('CHALET', '26'),
                ('GUESTHOUSE', '27'),
                ('HOSTEL', '28'),
                ('HOTEL', '29'),
                ('MOTEL', '30')])

        self.assertEqual(target, str(test_category))
