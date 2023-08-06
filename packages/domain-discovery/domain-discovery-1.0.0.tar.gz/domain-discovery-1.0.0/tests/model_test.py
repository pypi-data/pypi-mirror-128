import unittest
from json import loads
from domaindiscovery import Response, ErrorMessage


_json_response_ok_empty = '''{
   "domainsCount": 0,
   "domainsList": []
}'''

_json_response_ok = '''{
   "domainsCount": 2,
   "domainsList": [
        "aws.amazon.fr",
        "aws.amazon.org"
    ]
}'''

_json_response_error = '''{
    "code": 403,
    "messages": "Access restricted. Check credits balance or enter the correct API key."
}'''


class TestModel(unittest.TestCase):

    def test_response_parsing(self):
        response = loads(_json_response_ok)
        parsed = Response(response)
        self.assertEqual(parsed.domains_count, response['domainsCount'])
        self.assertIsInstance(parsed.domains_list, list)

        self.assertEqual(parsed.domains_list[0], response['domainsList'][0])

    def test_error_parsing(self):
        error = loads(_json_response_error)
        parsed_error = ErrorMessage(error)
        self.assertEqual(parsed_error.code, error['code'])
        self.assertEqual(parsed_error.message, error['messages'])
