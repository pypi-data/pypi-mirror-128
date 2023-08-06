import datetime
from json import loads, JSONDecodeError
import re

from .net.http import ApiRequester
from .models.response import Response
from .exceptions.error import ParameterError, EmptyApiKeyError, \
    UnparsableApiResponseError


class Client:
    __default_url = "https://domains-subdomains-discovery.whoisxmlapi.com" \
                    "/api/v1"
    _api_requester: ApiRequester or None
    _api_key: str

    _re_api_key = re.compile(r'^at_[a-z0-9]{29}$', re.IGNORECASE)

    _PARSABLE_FORMAT = 'json'

    JSON_FORMAT = 'json'
    XML_FORMAT = 'xml'

    __DATETIME_OR_NONE_MSG = 'Value should be None or an instance of ' \
                             'datetime.date'

    def __init__(self, api_key: str, **kwargs):
        """
        :param api_key: str: Your API key.
        :key base_url: str: (optional) API endpoint URL.
        :key timeout: float: (optional) API call timeout in seconds
        """

        self._api_key = ''

        self.api_key = api_key

        if 'base_url' not in kwargs:
            kwargs['base_url'] = Client.__default_url

        self.api_requester = ApiRequester(**kwargs)

    @property
    def api_key(self) -> str:
        return self._api_key

    @api_key.setter
    def api_key(self, value: str):
        self._api_key = Client._validate_api_key(value)

    @property
    def api_requester(self) -> ApiRequester or None:
        return self._api_requester

    @api_requester.setter
    def api_requester(self, value: ApiRequester):
        self._api_requester = value

    @property
    def base_url(self) -> str:
        return self._api_requester.base_url

    @base_url.setter
    def base_url(self, value: str or None):
        if value is None:
            self._api_requester.base_url = Client.__default_url
        else:
            self._api_requester.base_url = value

    @property
    def timeout(self) -> float:
        return self._api_requester.timeout

    @timeout.setter
    def timeout(self, value: float):
        self._api_requester.timeout = value

    def get(self, **kwargs) -> Response:
        """
        Get parsed API response as a `Response` instance.

        :key domains: Required if domains aren't specified.
                Dictionary. Take a look at API documentation for the format
        :key subdomains: Required if domains aren't specified
                Dictionary. Take a look at API documentation for the format
        :key since_date: Optional. datetime.date. Min date by default.
        :return: `Response` instance
        :raises ConnectionError:
        :raises DomainDiscoveryApiError: Base class for all errors below
        :raises ResponseError: response contains an error message
        :raises ApiAuthError: Server returned 401, 402 or 403 HTTP code
        :raises BadRequestError: Server returned 400 or 422 HTTP code
        :raises HttpApiError: HTTP code >= 300 and not equal to above codes
        :raises ParameterError: invalid parameter's value
        """

        kwargs['output_format'] = Client._PARSABLE_FORMAT

        response = self.get_raw(**kwargs)

        try:
            parsed = loads(str(response))
            if 'domainsCount' in parsed:
                return Response(parsed)
            raise UnparsableApiResponseError(
                "Could not find the correct root element.", None)
        except JSONDecodeError as error:
            raise UnparsableApiResponseError(
                    "Could not parse API response",
                    error)

    def get_raw(self, **kwargs) -> str:
        """
        Get raw API response.

        :key domains: Required if subdomains aren't specified.
                Dictionary. Take a look at API documentation for the format
        :key subdomains: Required if domains aren't specified
                Dictionary. Take a look at API documentation for the format
        :key since_date: Optional. datetime.date. Min date by default.
        :key output_format: Optional. Use constants JSON_FORMAT and XML_FORMAT
        :return: str
        :raises ConnectionError:
        :raises DomainDiscoveryApiError: Base class for all errors below
        :raises ResponseError: response contains an error message
        :raises ApiAuthError: Server returned 401, 402 or 403 HTTP code
        :raises BadRequestError: Server returned 400 or 422 HTTP code
        :raises HttpApiError: HTTP code >= 300 and not equal to above codes
        :raises ParameterError: invalid parameter's value
        """

        if self.api_key == '':
            raise EmptyApiKeyError('')

        if 'domains' in kwargs:
            domains = Client._validate_domains(kwargs['domains'])
        else:
            domains = None

        if 'subdomains' in kwargs:
            subdomains = Client._validate_subdomains(kwargs['subdomains'])
        else:
            subdomains = None

        if not domains and not subdomains:
            raise ParameterError(
                "Required either domains or subdomains")

        if 'response_format' in kwargs:
            kwargs['output_format'] = kwargs['response_format']
        if 'output_format' in kwargs:
            output_format = Client._validate_output_format(
                kwargs['output_format'])
        else:
            output_format = Client._PARSABLE_FORMAT

        if 'since_date' in kwargs:
            since_date = Client._validate_date(kwargs['since_date'])
        else:
            since_date = Client._validate_date(datetime.date.min)

        return self._api_requester.post(self._build_payload(
            self.api_key,
            domains,
            subdomains,
            since_date,
            output_format
        ))

    @staticmethod
    def _build_payload(
            api_key,
            domains,
            subdomains,
            since_date,
            output_format,
    ) -> dict:
        tmp = {
            'apiKey': api_key,
            'domains': domains,
            'subdomains': subdomains,
            'sinceDate': since_date,
            'outputFormat': output_format,
        }

        payload = {}
        for k, v in tmp.items():
            if v is not None:
                payload[k] = v
        return payload

    @staticmethod
    def _validate_api_key(api_key) -> str:
        if Client._re_api_key.search(
                str(api_key)
        ) is not None:
            return str(api_key)
        else:
            raise ParameterError("Invalid API key format.")

    @staticmethod
    def _validate_date(value: datetime.date or None):
        if value is None or isinstance(value, datetime.date):
            return str(value)

        raise ParameterError(Client.__DATETIME_OR_NONE_MSG)

    @staticmethod
    def _validate_domains(value) -> dict:
        if value is None:
            raise ParameterError("Domain list cannot be None.")
        else:
            return Client._validate_terms(value)

    @staticmethod
    def _validate_output_format(value: str):
        if value.lower() in [Client.JSON_FORMAT, Client.XML_FORMAT]:
            return value.lower()

        raise ParameterError(
            f"Response format must be {Client.JSON_FORMAT} "
            f"or {Client.XML_FORMAT}")

    @staticmethod
    def _validate_subdomains(value) -> dict:
        if value is None:
            raise ParameterError("Subdomain list cannot be None.")
        else:
            return Client._validate_terms(value)

    @staticmethod
    def _validate_terms(value) -> dict:
        include, exclude = [], []
        if type(value) is dict:
            if 'include' in value:
                include = list(map(lambda s: str(s), value['include']))
                include = list(
                    filter(lambda s: s is not None and len(s) > 0, include))
                if 4 <= len(include) <= 1:
                    raise ParameterError("Include terms list must have "
                                         "from 1 to 4 terms.")
            if 'exclude' in value:
                exclude = list(map(lambda s: str(s), value['exclude']))
                exclude = list(
                    filter(lambda s: s is not None and len(s) > 0, exclude))
                if 4 <= len(exclude) <= 0:
                    raise ParameterError("Exclude terms list must have "
                                         "from 0 to 4 terms.")
            if include:
                return {'include': include, 'exclude': exclude}

        raise ParameterError("Expected a dict with 2 lists of strings.")
