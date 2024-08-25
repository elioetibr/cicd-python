#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass, fields
from typing import Any, List

from cicd.Abstracts import Abstract
from cicd.Utils import from_str, to_class, from_bool, from_list, from_int, parse_dict_to_obj


@dataclass
class AwsAccount:
    aws_account_id: int
    description: str
    environment: str
    enabled: bool

    @staticmethod
    def from_dict(obj: Any) -> 'AwsAccount':
        if not isinstance(obj, dict):
            raise TypeError(f"Expected dictionary but got {type(obj).__name__}")
        try:
            aws_account_id = from_int(obj.get("aws_account_id"))
            description = from_str(obj.get("description"))
            environment = from_str(obj.get("environment"))
            enabled = from_bool(obj.get("enabled"))
        except (TypeError, ValueError) as e:
            raise ValueError(f"Error parsing AwsAccount: {e}")
        return AwsAccount(aws_account_id, description, environment, enabled)

    def to_dict(self) -> dict:
        return {
            "aws_account_id": from_int(self.aws_account_id),
            "description": from_str(self.description),
            "environment": from_str(self.environment),
            "enabled": from_bool(self.enabled)
        }


@dataclass
class EnvironmentPromotionPhases(Abstract):
    def __init__(self, accounts: dict[str, AwsAccount]):
        super().__init__(accounts)

    @staticmethod
    def from_dict(obj: Any) -> 'EnvironmentPromotionPhases':
        assert isinstance(obj, dict)
        accounts_dict = {
            env_name: AwsAccount.from_dict(aws_account_config_data)
            for env_name, aws_account_config_data in obj.items()
        }
        result = EnvironmentPromotionPhases(accounts_dict)
        return result

    def to_dict(self) -> dict:
        result: dict = {env_name: to_class(AwsAccount, aws_account_config_data)
                        for env_name, aws_account_config_data
                        in self.__dict__.items()}
        return result


@dataclass
class Environment(Abstract):
    aws_region: str
    cluster: str
    environment: str
    next_environment: str
    approval_for_promotion: bool
    enabled: bool
    with_gate: bool

    @staticmethod
    def from_dict(obj: Any) -> 'Environment':
        assert isinstance(obj, dict)
        environment_config = {env_name: Environment.from_dict(environment_config_data)
                              for env_name, environment_config_data in obj.items()}
        result = Environments(environment_config)
        return result

    def to_dict(self) -> dict:
        result: dict = {
            "aws_region": from_str(self.aws_region),
            "cluster": from_str(self.cluster),
            "environment": from_str(self.environment),
            "next_environment": from_str(self.next_environment),
            "approval_for_promotion": from_bool(self.approval_for_promotion),
            "enabled": from_bool(self.enabled),
            "with_gate": from_bool(self.with_gate)
        }
        return result


@dataclass
class EnvironmentWithRegion(Environment):
    additional_aws_regions: List[Any]

    @staticmethod
    def from_dict(obj: Any) -> 'EnvironmentWithRegion':
        parse_map = {
            "aws_region": from_str,
            "cluster": from_str,
            "environment": from_str,
            "next_environment": from_str,
            "additional_aws_regions": lambda x: from_list(lambda y: y, x),
            "approval_for_promotion": from_bool,
            "enabled": from_bool,
            "with_gate": from_bool
        }
        parsed = parse_dict_to_obj(parse_map, obj)
        return EnvironmentWithRegion(**parsed)

    def to_dict(self) -> dict:
        result: dict = {
            "aws_region": from_str(self.aws_region),
            "cluster": from_str(self.cluster),
            "environment": from_str(self.environment),
            "next_environment": from_str(self.next_environment),
            "additional_aws_regions": from_list(lambda x: x, self.additional_aws_regions),
            "approval_for_promotion": from_bool(self.approval_for_promotion),
            "enabled": from_bool(self.enabled),
            "with_gate": from_bool(self.with_gate)
        }
        return result


