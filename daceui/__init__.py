# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

from pyramid.config import Configurator
from pyramid.i18n import TranslationStringFactory

from substanced.db import root_factory


_ = TranslationStringFactory('daceui')


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings, root_factory=root_factory)
    config.add_translation_dirs('pontus:locale/')
    config.add_translation_dirs('dace:locale/')
    config.add_translation_dirs('deform:locale/')
    config.add_translation_dirs('colander:locale/')
    config.scan()
    YEAR = 86400 * 365
    config.add_static_view(
    	 'daceuistatic', 'daceui:static', cache_max_age=YEAR)
    return config.make_wsgi_app()