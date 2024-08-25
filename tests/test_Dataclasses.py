#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from dataclasses import asdict
from unittest import TestCase

from cicd.GitOpsDataClasses import GitOps, AwsAccount, gitops_from_dict
from tests.Fixtures import TEST_DATA


class TestAwsAccount(TestCase):
    def setUp(self):
        self.data = {
            "aws_account_id": 123456789,
            "description": "AWS Account for Dev",
            "environment": "dev",
            "enabled": True
        }
        self.aws_account = AwsAccount(**self.data)

    def test_to_dict(self):
        self.assertEqual(self.aws_account.to_dict(), self.data)

    def test_from_dict(self):
        self.assertEqual(asdict(AwsAccount.from_dict(self.data)), self.data)


class TestGitOps(TestCase):
    def setUp(self):
        self.gitops = GitOps.from_dict(TEST_DATA)

    def test_from_dict(self):
        self.assertEqual(asdict(gitops_from_dict(TEST_DATA)), asdict(self.gitops))

    def test_to_dict(self):
        expected = TEST_DATA
        result = self.gitops.to_dict()
        self.assertEqual(result, expected)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()  # pragma: no cover
