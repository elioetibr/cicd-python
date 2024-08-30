import json
import os
import re
from dataclasses import dataclass, field
from typing import Any, List, TypeVar, Type, cast, Callable, Dict

import yaml

from cicd.Utils import recursive_sort_dict_by_key

T = TypeVar("T")


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str | None)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


@dataclass
class AwsEnvironment:
    aws_account_id: int
    description: str
    enabled: bool
    environment: str

    @staticmethod
    def from_dict(obj: Any) -> 'AwsEnvironment':
        assert isinstance(obj, dict)
        aws_account_id = from_int(obj.get("aws_account_id"))
        description = from_str(obj.get("description"))
        enabled = from_bool(obj.get("enabled"))
        environment = from_str(obj.get("environment"))
        return AwsEnvironment(aws_account_id, description, enabled, environment)

    def to_dict(self) -> dict:
        result: dict = {}
        result["aws_account_id"] = from_int(self.aws_account_id)
        result["description"] = from_str(self.description)
        result["enabled"] = from_bool(self.enabled)
        result["environment"] = from_str(self.environment)
        return result


@dataclass
class EnvironmentPromotionPhases:
    def __init__(self, properties: Dict[str, AwsEnvironment]):
        for key, value in properties.items():
            setattr(self, key, value)

    @staticmethod
    def from_dict(obj: Any) -> 'EnvironmentPromotionPhases':
        assert isinstance(obj, dict)
        environments: Dict[str, AwsEnvironment] = {}
        for key, value in obj.items():
            environments[key] = AwsEnvironment.from_dict(value)
        return EnvironmentPromotionPhases(environments)

    def to_dict(self) -> dict:
        result: dict = {}
        result_dict = {key: value for key, value in self.__dict__.items() if isinstance(value, AwsEnvironment)}
        for key, value in result_dict.items():
            result[key] = to_class(AwsEnvironment, value)
        return result


@dataclass
class Environment:
    approval_for_promotion: bool
    aws_region: str
    cluster: str
    enabled: bool
    environment: str
    next_environment: str
    with_gate: bool

    def __init__(self, approval_for_promotion, aws_region, cluster, enabled, environment, next_environment, with_gate):
        self.approval_for_promotion = approval_for_promotion
        self.aws_region = aws_region
        self.cluster = cluster
        self.enabled = enabled
        self.environment = environment
        self.next_environment = next_environment
        self.with_gate = with_gate

    @staticmethod
    def from_dict(obj: Any) -> 'Environment':
        assert isinstance(obj, dict)
        approval_for_promotion = from_bool(obj.get("approval_for_promotion"))
        aws_region = from_str(obj.get("aws_region"))
        cluster = from_str(obj.get("cluster"))
        enabled = from_bool(obj.get("enabled"))
        environment = from_str(obj.get("environment"))
        next_environment = from_str(obj.get("next_environment"))
        with_gate = from_bool(obj.get("with_gate"))
        return Environment(approval_for_promotion, aws_region, cluster, enabled, environment, next_environment, with_gate)

    def to_dict(self) -> dict:
        result: dict = {}
        result["approval_for_promotion"] = from_bool(self.approval_for_promotion)
        result["aws_region"] = from_str(self.aws_region)
        result["cluster"] = from_str(self.cluster)
        result["enabled"] = from_bool(self.enabled)
        result["environment"] = from_str(self.environment)
        result["next_environment"] = from_str(self.next_environment)
        result["with_gate"] = from_bool(self.with_gate)
        final_result = recursive_sort_dict_by_key(result)
        return final_result


