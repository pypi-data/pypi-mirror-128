from saucelab_api_client.category import Base
from saucelab_api_client.models.sauce_connect import Tunnel, TunnelJobs, StoppedTunnel


class SauceConnectApi(Base):
    """
    https://app.eu-central-1.saucelabs.com/tunnels
    
    Information about tunnels on SauceLab
    """

    __sub_host = '/rest/v1'

    def get_tunnel_for_user(self, username: str):
        """
        https://docs.saucelabs.com/dev/api/connect/#get-tunnels-for-a-user

        Returns a list of IDs for any currently running tunnels launched by the specified user
        :param username: The authentication username of the user whose tunnels you are requesting
        :return: str or dict
        """
        return self._session.request('get', f'{self.__sub_host}/{username}/tunnels')

    def get_tunnel_information(self, username: str, tunnel_id: str):
        """
        https://docs.saucelabs.com/dev/api/connect/#get-tunnel-information

        Returns information about the specified tunnel
        :param username: The authentication username of the owner of the requested tunnel
        :param tunnel_id: The unique identifier of the requested tunnel
        :return:
        """
        return self._valid(self._session.request('get', f'{self.__sub_host}/{username}/tunnels/{tunnel_id}'), Tunnel)

    def get_current_jobs_for_tunnel(self, username: str, tunnel_id: str):
        """
        https://docs.saucelabs.com/dev/api/connect/#get-current-jobs-for-a-tunnel

        Returns the number of currently running jobs for the specified tunnel
        :param username: The authentication username of the user whose tunnels you are requesting
        :param tunnel_id: The unique identifier of the requested tunnel
        :return:
        """
        return self._valid(self._session.request('get', f'{self.__sub_host}/{username}/tunnels/{tunnel_id}/num_jobs'),
                           TunnelJobs)

    def stop_tunnel(self, username: str, tunnel_id: str):
        """
        https://docs.saucelabs.com/dev/api/connect/#stop-a-tunnel

        Shuts down the specified tunnel
        :param username: The authentication username of the user whose tunnels you are requesting
        :param tunnel_id: The unique identifier of the tunnel to stop
        :return:
        """
        return self._valid(self._session.request('delete', f'{self.__sub_host}/{username}/tunnels/{tunnel_id}'),
                           StoppedTunnel)
