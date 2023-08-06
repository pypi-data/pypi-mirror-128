class invalidLinkException(Exception):
    pass

class HTTP404PageNotFoundException(Exception):
    pass

class UnknownRequestException(Exception):
    pass

# Define some functions for easy checking if the link is even workable
def validate_link(link):
    if (link.startswith('https://www.archiveofourown.org/') or link.startswith('https://archiveofourown.org/')):
        return
    else:
        raise invalidLinkException(f'The link provided [{link}] is not supported')

def validate_status(r):
    if (r.status_code == 200):
        return
    elif (r.status_code == 404):
        raise HTTP404PageNotFoundException("Error 404: Web page not found")
    else:
        raise UnknownRequestException('idk, try again or use a different link')