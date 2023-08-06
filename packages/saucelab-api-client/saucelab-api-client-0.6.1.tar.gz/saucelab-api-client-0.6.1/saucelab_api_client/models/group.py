from saucelab_api_client.models.file import File


class Group:
    def __init__(self, data: dict):
        self.group_id: int = data.get('id')
        self.name: str = data.get('name')
        self.recent: File = File(data.get('recent'))
        self.count: int = data.get('count')
        self.access: dict = data.get('access')
        self.settings: dict = data.get('settings')

    def __str__(self):
        return self.name
