#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Any, List

from cicd.CICD import CICD


@dataclass
class Application(CICD):
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

    def __init__(self, data: dict[str, Any]) -> None:
        super().__init__(data)


@dataclass
class AwsAccount(CICD):
    aws_account_id: int
    description: str
    environment: str
    enabled: bool

    def __init__(self, data: dict[str, Any]):
        super().__init__(data)


@dataclass
class Environment(CICD):
    approval_for_promotion: bool
    aws_region: str
    cluster: str
    enabled: bool
    environment: str
    next_environment: str
    with_gate: bool

    def __init__(self, data: dict[str, Any]):
        super().__init__(data)


@dataclass
class EnvironmentWithAdditionalRegions(Environment):
    additional_aws_regions: List[Any]

    def __init__(self, data: dict[str, Any]):
        super().__init__(data)


@dataclass
class Environments(CICD):
    def __init__(self, data: dict[str, Any]):
        super().__init__(data)


@dataclass
class EnvironmentPromotionPhases(AwsAccount):
    def __init__(self, data: dict[str, Any]):
        super().__init__(data)


# @dataclass
# class PathConfiguration:
#     has_modifications: bool
#     paths: List[str]
#
#     @staticmethod
#     def from_dict(obj: Any) -> 'PathConfiguration':
#         assert isinstance(obj, dict)
#         has_modifications = from_bool(obj.get("hasModifications", False))
#         paths = from_list(from_str, obj.get("paths"))
#         return PathConfiguration(has_modifications, paths)
#
#     def to_dict(self) -> dict:
#         result: dict = {"hasModifications": from_bool(self.has_modifications), "paths": from_list(from_str, self.paths)}
#         return result
#
#
# @dataclass
# class PathMonitor:
#     def __init__(self, paths: dict[str, PathConfiguration]):
#         super().__init__(paths)
#
#     @staticmethod
#     def from_dict(obj: Any) -> 'PathMonitor':
#         assert isinstance(obj, dict)
#         path_config = {path: PathConfiguration.from_dict(path_monitor_config_data)
#                        for path, path_monitor_config_data in obj.items()}
#         result = PathMonitor(path_config)
#         return result
#
#     def to_dict(self) -> dict:
#         result: dict = {
#             path: to_class(PathConfiguration, path_config_data)
#             for path, path_config_data
#             in self.__dict__.items()
#         }
#         return result
#
#
# @dataclass
# class SlackChannel:
#     channel_id: str
#     channel_name: str
#
#     @staticmethod
#     def from_dict(obj: Any) -> 'SlackChannel':
#         assert isinstance(obj, dict)
#         channel_id = from_str(obj.get("id"))
#         channel_name = from_str(obj.get("name"))
#         return SlackChannel(channel_id, channel_name)
#
#     def to_dict(self) -> dict:
#         result: dict = {"id": from_str(self.channel_id), "name": from_str(self.channel_name)}
#         return result
#
#
# @dataclass
# class SlackEnvironmentChannels:
#     cd: List[SlackChannel]
#     ci: List[SlackChannel]
#
#     @staticmethod
#     def from_dict(obj: Any) -> 'SlackEnvironmentChannels':
#         assert isinstance(obj, dict)
#         cd = from_list(SlackChannel.from_dict, obj.get("cd"))
#         ci = from_list(SlackChannel.from_dict, obj.get("ci"))
#         return SlackEnvironmentChannels(cd, ci)
#
#     def to_dict(self) -> dict:
#         result: dict = {
#             "cd": from_list(lambda x: to_class(SlackChannel, x), self.cd),
#             "ci": from_list(lambda x: to_class(SlackChannel, x), self.ci)
#         }
#         return result
#
#
# @dataclass
# class SlackChannels:
#     def __init__(self, slack_channels: dict[str, SlackChannel]) -> None:
#         super().__init__(slack_channels)
#
#     @staticmethod
#     def from_dict(obj: Any) -> 'SlackEnvironmentChannels':
#         assert isinstance(obj, dict)
#         channel_configs = {channel: SlackEnvironmentChannels.from_dict(channel_data)
#                            for channel, channel_data in obj.items()}
#         result = SlackChannels(channel_configs)
#         return result
#
#     def to_dict(self) -> dict:
#         result: dict = {}
#         for channel, channel_data in self.__dict__.items():
#             channel_class = to_class(SlackEnvironmentChannels, channel_data)
#             result.update({channel: channel_class})
#         return result
#
#
# @dataclass
# class SlackConfig:
#     url: str
#     channels: SlackChannels
#
#     @staticmethod
#     def from_dict(obj: Any) -> 'SlackConfig':
#         assert isinstance(obj, dict)
#         url = from_str(obj.get("url"))
#         channels = SlackChannels.from_dict(obj.get("channels"))
#         return SlackConfig(url, channels)
#
#     def to_dict(self) -> dict:
#         result: dict = {"url": from_str(self.url), "channels": to_class(SlackChannels, self.channels)}
#         return result


