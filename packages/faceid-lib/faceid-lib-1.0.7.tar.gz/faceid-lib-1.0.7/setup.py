# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['faceid_lib',
 'faceid_lib.events',
 'faceid_lib.logger',
 'faceid_lib.ratelimiter',
 'faceid_lib.workflow']

package_data = \
{'': ['*']}

install_requires = \
['aioredis==1.3.1', 'fastapi', 'pika>=1.2.0,<2.0.0', 'requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['faceid-lib = faceid_lib:main']}

setup_kwargs = {
    'name': 'faceid-lib',
    'version': '1.0.7',
    'description': 'Simple and flexible AI/ML workflow engine by Picaso - FaceID',
    'long_description': '# picaso-engine ML faceid workflow\n\n## Overview\n\nThis is a helper library for picaso-engine ML faceid workflow product. The idea of this library is to wrap all reusable code to simplify and improve workflow implementation.\n\nSupported functionality:\n\n- API to communicate with RabbitMQ for event receiver/producer\n- Workflow call helper\n- Logger call helper\n- Rate-limiting strategies\n\n## Author\npicaso-engine ML (https://pypi.org/project/faceid-lib/), Dani Gunawan\n\n## Instructions\nVersion number should be updated in __init__.py and pyproject.toml\n\n1. Install Poetry\n\n```\npip install poetry\n```\n\n2. Add pika and requests libraries\n\n```\npoetry add pika\npoetry add requests\n```\n\n3. Build\n\n```\npoetry lock --no-update\npoetry install\npoetry build\n```\n\n4. Publish to TestPyPI\n\n```\npoetry publish -r testpypi\n```\n\n5. Install from TestPyPI\n\n```\npip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple  faceid-lib\n```\n\n6. Publish to PyPI\n\n```\npoetry publish\n```\n\n7. Install from PyPI\n\n```\npip install faceid-lib\n```\n\n8. Test imported library from CMD\n\n```\npython -m faceid_lib\n```\n\n9. Import EventReceiver\n\n```\nfrom faceid_lib.events.event_receiver import EventReceiver\n```\n\n10. Import EventProducer\n\n```\nfrom faceid_lib.events.event_producer import EventProducer\n```\n\n11. Import FastAPILimiter, RateLimiter\n\n```\nfrom faceid_lib.ratelimiter import FastAPILimiter\nfrom faceid_lib.ratelimiter.depends import RateLimiter\n```\n\n## Structure\n\n```\n.\n├── LICENSE\n├── poetry.lock\n├── pyproject.toml\n├── faceid_lib\n│   ├── __init__.py\n│   ├── __main__.py\n│   ├── events\n│       ├── __init__.py\n│       ├── event_producer.py\n│       └── event_receiver.py\n│   ├── ratelimiter\n│       ├── __init__.py\n│       └── depends.py\n│   ├── logger\n│       ├── __init__.py\n│       └── logger_helper.py\n│   ├── workflow\n│       ├── __init__.py\n│       └── workflow_helper.py\n└── README.md\n```\n\n## Changelogs 1.0.5 (2021-10-24)\n- downgrade pika version to 1.1.0\n\n## Changelogs 1.0.4 (2021-10-24)\n- enhancment rate limiting\n\n## License\nLicensed under the Apache License, Version 2.0. Copyright 2020-2021 picaso-engine ML, Dani Gunawan.\n',
    'author': 'Dani Gunawan',
    'author_email': 'danigunawan.elektroug@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.playcourt.id/picaso-faceid/picaso-faceid-engine/v1/faceid-lib',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
