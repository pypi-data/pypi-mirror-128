# Market Manager for Alliance Auth

Market Manager and Market Browser plugin for Alliance Auth.

![License](https://img.shields.io/badge/license-MIT-green)
![python](https://img.shields.io/badge/python-3.7-informational)
![django](https://img.shields.io/badge/django-3.2-informational)
![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)

## Features

- Market Browser
    - Item Search with Autocomplete
    - Buy/Sell Orders
    - Item Statistics (WIP)
- Fetching Public orders by selectable Regions
- Fetching Character Orders from provided Tokens
    - Will append EveCharacter (and more) details to orders gathered from other means
- Fetching Corporation Orders from provided Tokens
    - Will append EveCorporation (and more) details to orders gathered from other means
    - Minor sanity checking to check for ingame Roles before hitting market ESI to reduce errors from tokens with no access to data.
- WIP Structure ID Resolver
    - Resolves Stations via Django-EveUniverse EveEntity resolver
    - Resolves Citadels internally
        - Fetches Corporation Citadels from Corporation Tokens loaded with the appropriate EVE Roles ("Station_Manager")
        - get_universe_structures_structure_id requires docking ACL Access. As there is no way to tell who has docking (even the owner corporation is not a guarantee),

- Will detect and use any tokens loaded by other means, if you request the scopes as part of a wider scoped app (Such as an Audit tool etc.)


## Planned Features
- Configurable Alerts
    - Quantity and/or Price Orders.
- Item Statistics, Currently only Volume is calculated, welcoming advice on Medians and Percentiles in Django
- Manually defining Tokens that are on ACLs for use in pulling structures from the get_universe_structures_structure_id endpoint which wont require Station_Manager.

## Installation

### Step 1 - Django Eve Universe

Market Manager is an App for [Alliance Auth](https://gitlab.com/allianceauth/allianceauth/), Please make sure you have this installed. Market Manager is not a standalone Django Application


Market Manager needs the app [django-eveuniverse](https://gitlab.com/ErikKalkoken/django-eveuniverse) to function. Please make sure it is installed before continuing.

### Step 2 - Install app

```bash
pip install aa-marketmanager
```

### Step 3 - Configure Auth settings

Configure your Auth settings (`local.py`) as follows:

- Add `'marketmanager'` to `INSTALLED_APPS`
- Add below lines to your settings file:

```python
## Settings for AA-MarketManager
# Market Orders
CELERYBEAT_SCHEDULE['marketmanager_fetch_public_market_orders'] = {
    'task': 'marketmanager.tasks.fetch_public_market_orders',
    'schedule': crontab(minute=0, hour='*/3'),
}
CELERYBEAT_SCHEDULE['marketmanager_fetch_all_character_orders'] = {
    'task': 'marketmanager.tasks.fetch_all_character_orders',
    'schedule': crontab(minute=0, hour='*/3'),
}
CELERYBEAT_SCHEDULE['marketmanager_fetch_all_corporation_orders'] = {
    'task': 'marketmanager.tasks.fetch_all_corporation_orders',
    'schedule': crontab(minute=0, hour='*/3'),
}
# Structure Information
CELERYBEAT_SCHEDULE['marketmanager_fetch_public_structures'] = {
    'task': 'marketmanager.tasks.fetch_public_structures',
    'schedule': crontab(minute=0, hour=0, day_of_week=3),
}
CELERYBEAT_SCHEDULE['marketmanager_fetch_all_corporations_structures'] = {
    'task': 'marketmanager.tasks.fetch_all_corporations_structures',
    'schedule': crontab(minute=0, hour='*/3'),
}
```
- Run migrations `python manage.py migrate`
- Gather your staticfiles `python manage.py collectstatic`
- Restart your project `supervisorctl restart :myauth`
### Step 4 - Configure Further
In the Admin interface, visit `marketmanager > config > add` or `<AUTH-URL>/admin/marketmanager/config/add/`
Select the Regions you would like to pull Public Market Data for.
