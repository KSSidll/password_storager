class PasswordEntry:
    def __init__(self, rowid, password, username=None, domain=None, description=None):
        self.rowid: int = rowid
        self.password: str = password
        self.username: str | None = username
        self.domain: str | None = domain
        self.description: str | None = description
