from plutonkit.helper.template import convert_template
import unittest

RAW_TEMPLATE1 = """
({ 
    @content{
    from decouple import config
    from sqlalchemy import create_engine
     from sqlalchemy.orm import declarative_base,sessionmaker
    from urllib.parse import quote_plus
    }
})
{$See}
"""
class TestTemplate(unittest.TestCase):
    def test_convert_template_valid(self):
        TEST_RAW = """
from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker
from urllib.parse import quote_plus
1
"""     

        self.assertEqual(convert_template(RAW_TEMPLATE1,{"See":"1"}), TEST_RAW)
