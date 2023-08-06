from cone.tile import Tile
import json


class MapTile(Tile):
    """Tile rendering a leaflet map.

    Reference: https://leafletjs.com/reference.html
    """

    map_factory = 'cone_maps.Map'
    """Factory used for map creation in Javascript.

    The definded factory must accept the map related DOM element as argument
    and is responsible to initialize the leaflet map.

    It points to a class or function and does property lookup on window with
    '.' as delimiter, e.g:

        'cone_maps.Map'

    corresponds to:

        cone_maps: {
            Map: {}
        }

    If JS map factory needs to be customized, this is usually done by subclassing
    'cone_maps.Map':

        my_namespace = {};

        my_namespace.Map = class extends cone_maps.Map {
            constructor(elem) {
                elem.height(800);
                super(elem);
            }
        }
    """

    map_id = 'map'
    """HTML id of the map.
    """

    map_css = 'cone-map'
    """CSS class of the map element.

    The default JS map implementation searches for
    for all `div` elements with `cone-map` CSS class set and initializes map
    instances for them.

    If it's desired to completly customize map instancing on client side, this
    property must be changed.
    """

    map_options = {}
    """Map options passed to the leaflet map constructor.

    See: https://leafletjs.com/reference.html#map-l-map
    """

    map_control_options = {}
    """Layers control options passed to the leaflet layers control constructor.

    See: https://leafletjs.com/reference.html#control-layers
    """

    map_layers = [{
        # general layer options
        'factory': 'tile_layer',   # layer factory
        'category': 'base',        # base|overlay
        'display': True,           # initial display
        'title': 'OpenStreetMap',  # layer title
        # factory specific layer options
        'urlTemplate': '//{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        'options': {
            'attribution': 'OSM map data © <a href="http://openstreetmap.org">OSM</a>',
            'minZoom': 2,
            'maxZoom': 18
        }
    }]
    """List of map layer definitions.

    See: https://leafletjs.com/reference.html
    """

    map_center = [47.2688805, 11.3929127]
    """The default (initial) center of the map as lat/lng.
    """

    map_zoom = 8
    """The default (initial) zoom level of the map
    """

    map_markers = []
    """List of map markers to display.
    """

    map_markers_source = None
    """JSON endpoint to fetch markers from.
    """

    map_marker_groups = []
    """List of map marker groups to display.
    """

    map_marker_groups_source = None
    """JSON endpoint to fetch marker groups from.
    """

    def render(self):
        return (
            u'<div class="{css}"'
            u'     id="{id}"'
            u'     data-map-factory="{factory}"'
            u'     data-map-options=\'{options}\''
            u'     data-map-control-options=\'{control_options}\''
            u'     data-map-layers=\'{layers}\''
            u'     data-map-center=\'{center}\''
            u'     data-map-zoom="{zoom}"'
            u'     data-map-markers=\'{markers}\''
            u'     data-map-markers-source="{markers_source}"'
            u'     data-map-groups=\'{marker_groups}\''
            u'     data-map-groups-source="{marker_groups_source}" >'
            u'</div>'
        ).format(
            css=self.map_css,
            id=self.map_id,
            factory=self.map_factory,
            options=json.dumps(self.map_options),
            control_options=json.dumps(self.map_control_options),
            layers=json.dumps(self.map_layers),
            center=json.dumps(self.map_center),
            zoom=self.map_zoom,
            markers=self.map_markers,
            markers_source=self.map_markers_source,
            marker_groups=self.map_marker_groups,
            marker_groups_source=self.map_marker_groups_source,
        )