@dataclass
class EnvironmentWithAdditionalRegions(Environment):
    additional_aws_regions: List[Any]

    def __init__(self, additional_aws_regions, approval_for_promotion, aws_region, cluster, enabled, environment, next_environment, with_gate):
        super().__init__(approval_for_promotion, aws_region, cluster, enabled, environment, next_environment, with_gate)
        self.additional_aws_regions = additional_aws_regions

    @staticmethod
    def from_dict(obj: Any) -> 'EnvironmentWithAdditionalRegions':
        assert isinstance(obj, dict)
        additional_aws_regions = from_list(lambda x: x, obj.get("additional_aws_regions"))
        approval_for_promotion = from_bool(obj.get("approval_for_promotion"))
        aws_region = from_str(obj.get("aws_region"))
        cluster = from_str(obj.get("cluster"))
        enabled = from_bool(obj.get("enabled"))
        environment = from_str(obj.get("environment"))
        next_environment = from_str(obj.get("next_environment"))
        with_gate = from_bool(obj.get("with_gate"))
        return EnvironmentWithAdditionalRegions(additional_aws_regions, approval_for_promotion, aws_region, cluster, enabled, environment, next_environment,
                                                with_gate)

    def to_dict(self) -> dict:
        result: dict = {}
        result["additional_aws_regions"] = from_list(lambda x: x, self.additional_aws_regions)
        result["approval_for_promotion"] = from_bool(self.approval_for_promotion)
        result["aws_region"] = from_str(self.aws_region)
        result["cluster"] = from_str(self.cluster)
        result["enabled"] = from_bool(self.enabled)
        result["environment"] = from_str(self.environment)
        result["next_environment"] = from_str(self.next_environment)
        result["with_gate"] = from_bool(self.with_gate)
        return recursive_sort_dict_by_key(result)


@dataclass
class Environments:
    def __init__(self, properties: Dict[str, EnvironmentWithAdditionalRegions]):
        for key, value in properties.items():
            setattr(self, key, value)

    @staticmethod
    def from_dict(obj: Any) -> 'Environments':
        assert isinstance(obj, dict)
        environments: Dict[str, EnvironmentWithAdditionalRegions] = {}
        for key, value in obj.items():
            environments[key] = EnvironmentWithAdditionalRegions.from_dict(value)
        return Environments(environments)

    def to_dict(self) -> dict:
        result: dict = {}
        result_dict = {key: value for key, value in self.__dict__.items() if isinstance(value, EnvironmentWithAdditionalRegions)}
        for key, value in result_dict.items():
            result[key] = to_class(EnvironmentWithAdditionalRegions, value)
        return result


@dataclass
class Paths:
    has_modifications: bool
    paths: List[str]

    @staticmethod
    def from_dict(obj: Any) -> 'Paths':
        assert isinstance(obj, dict)
        has_modifications = from_bool(obj.get("hasModifications"))
        paths = from_list(from_str, obj.get("paths"))
        return Paths(has_modifications, paths)

    def to_dict(self) -> dict:
        result: dict = {}
        result["hasModifications"] = from_bool(self.has_modifications)
        result["paths"] = from_list(from_str, self.paths)
        return result


@dataclass
class PathMonitor:
    def __init__(self, properties: Dict[str, Paths]):
        for key, value in properties.items():
            setattr(self, key, value)

    @staticmethod
    def from_dict(obj: Any) -> 'PathMonitor':
        assert isinstance(obj, dict)
        environments: Dict[str, Paths] = {}
        for key, value in obj.items():
            environments[key] = Paths.from_dict(value)
        return PathMonitor(environments)

    def to_dict(self) -> dict:
        result: dict = {}
        result_dict = {key: value for key, value in self.__dict__.items() if isinstance(value, Paths)}
        for key, value in result_dict.items():
            result[key] = to_class(Paths, value)
        return result


