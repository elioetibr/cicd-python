#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from dataclasses import asdict
from unittest import TestCase

from cicd.GitOps import (
    AwsAccount,
    Application,
    Environment,
    EnvironmentWithAdditionalRegions,
    EnvironmentPromotionPhases, Environments,
)


class TestApplication(TestCase):
    def setUp(self):
        self.test_data = {
            "app_of_apps": 'app-of-apps',
            "app_of_apps_service_name": "devops",
            "app_repo": "elioetibr",
            "dockerfile": ".github/tests/app/Dockerfile",
            "ecr_repository_name": "devops",
            "enable_tests": True,
            "helm_chart_repo": "devops-helm-charts",
            "helm_chart_service_name": "devops",
            "is_mono_repo": False,
            "name": "devops",
            "service": "devops",
        }
        self.test_assertion = Application(self.test_data)

    def test_to_dict(self):
        test_dict: dict = self.test_assertion.to_dict()
        self.assertEqual(test_dict, self.test_data)
        self.assertEqual(self.test_assertion.to_dict(), self.test_data)
        print()

    def test_from_dict(self):
        self.assertEqual(asdict(Application.from_dict(self.test_data)), self.test_data)
        print()


class TestAwsAccount(TestCase):
    def setUp(self):
        self.test_data = {
            "aws_account_id": 123456789,
            "description": "AWS Account for Dev",
            "environment": "dev",
            "enabled": True
        }
        self.test_assertion = AwsAccount(self.test_data)

    def test_to_dict(self):
        test_dict: dict = self.test_assertion.to_dict()
        self.assertEqual(test_dict, self.test_data)
        self.assertEqual(self.test_assertion.to_dict(), self.test_data)
        print()

    def test_from_dict(self):
        self.assertEqual(asdict(AwsAccount.from_dict(self.test_data)), self.test_data)
        print()


class TestEnvironment(TestCase):
    def setUp(self):
        self.test_data = {
            'approval_for_promotion': False,
            'aws_region': 'us-east-2',
            'cluster': 'dev-eks',
            'enabled': True,
            'environment': 'dev',
            'next_environment': 'demo',
            'with_gate': False
        }
        self.test_assertion = Environment(self.test_data)

    def test_to_dict(self):
        test_dict: dict = self.test_assertion.to_dict()
        self.assertEqual(test_dict, self.test_data)
        self.assertEqual(self.test_assertion.to_dict(), self.test_data)
        print()

    def test_from_dict(self):
        self.assertEqual(asdict(Environment.from_dict(self.test_data)), self.test_data)
        print()


class TestEnvironmentWithRegion(TestCase):
    def setUp(self):
        self.test_data = {
            'additional_aws_regions': [
                "us-east-1",
                "us-west-1",
                "us-west-2",
            ],
            'approval_for_promotion': False,
            'aws_region': 'us-east-2',
            'cluster': 'dev-eks',
            'enabled': True,
            'environment': 'dev',
            'next_environment': 'demo',
            'with_gate': False
        }
        self.test_assertion = EnvironmentWithAdditionalRegions(self.test_data)

    def test_to_dict(self):
        test_dict: dict = self.test_assertion.to_dict()
        self.assertEqual(test_dict, self.test_data)
        self.assertEqual(self.test_assertion.to_dict(), self.test_data)
        print()

    def test_from_dict(self):
        self.assertEqual(asdict(EnvironmentWithAdditionalRegions.from_dict(self.test_data)), self.test_data)
        print()


class TestEnvironmentPromotionPhases(TestCase):
    def setUp(self):
        self.test_data = {
            'aws_account_id': 885015629014,
            'description': 'Development Workload',
            'enabled': True,
            'environment': 'dev'
        }
        self.test_assertion = EnvironmentPromotionPhases(self.test_data)

    def test_to_dict(self):
        test_dict: dict = self.test_assertion.to_dict()
        self.assertEqual(test_dict, self.test_data)
        self.assertEqual(self.test_assertion.to_dict(), self.test_data)
        print()

    def test_from_dict(self):
        self.assertEqual(asdict(type(self.test_assertion).from_dict(self.test_data)), self.test_data)
        print()


if __name__ == '__main__':  # pragma: no cover
    unittest.main()  # pragma: no cover
