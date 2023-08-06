import json


class Tunnel:
    def __init__(self, data: dict):
        if data is not None:
            self.team_ids: list = data.get('team_ids')
            self.ssh_port: int = data.get('ssh_port')
            self.creation_time: int = data.get('creation_time')
            self.domain_names = data.get('domain_names')
            self.owner: str = data.get('owner')
            self.use_kgp: bool = data.get('use_kgp')
            self.id: str = data.get('id')
            self.extra_info: TunnelExtraInfo = TunnelExtraInfo(data.get('extra_info'))
            self.direct_domains = data.get('direct_domains')
            self.vm_version: str = data.get('vm_version')
            self.no_ssl_bump_domains = data.get('no_ssl_bump_domains')
            self.shared_tunnel: bool = data.get('shared_tunnel')
            self.metadata: TunnelMetadata = TunnelMetadata(data.get('metadata'))
            self.status: str = data.get('status')
            self.shutdown_time = data.get('shutdown_time')
            self.host: str = data.get('host')
            self.ip_address = data.get('ip_address')
            self.last_connected: int = data.get('last_connected')
            self.user_shutdown = data.get('user_shutdown')
            self.use_caching_proxy = data.get('use_caching_proxy')
            self.launch_time: int = data.get('launch_time')
            self.no_proxy_caching: bool = data.get('no_proxy_caching')
            self.tunnel_identifier: str = data.get('tunnel_identifier')

    def __str__(self):
        return self.tunnel_identifier


class TunnelExtraInfo:
    def __init__(self, data: str):
        if data is not None:
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                pass
            else:
                self.tunnel_cert: str = data.get('tunnel_cert')
                self.inject_job_id: bool = data.get('inject_job_id')
                self.backend: str = data.get('backend')


class TunnelMetadata:
    def __init__(self, data: dict):
        if data is not None and isinstance(data, dict):
            self.hostname: str = data.get('hostname')
            self.command_args: TunnelMetadataCommandArgs = TunnelMetadataCommandArgs(data.get('command_args'))
            self.git_version: str = data.get('git_version')
            self.platform: str = data.get('platform')
            self.command: str = data.get('command')
            self.build: str = data.get('build')
            self.release: str = data.get('release')
            self.nofile_limit: int = data.get('nofile_limit')

    def __str__(self):
        return self.hostname


class TunnelMetadataCommandArgs:
    def __init__(self, data: str):
        if data is not None:
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                pass
            else:
                self.api_key: str = data.get('api-key')
                self.auth: list = data.get('auth')
                self.cainfo: str = data.get('cainfo')
                self.capath: str = data.get('capath')
                self.certificate: str = data.get('certificate')
                self.config_file: str = data.get('config-file')
                self.default_rest_url: str = data.get('default-rest-url')
                self.direct_domains: list = data.get('direct-domains')
                self.dns: list = data.get('dns')
                self.doctor: bool = data.get('doctor')
                self.ext: str = data.get('ext')
                self.ext_port: int = data.get('ext-port')
                self.extra_info: str = data.get('extra-info')
                self.fast_fail_regexps: list = data.get('fast-fail-regexps')
                self.jobwaittimeout: int = data.get('jobwaittimeout')
                self.key: str = data.get('key')
                self.kgp_handshake_timeout: str = data.get('kgp-handshake-timeout')
                self.kgp_host: str = data.get('kgp-host')
                self.kgp_hostname: str = data.get('kgp-hostname')
                self.kgp_port: int = data.get('kgp-port')
                self.log_stats: str = data.get('log-stats')
                self.logfile: str = data.get('logfile')
                self.max_logsize: int = data.get('max-logsize')
                self.max_missed_acks: int = data.get('max-missed-acks')
                self.metrics_address: str = data.get('metrics-address')
                self.no_autodetect: bool = data.get('no-autodetect')
                self.no_cert_verify: bool = data.get('no-cert-verify')
                self.no_http_cert_verify: bool = data.get('no-http-cert-verify')
                self.no_ocsp_verify: bool = data.get('no-ocsp-verify')
                self.no_proxy_caching: bool = data.get('no-proxy-caching')
                self.no_remove_colliding_tunnels: bool = data.get('no-remove-colliding-tunnels')
                self.no_ssl_bump_domains: list = data.get('no-ssl-bump-domains')
                self.ocsp: str = data.get('ocsp')
                self.output_config: bool = data.get('output-config')
                self.pac: str = data.get('pac')
                self.pac_auth: list = data.get('pac-auth')
                self.pidfile: str = data.get('pidfile')
                self.proxy: str = data.get('proxy')
                self.proxy_localhost: bool = data.get('proxy-localhost')
                self.proxy_tunnel: bool = data.get('proxy-tunnel')
                self.proxy_userpwd: str = data.get('proxy-userpwd')
                self.readyfile: str = data.get('readyfile')
                self.reconnect: bool = data.get('reconnect')
                self.region: str = data.get('region')
                self.rest_url: str = data.get('rest-url')
                self.scproxy_port: int = data.get('scproxy-port')
                self.scproxy_read_limit: int = data.get('scproxy-read-limit')
                self.scproxy_write_limit: int = data.get('scproxy-write-limit')
                self.se_port: int = data.get('se-port')
                self.server: bool = data.get('server')
                self.shared_tunnel: bool = data.get('shared-tunnel')
                self.start_timeout: str = data.get('start-timeout')
                self.tls_legacy: bool = data.get('tls-legacy')
                self.tunnel_cainfo: str = data.get('tunnel-cainfo')
                self.tunnel_capath: str = data.get('tunnel-capath')
                self.tunnel_cert: str = data.get('tunnel-cert')
                self.tunnel_cert_suffix: str = data.get('tunnel-cert-suffix')
                self.tunnel_domains: list = data.get('tunnel-domains')
                self.tunnel_identifier: str = data.get('tunnel-identifier')
                self.tunnel_name: str = data.get('tunnel-name')
                self.tunnel_pool: bool = data.get('tunnel-pool')
                self.user: str = data.get('user')
                self.verbose: str = data.get('verbose')
                self.vm_version: str = data.get('vm-version')


class TunnelJobs:
    def __init__(self, data: dict):
        if data is not None:
            self.tunnel_id: str = data.get('id')
            self.jobs_running: int = data.get('jobs_running')


class StoppedTunnel:
    def __init__(self, data: dict):
        if data is not None:
            self.result: bool = data.get('result')
            self.tunnel_id: str = data.get('id')
            self.jobs_running: int = data.get('jobs_running')
