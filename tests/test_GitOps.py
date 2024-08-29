#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from unittest import TestCase

from cicd.GitOps import GitOpsManager, GitOps, Slack, Environments, Environment, Application
from cicd.Utils import recursive_sort_dict_by_key
from tests.Fixtures import TEST_DATA


class TestGitOps(TestCase):
    def setUp(self):
        self.test_data = TEST_DATA
        self.test_assertion_gitops = GitOpsManager.from_dict(self.test_data)

    def test_gitops_manager_to_dict(self):
        self.test_assertion = GitOpsManager.to_dict(self.test_assertion_gitops)
        self.assertDictEqual(self.test_assertion, self.test_data)

    def test_gitops_manager_from_dict(self):
        self.test_assertion = GitOpsManager.from_dict(self.test_assertion_gitops.to_dict()).to_dict()
        self.assertDictEqual(self.test_assertion, self.test_data)

    def test_gitops_to_dict(self):
        self.test_assertion = GitOps.from_dict(self.test_data).to_dict()
        self.assertDictEqual(self.test_assertion, self.test_data)

    def test_gitops_from_dict(self):
        self.test_assertion = GitOps.from_dict(self.test_data).to_dict()
        self.assertDictEqual(self.test_assertion, self.test_data)

    def test_slack_from_dict(self):
        self.test_assertion = Slack.from_dict(self.test_data["slack"]).to_dict()
        self.assertDictEqual(self.test_assertion, self.test_data["slack"])

    def test_slack_to_dict(self):
        self.test_assertion = Slack.from_dict(self.test_data["slack"]).to_dict()
        self.assertDictEqual(self.test_assertion, self.test_data["slack"])

    def test_environments_from_dict(self):
        self.test_assertion = Environments.from_dict(self.test_data["environments"]).to_dict()
        self.assertDictEqual(self.test_assertion, self.test_data["environments"])

    def test_environments_to_dict(self):
        self.test_assertion = Environments.from_dict(self.test_data["environments"]).to_dict()
        self.assertDictEqual(self.test_assertion, self.test_data["environments"])

    def test_environment_to_dict(self):
        test_data = recursive_sort_dict_by_key({
            "aws_region": "us-west-2",
            "cluster": "demo-cluster",
            "environment": "demo",
            "next_environment": "prod",
            "approval_for_promotion": True,
            "enabled": True,
            "with_gate": False
        })
        self.test_assertion = Environment.from_dict(test_data)
        result_dict = self.test_assertion.to_dict()
        self.assertDictEqual(result_dict, test_data)

    def test_environment_from_dict(self):
        test_data = {
            "aws_region": "us-west-2",
            "cluster": "demo-cluster",
            "environment": "demo",
            "next_environment": "prod",
            "approval_for_promotion": True,
            "enabled": True,
            "with_gate": False
        }
        self.assertDictEqual(Environment.from_dict(test_data).to_dict(), test_data)

    def test_manifest_from_dict(self):
        test_data = recursive_sort_dict_by_key({
            "app_of_apps": "meta-app",
            "app_of_apps_service_name": "meta-service",
            "app_repo": "https://repo.url",
            "dockerfile": "Dockerfile",
            "ecr_repository_name": "repo-name",
            "enable_tests": True,
            "helm_chart_repo": "chart-repo",
            "helm_chart_repo_path": "charts/test-chart",
            "is_mono_repo": False,
            "name": "GitOps App",
            "service": "some-service",
        })
        manifest = Application.from_dict(test_data)
        self.assertDictEqual(manifest.to_dict(), test_data)


