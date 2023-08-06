import logging

from datetime import datetime, timezone
import hmac
import time
import json
import hashlib
import websupportsk.exceptions
import requests

# logging.basicConfig()
# logging.getLogger('urllib3').setLevel(logging.WARNING)
logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)


class Client:
    """API client that handles connection with Websupport REST API"""

    def __init__(self, identifier, secret_key, domain):
        """Constructor for WebsupportClient.

        Args:
            identifier (string): Account API identifier
            secret_key (string): Account API secret key
            domain: (string): domain you want to manage, i.e. example.com

        Raises:
            websupportsk.exceptions.WebsupportAuthenticationError: If authentication failed.
            websupportsk.exceptions.WebsupportZoneNotFound: If domain specified was not found inside user account.
            websupportsk.exceptions.WebsupportConnectionError: If connection failed, i.e. no internet access,
                DNS resolution issue,...
        """

        self.api = "https://rest.websupport.sk"
        self.default_path = "/v1/user/self"
        self.query = ""  # query part is optional and may be empty
        self.domain = domain

        # creating signature
        method = "GET"
        timestamp = int(time.time())
        canonical_request = "%s %s %s" % (method, self.default_path, timestamp)
        signature = hmac.new(bytes(secret_key, 'UTF-8'), bytes(canonical_request, 'UTF-8'), hashlib.sha1).hexdigest()

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Date": datetime.fromtimestamp(timestamp, timezone.utc).isoformat()
        }

        # creating session
        self.session = requests.Session()
        self.session.auth = (identifier, signature)
        self.session.headers.update(headers)

        self.test_connection()

    def send_login(self):
        """Wrapper that send HTTP login request to REST API.

        Since Nov 2021 websupport servers returns "401: Incorrect api key or signature" messages on all your
        query requests if you don't send this default login request before your API request/update. After this
        request, you are "logged in" for next 59 seconds. If you make any API request/update in this time,
        it will be processed correctly, however it won't reset this timer back to 59 seconds. For this same reason, this
        login request is sent before any API request/update.
        (Notice: This behaviour was not confirmed from official developers of Websupport REST API and may be only
        limited to my personal account, what is however unlikely)"""

        self.session.get(f"{self.api}{self.default_path}")

    def test_connection(self):
        """Test if connection is established and no errors occurred.

        Raises:
            websupportsk.exceptions.WebsupportAuthenticationError: If authentication failed.
            websupportsk.exceptions.WebsupportZoneNotFound: If domain specified was not found inside user account.
            websupportsk.exceptions.WebsupportConnectionError: If connection failed, i.e. no internet access,
                DNS resolution issue,...

        Returns:
            Message if test was successful.
        """

        try:
            login_response = self.session.get("%s%s%s" % (self.api, self.default_path, self.query)).json()
        except requests.exceptions.ConnectionError as e:
            raise websupportsk.exceptions.WebsupportConnectionError('Connection failed.', 503)

        # testing login credentials
        if 'message' and 'code' in login_response:
            raise websupportsk.exceptions.WebsupportAuthenticationError(login_response['message'],
                                                                        login_response['code'])
        # testing domain access
        domain_response = self.session.get(f"{self.api}{self.default_path}/zone/{self.domain}").json()
        if 'message' and 'code' in domain_response:
            raise websupportsk.exceptions.WebsupportZoneNotFound(domain_response['message'], domain_response['code'])

        logger.debug("Connection is established and no errors occurred.")
        return "Connection is established and no errors occurred."

    def get_records(self, type_=None, id_=None, name=None, content=None, ttl=None, note=None):
        """Request list of records with values specified.

        Returns:
            List of records that match arguments specified above.
        """

        self.send_login()
        # create dict of arguments passed to method, filter out 'None' values
        # and 'self' argument, rename keys(remove "_" trailing)
        args = {k.replace("_", ""): v for k, v in locals().items() if v is not None and k != 'self'}

        # get data from api
        data = json.loads(
            self.session.get(f"{self.api}{self.default_path}/zone/{self.domain}/record{self.query}").content)
        records = data["items"]

        matched_records = list()
        for record in records:
            # keys to compare
            keys_to_compare = args.keys() & record.keys()
            # keys that have same value in record and arguments
            shared_elements = [k for k in keys_to_compare if record[k] == args[k]]
            # record is valid only if all values from args match
            matched_records.append(record) if len(shared_elements) == len(args) else None

        logger.debug(
            f"GETTING RECORDS, {len(args)} argument(s) specified: {args},... found: {len(matched_records)} record(s)")
        return matched_records

    def create_record(self, type_, name, content, ttl=600, **kwargs):
        """Create record with arguments specified.

        Some types of records support additional arguments. In that case you can specify them as keyword argument.
        MX record for example requires parameter "prio", so you will have to specify it as well (i.e. prio=5).
        All parameters can be found inside REST API documentation.

        Returns:
            Response from API call. Response contain if request succeeded or failed with errors listed.
        """

        self.send_login()
        args = {k.replace("_", ""): v for k, v in locals().items()}
        args.pop('self')
        args.pop('kwargs')
        args.update(**kwargs)

        response = self.session.post(f"{self.api}{self.default_path}/zone/{self.domain}/record", json=args).json()
        log_response("CREATING RECORD", response)

        return response

    def edit_record(self, id_, **kwargs):
        """Edit record's keyword arguments specified, i.e. name="subdomain1".

        Returns:
            Response from API call. Response contain if request succeeded or failed with errors listed.
        """

        if self.is_valid_id(id_):
            response = self.session.put(f"{self.api}{self.default_path}/zone/{self.domain}/record/{id_}",
                                        json=kwargs).json()
        else:
            response = {'status': 'error', 'item': 'Not found',
                        'errors': {'content': ['Specified ID is invalid, no record found.']}}

        log_response("EDITING RECORD", response)
        return response

    def delete_record(self, id_):
        """Remove record based on id specified.

        Returns:
            Response from API call. Response contain if request succeeded or failed with errors listed.
        """

        if self.is_valid_id(id_):
            response = self.session.delete(f"{self.api}{self.default_path}/zone/{self.domain}/record/{id_}").json()
        else:
            response = {'status': 'error', 'item': 'Not found',
                        'errors': {'content': ['Specified ID is invalid, no record found.']}}
        log_response("DELETING RECORD", response.copy())
        return response

    # return just first record found
    # TO-DO: add error handling for not found record and multiple records found
    def get_record_id(self, type_, name, **kwargs):
        """Same functionality as get_records function, just return id of first record found.

        Returns:
            Id of the first record found.
        """

        record = self.get_records(type_=type_, name=name, **kwargs)
        if record:
            logger.debug(f"RECORD SELECTED, returning id `{record[0]['id']}`")
            return record[0]['id']
        else:
            logger.debug(f"RECORD NOT FOUND, returning id `None`")
            return None

    def is_valid_id(self, id_):
        """
        Check validity of `id_`.

        Returns:
            True if `id_` is valid, otherwise False.
        """

        if id_ is not None and self.get_records(id_=id_):
            logger.debug(f"ID `{id_}` is valid.")
            return True
        else:
            logger.debug(f"ID `{id_}` is invalid.")
            return False


def log_response(action, record):
    """Format and log record response from REST API.

    Args:
        action (string): Name of action performed.
        record (dict): Dictionary containing all information about record.
    """

    logger.debug(f"{action}:: STATUS: {record['status']}, ITEM: {record['item']}, ERRORS: {record['errors']}")
