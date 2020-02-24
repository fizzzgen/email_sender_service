pip install flake8
echo 'PYLINTER-------->'
flake8 .
echo '---->PYLINTER END'
python -m unittest discover -s ut/ -t ut/
