#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from unittest import TestCase

from cicd.GitOpsDataClasses import GitOps
from tests.Fixtures import TEST_DATA


class TestGitOps(TestCase):
    def setUp(self):
        self.gitops = GitOps.from_dict(TEST_DATA)

    def test_to_dict(self):
        expected = TEST_DATA
        result = self.gitops.to_dict()
        self.assertEqual(result, expected)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()  # pragma: no cover