# @dataclass
# class GitOps(ApplicationConfig):
#     environment_promotion_phases: EnvironmentPromotionPhases
#     environments: Environments
#     path_monitor: PathMonitor
#     slack: SlackConfig
#
#     @staticmethod
#     def from_dict(obj: Any) -> 'GitOps':
#         assert isinstance(obj, dict)
#         app_of_apps = from_str(obj.get("app_of_apps"))
#         app_of_apps_service_name = from_str(obj.get("app_of_apps_service_name"))
#         app_repo = from_str(obj.get("app_repo"))
#         dockerfile = from_str(obj.get("dockerfile"))
#         ecr_repository_name = from_str(obj.get("ecr_repository_name"))
#         enable_tests = from_bool(obj.get("enable_tests"))
#         helm_chart_repo = from_str(obj.get("helm_chart_repo"))
#         helm_chart_service_name = from_str(obj.get("helm_chart_service_name"))
#         is_mono_repo = from_bool(obj.get("is_mono_repo"))
#         name = from_str(obj.get("name"))
#         service = from_str(obj.get("service"))
#         environment_promotion_phases = EnvironmentPromotionPhases.from_dict(obj.get("environment_promotion_phases"))
#         environments = Environments.from_dict(obj.get("environments"))
#         path_monitor = PathMonitor.from_dict(obj.get("path_monitor"))
#         slack = SlackConfig.from_dict(obj.get("slack"))
#         return GitOps(app_of_apps, app_of_apps_service_name, app_repo, dockerfile, ecr_repository_name, enable_tests,
#                       helm_chart_repo, helm_chart_service_name, is_mono_repo, name, service,
#                       environment_promotion_phases, environments, path_monitor, slack)
#
#     def to_dict(self) -> dict:
#         result: dict = {
#             "app_of_apps": from_str(self.app_of_apps),
#             "app_of_apps_service_name": from_str(self.app_of_apps_service_name),
#             "app_repo": from_str(self.app_repo),
#             "dockerfile": from_str(self.dockerfile),
#             "ecr_repository_name": from_str(self.ecr_repository_name),
#             "enable_tests": from_bool(self.enable_tests),
#             "helm_chart_repo": from_str(self.helm_chart_repo),
#             "helm_chart_service_name": from_str(self.helm_chart_service_name),
#             "is_mono_repo": from_bool(self.is_mono_repo),
#             "name": from_str(self.name),
#             "service": from_str(self.service),
#             "environment_promotion_phases": to_class(EnvironmentPromotionPhases, self.environment_promotion_phases),
#             "environments": to_class(Environments, self.environments),
#             "path_monitor": to_class(PathMonitor, self.path_monitor),
#             "slack": to_class(SlackConfig, self.slack)
#         }
#         return result
#
#
# @dataclass
# class Manifest(ApplicationConfig, Environment):
#     @classmethod
#     def from_gitops(cls, gitops: GitOps, environment_name: str = 'dev') -> 'Manifest':
#         manifest_fields: list[str] = sorted(list(cls.__dataclass_fields__.keys()))
#         environment_with_region: EnvironmentWithRegion = getattr(gitops.environments, environment_name)
#         temp_environment_fields: list[str] = sorted([attr.name for attr in fields(environment_with_region)])
#         environment_fields: list[str] = sorted(list(set(temp_environment_fields).intersection(manifest_fields)))
#
#         processed_fields: list[str] = []
#         for attr in environment_fields:
#             setattr(cls, attr, getattr(environment_with_region, attr))
#             processed_fields.append(attr)
#
#         application_fields = sorted(list(set(manifest_fields).difference(processed_fields)))
#         manifest_fields = sorted(list(set(manifest_fields).intersection(application_fields)))
#         for attr in manifest_fields:
#             setattr(cls, attr, getattr(gitops, attr))
#
#         return cls
#
#
# def gitops_from_dict(s: Any) -> GitOps:
#     return GitOps.from_dict(s)
#
#
# def gitops_to_dict(x: GitOps) -> Any:
#     return to_class(GitOps, x)
