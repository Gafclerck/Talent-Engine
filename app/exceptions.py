class ErreurMetier(Exception):
    """Exception metier de base.

    Elle sera convertie en reponse HTTP francaise par un gestionnaire
    centralise, jamais exposee telle quelle (AD-8).
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message
