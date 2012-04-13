"""import haystack
from cms.models import monkeypatch_reverse
from cms.plugin_pool import plugin_pool

plugin_pool.get_plugin('TextPlugin').search_fulltext = True

monkeypatch_reverse()    
haystack.autodiscover()"""