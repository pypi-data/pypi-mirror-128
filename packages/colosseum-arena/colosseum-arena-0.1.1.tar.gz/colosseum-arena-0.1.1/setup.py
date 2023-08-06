# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['colosseum',
 'colosseum.games',
 'colosseum.games.food_catcher',
 'colosseum.games.food_catcher.tests',
 'colosseum.tests']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.21.4,<2.0.0',
 'pexpect>=4.8.0,<5.0.0',
 'python-dotenv>=0.19.2,<0.20.0',
 'requests>=2.26.0,<3.0.0',
 'simple-elo>=0.1.1,<0.2.0']

setup_kwargs = {
    'name': 'colosseum-arena',
    'version': '0.1.1',
    'description': 'An AI arena, where agents fight each other',
    'long_description': '# Colosseum\n\nAn modular AI playground where agents are put in a multiple scenarios to\ncompete each other. Automated tournaments are supported, with rankins by score\n(wins are 1 point and draws are 0.5) and ELO ratings. Agents can be implemented\nin any language, as long as they are able to parse json payloads and\ncommunicate via stdin and stdout.\n\nCurrently the project is in an early stage and many things are subject to\nbreaking changes. Nevertheless, it is in an state where it is ready to use\nand have fun.\n\n## Features\n\n- Round robin tournament formats\n- Open format using json for data representation and stdin / stdout to communicate\n- Sample agents\n- Python SDK\n- Sample game\n- Replay Renderer\n- Headless mode\n\n## Planned\n\n- Swiss tournament format\n- Bracket tournament format\n- Website to register and upload bots\n- Automated runner to download agents and play a match with them\n- Persistent elo ratings\n- Seasons\n- Downloadable replays\n\n# Running locally\n\n- Setup `poetry`\n- Run `poetry install`\n- `poetry run python tournament.py agents/foo agent/bar agent/qux` runs a\n  tournament with the given agents. The arguments must be a path to the agent\n  executable file.\n- `poetry run python skirmish.py agents/foo agent/bar` to run a skirmish with\n  the given agents.\n- `poetry run python renderer.py replay_file.jsonl` renders the replay of a\n  match (either from a skirmish or a tournament).\n\n# LICENSE\n\nAll files in this repository are released under [MIT](LICENSE) license, unless\nexplicitly noted.\n',
    'author': 'h3nnn4n',
    'author_email': 'colosseum@h3nnn4n.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.colosseum.website/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
