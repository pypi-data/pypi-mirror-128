from saucelab_api_client.base_classes.exceptions import MissingArguments
from saucelab_api_client.category import Base
from saucelab_api_client.models.accounts import TeamSearch, Team, UserSearch, User
from saucelab_api_client.models.service import validate_dict, get_dict_from_locals


class Accounts(Base):

    @property
    def account_team(self):
        return AccountTeam(self._session)

    @property
    def account_user(self):
        return AccountUser(self._session)


class AccountTeam(Base):
    __sub_host = '/team-management/v1'

    def teams(self, team_name: str = None):
        """
        https://docs.saucelabs.com/dev/api/accounts/#lookup-teams

        Queries the organization of the requesting account and returns the number of teams matching the query and
        a summary of each team, including the ID value, which may be a required parameter of other API calls
        related to a specific team.
        You can filter the results of your query using the name parameter below
        :param team_name: Returns the set of teams that begin with the specified name value
        :return:
        """
        params = {'name': team_name} if team_name else {}
        return self._valid(self._session.request('get', f'{self.__sub_host}/teams/', params=params), TeamSearch,
                           'results')

    def get_team(self, team_id: str):
        """
        https://docs.saucelabs.com/dev/api/accounts/#get-a-specific-team

        Returns the full profile of the specified team. The ID of the team is the only valid unique identifier
        :param team_id: The unique identifier of the team
        :return:
        """
        return self._valid(self._session.request('get', f'{self.__sub_host}/teams/{team_id}'), Team)

    def create_team(self, name: str, organization: str, settings: dict, description: str = None):
        """
        https://docs.saucelabs.com/dev/api/accounts/#create-a-team

        Creates a new team under the organization of the requesting account
        :param name: A name for the new team
        :param organization: The unique ID of the organization under which the team is created
        :param settings: The settings object specifies the concurrency allocations for the team within the organization.
                            The available attributes are:
                            - virtual_machines - integer
                            - real devices - integer
                            - live only - boolean Defaults to false.
        :param description: A description to distinguish the team within the organization
        :return: Team object
        """
        validate_dict(settings, ('virtual_machines', 'real_devices', 'live_only'), soft_check=True)
        data = {
            'name': name,
            'organization': organization,
            'settings': settings,
        }
        if description is not None:
            data['description'] = description
        return self._valid(self._session.request('post', f'{self.__sub_host}/teams', data=data), Team)

    def delete_team(self, team_id: str):
        """
        https://docs.saucelabs.com/dev/api/accounts/#delete-a-team

        Deletes the specified team from the organization of the requesting accoun
        :param team_id: The unique identifier of the team
        :return: None
        """
        self._session.request('delete', f'{self.__sub_host}/teams/{team_id}')

    def update_team(self, team_id: str, name: str, settings: dict, description: str = None):
        """
        https://docs.saucelabs.com/dev/api/accounts/#update-a-team

        Replaces all values of the specified team with the new set of parameters passed in the request.
        To update only certain parameters, see Partially Update Team.
        :param team_id: The unique identifier of the team
        :param name: The name of the team as it will be after the update.
                        Pass the current value to keep the name unchanged.
        :param settings: The settings object specifies the concurrency allocations for the team within the organization.
                            The available attributes are:
                            - virtual_machines - integer
                            - real devices - integer
                            - live only - boolean Defaults to false.
        :param description: A description to distinguish the team within the organization.
                            If the previous team definition included a description, omitting the parameter in the
                            update will delete it from the team record.
        :return:
        """
        validate_dict(settings, ('virtual_machines', 'real_devices', 'live_only'), soft_check=True)
        data = {
            'name': name,
            'settings': settings,
            'description': description
        }
        return self._valid(self._session.request('put', f'{self.__sub_host}/teams/{team_id}', data=data), Team)

    def partially_update_team(self, team_id: str = None, name: str = None, settings: dict = None,
                              description: str = None):
        """
        https://docs.saucelabs.com/dev/api/accounts/#partially-update-a-team

        Updates one or more individual editable parameters (such as the concurrency allocation) of the
        specified team without requiring a full profile update.
        :param team_id: The unique identifier of the team
        :param name: An updated name for the team
        :param settings: The settings object specifies the concurrency allocations for the team within the organization.
                            The available attributes are:
                            - virtual_machines - integer
                            - real devices - integer
                            - live only - boolean Defaults to false.
        :param description: An updated description
        :return:
        """
        if settings is not None:
            validate_dict(settings, ('virtual_machines', 'real_devices', 'live_only'), soft_check=True)
        data = {key: value for key, value in locals().items() if key in ('team_id', 'name', 'settings', 'description')}
        if len(data.keys()) == 0:
            raise MissingArguments('Missing any arguments')
        return self._valid(self._session.request('patch', f'{self.__sub_host}/teams/{team_id}/', data=data), Team)

    def list_team_members(self, team_id: str):
        """
        https://docs.saucelabs.com/dev/api/accounts/#list-team-members

        Returns the number of members in the specified team and lists each member
        :param team_id: Identifies the team for which you are requesting the list of members
        :return:
        """
        return self._valid(self._session.request('get', f'{self.__sub_host}/teams/{team_id}/members'), UserSearch,
                           'results')

    def reset_access_key_for_team(self, team_id: str):
        """
        https://docs.saucelabs.com/dev/api/accounts/#reset-access-keys-for-entire-team

        Globally regenerates new access key values for every member of the specified team
        Regenerating an access key invalidates the previous value and any tests containing the prior value will fail,
        so make sure you edit any tests and credential environment variables with the new value.
        :param team_id: Identifies the team for which you are resetting member access keys
        :return: None
        """
        self._session.request('post', f'{self.__sub_host}/teams/{team_id}/reset-access-key/')


