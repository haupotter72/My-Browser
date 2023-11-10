
import validators
import urllib.parse

def is_valid_domain(url):
    if validators.domain(url):
        return True
    return False

def is_valid_url(url):
    try:
        result = urllib.parse.urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False
