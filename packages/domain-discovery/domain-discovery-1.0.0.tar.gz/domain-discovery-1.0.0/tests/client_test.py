import datetime
import os
import unittest
from domaindiscovery import Client
from domaindiscovery import ParameterError, ApiAuthError


class TestClient(unittest.TestCase):
    """
    Final integration tests without mocks.

    Active API_KEY is required.
    """

    def setUp(self) -> None:
        self.client = Client(os.getenv('API_KEY'))
        self.correct_domains = {
            'include': ['example.com']
        }

        self.incorrect_domains = {
            'include': []
        }

    def test_get_correct_data(self):
        response = self.client.get(domains=self.correct_domains)
        self.assertIsNotNone(response.domains_count)

    def test_extra_parameters(self):
        response = self.client.get(
            domains=self.correct_domains,
            since_date=datetime.date.today() - datetime.timedelta(days=10)
        )
        self.assertIsNotNone(response.domains_count)

    def test_empty_terms(self):
        with self.assertRaises(ParameterError):
            self.client.get()

    def test_empty_api_key(self):
        with self.assertRaises(ParameterError):
            client = Client('')
            client.get(domains=self.correct_domains)

    def test_incorrect_api_key(self):
        client = Client('at_00000000000000000000000000000')
        with self.assertRaises(ApiAuthError):
            client.get(domains=self.correct_domains)

    def test_raw_data(self):
        response = self.client.get_raw(
            domains=self.correct_domains,
            output_format=Client.XML_FORMAT)
        self.assertTrue(response.startswith('<?xml'))

    def test_subdomains(self):
        response = self.client.get(
            subdomains=self.correct_domains
        )
        self.assertIsNotNone(response.domains_count)

    def test_incorrect_domains(self):
        with self.assertRaises(ParameterError):
            self.client.get(domains=self.incorrect_domains)

    def test_incorrect_subdomains(self):
        with self.assertRaises(ParameterError):
            self.client.get(subdomains=self.incorrect_domains)

    def test_incorrect_date(self):
        with self.assertRaises(ParameterError):
            self.client.get(domains=self.correct_domains,
                            since_date='19-19-19')

    def test_output(self):
        with self.assertRaises(ParameterError):
            self.client.get(domains=self.correct_domains,
                            response_format='yaml')


if __name__ == '__main__':
    unittest.main()
