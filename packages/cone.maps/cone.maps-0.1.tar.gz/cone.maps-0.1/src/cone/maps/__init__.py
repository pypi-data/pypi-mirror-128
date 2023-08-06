from cone.app import cfg
from cone.app import main_hook
from cone.maps.browser import static_resources
import logging


logger = logging.getLogger('cone.maps')


@main_hook
def initialize_maps(config, global_config, settings):
    # application startup initialization

    # ignore yafowil leaflet dependencies if cone.maps is installed
    cfg.yafowil.js_skip.add('yafowil.widget.location.dependencies')
    cfg.yafowil.css_skip.add('yafowil.widget.location.dependencies')

    # resources
    if settings.get('cone.maps.public', 'false') == 'true':
        css_res = cfg.css.public
        js_res = cfg.js.public
    else:
        css_res = cfg.css.protected
        js_res = cfg.js.protected

    # leaflet core
    css_res.append('maps-static/leaflet/leaflet.css')
    js_res.append('maps-static/leaflet/leaflet.js')

    # Leaflet.TileLayer.NoGap
    if settings.get('cone.maps.nogap', 'false') == 'true':
        js_res.append('maps-static/leaflet-nogap/L.TileLayer.NoGap.js')

    # leaflet-geosearch
    if settings.get('cone.maps.geosearch', 'false') == 'true':
        css_res.append('maps-static/leaflet-geosearch/geosearch.css')
        js_res.append('maps-static/leaflet-geosearch/geosearch.umd.js')

    # Leaflet.markercluster
    if settings.get('cone.maps.markercluster', 'false') == 'true':
        css_res.append('maps-static/leaflet-markercluster/MarkerCluster.css')
        css_res.append('maps-static/leaflet-markercluster/MarkerCluster.Default.css')
        js_res.append('maps-static/leaflet-markercluster/leaflet.markercluster.js')

    # Leaflet-active-area
    if settings.get('cone.maps.activearea', 'false') == 'true':
        js_res.append('maps-static/leaflet-activearea/leaflet.activearea.js')

    # proj4js and Proj4Leaflet
    if settings.get('cone.maps.proj4', 'false') == 'true':
        js_res.append('maps-static/proj4js/proj4.js')
        js_res.append('maps-static/leaflet-proj4/proj4leaflet.js')

    # cone maps
    js_res.append('maps-static/cone.maps.js')

    # add translation
    config.add_translation_dirs('cone.maps:locale/')

    # static resources
    config.add_view(static_resources, name='maps-static')

    # scan browser package
    config.scan('cone.maps.browser')
