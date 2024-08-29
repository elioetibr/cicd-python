#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os

import yaml

from cicd.GitOps import gitops_from_dict, gitops_to_dict


def main() -> None:
    fixtures = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'fixtures')
    fixtures_outputs = os.path.join(fixtures, 'outputs')
    gitops_yaml_file = os.path.join(fixtures, 'gitops.yaml')
    with open(gitops_yaml_file, 'r') as file:
        try:
            gitops_yaml_file_to_dict = yaml.safe_load(file)
        except Exception as e:
            raise e

    print(json.dumps(gitops_yaml_file_to_dict, indent=2, sort_keys=True))
    gitops = gitops_from_dict(gitops_yaml_file_to_dict)
    print(gitops)
    gitops_result_dict = gitops_to_dict(gitops)
    with open(os.path.join(fixtures_outputs, 'gitops.yaml'), "w") as file:
        yaml.dump(gitops_result_dict, file)

    with open(os.path.join(fixtures_outputs, 'gitops.json'), "w") as file:
        json.dump(gitops_result_dict, file)

    # manifest = Manifest.from_gitops(gitops)
    # manifest_dict = manifest.to_dict()
    # with open(os.path.join(fixtures_outputs, 'manifest.yaml'), "w") as file:
    #     yaml.dump(manifest_dict, file)
    # print()


if __name__ == '__main__':
    main()
