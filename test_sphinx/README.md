## Step to set up Sphinx for python doc

- create a folder for the sphinx project as root
- inside root, create directories as html, rst and scripts
- in the terminal under root directory, run command: 
```sh
> sphinx-quickstart
```
- a list of choices will be provided, for most of them use default value except when make choice for **autodoc**, **create makefiles** and **create womdpws command file**, using yes;
- go to conf.py make changes as
```python
import sys
sys.path.append("C:\\Users\\xiyang\\Desktop\\test_sphinx\\scripts\\")
html_theme = 'default'
```
- comment out following code
```python
#html_sidebars = {
#    '**': [
#        'about.html',
#        'navigation.html',
#        'relations.html',  # needs 'show_related': True theme option to display
#        'searchbox.html',
#        'donate.html',
#    ]
#}
``` 
- run command: 
```sh
> make html
```
- copy conf.py into the rst folder, make a folder named _static
- copy all the source code into the scripts folder and run command:
```sh
> sphinx-apidoc -o rst/ scripts/
```
- copy the modules.rst and rename it as index.rst or you can copy the index.rst in the root folder to rst folder
- run command
```sh
sphinx-build -b html rst html/ 
```
- if code changed, and doc need to be updated, just remove the files from rst and html folder and re-run the steps above
