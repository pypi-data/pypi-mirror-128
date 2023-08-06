from cone.app import testing
from cone.tile.tests import TileTestCase
from cone.app.model import BaseNode
from cone.maps.browser.map import MapTile
import sys
import unittest


class MapsLayer(testing.Security):

    def make_app(self, **kw):
        super(MapsLayer, self).make_app(**{
            'cone.plugins': 'cone.maps'
        })


class TestMapsTile(TileTestCase):
    layer = MapsLayer()

    def test_map_tile(self):
        model = BaseNode(name='map')
        request = self.layer.new_request()

        map_tile = MapTile()
        res = map_tile(model, request)
        self.assertTrue(res.find('class="cone_map"') > -1)
        self.assertTrue(res.find('id="map"') > -1)
        self.assertTrue(res.find('data-map-factory="cone.maps.Map"') > -1)
        self.assertTrue(res.find('data-map-layers=') > -1)
        self.assertTrue(res.find('data-map-center=') > -1)
        self.assertTrue(res.find('data-map-zoom="8"') > -1)
        self.assertTrue(res.find('data-map-source="None"') > -1)


def run_tests():
    from cone.maps import tests
    from zope.testrunner.runner import Runner

    suite = unittest.TestSuite()
    suite.addTest(unittest.findTestCases(tests))

    runner = Runner(found_suites=[suite])
    runner.run()
    sys.exit(int(runner.failed))


if __name__ == '__main__':
    run_tests()
