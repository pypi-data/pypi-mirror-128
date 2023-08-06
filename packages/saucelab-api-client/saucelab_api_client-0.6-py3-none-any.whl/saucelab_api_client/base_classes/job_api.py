import os
from threading import Thread, Event

from saucelab_api_client.category import Base
from saucelab_api_client.models.build import Build
from saucelab_api_client.models.job import JobSearch, Job, JobAssets
from saucelab_api_client.models.service import print_progress, get_dict_from_locals


class JobsApi(Base):
    __sub_host = '/rest/v1'

    def get_user_jobs(self, username: str, limit: int = None, skip: int = None, from_: str = None, to: str = None) \
            :
        """
        https://docs.saucelabs.com/dev/api/jobs/#jobs-methods

        Get a list of recent jobs run by the specified user
        :param username: The username of the Sauce Labs user whose jobs you are looking up
        :param limit: The maximum number of jobs to return
        :param skip: Returns only the jobs beginning after this index number
        :param from_: Return only jobs that ran on or after this Unix timestamp
        :param to: Return only jobs that ran on or before this Unix timestamp
        :return:
        """
        params = {key.replace('_', ''): value for key, value in locals().items() if value}
        return self._valid(self._session.request('get', f'{self.__sub_host}/{username}/jobs', params=params), JobSearch)

    def get_job_details(self, username: str, job_id: str):
        """
        https://docs.saucelabs.com/dev/api/jobs/#get-job-details

        Get detailed information about a specific job
        :param username: The username of the Sauce Labs user whose jobs you are looking up
        :param job_id: The Sauce Labs identifier of the job you are looking up
        :return:
        """
        return self._valid(self._session.request('get', f'{self.__sub_host}/{username}/jobs/{job_id}'), Job)

    def update_job(self, username: str, job_id: str, name: str = None, tags: [tuple, list] = None, public: str = None,
                   passed: str = None, build: str = None, custom_data: dict = None):
        """
        https://docs.saucelabs.com/dev/api/jobs/#update-a-job

        Edit job attributes based on parameters passed in the request, including setting the status of the job.
        :param username: The username of the owner of the job you are updating
        :param job_id: The Sauce Labs identifier of the job to be update
        :param name: A new name for the job
        :param tags: The set of distinguishing tags to apply to the job
        :param public: Specifies the level of visibility permitted for the job
        :param passed: Asserts whether the job passed (true) or not (false)
        :param build: Assign the job to a build
        :param custom_data: Any relevant attributes you wish to add to the job details
        :return: JobSearch object
        """
        data = get_dict_from_locals(locals(), replace_underscore=True)
        return self._valid(self._session.request('put', f'{self.__sub_host}/{username}/jobs/{job_id}', data=data), Job)

    def stop_job(self, username: str, job_id: str):
        """
        https://docs.saucelabs.com/dev/api/jobs/#stop-a-job

        Stop indicated job
        :param username: The username of the owner of the job to stop
        :param job_id: The Sauce Labs identifier of the job to stop
        :return: Job object
        """
        return self._valid(self._session.request('put', f'{self.__sub_host}/{username}/jobs/{job_id}/stop'), Job)

    def delete_job(self, job_id: str):
        """
        https://docs.saucelabs.com/dev/api/jobs/#delete-a-job

        Delete a job and all of its assets from the Sauce Labs test history
        :param job_id: The Sauce Labs identifier of the job to delete
        :return: None
        """
        self._session.request('delete', f'/rest/v1.1/jobs/{job_id}')

    def delete_all_users_jobs(self, username: str):
        """
        https://docs.saucelabs.com/dev/api/jobs/#delete-all-of-a-users-jobs

        Delete the entire test history and all assets for the specified user
        :param username: The username of the Sauce Labs user whose jobs you are deleting
        :return: None
        """
        self._session.request('get', f'/rest/v1.1/{username}/jobs')

    def get_job_assets(self, username: str, job_id: str):
        """
        https://docs.saucelabs.com/dev/api/jobs/#list-job-assets

        Get a list of files associated with a specific test, such as the logs, video, and screenshots
        :param username: The username of the owner of the job
        :param job_id: The Sauce Labs identifier of the job for which you are retrieving the asset list
        :return:
        """
        return self._valid(self._session.request('get', f'{self.__sub_host}/{username}/jobs/{job_id}/assets'),
                           JobAssets)

    def get_job_asset_file(self, username: str, job_id: str, file_name: str, media_path: str = None,
                           media_file_name: str = None):
        """
        https://docs.saucelabs.com/dev/api/jobs/#get-a-job-asset-file

        Retrieve one of the asset files associated with a job, such as a log file, video, or screenshot
        :param username: The username of the owner of the job
        :param job_id: The Sauce Labs identifier of the job for which you are retrieving the asset list
        :param file_name: The name of the asset file you wish to download
        :param media_path: Download file folder
        :param media_file_name: File name for downloaded file (if not indicated - script use file name from SauceLab
        :return:
        """
        file_type = file_name.split('.')
        if len(file_type) > 0:
            content_type, file_type = None, file_type[1]
            if file_type in ('log', 'har'):
                content_type = 'text'
            elif file_type in ('mp4', 'png'):
                if media_path is None:
                    raise FileNotFoundError('Media path is not indicated for media file')
                content_type = 'content'
            response = self._session.request('get', f'{self.__sub_host}/{username}/jobs/{job_id}/assets/{file_name}',
                                             return_type=content_type)
            if content_type == 'content':
                download_path = media_path if media_file_name is None else os.path.join(media_path, media_file_name)
                exit_event = Event()
                thread = Thread(target=print_progress, args=(exit_event, 'download'))
                thread.start()
                exit_event.set()
                open(download_path, 'wb').write(response)
            else:
                return response
        else:
            raise FileNotFoundError('Wrong file name')

    def delete_all_job_assets(self, username: str, job_id: str):
        """
        https://docs.saucelabs.com/dev/api/jobs/#delete-job-assets

         This request deletes all of the asset files associated with a job.
         Deleting a single asset file is not supported at this time
        :param username: The username of the owner of the job
        :param job_id: The Sauce Labs identifier of the job for which you are retrieving the asset list
        :return:
        """

        return self._session.request('delete', f'/{username}/jobs/{job_id}/assets')

    def get_builds(self, username: str):
        """
        https://docs.saucelabs.com/dev/api/jobs/#get-builds

        Get a list of recent builds run by the specified user
        :param username: The username of the Sauce Labs users whose builds you are looking up
        :return:
        """
        return self._valid(self._session.request('get', f'{self.__sub_host}/{username}/builds'), Build)
