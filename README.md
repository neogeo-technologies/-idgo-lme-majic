# IDGO LME-MAJIC

## Installation et configuration

Application initialement développée dans un environnement virtuel __Python 3.5__.

```shell
> cd /
/> cd idgo_venv
/idgo_venv> source bin/activate
(idgo_venv) /idgo_venv> pip install -e https://git.neogeo.fr/idgo/apps/idgo-lme-majic.git
```

### Paramètres additionnels du `settings.py`


#### Paramètres obligatoire

MAJIC_API = 'http://majic.datasud.neogeo.fr/'

BASE_MAJIC_LME = DOMAIN_NAME + '/lmemajic/'


## Données par défaut

Installation des mails par défaut:

```
(idgo_venv) /idgo_venv> python manage.py loaddata src/idgo-lme-majic/idgo_lme_majic/fixtures/initial_data.json
```
