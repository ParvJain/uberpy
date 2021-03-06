__author__ = 'Vivan'

from api import Api


class Uber(Api):
    """
    Class holding all Uber API calls. Inherits from the base API class.
    This class is used to provide access to all the API calls which are abstracted as methods.
    """
    def __init__(self, client_id, server_token, secret, redirect_uri):
        """
        Instantiate a new Uber object.
        :param client_id: Client ID for an application provided by Uber.
        :param server_token: Server token for an application provided by Uber.
        :param secret: Secret for an application provided by Uber.
        :param redirect_uri: The URI we will redirect back to after an authorization by the
        resource owner. The base of the URI must match the redirect_uri used during the registration
        of your application.
        """

        self.client_id = client_id
        self.server_token = server_token
        self.secret = secret
        self.redirect_uri = redirect_uri

        super(Uber, self).__init__(self.client_id, self.server_token, self.secret, self.redirect_uri)

    def get_products(self, latitude, longitude):
        """
        Get a list of all Uber products based on latitude and longitude coordinates.
        :param latitude: Latitude for which product list is required.
        :param longitude: Longitude for which product list is required.
        :return: JSON
        """
        endpoint = 'products'
        query_parameters = {
            'latitude': latitude,
            'longitude': longitude
        }

        return self.get_json(endpoint, 'GET', query_parameters, None, None)

    def get_price_estimate(self, start_latitude, start_longitude, end_latitude, end_longitude):
        """
        Returns the fare estimate based on two sets of coordinates.
        :param start_latitude: Starting latitude or latitude of pickup address.
        :param start_longitude: Starting longitude or longitude of pickup address.
        :param end_latitude: Ending latitude or latitude of destination address.
        :param end_longitude: Ending longitude or longitude of destination address.
        :return: JSON
        """
        endpoint = 'estimates/price'
        query_parameters = {
            'start_latitude': start_latitude,
            'start_longitude': start_longitude,
            'end_latitude': end_latitude,
            'end_longitude': end_longitude
        }

        return self.get_json(endpoint, 'GET', query_parameters, None, None)

    def get_time_estimate(self, start_latitude, start_longitude, customer_uuid=None, product_id=None):
        """
        Get the ETA for Uber products.
        :param start_latitude: Starting latitude.
        :param start_longitude: Starting longitude.
        :param customer_uuid: (Optional) Customer unique ID.
        :param product_id: (Optional) If ETA is needed only for a specific product type.
        :return: JSON
        """

        endpoint = 'estimates/time'
        query_parameters = {
            'start_latitude': start_latitude,
            'start_longitude': start_longitude
        }

        if customer_uuid is not None:
            query_parameters['customer_uuid'] = customer_uuid
        elif product_id is not None:
            query_parameters['product_id'] = product_id
        elif customer_uuid is not None and product_id is not None:
            query_parameters['customer_uuid'] = customer_uuid
            query_parameters['product_id'] = product_id

        return self.get_json(endpoint, 'GET', query_parameters, None, None)

    def get_promotions(self, start_latitude, start_longitude, end_latitude, end_longitude):
        """
        Get promotions for new user based on user location.
        :param start_latitude: Starting latitude or latitude of pickup address.
        :param start_longitude: Starting longitude or longitude of pickup address.
        :param end_latitude: Ending latitude or latitude of destination address.
        :param end_longitude: Ending longitude or longitude of destination address.
        :return: JSON
        """

        endpoint = 'promotions'
        query_parameters = {
            'start_latitude': start_latitude,
            'start_longitude': start_longitude,
            'end_latitude': end_latitude,
            'end_longitude': end_longitude
        }

        return self.get_json(endpoint, 'GET', query_parameters, None, None)

    def get_authorize_url(self, scopes=[], state=None, response_type='code'):
        """
        Returns a URL to redirect users to to begin the OAuth login flow 

        :param scopes:     List of requested permissions. Available scopes are
                    "profile" and "history"
        :param state:      Optional nonce value to append to the OAuth callback after
                    successful authentication. This allows you to track a user
                    throughout the full OAuth flow.
        :param response_type: Type of authorization flow to use. Only "code" is
                       supported at this time and is the default.
        :return: string
        """

        path = 'authorize'
        query_parameters = {
            'client_id': self.client_id,
            'response_type': response_type,
            'scopes': ','.join(scopes),
        }

        return Api.build_request(self, path, query_parameters, authorisation=True)

    def get_access_token(self, code):
        """
        Exchange the code parameter from an OAuth callback request to your
        redirect_uri for an access token that can be used to perform
        requests on behalf of the authorized user.

        :param code:       The value of the "code" query string parameter passed
                    by the client to your redirect_uri after successfully
                    authenticating with Uber
        :return: JSON
        """

        endpoint = 'token'
        query_parameters = {
            'client_id': self.client_id,
            'client_secret': self.secret,
            'grant_type': 'authorization_code',
            'redirect_uri': self.redirect_uri,
            'code': code
        }

        return self.get_json(endpoint, 'POST', query_parameters, None, None, authorisation=True)

    def refresh_token(self, refresh_token):
        """
        Exchange a refresh token received in response to get_access_token
        for a new access token with a later expiration time.

        :param refresh_token:  The refresh_token value from the get_access_token
                        response.
        :return: JSON
        """

        endpoint = 'token'
        query_parameters = {
            'client_id': self.client_id,
            'client_secret': self.secret,
            'grant_type': 'authorization_code',
            'redirect_uri': self.redirect_uri,
            'refresh_token': refresh_token
        }

        return self.get_json(endpoint, 'POST', query_parameters, None, None, authorisation=True)

    def revoke_token(self, token):

        endpoint = 'revoke'
        query_parameters = {
            'client_id': self.client_id,
            'client_secret': self.secret,
            'token': token
        }

        return self.get_json(endpoint, 'POST', query_parameters, None, None, authorisation=True)