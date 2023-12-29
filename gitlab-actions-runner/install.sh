#!/bin/sh

ansible-galaxy role install MonolithProjects.github_actions_runner

ansible-playbook -i inventory.yaml playbook.yml
