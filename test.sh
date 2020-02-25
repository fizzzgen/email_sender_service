pip install flake8
echo 'PYLINTER-------->'
flake8 .
echo '---->PYLINTER END'
python -m unittest discover -s ut/ -t ut/
rm *.pyc
rm *.sqlite
rm ut/*.pyc
rm ut/*.sqlite
rm engine/*.pyc
rm engine/*.sqlite
rm reader/*.pyc
rm reader/*.sqlite
rm sender/*.pyc
rm sender/*.sqlite
rm interface/*.pyc
rm interface/*.sqlite
