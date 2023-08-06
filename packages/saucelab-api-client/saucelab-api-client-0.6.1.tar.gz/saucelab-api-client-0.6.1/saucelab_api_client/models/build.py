class Build:
    def __init__(self, data: dict):
        if data is not None:
            self.status: str = data.get('status')
            self.jobs: dict = data.get('jobs')
            self.name: str = data.get('name')
            self.deletion_time = data.get('deletion_time')
            self.org_id: str = data.get('org_id')
            self.start_time: int = data.get('start_time')
            self.creation_time: int = data.get('creation_time')
            self.number = data.get('number')
            self.public: bool = data.get('public')
            self.modification_time: int = data.get('modification_time')
            self.prefix = data.get('prefix')
            self.end_time: int = data.get('end_time')
            self.passed: bool = data.get('passed')
            self.owner: str = data.get('owner')
            self.run: int = data.get('run')
            self.team_id: str = data.get('team_id')
            self.group_id: str = data.get('group_id')
            self.build_id: str = data.get('id')

    def __str__(self):
        return self.name
