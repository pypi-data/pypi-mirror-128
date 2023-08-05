# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['circuit_maintenance_parser',
 'circuit_maintenance_parser.parsers',
 'circuit_maintenance_parser.processors']

package_data = \
{'': ['*'], 'circuit_maintenance_parser': ['data/*']}

install_requires = \
['backoff>=1.11.1,<2.0.0',
 'bs4>=0.0.1,<0.0.2',
 'click>=7.1,<9.0',
 'geopy>=2.1.0,<3.0.0',
 'icalendar>=4.0.7,<5.0.0',
 'lxml>=4.6.2,<5.0.0',
 'pydantic[dotenv]>=1.8.2,<2.0.0',
 'toml==0.10.2',
 'tzwhere>=3.0.3,<4.0.0']

entry_points = \
{'console_scripts': ['circuit-maintenance-parser = '
                     'circuit_maintenance_parser.cli:main']}

setup_kwargs = {
    'name': 'circuit-maintenance-parser',
    'version': '2.0.5',
    'description': 'Python library to parse Circuit Maintenance notifications and return a structured data back',
    'long_description': '# circuit-maintenance-parser\n\n`circuit-maintenance-parser` is a Python library that parses circuit maintenance notifications from Network Service Providers (NSPs), converting heterogeneous formats to a well-defined structured format.\n\n## Context\n\nEvery network depends on external circuits provided by NSPs who interconnect them to the Internet, to office branches or to\nexternal service providers such as Public Clouds.\n\nObviously, these services occasionally require operation windows to upgrade or to fix related issues, and usually they happen in the form of **circuit maintenance periods**.\nNSPs generally notify customers of these upcoming events so that customers can take actions to minimize the impact on the regular usage of the related circuits.\n\nThe challenge faced by many customers is that mostly every NSP defines its own maintenance notification format, even though in the\nend the relevant information is mostly the same across NSPs. This library is built to parse notification formats from\nseveral providers and to return always the same object struct that will make it easier to process them afterwards.\n\nThe format of this output is following the [BCOP](https://github.com/jda/maintnote-std/blob/master/standard.md) defined\nduring a NANOG meeting that aimed to promote the usage of the iCalendar format. Indeed, if the NSP is using the\nproposed iCalendar format, the parser is straight-forward and there is no need to define custom logic, but this library\nenables supporting other providers that are not using this proposed practice, getting the same outcome.\n\nYou can leverage this library in your automation framework to process circuit maintenance notifications, and use the standardized [`Maintenance`](https://github.com/networktocode/circuit-maintenance-parser/blob/develop/circuit_maintenance_parser/output.py) to handle your received circuit maintenance notifications in a simple way. Every `maintenance` object contains, at least, the following attributes:\n\n- **provider**: identifies the provider of the service that is the subject of the maintenance notification.\n- **account**: identifies an account associated with the service that is the subject of the maintenance notification.\n- **maintenance_id**: contains text that uniquely identifies the maintenance that is the subject of the notification.\n- **circuits**: list of circuits affected by the maintenance notification and their specific impact.\n- **status**: defines the overall status or confirmation for the maintenance.\n- **start**: timestamp that defines the start date of the maintenance in GMT.\n- **end**: timestamp that defines the end date of the maintenance in GMT.\n- **stamp**: timestamp that defines the update date of the maintenance in GMT.\n- **organizer**: defines the contact information included in the original notification.\n\n> Please, refer to the [BCOP](https://github.com/jda/maintnote-std/blob/master/standard.md) to more details about these attributes.\n\n## Workflow\n\n1. We instantiate a `Provider`, directly or via the `init_provider` method, that depending on the selected type will return the corresponding instance.\n2. Get an instance of the `NotificationData` class. This instance groups together `DataParts` which each contain some content and a specific type (that will match a specific `Parser`). For example, a `NotificationData` might describe a received email message, with `DataParts` corresponding to the subject line and body of the email. There are factory methods to initialize a `NotificationData` describing a single chunk of binary data, as well as others to initialize one directly from a raw email message or `email.message.EmailMessage` instance.\n3. Each `Provider` uses one or more `Processors` that will be used to build `Maintenances` when the `Provider.get_maintenances(data)` method is called.\n4. Each `Processor` class uses one or more `Parsers` to process each type of data that it handles. It can have custom logic to combine the parsed data from multiple `Parsers` to create the final `Maintenance` object.\n5. Each `Parser` class supports one or a set of related data types, and implements the `Parser.parse()` method used to retrieve a `Dict` with the relevant keys/values.\n\n<p align="center">\n<img src="https://raw.githubusercontent.com/networktocode/circuit-maintenance-parser/develop/docs/images/new_workflow.png" width="800" class="center">\n</p>\n\nBy default, there is a `GenericProvider` that support a `SimpleProcessor` using the standard `ICal` `Parser`, being the easiest path to start using the library in case the provider uses the reference iCalendar standard.\n\n### Supported Providers\n\n#### Supported providers using the BCOP standard\n\n- EuNetworks\n- NTT\n- PacketFabric\n- Telia\n- Telstra\n\n#### Supported providers based on other parsers\n\n- AWS\n- AquaComms\n- Cogent\n- Colt\n- Equinix\n- EXA (formerly GTT)\n- HGC\n- Lumen\n- Megaport\n- Momentum\n- Seaborn\n- Sparkle\n- Telstra\n- Turkcell\n- Verizon\n- Zayo\n\n> Note: Because these providers do not support the BCOP standard natively, maybe there are some gaps on the implemented parser that will be refined with new test cases. We encourage you to report related **issues**!\n\n## Installation\n\nThe library is available as a Python package in pypi and can be installed with pip:\n`pip install circuit-maintenance-parser`\n\n## How to use it?\n\nThe library requires two things:\n\n- The `notificationdata`: this is the data that the library will check to extract the maintenance notifications. It can be simple (only one data type and content, such as an iCalendar notification) or more complex (with multiple data parts of different types, such as from an email).\n- The `provider` identifier: used to select the proper `Provider` which contains the `processor` logic to take the proper `Parsers` and use the data that they extract. By default, the `GenericProvider` (used when no other provider type is defined) will support parsing of `iCalendar` notifications using the recommended format.\n\n### Python Library\n\nFirst step is to define the `Provider` that we will use to parse the notifications. As commented, there is a `GenericProvider` that implements the gold standard format and can be reused for any notification matching the expectations.\n\n```python\nfrom circuit_maintenance_parser import init_provider\n\ngeneric_provider = init_provider()\n\ntype(generic_provider)\n<class \'circuit_maintenance_parser.provider.GenericProvider\'>\n```\n\nHowever, usually some `Providers` don\'t fully implement the standard and maybe some information is missing, for example the `organizer` email or maybe a custom logic to combine information is required, so we allow custom `Providers`:\n\n```python\nntt_provider = init_provider("ntt")\n\ntype(ntt_provider)\n<class \'circuit_maintenance_parser.provider.NTT\'>\n```\n\nOnce we have the `Provider` ready, we need to initialize the data to process, we call it `NotificationData` and can be initialized from a simple content and type or from more complex structures, such as an email.\n\n```python\nfrom circuit_maintenance_parser import NotificationData\n\nraw_data = b"""BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//Maint Note//https://github.com/maint-notification//\nBEGIN:VEVENT\nSUMMARY:Maint Note Example\nDTSTART;VALUE=DATE-TIME:20151010T080000Z\nDTEND;VALUE=DATE-TIME:20151010T100000Z\nDTSTAMP;VALUE=DATE-TIME:20151010T001000Z\nUID:42\nSEQUENCE:1\nX-MAINTNOTE-PROVIDER:example.com\nX-MAINTNOTE-ACCOUNT:137.035999173\nX-MAINTNOTE-MAINTENANCE-ID:WorkOrder-31415\nX-MAINTNOTE-IMPACT:OUTAGE\nX-MAINTNOTE-OBJECT-ID;X-MAINTNOTE-OBJECT-IMPACT=NO-IMPACT:acme-widgets-as-a-service\nX-MAINTNOTE-OBJECT-ID;X-MAINTNOTE-OBJECT-IMPACT=OUTAGE:acme-widgets-as-a-service-2\nX-MAINTNOTE-STATUS:TENTATIVE\nORGANIZER;CN="Example NOC":mailto:noone@example.com\nEND:VEVENT\nEND:VCALENDAR\n"""\n\ndata_to_process = NotificationData.init_from_raw("ical", raw_data)\n\ntype(data_to_process)\n<class \'circuit_maintenance_parser.data.NotificationData\'>\n```\n\nFinally, with we retrieve the maintenances (it is a `List` because a notification can contain multiple maintenances) from the data calling the `get_maintenances` method from the `Provider` instance:\n\n```python\nmaintenances = generic_provider.get_maintenances(data_to_process)\n\nprint(maintenances[0].to_json())\n{\n"account": "137.035999173",\n"circuits": [\n{\n"circuit_id": "acme-widgets-as-a-service",\n"impact": "NO-IMPACT"\n},\n{\n"circuit_id": "acme-widgets-as-a-service-2",\n"impact": "OUTAGE"\n}\n],\n"end": 1444471200,\n"maintenance_id": "WorkOrder-31415",\n"organizer": "mailto:noone@example.com",\n"provider": "example.com",\n"sequence": 1,\n"stamp": 1444435800,\n"start": 1444464000,\n"status": "TENTATIVE",\n"summary": "Maint Note Example",\n"uid": "42"\n}\n```\n\nNotice that, either with the `GenericProvider` or `NTT` provider, we get the same result from the same data, because they are using exactly the same `Processor` and `Parser`. The only difference is that `NTT` notifications come without `organizer` and `provider` in the notification, and this info is fulfilled with some default values for the `Provider`, but in this case the original notification contains all the necessary information, so the defaults are not used.\n\n```python\nntt_maintenances = ntt_provider.get_maintenances(data_to_process)\nassert maintenances_ntt == maintenances\n```\n\n### CLI\n\nThere is also a `cli` entrypoint `circuit-maintenance-parser` which offers easy access to the library using few arguments:\n\n- `data-file`: file storing the notification.\n- `data-type`: `ical`, `html` or `email`, depending on the data type.\n- `provider-type`: to choose the right `Provider`. If empty, the `GenericProvider` is used.\n\n```bash\ncircuit-maintenance-parser --data-file "/tmp/___ZAYO TTN-00000000 Planned MAINTENANCE NOTIFICATION___.eml" --data-type email --provider-type zayo\nCircuit Maintenance Notification #0\n{\n  "account": "some account",\n  "circuits": [\n    {\n      "circuit_id": "/OGYX/000000/ /ZYO /",\n      "impact": "OUTAGE"\n    }\n  ],\n  "end": 1601035200,\n  "maintenance_id": "TTN-00000000",\n  "organizer": "mr@zayo.com",\n  "provider": "zayo",\n  "sequence": 1,\n  "stamp": 1599436800,\n  "start": 1601017200,\n  "status": "CONFIRMED",\n  "summary": "Zayo will implement planned maintenance to troubleshoot and restore degraded span",\n  "uid": "0"\n}\n```\n\n## How to Extend the Library?\n\nEven though the library aims to include support for as many providers as possible, it\'s likely that not all the thousands of NSP are supported and you may need to add support for some new one. Adding a new `Provider` is quite straightforward, and in the following example we are adding support for an imaginary provider, ABCDE, that uses HTML notifications.\n\nFirst step is creating a new file: `circuit_maintenance_parser/parsers/abcde.py`. This file will contain all the custom parsers needed for the provider and it will import the base classes for each parser type from `circuit_maintenance_parser.parser`. In the example, we only need to import `Html` and in the child class implement the methods required by the class, in this case `parse_html()` which will return a `dict` with all the data that this `Parser` can extract. In this case we have to helper methods, `_parse_bs` and `_parse_tables` that implement the logic to navigate the notification data.\n\n```python\nfrom typing import Dict\nimport bs4  # type: ignore\nfrom bs4.element import ResultSet  # type: ignore\nfrom circuit_maintenance_parser.parser import Html\n\nclass HtmlParserABCDE1(Html):\n    def parse_html(self, soup: ResultSet) -> Dict:\n        data = {}\n        self._parse_bs(soup.find_all("b"), data)\n        self._parse_tables(soup.find_all("table"), data)\n        return [data]\n\n    def _parse_bs(self, btags: ResultSet, data: Dict):\n      ...\n\n    def _parse_tables(self, tables: ResultSet, data: Dict):\n      ...\n```\n\nNext step is to create the new `Provider` by defining a new class in `circuit_maintenance_parser/provider.py`. This class that inherits from `GenericProvider` only needs to define two attributes:\n\n- `_processors`: is a `list` of `Processor` instances that uses several data `Parsers`. In this example, we don\'t need to create a new custom `Processor` because the combined logic serves well (the most likely case), and we only need to use the new defined `HtmlParserABCDE1` and also the generic `EmailDateParser` that extract the email date. Also notice that you could have multiple `Processors` with different `Parsers` in this list, supporting several formats.\n- `_default_organizer`: this is a default helper to fill the `organizer` attribute in the `Maintenance` if the information is not part of the original notification.\n\n```python\nclass ABCDE(GenericProvider):\n    _processors: List[GenericProcessor] = [\n        CombinedProcessor(data_parsers=[EmailDateParser, HtmlParserABCDE1]),\n    ]\n    _default_organizer = "noc@abcde.com"\n```\n\nAnd expose the new `Provider` in `circuit_maintenance_parser/__init__.py`:\n\n```python\nfrom .provider import (\n    GenericProvider,\n    ABCDE,\n    ...\n)\n\nSUPPORTED_PROVIDERS = (\n    GenericProvider,\n    ABCDE,\n    ...\n)\n```\n\nLast, but not least, you should update the tests!\n\n- Test the new `Parser` in `tests/unit/test_parsers.py`\n- Test the new `Provider` logic in `tests/unit/test_e2e.py`\n\n... adding the necessary data samples in `tests/unit/data/abcde/`.\n\n# Contributing\n\nPull requests are welcomed and automatically built and tested against multiple versions of Python through Travis CI.\n\nThe project is following Network to Code software development guidelines and is leveraging:\n\n- Black, Pylint, Mypy, Bandit and pydocstyle for Python linting and formatting.\n- Unit and integration tests to ensure the library is working properly.\n\n## Local Development\n\n### Requirements\n\n- Install `poetry`\n- Install dependencies and library locally: `poetry install`\n- Run CI tests locally: `invoke tests --local`\n\n### How to add a new Circuit Maintenance provider?\n\n1. Define the `Parsers`(inheriting from some of the generic `Parsers` or a new one) that will extract the data from the notification, that could contain itself multiple `DataParts`. The `data_type` of the `Parser` and the `DataPart` have to match. The custom `Parsers` will be placed in the `parsers` folder.\n2. Update the `unit/test_parsers.py` with the new parsers, providing some data to test and validate the extracted data.\n3. Define a new `Provider` inheriting from the `GenericProvider`, defining the `Processors` and the respective `Parsers` to be used. Maybe you can reuse some of the generic `Processors` or maybe you will need to create a custom one. If this is the case, place it in the `processors` folder.\n   - The `Provider` also supports the definition of a `_include_filter` and a `_exclude_filter` to limit the notifications that are actually processed, avoiding false positive errors for notification that are not relevant.\n4. Update the `unit/test_e2e.py` with the new provider, providing some data to test and validate the final `Maintenances` created.\n5. **Expose the new `Provider` class** updating the map `SUPPORTED_PROVIDERS` in `circuit_maintenance_parser/__init__.py` to officially expose the `Provider`.\n\n## Questions\n\nFor any questions or comments, please check the [FAQ](FAQ.md) first and feel free to swing by the [Network to Code slack channel](https://networktocode.slack.com/) (channel #networktocode).\nSign up [here](http://slack.networktocode.com/)\n\n## License notes\n\nThis library uses a Basic World Cities Database by Pareto Software, LLC, the owner of Simplemaps.com: The Provider offers a Basic World Cities Database free of charge. This database is licensed under the Creative Commons Attribution 4.0 license as described at: https://creativecommons.org/licenses/by/4.0/.\n',
    'author': 'Network to Code',
    'author_email': 'opensource@networktocode.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/networktocode/circuit-maintenance-parser',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
