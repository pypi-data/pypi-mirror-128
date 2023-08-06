# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['bn_adjustable_bed',
 'bn_adjustable_bed.app_api',
 'bn_adjustable_bed.bed_socket',
 'bn_adjustable_bed.controller_api']

package_data = \
{'': ['*'], 'bn_adjustable_bed': ['config/*']}

install_requires = \
['fastapi>=0.70,<0.71',
 'pyyaml>=6.0,<7.0',
 'redis>=4.0,<5.0',
 'uvicorn>=0.15,<0.16']

extras_require = \
{'test': ['pytest>=6.2,<7.0',
          'pytest-mock>=3.6,<4.0',
          'pytest-cov>=3.0,<4.0',
          'requests>=2.26,<3.0']}

entry_points = \
{'console_scripts': ['bn-app-api = bn_adjustable_bed.app_api:main',
                     'bn-bed-socket = bn_adjustable_bed.bed_socket:main',
                     'bn-controller-api = '
                     'bn_adjustable_bed.controller_api:main']}

setup_kwargs = {
    'name': 'bn-adjustable-bed',
    'version': '1.3.12',
    'description': 'BN Adjustable Bed Mock API and Socket Interface',
    'long_description': '# BN Adjustable Bed Mock API and Socket Interface\n\n_**This project is not an official project of, and is in no way affiliated with, Blissful Nights or the Ronin Wifi mobile app**_\n\n[![codecov](https://codecov.io/gh/trevorlauder/bn-adjustable-bed/branch/main/graph/badge.svg?token=DHZC7X92PP)](https://codecov.io/gh/trevorlauder/bn-adjustable-bed)\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/trevorlauder/bn-adjustable-bed/main.svg)](https://results.pre-commit.ci/latest/github/trevorlauder/bn-adjustable-bed/main)\n[![CI](https://github.com/trevorlauder/bn-adjustable-bed/actions/workflows/ci.yml/badge.svg)](https://github.com/trevorlauder/bn-adjustable-bed/actions/workflows/ci.yml)\n[![Release](https://github.com/trevorlauder/bn-adjustable-bed/actions/workflows/release.yml/badge.svg)](https://github.com/trevorlauder/bn-adjustable-bed/actions/workflows/release.yml)\n[![PyPI version](https://badge.fury.io/py/bn-adjustable-bed.svg)](https://badge.fury.io/py/bn-adjustable-bed)\n\n![image](https://user-images.githubusercontent.com/2594126/141405656-401480c5-f23f-4846-a241-405e7ca7c813.png)\n![image](https://user-images.githubusercontent.com/2594126/141405860-21e5c871-292e-42c5-a5ab-f0efaf072c0f.png)\n\n\nThis project sets up an HTTP API and Socket Interface for the [Blissful Nights Wall Hugger Adjustable Bed with Massage and Alexa Voice Command](https://www.blissfulnights.com/collections/adjustable-bed-bases/products/wall-glide-adjustable-bed-with-massage-and-voice-command).\n\nI can control the bed using the HTTP API or the mobile app without having anything connected to the official servers hosted in AWS.\n\nI have the HTTP API hooked up to my iOS Shortcuts which allows me to use it in my automation.\n\nNot all of the socket communication protocol is understood, but enough of it has been reverse engineered to provide this functionality.\n\n## Docker Hub Links\n\n* [bn-adjustable-bed](https://hub.docker.com/r/trevorlauder/bn-adjustable-bed)\n\n## How to Use\n\nTo use it, you must hijack the DNS queries for `cm2.xlink.cn` and `api2.xlink.cn` and redirect them to your server.\n\n`api2.xlink.cn` is used by the Ronin WiFi mobile app [ [ios](https://apps.apple.com/us/app/ronin-wifi/id1392877882) | [android](https://play.google.com/store/apps/details?id=com.keeson.rondurewifi) ].\n\n`cm2.xlink.cn` is used by the bed.  The bed creates a persistent socket connection to this address.\n\nUse of the mobile app is required to perform the initial setup and get the bed hooked up to your wireless network.  Once you have it setup, use of the mobile app is optional.\n\n### Mobile App API\n\nThe HTTP API is exposed on port `80` and provides endpoints that will allow you to log into the app without creating an account.\n\n#### Setup\n\n1. An [example](https://github.com/trevorlauder/bn-adjustable-bed/blob/main/docker-compose.yml.example) Docker Compose Config File is provided.  It uses a default bridge network for communcation to the redis instance and configures the other 3 services to use an IP on a `macvlan` network named `lan`.  Change `<IP>` in the example file based on your network, they all need to be unique.  If you prefer, you could use the [main](https://github.com/trevorlauder/bn-adjustable-bed/blob/main/docker-compose.yml) Docker Compose Config File used for development as a start, it uses the default network and exposes the service ports through a single IP instead.  In this case the `Bed Controller API` will be on port `8080` instead of `80`.\n\n1. Setup a directory for the services and run Docker Compose to start the 4 services (Redis, App API, Bed Socket Interface and Controller API).\n\n```bash\nmkdir bn-adjustable-bed\n\ncd bn-adjustable-bed\n\nwget https://github.com/trevorlauder/bn-adjustable-bed/blob/main/docker-compose.yml.example -O docker-compose.yml\n\n# adjust <IP> and config for your network\n\ndocker-compose up\n```\n\n1. Hijack DNS queries to `api2.xlink.cn` and `cm2.xlink.cn` on your network so that they resolve to the IP address of your docker services.  If you\'re using separate IP\'s for each service, `api2.xlink.cn` should be pointed at the `app-api` service and `cm2.xlink.cn` should be pointed at the `bed-socket` service.\n\n1. Log into the Ronin Wifi mobile app using any email address and password, neither need to be valid.  Make sure your mobile device is connected to your network so that is resolves your hijacked domains properly.\n\n1. Select `My Bed` from the menu and then `Connect new bed`\n\n    * Follow the instructions in the app to "_Long press the Foot Up and Down buttons for 5 seconds until you hear a beep every 3 seconds_".  Click `Next`\n\n    * Connect your mobile device to the `KeesonAp-XXXXXXXXXX` Wireless SSID.  Click `Next`\n\n    * Continue with the instructions and provide the Wireless network credentials for the network you wish to connect the bed to.\n\n    * The bed will beep a couple times and connect to your Wireless Network.  The bed should show up shortly in the list with an option to `Connect`.  Skip this part as not enough of the communications protocol has been reverse engineered at this point for the app to completely perform the setup.  At this point you can force quit the app and re-open it, you should be able to control the bed now and see it in the list of beds.\n\n### Bed Controller API\n\nThe Bed Controller API is exposed on port `80` and provides an endpoint that allows you to send commands to the bed.\n\nThis can be easily added to Siri Shortcuts or similar tools to add bed control to whatever automation platform you use.\n\n```bash\n\n# Tell the bed to move to the flat position\ncurl -X \'PUT\' \\\n  \'http://bn-adjustable-bed-controller.changethistoyourdomain.com/command?name=flat\' \\\n  -H \'accept: application/json\'\n\n# Tell the bed to move to the Zero-G position\ncurl -X \'PUT\' \\\n  \'http://bn-adjustable-bed-controller.changethistoyourdomain.com/command?name=zero_g\' \\\n  -H \'accept: application/json\'\n\n# Tell the bed to move to the Preset I position\ncurl -X \'PUT\' \\\n  \'http://bn-adjustable-bed-controller.changethistoyourdomain.com/command?name=preset_one\' \\\n  -H \'accept: application/json\'\n\n# Tell the bed to move to the Preset II position\ncurl -X \'PUT\' \\\n  \'http://bn-adjustable-bed-controller.changethistoyourdomain.com/command?name=preset_two\' \\\n  -H \'accept: application/json\'\n\n# Tell the bed to move to the Preset III position\ncurl -X \'PUT\' \\\n  \'http://bn-adjustable-bed-controller.changethistoyourdomain.com/command?name=preset_three\' \\\n  -H \'accept: application/json\'\n```\n',
    'author': 'Trevor Lauder',
    'author_email': 'trevor@lauder.family',
    'maintainer': 'Trevor Lauder',
    'maintainer_email': 'trevor@lauder.family',
    'url': 'https://github.com/trevorlauder/bn-adjustable-bed',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
