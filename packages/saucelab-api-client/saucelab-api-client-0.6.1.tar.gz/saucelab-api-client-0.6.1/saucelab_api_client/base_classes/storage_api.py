import os
from threading import Event, Thread

from saucelab_api_client.base_classes.exceptions import WrongFileExtension
from saucelab_api_client.category import Base
from saucelab_api_client.models.file import File
from saucelab_api_client.models.group import Group
from saucelab_api_client.models.service import print_progress, get_dict_from_locals


class Storage(Base):
    __sub_host = '/v1/storage'

    def files(self, q=None, kind=None, file_id=None, team_id=None, page=None, per_page=None):
        """
        https://docs.saucelabs.com/dev/api/storage/#get-app-storage-files

        Returns the set of files that have been uploaded to Sauce Storage by the requestor
        :param q: Any search term (such as build number or file name) by which you want to filter results
        :param kind: The application type associated with the file, such as android or ios
        :param file_id: One or more specific IDs of the files to return
        :param team_id: One or more IDs of teams with which the files are shared
        :param page: Return results beginning with a specific page. Default is 1
        :param per_page: The maximum number of results to show per page
        :return:
        """
        params = get_dict_from_locals(locals())
        return self._valid(self._session.request('get', f'{self.__sub_host}/files', params=params), File, 'items')

    def file_by_id(self, file_id: str):
        """
        Get file by file_id
        :param file_id: One or more specific IDs of the files to return
        :return: File object
        """
        return self.files(file_id=file_id)[0]

    def file_by_bundle_id(self, bundle_id: str, get_last: bool = True):
        """
        Get File objects
        :param bundle_id:
        :param get_last: return last uploaded file
        :return: File or [File]
        """
        result = list(app for app in self.files() if app.metadata.identifier == bundle_id)
        if get_last:
            return max(result, key=lambda file: file.upload_timestamp)
        else:
            return result

    def groups(self, q=None, kind=None, group_id=None, page=None, per_page=None):
        """
        https://docs.saucelabs.com/dev/api/storage/#get-app-storage-groups

        Returns an array of groups (applications containing multiple files) currently in storage
        for the authenticated requestor
        :param q: Any search term (such as build number or file name) by which you want to filter results
        :param kind: The application type associated with the group, such as android or ios
        :param group_id: One or more specific IDs of the groups to return
        :param page: Return results beginning with a specific page. Default is 1
        :param per_page: The maximum number of results to show per page
        :return:
        """
        params = get_dict_from_locals(locals())
        return self._valid(self._session.request('get', f'{self.__sub_host}/groups', params=params), Group, 'items')

    def upload(self, app_path: str):
        """
        https://docs.saucelabs.com/dev/api/storage/#upload-file-to-app-storage

        Uploads an application file to Sauce Storage for the purpose of mobile application testing and returns a
        unique file ID assigned to the app.
        Sauce Storage supports app files in *.apk, *.aab, *.ipa, or *.zip format, up to 4GB
        :param app_path: app file path
        :return: File object of uploaded app
        """
        if app_path.split('.')[-1] in ('apk', 'aab', 'ipa', 'zip'):
            exit_event = Event()
            thread = Thread(target=print_progress, args=(exit_event, 'upload'))
            thread.start()
            files = {'payload': open(app_path, 'rb')}
            response = self._valid(self._session.request('post', f'{self.__sub_host}/upload', files=files), File,
                                   'item')
            if str(response).startswith('Error'):
                print(f'Upload error\n{response}')
            exit_event.set()
            return response
        else:
            raise WrongFileExtension('File to send must have following extension: apk, aab, ipa, zip')

    def download_file(self, file_id: str, file_path: str, file_name: str = None):
        """
        https://docs.saucelabs.com/dev/api/storage/#download-a-file-from-app-storage

        Returns an application file from Sauce Storage as a payload object in the response
        :param file_id: The Sauce Labs identifier of the stored file
        :param file_path: File path
        :param file_name: File name. Optional. Default - file name from Sauce Lab
        :return:
        """
        file = self.file_by_id(file_id=file_id)
        if isinstance(file, str):
            return 'File with given file_id doesn\'t found'
        else:
            exit_event = Event()

            if file_name is None:
                file_name = file.name

            path = os.path.join(file_path, file_name)
            if os.path.isfile(path):
                os.remove(path)
            thread = Thread(target=print_progress, args=(exit_event, 'download'))
            thread.start()
            response = self._session.request('get', f'{self.__sub_host}/download/{file_id}', return_type='content')
            exit_event.set()
            open(path, 'wb').write(response)

    def edit_description(self, file_id: str, new_description: str):
        """
        https://docs.saucelabs.com/dev/api/storage/#edit-a-stored-files-description

        Adds or updates the description attribute of the specified file
        :param file_id: The Sauce Labs identifier of the stored file
        :param new_description: A description to more clearly distinguish the stored file within the Sauce Labs system
        :return: File object
        """

        data = {'item': {'description': new_description}}
        return self._valid(self._session.request('put', f'{self.__sub_host}/files/{file_id}', data=data), File, 'item')

    def delete_by_file_id(self, file_id: str):
        """
        https://docs.saucelabs.com/dev/api/storage/#delete-an-app-storage-file

        Deletes the specified file from Sauce Storage
        :param file_id: The Sauce Labs identifier of the stored file
        :return:
        """
        return self._valid(self._session.request('delete', f'{self.__sub_host}/files/{file_id}'), File, 'item')

    def delete_all_files_by_bundle_id(self, bundle_id: str):
        """

        :param bundle_id:
        :return:
        """
        return tuple(self.delete_by_file_id(app_id) for app_id in (app.file_id for app in self.files()
                                                                   if app.metadata.identifier == bundle_id))

    def delete_by_group_id(self, group_id: str):
        """
        https://docs.saucelabs.com/dev/api/storage/#delete-a-group-of-app-storage-files

        Deletes the specified group of files from Sauce Storage
        :param group_id: The Sauce Labs identifier of the group of files
        :return: None
        """
        self._session.request('delete', f'{self.__sub_host}/files/{group_id}')
