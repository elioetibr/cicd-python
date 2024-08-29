#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__test__ = False

from cicd.Utils import recursive_sort_dict_by_key

# pragma: no cover
TEST_DATA = recursive_sort_dict_by_key({
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
    "environment_promotion_phases": {
        "01-dev": {
            "aws_account_id": 123456789,
            "description": "AWS Account for Dev",
            "environment": "dev",
            "enabled": True
        },
        "02-demo": {
            "aws_account_id": 987654321,
            "description": "AWS Account for Demo",
            "environment": "demo",
            "enabled": False
        },
        "03-prod": {
            "aws_account_id": 123987456,
            "description": "AWS Account for Prod",
            "environment": "prod",
            "enabled": True
        }
    },
    "environments": {
        "demo": {
            "aws_region": "us-west-2",
            "cluster": "demo-cluster",
            "environment": "demo",
            "next_environment": "prod",
            "additional_aws_regions": ["eu-west-1"],
            "approval_for_promotion": True,
            "enabled": True,
            "with_gate": False
        },
        "dev": {
            "aws_region": "us-west-1",
            "cluster": "dev-cluster",
            "environment": "dev",
            "next_environment": "demo",
            "additional_aws_regions": ["us-west-2", "us-east-1"],
            "approval_for_promotion": False,
            "enabled": True,
            "with_gate": True
        },
        "prod": {
            "aws_region": "us-east-1",
            "cluster": "prod-cluster",
            "environment": "prod",
            "next_environment": "",
            "additional_aws_regions": [],
            "approval_for_promotion": True,
            "enabled": True,
            "with_gate": True
        }
    },
    "path_monitor": {
        "application": {
            "hasModifications": True,
            "paths": ["path/to/application"]
        },
        "helm_charts": {
            "hasModifications": False,
            "paths": ["path/to/helm"]
        }
    },
    "slack": {
        "url": "https://slack.com",
        "channels": {
            "default": {
                "cd": [{"id": "C12345", "name": "cd-channel"}],
                "ci": [{"id": "C67890", "name": "ci-channel"}]
            },
            "dev": {
                "cd": [{"id": "C112233", "name": "dev-cd-channel"}],
                "ci": [{"id": "C445566", "name": "dev-ci-channel"}]
            },
            "demo": {
                "cd": [{"id": "C998877", "name": "demo-cd-channel"}],
                "ci": [{"id": "C665544", "name": "demo-ci-channel"}]
            },
            "prod": {
                "cd": [{"id": "C123123", "name": "prod-cd-channel"}],
                "ci": [{"id": "C321321", "name": "prod-ci-channel"}]
            }
        }
    }
})