# class TestApplication(TestCase):
#     def setUp(self):
#         self.test_data = {
#             "app_of_apps": 'app-of-apps',
#             "app_of_apps_service_name": "devops",
#             "app_repo": "elioetibr",
#             "dockerfile": ".github/tests/app/Dockerfile",
#             "ecr_repository_name": "devops",
#             "enable_tests": True,
#             "helm_chart_repo": "devops-helm-charts",
#             "helm_chart_repo_path": "devops",
#             "is_mono_repo": False,
#             "name": "devops",
#             "service": "devops",
#         }
#
#     def test_to_dict(self):
#         # test_dict: dict = self.test_assertion.to_dict()
#         # self.assertEqual(test_dict, self.test_data)
#         # self.assertEqual(self.test_assertion.to_dict(), self.test_data)
#         print()

# def test_from_dict(self):
#     self.assertEqual(asdict(Paths.from_dict(self.test_data)), self.test_data)


# class TestAwsAccount(TestCase):
#     def setUp(self):
#         self.test_data = {
#             "aws_account_id": 123456789,
#             "description": "AWS Account for Dev",
#             "environment": "dev",
#             "enabled": True
#         }
#         self.test_assertion = AwsAccount(self.test_data)
#
#     def test_to_dict(self):
#         test_dict: dict = self.test_assertion.to_dict()
#         self.assertEqual(test_dict, self.test_data)
#         self.assertEqual(self.test_assertion.to_dict(), self.test_data)
#
#     def test_from_dict(self):
#         self.assertEqual(asdict(AwsAccount.from_dict(self.test_data)), self.test_data)
#
#
# class TestEnvironment(TestCase):
#     def setUp(self):
#         self.test_data = {
#             'approval_for_promotion': False,
#             'aws_region': 'us-east-2',
#             'cluster': 'dev-eks',
#             'enabled': True,
#             'environment': 'dev',
#             'next_environment': 'demo',
#             'with_gate': False
#         }
#         self.test_assertion = Environment(self.test_data)
#
#     def test_to_dict(self):
#         test_dict: dict = self.test_assertion.to_dict()
#         self.assertEqual(test_dict, self.test_data)
#         self.assertEqual(self.test_assertion.to_dict(), self.test_data)
#
#     def test_from_dict(self):
#         self.assertEqual(asdict(Environment.from_dict(self.test_data)), self.test_data)
#
#
# class TestEnvironmentWithRegion(TestCase):
#     def setUp(self):
#         self.test_data = {
#             'additional_aws_regions': [
#                 "us-east-1",
#                 "us-west-1",
#                 "us-west-2",
#             ],
#             'approval_for_promotion': False,
#             'aws_region': 'us-east-2',
#             'cluster': 'dev-eks',
#             'enabled': True,
#             'environment': 'dev',
#             'next_environment': 'demo',
#             'with_gate': False
#         }
#         self.test_assertion = EnvironmentWithAdditionalRegions(self.test_data)
#
#     def test_to_dict(self):
#         test_dict: dict = self.test_assertion.to_dict()
#         self.assertEqual(test_dict, self.test_data)
#         self.assertEqual(self.test_assertion.to_dict(), self.test_data)
#         print()
#
#     def test_from_dict(self):
#         self.assertEqual(asdict(EnvironmentWithAdditionalRegions.from_dict(self.test_data)), self.test_data)
#         print()
#
#
# class TestEnvironmentPromotionPhases(TestCase):
#     def setUp(self):
#         self.test_data = {
#             'aws_account_id': 885015629014,
#             'description': 'Development Workload',
#             'enabled': True,
#             'environment': 'dev'
#         }
#         self.test_assertion = EnvironmentPromotionPhases(self.test_data)
#
#     def test_to_dict(self):
#         test_dict: dict = self.test_assertion.to_dict()
#         self.assertEqual(test_dict, self.test_data)
#         self.assertEqual(self.test_assertion.to_dict(), self.test_data)
#         print()
#
#     def test_from_dict(self):
#         self.assertEqual(asdict(type(self.test_assertion).from_dict(self.test_data)), self.test_data)
#         print()


if __name__ == '__main__':  # pragma: no cover
    unittest.main()  # pragma: no cover