@dataclass
class Environments(Abstract):
    def __init__(self, environment: dict[str, EnvironmentWithRegion]):
        super().__init__(environment)

    @staticmethod
    def from_dict(obj: Any) -> 'Environments':
        assert isinstance(obj, dict)
        environment_config = {env_name: EnvironmentWithRegion.from_dict(environment_config_data)
                              for env_name, environment_config_data in obj.items()}
        result = Environments(environment_config)
        return result

    def to_dict(self) -> dict:
        result: dict = {
            env_name: to_class(EnvironmentWithRegion, environment_config_data)
            for env_name, environment_config_data
            in self.__dict__.items()
        }
        return result


@dataclass
class PathConfiguration:
    has_modifications: bool
    paths: List[str]

    @staticmethod
    def from_dict(obj: Any) -> 'PathConfiguration':
        assert isinstance(obj, dict)
        has_modifications = from_bool(obj.get("hasModifications", False))
        paths = from_list(from_str, obj.get("paths"))
        return PathConfiguration(has_modifications, paths)

    def to_dict(self) -> dict:
        result: dict = {"hasModifications": from_bool(self.has_modifications), "paths": from_list(from_str, self.paths)}
        return result


@dataclass
class PathMonitor(Abstract):
    def __init__(self, paths: dict[str, PathConfiguration]):
        super().__init__(paths)

    @staticmethod
    def from_dict(obj: Any) -> 'PathMonitor':
        assert isinstance(obj, dict)
        path_config = {path: PathConfiguration.from_dict(path_monitor_config_data)
                       for path, path_monitor_config_data in obj.items()}
        result = PathMonitor(path_config)
        return result

    def to_dict(self) -> dict:
        result: dict = {
            path: to_class(PathConfiguration, path_config_data)
            for path, path_config_data
            in self.__dict__.items()
        }
        return result


@dataclass
class SlackChannel:
    channel_id: str
    channel_name: str

    @staticmethod
    def from_dict(obj: Any) -> 'SlackChannel':
        assert isinstance(obj, dict)
        channel_id = from_str(obj.get("id"))
        channel_name = from_str(obj.get("name"))
        return SlackChannel(channel_id, channel_name)

    def to_dict(self) -> dict:
        result: dict = {"id": from_str(self.channel_id), "name": from_str(self.channel_name)}
        return result


@dataclass
class SlackEnvironmentChannels:
    cd: List[SlackChannel]
    ci: List[SlackChannel]

    @staticmethod
    def from_dict(obj: Any) -> 'SlackEnvironmentChannels':
        assert isinstance(obj, dict)
        cd = from_list(SlackChannel.from_dict, obj.get("cd"))
        ci = from_list(SlackChannel.from_dict, obj.get("ci"))
        return SlackEnvironmentChannels(cd, ci)

    def to_dict(self) -> dict:
        result: dict = {
            "cd": from_list(lambda x: to_class(SlackChannel, x), self.cd),
            "ci": from_list(lambda x: to_class(SlackChannel, x), self.ci)
        }
        return result


@dataclass
class SlackChannels(Abstract):
    def __init__(self, slack_channels: dict[str, SlackChannel]) -> None:
        super().__init__(slack_channels)

    @staticmethod
    def from_dict(obj: Any) -> 'SlackEnvironmentChannels':
        assert isinstance(obj, dict)
        channel_configs = {channel: SlackEnvironmentChannels.from_dict(channel_data)
                           for channel, channel_data in obj.items()}
        result = SlackChannels(channel_configs)
        return result

    def to_dict(self) -> dict:
        result: dict = {}
        for channel, channel_data in self.__dict__.items():
            channel_class = to_class(SlackEnvironmentChannels, channel_data)
            result.update({channel: channel_class})
        return result


@dataclass
class SlackConfig:
    url: str
    channels: SlackChannels

    @staticmethod
    def from_dict(obj: Any) -> 'SlackConfig':
        assert isinstance(obj, dict)
        url = from_str(obj.get("url"))
        channels = SlackChannels.from_dict(obj.get("channels"))
        return SlackConfig(url, channels)

    def to_dict(self) -> dict:
        result: dict = {"url": from_str(self.url), "channels": to_class(SlackChannels, self.channels)}
        return result