class AccountUser(Base):
    __sub_host = '/team-management/v1'

    def all_users(self, username: str = None, teams: str = None, team_name: str = None, roles: int = None,
                  phrase: str = None, status: str = None, limit: int = None, offset: int = None):
        """
        https://docs.saucelabs.com/dev/api/accounts/#lookup-users

        Queries the organization of the requesting account and returns the number of users matching the query and
        a basic profile of each user, including the ID value, which may be a required parameter of other API calls
        related to a specific user.

        You can narrow the results of your query using any of the following filtering parameters.
        :param username: Limits the results to usernames that begin with the specified value
        :param teams: Limit results to users who belong to the specified team_ids.
                        Specify multiple teams as comma-separated values
        :param team_name: Limit results to users who belong to the specified team names.
                        Specify multiple teams as comma-separated values
        :param roles: Limit results to users who are assigned certain roles. Valid values are:
                        1 - Organaization Admin. 4 - Team Admin. 3 - Member.
                        Specify multiple roles as comma-separated values
        :param phrase: Limit results to users whose first name, last name, or email address begins
                        with the specified value
        :param status: Limit results to users of the specifid status. Valid values are: active, pending, inactive
        :param limit: Limit results to a maximum number per page. Default value is 20
        :param offset: The starting record number from which to return results
        :return:
        """
        params = get_dict_from_locals(locals())
        return self._valid(self._session.request('get', f'{self.__sub_host}/users/', params=params), UserSearch,
                           'results')

    def get_user(self, user_id: str):
        """
        https://docs.saucelabs.com/dev/api/accounts/#get-a-specific-user

        Returns the full profile of the specified user. The ID of the user is the only valid unique identifier
        :param user_id: The user's unique identifier
        :return: UserSearch or str
        """
        return self._valid(self._session.request('get', f'{self.__sub_host}/users/{user_id}'), User)

    def create(self, email: str, username: str, password: str, first_name: str = None, last_name: str = None,
               organization: str = None, role: str = None, team: str = None):
        """
        https://docs.saucelabs.com/dev/api/accounts/#create-a-new-user

        Creates a new user in the Sauce Labs platform
        :param first_name: The new user's first name
        :param last_name: The new user's last name
        :param email: The user's contact email address
        :param username: A login username for the new user
        :param password: A login password for the new user
        :param organization: The identifier of the organization to create the user's account
        :param role: The new user's permission role.
                        Valid values are  1 - Organaization Admin. 4 - Team Admin. 3 - Member
        :param team: The identifier of the team of which the new user is a member
        :return:
        """
        data = get_dict_from_locals(locals())
        return self._valid(self._session.request('post', f'{self.__sub_host}/users/', data=data), User)

    def update_user(self, user_id: str, first_name: str, last_name: str, email: str, password: str):
        """
        https://docs.saucelabs.com/dev/api/accounts/#update-a-user

        Replaces all values of the specified user profile with the new set of parameters passed in the request.
        To update only certain parameters, see Partially Update a User.
        :param user_id: The unique identifier of the use
        :param first_name: The user's first name
        :param last_name: The user's last name
        :param email: The user's contact email address
        :param password: A login password for the new user
        :return: User or str
        """
        data = get_dict_from_locals(locals())
        data['verify_password'] = password
        return self._valid(self._session.request('put', f'{self.__sub_host}/users/{user_id}', data=data), User)

    def partially_update_user(self, user_id: str, first_name: str = None, last_name: str = None, email: str = None,
                              password: str = None):
        """
        https://docs.saucelabs.com/dev/api/accounts/#partially-update-a-user

        Allows you to update individual user values without replacing the entire profile
        :param user_id: The unique identifier of the user to update
        :param first_name: The user's first name
        :param last_name: The user's last name
        :param email: The user's contact email address
        :param password: A login password for the new user
        :return:
        """
        data = get_dict_from_locals(locals())
        if 'password' in data:
            data['verify_password'] = password
        if len(data.keys()) == 0:
            raise MissingArguments('Missing any arguments')
        return self._valid(self._session.request('patch', f'{self.__sub_host}/users/{user_id}', data=data), User)

    def get_user_concurrency(self, username: str):
        """
        https://docs.saucelabs.com/dev/api/accounts/#get-user-concurrency

        Allows you to update individual user values without replacing the entire profile
        :param username: The username of the user whose concurrency you are looking up
        :return:
        """
        return self._session.request('get', f'/rest/v1.2/users/{username}/concurrency')

    def user_teams(self, user_id: str):
        """
        https://docs.saucelabs.com/dev/api/accounts/#get-a-users-team

        Returns the number of teams a user belongs to and provides information about each team,
        including whether it is the default and its concurrency settings.
        :param user_id: The unique identifier of the user
        :return:
        """
        return self._session.request('get', f'{self.__sub_host}/users/{user_id}/teams')['results']

    def get_active_user(self):
        return self._valid(self._session.request('get', f'{self.__sub_host}/users/me'), User)
