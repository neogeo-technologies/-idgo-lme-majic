# IDGO LME-MAJIC

## Installation et configuration

Application initialement développée dans un environnement virtuel __Python 3.5__.

```shell
> cd /
/> mkdir idgo_venv
/> cd idgo_venv
/idgo_venv> pyvenv-3.5 ./
/idgo_venv> source bin/activate
(idgo_venv) /idgo_venv> cd /path/to/idgo
(idgo_venv) /idgo_venv> python setup.py
(idgo_venv) /idgo_venv>
```

_**TODO** : Création des fichiers de configuration, création des bases de données, etc._


### Paramètres additionnels du `settings.py`


#### Paramètres obligatoire

MAJIC_API = 'http://majic.datasud.neogeo.fr/'

BASE_MAJIC_LME = DOMAIN_NAME + '/lmemajic/'
