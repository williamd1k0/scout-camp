#!/bin/bash
path_src='PROJECT/src'
path_proj='PROJECT/base_project'
echo 'ScoutCamp Linux Build (w/ render)'
echo 'scout --version'
python "$path_src/scout.py" --version
python "$path_src/scout.py" --path "$path_proj" --render