@dataclass
class Channel:
    channel_id: str
    channel_name: str

    @staticmethod
    def from_dict(obj: Any) -> 'Channel':
        assert isinstance(obj, dict)
        channel_id = from_str(obj.get("id"))
        channel_name = from_str(obj.get("name"))
        return Channel(channel_id, channel_name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_str(self.channel_id)
        result["name"] = from_str(self.channel_name)
        return result


@dataclass
class ChannelsConfigurations:
    cd: List[Channel]
    ci: List[Channel]

    @staticmethod
    def from_dict(obj: Any) -> 'ChannelsConfigurations':
        assert isinstance(obj, dict)
        cd = from_list(Channel.from_dict, obj.get("cd"))
        ci = from_list(Channel.from_dict, obj.get("ci"))
        return ChannelsConfigurations(cd, ci)

    def to_dict(self) -> dict:
        result: dict = {}
        result["cd"] = from_list(lambda x: to_class(Channel, x), self.cd)
        result["ci"] = from_list(lambda x: to_class(Channel, x), self.ci)
        return result


@dataclass
class Channels:
    def __init__(self, properties: Dict[str, Paths]):
        for key, value in properties.items():
            setattr(self, key, value)

    @staticmethod
    def from_dict(obj: Any) -> 'Channels':
        assert isinstance(obj, dict)
        channels: Dict[str, ChannelsConfigurations] = {}
        for key, value in obj.items():
            channels[key] = ChannelsConfigurations.from_dict(value)
        return Channels(channels)

    def to_dict(self) -> dict:
        result: dict = {}
        result_dict = {key: value for key, value in self.__dict__.items() if isinstance(value, ChannelsConfigurations)}
        for key, value in result_dict.items():
            result[key] = to_class(ChannelsConfigurations, value)
        return result


@dataclass
class Slack:
    channels: Channels
    url: str

    @staticmethod
    def from_dict(obj: Any) -> 'Slack':
        assert isinstance(obj, dict)
        channels = Channels.from_dict(obj.get("channels"))
        url = from_str(obj.get("url"))
        return Slack(channels, url)

    def to_dict(self) -> dict:
        result: dict = {}
        result["channels"] = to_class(Channels, self.channels)
        result["url"] = from_str(self.url)
        return result


@dataclass
class Application:
    app_of_apps: str
    app_of_apps_service_name: str
    app_repo: str
    dockerfile: str
    ecr_repository_name: str
    enable_tests: bool
    helm_chart_repo: str
    helm_chart_repo_path: str
    is_mono_repo: bool
    name: str
    service: str

    def __init__(self, app_of_apps, app_of_apps_service_name, app_repo, dockerfile, ecr_repository_name, enable_tests,
                 helm_chart_repo, helm_chart_repo_path, is_mono_repo, name, service):
        self.app_of_apps = app_of_apps
        self.app_of_apps_service_name = app_of_apps_service_name
        self.app_repo = app_repo
        self.dockerfile = dockerfile
        self.ecr_repository_name = ecr_repository_name
        self.enable_tests = enable_tests
        self.helm_chart_repo = helm_chart_repo
        self.helm_chart_repo_path = helm_chart_repo_path
        self.is_mono_repo = is_mono_repo
        self.name = name
        self.service = service

    @staticmethod
    def from_dict(obj: Any) -> 'Application':
        assert isinstance(obj, dict)
        app_of_apps = from_str(obj.get("app_of_apps"))
        app_of_apps_service_name = from_str(obj.get("app_of_apps_service_name"))
        app_repo = from_str(obj.get("app_repo"))
        dockerfile = from_str(obj.get("dockerfile"))
        ecr_repository_name = from_str(obj.get("ecr_repository_name"))
        enable_tests = from_bool(obj.get("enable_tests"))
        helm_chart_repo = from_str(obj.get("helm_chart_repo"))
        helm_chart_repo_path = from_str(obj.get("helm_chart_repo_path", None))
        is_mono_repo = from_bool(obj.get("is_mono_repo"))
        name = from_str(obj.get("name"))
        service = from_str(obj.get("service"))
        return Application(app_of_apps, app_of_apps_service_name, app_repo, dockerfile, ecr_repository_name, enable_tests,
                           helm_chart_repo, helm_chart_repo_path, is_mono_repo, name, service)

    def to_dict(self) -> dict:
        result: dict = {}
        result["app_of_apps"] = from_str(self.app_of_apps)
        result["app_of_apps_service_name"] = from_str(self.app_of_apps_service_name)
        result["app_repo"] = from_str(self.app_repo)
        result["dockerfile"] = from_str(self.dockerfile)
        result["ecr_repository_name"] = from_str(self.ecr_repository_name)
        result["enable_tests"] = from_bool(self.enable_tests)
        result["helm_chart_repo"] = from_str(self.helm_chart_repo)
        result["helm_chart_repo_path"] = from_str(self.helm_chart_repo_path)
        result["is_mono_repo"] = from_bool(self.is_mono_repo)
        result["name"] = from_str(self.name)
        result["service"] = from_str(self.service)
        return result


@dataclass
class Version:
    sem_ver: str
    version: str
    major: int
    minor: int
    patch: int
    __regex: str = r"(.*)((\d+)\.(\d+)\.(\d+))(.*)"

    def __init__(self, version: str):
        self.__set_version(version)

    @staticmethod
    def __ensure_semantic_version_prefix(version: str) -> str:
        if version.startswith('v'):
            return version
        else:
            return f'v{version}'

    def __set_version(self, version: str):

        version = self.__ensure_semantic_version_prefix(version)
        result = re.sub(self.__regex, "\\3.\\4.\\5", version, 0, re.MULTILINE).split('.')
        self.version = version
        self.sem_ver = f'{result[0]}.{result[1]}.{result[2]}'
        self.major = int(result[0])
        self.minor = int(result[1])
        self.patch = int(result[2])


@dataclass
class GitOps(Application):
    environment_promotion_phases: EnvironmentPromotionPhases
    environments: Environments
    path_monitor: PathMonitor
    slack: Slack

    def __init__(self, app_of_apps, app_of_apps_service_name, app_repo, dockerfile, ecr_repository_name, enable_tests, environment_promotion_phases,
                 environments, helm_chart_repo, helm_chart_repo_path, is_mono_repo, name, path_monitor, service, slack):
        super().__init__(app_of_apps, app_of_apps_service_name, app_repo, dockerfile, ecr_repository_name, enable_tests,
                         helm_chart_repo, helm_chart_repo_path, is_mono_repo, name, service)
        self.environment_promotion_phases = environment_promotion_phases
        self.environments = environments
        self.path_monitor = path_monitor
        self.slack = slack

    @staticmethod
    def from_dict(obj: Any) -> 'GitOps':
        assert isinstance(obj, dict)
        app_of_apps = from_str(obj.get("app_of_apps"))
        app_of_apps_service_name = from_str(obj.get("app_of_apps_service_name"))
        app_repo = from_str(obj.get("app_repo"))
        dockerfile = from_str(obj.get("dockerfile"))
        ecr_repository_name = from_str(obj.get("ecr_repository_name"))
        enable_tests = from_bool(obj.get("enable_tests"))
        environment_promotion_phases = EnvironmentPromotionPhases.from_dict(obj.get("environment_promotion_phases"))
        environments = Environments.from_dict(obj.get("environments"))
        helm_chart_repo = from_str(obj.get("helm_chart_repo"))
        helm_chart_repo_path = from_str(obj.get("helm_chart_repo_path"))
        is_mono_repo = from_bool(obj.get("is_mono_repo"))
        name = from_str(obj.get("name"))
        path_monitor = PathMonitor.from_dict(obj.get("path_monitor"))
        service = from_str(obj.get("service"))
        slack = Slack.from_dict(obj.get("slack"))
        return GitOps(app_of_apps, app_of_apps_service_name, app_repo, dockerfile, ecr_repository_name, enable_tests, environment_promotion_phases,
                      environments, helm_chart_repo, helm_chart_repo_path, is_mono_repo, name, path_monitor, service, slack)

    def to_dict(self) -> dict:
        result: dict = {}
        result["app_of_apps"] = from_str(self.app_of_apps)
        result["app_of_apps_service_name"] = from_str(self.app_of_apps_service_name)
        result["app_repo"] = from_str(self.app_repo)
        result["dockerfile"] = from_str(self.dockerfile)
        result["ecr_repository_name"] = from_str(self.ecr_repository_name)
        result["enable_tests"] = from_bool(self.enable_tests)
        result["environment_promotion_phases"] = to_class(EnvironmentPromotionPhases, self.environment_promotion_phases)
        result["environments"] = to_class(Environments, self.environments)
        result["helm_chart_repo"] = from_str(self.helm_chart_repo)
        result["helm_chart_repo_path"] = from_str(self.helm_chart_repo_path)
        result["is_mono_repo"] = from_bool(self.is_mono_repo)
        result["name"] = from_str(self.name)
        result["path_monitor"] = to_class(PathMonitor, self.path_monitor)
        result["service"] = from_str(self.service)
        result["slack"] = to_class(Slack, self.slack)
        return result


class GitOpsManager:
    @staticmethod
    def from_dict(s: Any) -> GitOps:
        return GitOps.from_dict(s)

    @staticmethod
    def to_dict(x: GitOps) -> Dict[str, Any]:
        return recursive_sort_dict_by_key(to_class(GitOps, x))


class Manifest(Application, Environment):
    app_version: str
    helm_chart_version: str
    branch: str

    def __init__(self, branch: str, app: Application, env: Environment):
        Application.__init__(self, app.app_of_apps, app.app_of_apps_service_name, app.app_repo,
                             app.dockerfile, app.ecr_repository_name, app.enable_tests,
                             app.helm_chart_repo, app.helm_chart_repo_path,
                             app.is_mono_repo, app.name, app.service)

        Environment.__init__(self, env.approval_for_promotion, env.aws_region,
                             env.cluster, env.enabled, env.environment,
                             env.next_environment, env.with_gate)
        self.app_version = None
        self.helm_chart_version = None
        self.branch = branch

    def to_dict(self) -> dict:
        result: dict = {}
        result["app_of_apps"] = from_str(self.app_of_apps)
        result["app_of_apps_service_name"] = from_str(self.app_of_apps_service_name)
        result["app_repo"] = from_str(self.app_repo)
        result["app_version"] = from_str(self.app_version)
        result["approval_for_promotion"] = from_bool(self.approval_for_promotion)
        result["aws_region"] = from_str(self.aws_region)
        result["branch"] = from_str(self.branch)
        result["cluster"] = from_str(self.cluster)
        result["dockerfile"] = from_str(self.dockerfile)
        result["ecr_repository_name"] = from_str(self.ecr_repository_name)
        result["enable_tests"] = from_bool(self.enable_tests)
        result["enabled"] = from_bool(self.enabled)
        result["environment"] = from_str(self.environment)
        result["helm_chart_repo"] = from_str(self.helm_chart_repo)
        result["helm_chart_repo_path"] = from_str(self.helm_chart_repo_path)
        result["helm_chart_version"] = from_str(self.helm_chart_version)
        result["is_mono_repo"] = from_bool(self.is_mono_repo)
        result["name"] = from_str(self.name)
        result["next_environment"] = from_str(self.next_environment)
        result["service"] = from_str(self.service)
        result["with_gate"] = from_bool(self.with_gate)
        return recursive_sort_dict_by_key(result)


class ManifestManager:
    gitops: GitOps = field(default_factory=None)

    def __init__(self, gitops: GitOps):
        self.gitops = gitops

    def __get_application(self) -> Application:
        try:
            application: Application = cast(Application, self.gitops)
            return application
        except AttributeError as ex:
            raise Exception(ex)

    def __get_environment(self, env: str) -> Environment:
        try:
            environment: Environment = getattr(self.gitops.environments, env)
            return cast(Environment, environment)
        except AttributeError:
            attr_keys = self.gitops.environments.to_dict().keys()
            raise Exception(f'The Environment "{env}" '
                            f'does not exist. Available Environment{'s are' if len(attr_keys) > 1 else ' is'}: '
                            f'"{', '.join(attr_keys)}"')

    def get_manifest(self, branch: str, env: str, version: str) -> Manifest:
        try:
            version: Version = Version(version)
            application: Application = self.__get_application()
            environment: Environment = self.__get_environment(env)
            return Manifest(branch, application, environment)
        except AttributeError as ex:
            raise Exception(ex)


if __name__ == '__main__':  # pragma: no cover
    fixtures = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'fixtures')
    fixtures_outputs = os.path.join(fixtures, 'outputs')
    gitops_yaml_file = os.path.join(fixtures, 'gitops.yaml')
    with open(gitops_yaml_file, 'r') as file:
        try:
            gitops_yaml_file_to_dict = yaml.safe_load(file)
        except Exception as e:
            raise e

    gitops_manager = GitOpsManager.from_dict(gitops_yaml_file_to_dict)
    manager = ManifestManager(gitops_manager)
    manifest = manager.get_manifest('main', 'demos', 'v1.0.0')
    manifest_dict = manifest.to_dict()
    print(manifest_dict)
    print(json.dumps(manifest_dict, sort_keys=True, indent=None, separators=None))
    print()
