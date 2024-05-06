#!/usr/bin/env python
#
# This illustrates the call-flow required to complete an OAuth request
# against the discogs.com API, using the discogs_client libary.
# The script will download and save a single image and perform and
# an API search API as an example. See README.md for further documentation.

import sys
import discogs_client
from discogs_client.exceptions import HTTPError

# Your consumer key and consumer secret generated and provided by Discogs.
# See http://www.discogs.com/settings/developers . These credentials
# are assigned by application and remain static for the lifetime of your discogs
# application. the consumer details below were generated for the
# 'discogs-oauth-example' application.
# NOTE: these keys are typically kept SECRET. I have requested these for
# demonstration purposes.
def authenticate():

    consumer_key = user = input("Please enter consumer key: ")
    consumer_secret = input("Please enter consumer secret: ")

    # A user-agent is required with Discogs API requests. Be sure to make your
    # user-agent unique, or you may get a bad response.
    user_agent = input("Please enter user agent: ")

    # instantiate our discogs_client object.
    discogsclient = discogs_client.Client(user_agent)

    # prepare the client with our API consumer data.
    discogsclient.set_consumer_key(consumer_key, consumer_secret)
    token, secret, url = discogsclient.get_authorize_url()

    print(' == Request Token == ')
    print('    * oauth_token        = {0}'.format(token))
    print('    * oauth_token_secret = {0}'.format(secret))


    # Prompt your user to "accept" the terms of your application. The application
    # will act on behalf of their discogs.com account.
    # If the user accepts, discogs displays a key to the user that is used for
    # verification. The key is required in the 2nd phase of authentication.
    print('Please browse to the following URL {0}'.format(url))

    accepted = 'n'
    while accepted.lower() == 'n':
        accepted = input('Have you authorized me at {0} [y/n] :'.format(url))


    # Waiting for user input. Here they must enter the verifier key that was
    # provided at the unqiue URL generated above.
    oauth_verifier = input('Verification code :')

    try:
        access_token, access_secret = discogsclient.get_access_token(oauth_verifier)
    except HTTPError:
        print('Unable to authenticate.')
        sys.exit(1)

    # fetch the identity object for the current logged in user.
    user = discogsclient.identity()

    print
    print(' == User ==')
    print('    * username           = {0}'.format(user.username))
    print( '    * name               = {0}'.format(user.name))
    print( ' == Access Token ==')
    print( '    * oauth_token        = {0}'.format(access_token))
    print( '    * oauth_token_secret = {0}'.format(access_secret))
    print( ' Authentication complete. Future requests will be signed with the above tokens.')

    return discogsclient

if __name__ == '__main__':
    authenticate()

