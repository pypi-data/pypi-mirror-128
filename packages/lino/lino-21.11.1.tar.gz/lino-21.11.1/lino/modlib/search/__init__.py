# Copyright 2008-2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""
Intelligent search functionality.

Requires ElasticSearch to be installed.

See :doc:`/plugins/search`.
"""

import os
import subprocess
from pathlib import Path

from django.conf import settings

from lino.api import ad
from lino.core.site import has_elasticsearch

class Plugin(ad.Plugin):
    "See :class:`lino.core.plugin.Plugin`."

    # needs_plugins = ['lino.modlib.restful']

    use_elasticsearch = False

    # ES_url = 'localhost:9200' # running a docker instance locally
    ES_url = 'https://elastic:mMh6KlFP0UAooywwsWPLJ3ae@lino.es.us-central1.gcp.cloud.es.io:9243'
    """URL to the elasticsearch instance"""

    mappings_dir = Path(__file__).parent / 'search/mappings'

    debian_dev_server = False

    DEFAULT_ES_INDEX_SETTINGS = {
        'settings': {
            'analysis': {
                'analyzer': {
                    'autocomplete': {
                        'tokenizer': 'autocomplete',
                        'filter': ['lowercase']
                    },
                    'autocomplete_search': {
                        'tokenizer': 'lowercase'
                    },
                    'index_analyzer': {
                        'tokenizer': 'autocomplete',
                        'filter': ['lowercase']
                    }
                },
                'tokenizer': {
                    'autocomplete': {
                        'type': 'edge_ngram',
                        'min_gram': 2,
                        'max_gram': 20,
                        'token_chars': ['letter', 'digit', 'punctuation'],
                        'custom_token_chars': '#+-_'
                    }
                }
            }
        }
    }

    def on_init(self):
        super().on_init()
        if self.site.use_elasticsearch:
            from lino.modlib.search.utils import ESResolver, get_client
            if get_client is not None:
                self.needs_plugins.append('elasticsearch_django')

                sarset = {
                    'connections': {
                        'default': self.ES_url,
                    },
                    'indexes': ESResolver.read_indexes(),
                    'settings': {
                        'chunk_size': 500,
                        'page_size': 15,
                        'auto_sync': True,
                        'strict_validation': False,
                        'mappings_dir': self.mappings_dir,
                        'never_auto_sync': [],
                    }
                }
                self.site.update_settings(SEARCH_SETTINGS=sarset)

    def get_requirements(self, site):
        if site.use_elasticsearch:
            yield 'elasticsearch-django'
        # else:
        #     return []

    def get_quicklinks(self):
        if has_elasticsearch and self.site.use_elasticsearch:
            yield 'search.ElasticSiteSearch'
        else:
            yield 'search.SiteSearch'