@dataclass
class ApplicationConfig(Abstract):
    app_of_apps: str
    app_of_apps_service_name: str
    app_repo: str
    dockerfile: str
    ecr_repository_name: str
    enable_tests: bool
    helm_chart_repo: str
    helm_chart_service_name: str
    is_mono_repo: bool
    name: str
    service: str


@dataclass
class GitOps(ApplicationConfig):
    environment_promotion_phases: EnvironmentPromotionPhases
    environments: Environments
    path_monitor: PathMonitor
    slack: SlackConfig

    @staticmethod
    def from_dict(obj: Any) -> 'GitOps':
        assert isinstance(obj, dict)
        app_of_apps = from_str(obj.get("app_of_apps"))
        app_of_apps_service_name = from_str(obj.get("app_of_apps_service_name"))
        app_repo = from_str(obj.get("app_repo"))
        dockerfile = from_str(obj.get("dockerfile"))
        ecr_repository_name = from_str(obj.get("ecr_repository_name"))
        enable_tests = from_bool(obj.get("enable_tests"))
        helm_chart_repo = from_str(obj.get("helm_chart_repo"))
        helm_chart_service_name = from_str(obj.get("helm_chart_service_name"))
        is_mono_repo = from_bool(obj.get("is_mono_repo"))
        name = from_str(obj.get("name"))
        service = from_str(obj.get("service"))
        environment_promotion_phases = EnvironmentPromotionPhases.from_dict(obj.get("environment_promotion_phases"))
        environments = Environments.from_dict(obj.get("environments"))
        path_monitor = PathMonitor.from_dict(obj.get("path_monitor"))
        slack = SlackConfig.from_dict(obj.get("slack"))
        return GitOps(app_of_apps, app_of_apps_service_name, app_repo, dockerfile, ecr_repository_name, enable_tests,
                      helm_chart_repo, helm_chart_service_name, is_mono_repo, name, service,
                      environment_promotion_phases, environments, path_monitor, slack)

    def to_dict(self) -> dict:
        result: dict = {
            "app_of_apps": from_str(self.app_of_apps),
            "app_of_apps_service_name": from_str(self.app_of_apps_service_name),
            "app_repo": from_str(self.app_repo),
            "dockerfile": from_str(self.dockerfile),
            "ecr_repository_name": from_str(self.ecr_repository_name),
            "enable_tests": from_bool(self.enable_tests),
            "helm_chart_repo": from_str(self.helm_chart_repo),
            "helm_chart_service_name": from_str(self.helm_chart_service_name),
            "is_mono_repo": from_bool(self.is_mono_repo),
            "name": from_str(self.name),
            "service": from_str(self.service),
            "environment_promotion_phases": to_class(EnvironmentPromotionPhases, self.environment_promotion_phases),
            "environments": to_class(Environments, self.environments),
            "path_monitor": to_class(PathMonitor, self.path_monitor),
            "slack": to_class(SlackConfig, self.slack)
        }
        return result


@dataclass
class Manifest(ApplicationConfig, Environment):
    @classmethod
    def from_gitops(cls, gitops: GitOps, environment_name: str = 'dev') -> 'Manifest':
        manifest_fields: list[str] = sorted(list(cls.__dataclass_fields__.keys()))
        environment_with_region: EnvironmentWithRegion = getattr(gitops.environments, environment_name)
        temp_environment_fields: list[str] = sorted([attr.name for attr in fields(environment_with_region)])
        environment_fields: list[str] = sorted(list(set(temp_environment_fields).intersection(manifest_fields)))

        processed_fields: list[str] = []
        for attr in environment_fields:
            setattr(cls, attr, getattr(environment_with_region, attr))
            processed_fields.append(attr)

        application_fields = sorted(list(set(manifest_fields).difference(processed_fields)))
        manifest_fields = sorted(list(set(manifest_fields).intersection(application_fields)))
        for attr in manifest_fields:
            setattr(cls, attr, getattr(gitops, attr))

        return cls


def gitops_from_dict(s: Any) -> GitOps:
    return GitOps.from_dict(s)


def gitops_to_dict(x: GitOps) -> Any:
    return to_class(GitOps, x)
