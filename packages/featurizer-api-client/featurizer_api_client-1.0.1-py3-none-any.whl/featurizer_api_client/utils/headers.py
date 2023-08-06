def get_header_with_authentication_credentials(username, password):
    """
    Returns the header with the user authentication credentials.

    :param username: username
    :type username: str
    :param password: password
    :type password: str
    :return: request header
    :rtype: dict
    """
    return {
        "username": username,
        "password": password
    }


def get_header_with_access_token(access_token):
    """
    Returns the header with the user access token.

    :param access_token: access token
    :type access_token: str
    :return: request header
    :rtype: dict
    """
    return {"Authorization": f"Bearer {access_token}"}


def get_header_with_refresh_token(refresh_token):
    """
    Returns the header with the user refresh token.

    :param refresh_token: refresh token
    :type refresh_token: str
    :return: request header
    :rtype: dict
    """
    return {"Authorization": f"Bearer {refresh_token}"}
