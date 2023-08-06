.. image:: https://img.shields.io/pypi/v/cone.maps.svg
    :target: https://pypi.python.org/pypi/cone.maps
    :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/dm/cone.maps.svg
    :target: https://pypi.python.org/pypi/cone.maps
    :alt: Number of PyPI downloads

.. image:: https://github.com/conestack/cone.maps/actions/workflows/python-package.yml/badge.svg
    :target: https://github.com/conestack/cone.maps/actions/workflows/python-package.yml
    :alt: Package build

.. image:: https://coveralls.io/repos/github/bluedynamics/cone.maps/badge.svg?branch=master
    :target: https://coveralls.io/github/bluedynamics/cone.maps?branch=master


This package provides maps integration in to cone.app.

* As maps library, `Leaflet JS <https://leafletjs.com/>`_ (v1.7.1) is included.
  It utilizes `Leaflet JS <https://leafletjs.com/>`_.

* For avoiding 1px gap between tiles,
  `Leaflet.TileLayer.NoGap <https://github.com/Leaflet/Leaflet.TileLayer.NoGap>`_
  `(ab4f107) <https://github.com/Leaflet/Leaflet.TileLayer.NoGap/commit/ab4f107fecb80e12ffbdc4ebbedf5f85b8da7173>`_ is included.

* For geocoding,
  `leaflet-geosearch <https://smeijer.github.io/leaflet-geosearch>`_
  (3.5.0) is included.

* For grouping of map markers,
  `Leaflet.markercluster <https://github.com/Leaflet/Leaflet.markercluster>`_
  (1.5.3) is included.

* For defining active map area, e.g. if parts of a map is used as background,
  `Leaflet-active-area <https://github.com/Mappy/Leaflet-active-area>`_
  (1.2.0) is included.

* For general CRS projection support,
  `proj4js <https://github.com/proj4js/proj4js>`_ (2.7.5) and
  `Proj4Leaflet <https://github.com/kartena/Proj4Leaflet>`_ (1.0.2)
  are included


Map Widget
----------

A map widget tile is included which provides OOTB default map behavior and
can be used as starting point for complex custom maps.

.. code-block:: python

    from cone.maps.browser.map import MapTile
    from cone.tile import tile
    from myplugin import MyModel

    @tile(name='map', interface=MyModel)
    class MyMap(MapTile):
        """See ``cone.maps.browser.map`` for available tile options.
        """


Resources
---------

The following ``cone.maps`` related application configuration options are
available :

- **cone.maps.public**: Flag whether browser resources are delivered for
  unauthenticated users. Defaults to `false`.

- **cone.maps.nogap**: Flag whether to include ``Leaflet.TileLayer.NoGap``
  plugin. Defaults to `false`.

- **cone.maps.geosearch**: Flag whether to include ``leaflet-geosearch``
  plugin. Defaults to `false`.

- **cone.maps.markercluster**: Flag whether to include ``Leaflet.markercluster``
  plugin. Defaults to `false`.

- **cone.maps.activearea**: Flag whether to include ``Leaflet-active-area``
  plugin. Defaults to `false`.

- **cone.maps.proj4**: Flag whether to include ``proj4js`` and ``Proj4Leaflet``
  plugins. Defaults to `false`.


Contributors
============

- Robert Niederreiter


TODO
====

- Default map marker rendering (from DOM elem data directly and from
  JSON endpoint)

- Default map markercluster rendering (from DOM elem data directly and from
  JSON endpoint)

- Geosearch on default map.

- Activearea config on default map.
