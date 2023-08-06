#!/usr/bin/env bash
#python create_git_tag.py
python setup.py sdist && twine upload --skip-existing dist/*
