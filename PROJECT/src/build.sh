#!/bin/bash
path_src='PROJECT/src'
path_proj='PROJECT/base_project'
pip install -r "$path_src/requirements.txt"
echo 'ScoutCamp Linux Build (w/ render)'
echo '$ scout --version'
python "$path_src/scout.py" --version
echo '$ scout --path "$path_proj" --render'
python "$path_src/scout.py" --path "$path_proj" --render
