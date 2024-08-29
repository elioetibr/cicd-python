from dataclasses import dataclass, fields
from typing import Any, List, TypeVar, Type, cast, Callable, Dict

from cicd.Utils import recursive_sort_dict_by_key

T = TypeVar("T")


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
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
class Manifest:
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


    def __init__(self, properties: Dict[str, Any]):
        if properties is None:
            self.__class__ = None
        class_fields = fields(self)
        for key, value in properties.items():
            setattr(self, key, value)

    @staticmethod
    def from_dict(obj: Any) -> 'Manifest':
        assert isinstance(obj, dict)
        class_fields = fields(Manifest)
        manifest: Dict[str, Any] = {}
        for idx, field in enumerate(class_fields):
            manifest[field.name] = Manifest.from_dict(obj[field.name])
        return Manifest(manifest)

    def to_dict(self) -> dict:
        result: dict = {}
        for key, value in self.__dict__.items():
            if key.startswith('__') or key.startswith('_'):
                continue
            result[key] = to_class(Manifest, value)
        return result

    # @staticmethod
    # def from_dict(obj: Any) -> 'Manifest':
    #     assert isinstance(obj, dict)
    #     app_of_apps = from_str(obj.get("app_of_apps"))
    #     app_of_apps_service_name = from_str(obj.get("app_of_apps_service_name"))
    #     app_repo = from_str(obj.get("app_repo"))
    #     dockerfile = from_str(obj.get("dockerfile"))
    #     ecr_repository_name = from_str(obj.get("ecr_repository_name"))
    #     enable_tests = from_bool(obj.get("enable_tests"))
    #     helm_chart_repo = from_str(obj.get("helm_chart_repo"))
    #     helm_chart_repo_path = from_str(obj.get("helm_chart_repo_path", None))
    #     is_mono_repo = from_bool(obj.get("is_mono_repo"))
    #     name = from_str(obj.get("name"))
    #     service = from_str(obj.get("service"))
    #     return Manifest(app_of_apps, app_of_apps_service_name, app_repo, dockerfile, ecr_repository_name, enable_tests,
    #                     helm_chart_repo, helm_chart_repo_path, is_mono_repo, name, service)
    #
    # def to_dict(self) -> dict:
    #     result: dict = {}
    #     result["app_of_apps"] = from_str(self.app_of_apps)
    #     result["app_of_apps_service_name"] = from_str(self.app_of_apps_service_name)
    #     result["app_repo"] = from_str(self.app_repo)
    #     result["dockerfile"] = from_str(self.dockerfile)
    #     result["ecr_repository_name"] = from_str(self.ecr_repository_name)
    #     result["enable_tests"] = from_bool(self.enable_tests)
    #     result["helm_chart_repo"] = from_str(self.helm_chart_repo)
    #     result["is_mono_repo"] = from_bool(self.is_mono_repo)
    #     result["name"] = from_str(self.name)
    #     result["service"] = from_str(self.service)
    #     return result


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
    dev: AwsEnvironment
    demo: AwsEnvironment
    prod: AwsEnvironment

    @staticmethod
    def from_dict(obj: Any) -> 'EnvironmentPromotionPhases':
        assert isinstance(obj, dict)
        dev = AwsEnvironment.from_dict(obj.get("01-dev"))
        demo = AwsEnvironment.from_dict(obj.get("02-demo"))
        prod = AwsEnvironment.from_dict(obj.get("03-prod"))
        return EnvironmentPromotionPhases(dev, demo, prod)

    def to_dict(self) -> dict:
        result: dict = {}
        result["01-dev"] = to_class(AwsEnvironment, self.dev)
        result["02-demo"] = to_class(AwsEnvironment, self.demo)
        result["03-prod"] = to_class(AwsEnvironment, self.prod)
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
        self.additional_aws_regions = additional_aws_regions
        super().__init__(approval_for_promotion, aws_region, cluster, enabled, environment, next_environment, with_gate)

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
        return EnvironmentWithAdditionalRegions(additional_aws_regions, approval_for_promotion, aws_region, cluster, enabled, environment, next_environment, with_gate)

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
        if properties is None:
            self.__class__ = None
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
        for key, value in self.__dict__.items():
            if key.startswith('__') or key.startswith('_'):
                continue
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
    application: Paths
    helm_charts: Paths

    @staticmethod
    def from_dict(obj: Any) -> 'PathMonitor':
        assert isinstance(obj, dict)
        application = Paths.from_dict(obj.get("application"))
        helm_charts = Paths.from_dict(obj.get("helm_charts"))
        return PathMonitor(application, helm_charts)

    def to_dict(self) -> dict:
        result: dict = {}
        result["application"] = to_class(Paths, self.application)
        result["helm_charts"] = to_class(Paths, self.helm_charts)
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
    def __init__(self, properties: Dict[str, ChannelsConfigurations]):
        if properties is None:
            self.__class__ = None
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
        for key, value in self.__dict__.items():
            if key.startswith('__') or key.startswith('_'):
                continue
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
class GitOps:
    app_of_apps: str
    app_of_apps_service_name: str
    app_repo: str
    dockerfile: str
    ecr_repository_name: str
    enable_tests: bool
    environment_promotion_phases: EnvironmentPromotionPhases
    environments: Environments
    helm_chart_repo: str
    helm_chart_service_name: str
    is_mono_repo: bool
    name: str
    path_monitor: PathMonitor
    service: str
    slack: Slack

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
        helm_chart_service_name = from_str(obj.get("helm_chart_service_name"))
        is_mono_repo = from_bool(obj.get("is_mono_repo"))
        name = from_str(obj.get("name"))
        path_monitor = PathMonitor.from_dict(obj.get("path_monitor"))
        service = from_str(obj.get("service"))
        slack = Slack.from_dict(obj.get("slack"))
        return GitOps(app_of_apps, app_of_apps_service_name, app_repo, dockerfile, ecr_repository_name, enable_tests, environment_promotion_phases, environments, helm_chart_repo, helm_chart_service_name, is_mono_repo, name, path_monitor, service, slack)

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
        result["helm_chart_service_name"] = from_str(self.helm_chart_service_name)
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

