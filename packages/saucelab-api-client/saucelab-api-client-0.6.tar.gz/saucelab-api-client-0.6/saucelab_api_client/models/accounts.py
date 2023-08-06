class TeamSearch:
    def __init__(self, data: dict):
        if data is not None:
            self.team_id: str = data.get('id')
            self.name: str = data.get('name')
            self.settings: Settings = Settings(data.get('settings'))
            self.group: AccountGroup = AccountGroup(data.get('group'))
            self.is_default: bool = data.get('is_default')
            self.org_uuid: str = data.get('org_uuid')
            self.user_count: int = data.get('user_count')

    def __str__(self):
        return self.name


class Team:
    def __init__(self, data: dict):
        if data is not None:
            self.team_id: str = data.get('id')
            self.name: str = data.get('name')
            self.org_uuid: str = data.get('org_uuid')
            self.group: AccountGroup = AccountGroup(data.get('group'))
            self.created_at: str = data.get('created_at')
            self.updated_at: str = data.get('updated_at')
            self.settings: Settings = Settings(data.get('settings'))
            self.description: str = data.get('description')
            self.is_default: bool = data.get('is_default')

    def __str__(self):
        return self.name


class Settings:
    def __init__(self, data: dict):
        if data is not None:
            self.virtual_machines: int = data.get('virtual_machines')
            self.real_devices: int = data.get('real_devices')
            self.live_only: bool = data.get('live_only')


class AccountGroup:
    def __init__(self, data: dict):
        if data is not None:
            self.group_id: str = data.get('id')
            self.name: str = data.get('name')
            self.virtual_machines: int = data.get('virtual_machines')
            self.real_devices: int = data.get('real_devices')

    def __str__(self):
        return self.name


class User:
    def __init__(self, data: dict):
        if data is not None:
            self.user_id: str = data.get('id')
            self.username: str = data.get('username')
            self.email: str = data.get('email')
            self.first_name: str = data.get('first_name')
            self.last_name: str = data.get('last_name')
            self.is_active: bool = data.get('is_active')
            self.created_at: str = data.get('created_at')
            self.updated_at: str = data.get('updated_at')
            self.teams: list[Team] = [Team(team) for team in data.get('teams')]
            self.roles: list[Role] = [Role(role) for role in data.get('roles')]
            self.is_staff: bool = data.get('is_staff')
            self.is_superuser: bool = data.get('is_superuser')
            self.user_type: str = data.get('user_type')
            self.groups: list = data.get('groups')
            self.organization: Organization = Organization(data.get('organization'))
            self.phone: str = data.get('phone')
            self.is_organization_admin: bool = data.get('is_organization_admin')
            self.is_team_admin: bool = data.get('is_team_admin')

    def __str__(self):
        return self.username


class UserSearch:
    def __init__(self, data: dict):
        if data is not None:
            self.user_id: str = data.get('id')
            self.username: str = data.get('username')
            self.first_name: str = data.get('first_name')
            self.last_name: str = data.get('last_name')
            self.is_active: bool = data.get('is_active')
            self.email: str = data.get('email')
            self.teams: list[Team] = [Team(team) for team in data.get('teams')]
            self.roles: list[Role] = [Role(role) for role in data.get('roles')]
            self.organization: Organization = Organization(data.get('organization'))

    def __str__(self):
        return self.username


class Role:
    def __init__(self, data: dict):
        if data is not None:
            self.name: str = data.get('name')
            self.role: int = data.get('role')

    def __str__(self):
        return self.name


class Organization:
    def __init__(self, data: dict):
        if data is not None:
            self.organization_id: str = data.get('id')
            self.name: str = data.get('name')

    def __str__(self):
        return self.name
