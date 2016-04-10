class DownloadError(Exception):
    def __init__(self, message="File can't be downloaded"):
        # Call the base class constructor with the parameters it needs
        super(DownloadError, self).__init__(message)


class Timeout(Exception):
    def __init__(self, message="Connection with server timeout"):
        # Call the base class constructor with the parameters it needs
        super(Timeout, self).__init__(message)


class AttemptsError(Exception):
    def __init__(self, message="Attempts reached it's limit of tries"):
        # Call the base class constructor with the parameters it needs
        super(AttemptsError, self).__init__(message)


class PageNotFound(Exception):
    def __init__(self, message="Page not found"):
        # Call the base class constructor with the parameters it needs
        super(PageNotFound, self).__init__(message)


class UnsupportedSection(Exception):
    def __init__(self, message="Section don't contain any structure"):
        # Call the base class constructor with the parameters it needs
        super(UnsupportedSection, self).__init__(message)


class UnsupportedDomain(Exception):
    def __init__(self, message="Domain isn't supported"):
        # Call the base class constructor with the parameters it needs
        super(UnsupportedDomain, self).__init__(message)


class UnsupportedURL(Exception):
    def __init__(self, message="Domain doesn't contain any structure"):
        # Call the base class constructor with the parameters it needs
        super(UnsupportedURL, self).__init__(message)


class EmptyNodeContent(Exception):
    def __init__(self, message="Node doesn't contain any content"):
        # Call the base class constructor with the parameters it needs
        super(EmptyNodeContent, self).__init__(message)


class IncorrectQuery(Exception):
    def __init__(self, message="An incorrect query was done"):
        # Call the base class constructor with the parameters it needs
        super(IncorrectQuery, self).__init__(message)


class NotHaveSection(Exception):
    def __init__(self, message="This url don't have a valid section"):
        # Call the base class constructor with the parameters it needs
        super(NotHaveSection, self).__init__(message)


class TitleNotAvailable(Exception):
    def __init__(self, message="Can't retrieve the title from source"):
        # Call the base class constructor with the parameters it needs
        super(TitleNotAvailable, self).__init__(message)


class AuthorNotAvailable(Exception):
    def __init__(self, message="Can't retrieve the author from source"):
        # Call the base class constructor with the parameters it needs
        super(AuthorNotAvailable, self).__init__(message)

class DateNotAvailable(Exception):
    def __init__(self, message="Can't retrieve the date from source"):
        # Call the base class constructor with the parameters it needs
        super(DateNotAvailable, self).__init__(message)

