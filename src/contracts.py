import json

'''
{
  "id": "6253282",
  "name": "Twitter API",
  "username": "TwitterAPI",
  "profile_image_url": "..."
}
'''


class UserBasicDto:
    def __init__(self, id: str, name: str, username: str) -> None:
        self.id = id
        self.name = name
        self.username = username

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, value: str):
        self._id = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def username(self) -> str:
        return self._username

    @username.setter
    def username(self, value: str):
        self._username = value

    @classmethod
    def from_json(payload: str):
        d = json.loads(payload)
        return UserBasicDto(d['id'], d['name'], d['username'])
