# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2021 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/
"""Basic tests for PlotWidget"""

__authors__ = ["T. Vincent"]
__license__ = "MIT"
__date__ = "03/01/2019"


import unittest
import logging
import numpy
import pytest

from silx.utils.testutils import ParametricTestCase
from silx.gui.utils.testutils import SignalListener
from silx.gui.utils.testutils import TestCaseQt

from silx.gui import qt
from silx.gui.plot import PlotWidget
from silx.gui.plot.items.curve import CurveStyle
from silx.gui.plot.items import BoundingRect, XAxisExtent, YAxisExtent, Axis
from silx.gui.colors import Colormap

from .utils import PlotWidgetTestCase


SIZE = 1024
"""Size of the test image"""

DATA_2D = numpy.arange(SIZE ** 2).reshape(SIZE, SIZE)
"""Image data set"""


logger = logging.getLogger(__name__)


class TestSpecialBackend(PlotWidgetTestCase, ParametricTestCase):

    def __init__(self, methodName='runTest', backend=None):
        TestCaseQt.__init__(self, methodName=methodName)
        self.__backend = backend

    def _createPlot(self):
        return PlotWidget(backend=self.__backend)

    def testPlot(self):
        self.assertIsNotNone(self.plot)


class TestPlotWidget(PlotWidgetTestCase, ParametricTestCase):
    """Basic tests for PlotWidget"""

    def testShow(self):
        """Most basic test"""
        pass

    def testSetTitleLabels(self):
        """Set title and axes labels"""

        title, xlabel, ylabel = 'the title', 'x label', 'y label'
        self.plot.setGraphTitle(title)
        self.plot.getXAxis().setLabel(xlabel)
        self.plot.getYAxis().setLabel(ylabel)
        self.qapp.processEvents()

        self.assertEqual(self.plot.getGraphTitle(), title)
        self.assertEqual(self.plot.getXAxis().getLabel(), xlabel)
        self.assertEqual(self.plot.getYAxis().getLabel(), ylabel)

    def _checkLimits(self,
                     expectedXLim=None,
                     expectedYLim=None,
                     expectedRatio=None):
        """Assert that limits are as expected"""
        xlim = self.plot.getXAxis().getLimits()
        ylim = self.plot.getYAxis().getLimits()
        ratio = abs(xlim[1] - xlim[0]) / abs(ylim[1] - ylim[0])

        if expectedXLim is not None:
            self.assertEqual(expectedXLim, xlim)

        if expectedYLim is not None:
            self.assertEqual(expectedYLim, ylim)

        if expectedRatio is not None:
            self.assertTrue(
                numpy.allclose(expectedRatio, ratio, atol=0.01))

    def testChangeLimitsWithAspectRatio(self):
        self.plot.setKeepDataAspectRatio()
        self.qapp.processEvents()
        xlim = self.plot.getXAxis().getLimits()
        ylim = self.plot.getYAxis().getLimits()
        defaultRatio = abs(xlim[1] - xlim[0]) / abs(ylim[1] - ylim[0])

        self.plot.getXAxis().setLimits(1., 10.)
        self._checkLimits(expectedXLim=(1., 10.), expectedRatio=defaultRatio)
        self.qapp.processEvents()
        self._checkLimits(expectedXLim=(1., 10.), expectedRatio=defaultRatio)

        self.plot.getYAxis().setLimits(1., 10.)
        self._checkLimits(expectedYLim=(1., 10.), expectedRatio=defaultRatio)
        self.qapp.processEvents()
        self._checkLimits(expectedYLim=(1., 10.), expectedRatio=defaultRatio)

    def testResizeWidget(self):
        """Test resizing the widget and receiving limitsChanged events"""
        self.plot.resize(200, 200)
        self.qapp.processEvents()
        self.qWait(100)

        xlim = self.plot.getXAxis().getLimits()
        ylim = self.plot.getYAxis().getLimits()

        listener = SignalListener()
        self.plot.getXAxis().sigLimitsChanged.connect(listener.partial('x'))
        self.plot.getYAxis().sigLimitsChanged.connect(listener.partial('y'))

        # Resize without aspect ratio
        self.plot.resize(200, 300)
        self.qapp.processEvents()
        self.qWait(100)
        self._checkLimits(expectedXLim=xlim, expectedYLim=ylim)
        self.assertEqual(listener.callCount(), 0)

        # Resize with aspect ratio
        self.plot.setKeepDataAspectRatio(True)
        self.qapp.processEvents()
        self.qWait(1000)
        listener.clear()  # Clean-up received signal

        self.plot.resize(200, 200)
        self.qapp.processEvents()
        self.qWait(100)
        self.assertNotEqual(listener.callCount(), 0)

    def testAddRemoveItemSignals(self):
        """Test sigItemAdded and sigItemAboutToBeRemoved"""
        listener = SignalListener()
        self.plot.sigItemAdded.connect(listener.partial('add'))
        self.plot.sigItemAboutToBeRemoved.connect(listener.partial('remove'))

        self.plot.addCurve((1, 2, 3), (3, 2, 1), legend='curve')
        self.assertEqual(listener.callCount(), 1)

        curve = self.plot.getCurve('curve')
        self.plot.remove('curve')
        self.assertEqual(listener.callCount(), 2)
        self.assertEqual(listener.arguments(callIndex=0), ('add', curve))
        self.assertEqual(listener.arguments(callIndex=1), ('remove', curve))

    def testGetItems(self):
        """Test getItems method"""
        curve_x = 1, 2
        self.plot.addCurve(curve_x, (3, 4))
        image = (0, 1), (2, 3)
        self.plot.addImage(image)
        scatter_x = 10, 11
        self.plot.addScatter(scatter_x, (12, 13), (0, 1))
        marker_pos = 5, 5
        self.plot.addMarker(*marker_pos)
        marker_x = 6
        self.plot.addXMarker(marker_x)
        self.plot.addShape((0, 5), (2, 10), shape='rectangle')

        items = self.plot.getItems()
        self.assertEqual(len(items), 6)
        self.assertTrue(numpy.all(numpy.equal(items[0].getXData(), curve_x)))
        self.assertTrue(numpy.all(numpy.equal(items[1].getData(), image)))
        self.assertTrue(numpy.all(numpy.equal(items[2].getXData(), scatter_x)))
        self.assertTrue(numpy.all(numpy.equal(items[3].getPosition(), marker_pos)))
        self.assertTrue(numpy.all(numpy.equal(items[4].getPosition()[0], marker_x)))
        self.assertEqual(items[5].getType(), 'rectangle')

    def testRemoveDiscardItem(self):
        """Test removeItem and discardItem"""
        self.plot.addCurve((1, 2, 3), (1, 2, 3))
        curve = self.plot.getItems()[0]
        self.plot.removeItem(curve)
        with self.assertRaises(ValueError):
            self.plot.removeItem(curve)

        self.plot.addCurve((1, 2, 3), (1, 2, 3))
        curve = self.plot.getItems()[0]
        result = self.plot.discardItem(curve)
        self.assertTrue(result)
        result = self.plot.discardItem(curve)
        self.assertFalse(result)

    def testBackGroundColors(self):
        self.plot.setVisible(True)
        self.qWaitForWindowExposed(self.plot)
        self.qapp.processEvents()

        # Custom the full background
        color = self.plot.getBackgroundColor()
        self.assertTrue(color.isValid())
        self.assertEqual(color, qt.QColor(255, 255, 255))
        self.plot.setBackgroundColor("red")
        color = self.plot.getBackgroundColor()
        self.assertTrue(color.isValid())
        self.qapp.processEvents()

        # Custom the data background
        color = self.plot.getDataBackgroundColor()
        self.assertFalse(color.isValid())
        self.plot.setDataBackgroundColor("red")
        color = self.plot.getDataBackgroundColor()
        self.assertTrue(color.isValid())
        self.qapp.processEvents()

        # Back to default
        self.plot.setBackgroundColor('white')
        self.plot.setDataBackgroundColor(None)
        color = self.plot.getBackgroundColor()
        self.assertTrue(color.isValid())
        self.assertEqual(color, qt.QColor(255, 255, 255))
        color = self.plot.getDataBackgroundColor()
        self.assertFalse(color.isValid())
        self.qapp.processEvents()


class TestPlotImage(PlotWidgetTestCase, ParametricTestCase):
    """Basic tests for addImage"""

    def setUp(self):
        super(TestPlotImage, self).setUp()

        self.plot.getYAxis().setLabel('Rows')
        self.plot.getXAxis().setLabel('Columns')

    def testPlotColormapTemperature(self):
        self.plot.setGraphTitle('Temp. Linear')

        colormap = Colormap(name='temperature',
                            normalization='linear',
                            vmin=None,
                            vmax=None)
        self.plot.addImage(DATA_2D, legend="image 1", colormap=colormap)

    def testPlotColormapGray(self):
        self.plot.setKeepDataAspectRatio(False)
        self.plot.setGraphTitle('Gray Linear')

        colormap = Colormap(name='gray',
                            normalization='linear',
                            vmin=None,
                            vmax=None)
        self.plot.addImage(DATA_2D, legend="image 1", colormap=colormap)

    def testPlotColormapTemperatureLog(self):
        self.plot.setGraphTitle('Temp. Log')

        colormap = Colormap(name='temperature',
                            normalization=Colormap.LOGARITHM,
                            vmin=None,
                            vmax=None)
        self.plot.addImage(DATA_2D, legend="image 1", colormap=colormap)

    def testPlotRgbRgba(self):
        self.plot.setKeepDataAspectRatio(False)
        self.plot.setGraphTitle('RGB + RGBA')

        rgb = numpy.array(
            (((0, 0, 0), (128, 0, 0), (255, 0, 0)),
             ((0, 128, 0), (0, 128, 128), (0, 128, 255))),
            dtype=numpy.uint8)

        self.plot.addImage(rgb, legend="rgb_uint8",
                           origin=(0, 0), scale=(1, 1),
                           resetzoom=False)

        rgb = numpy.array(
            (((0, 0, 0), (32768, 0, 0), (65535, 0, 0)),
             ((0, 32768, 0), (0, 32768, 32768), (0, 32768, 65535))),
            dtype=numpy.uint16)

        self.plot.addImage(rgb, legend="rgb_uint16",
                           origin=(3, 2), scale=(2, 2),
                           resetzoom=False)

        rgba = numpy.array(
            (((0, 0, 0, .5), (.5, 0, 0, 1), (1, 0, 0, .5)),
             ((0, .5, 0, 1), (0, .5, .5, 1), (0, 1, 1, .5))),
            dtype=numpy.float32)

        self.plot.addImage(rgba, legend="rgba_float32",
                           origin=(9, 6), scale=(1, 1),
                           resetzoom=False)

        self.plot.resetZoom()

    def testPlotColormapCustom(self):
        self.plot.setKeepDataAspectRatio(False)
        self.plot.setGraphTitle('Custom colormap')

        colormap = Colormap(name=None,
                            normalization=Colormap.LINEAR,
                            vmin=None,
                            vmax=None,
                            colors=((0., 0., 0.), (1., 0., 0.),
                               (0., 1., 0.), (0., 0., 1.)))
        self.plot.addImage(DATA_2D, legend="image 1", colormap=colormap,
                           resetzoom=False)

        colormap = Colormap(name=None,
                            normalization=Colormap.LINEAR,
                            vmin=None,
                            vmax=None,
                            colors=numpy.array(
                                ((0, 0, 0, 0), (0, 0, 0, 128),
                                 (128, 128, 128, 128), (255, 255, 255, 255)),
                                dtype=numpy.uint8))
        self.plot.addImage(DATA_2D, legend="image 2", colormap=colormap,
                           origin=(DATA_2D.shape[0], 0),
                           resetzoom=False)
        self.plot.resetZoom()

    def testPlotColormapNaNColor(self):
        self.plot.setKeepDataAspectRatio(False)
        self.plot.setGraphTitle('Colormap with NaN color')

        colormap = Colormap()
        colormap.setNaNColor('red')
        self.assertEqual(colormap.getNaNColor(), qt.QColor(255, 0, 0))
        data = DATA_2D.astype(numpy.float32)
        data[len(data)//2:] = numpy.nan
        self.plot.addImage(data, legend="image 1", colormap=colormap,
                           resetzoom=False)
        self.plot.resetZoom()

        colormap.setNaNColor((0., 1., 0., 1.))
        self.assertEqual(colormap.getNaNColor(), qt.QColor(0, 255, 0))
        self.qapp.processEvents()

    def testImageOriginScale(self):
        """Test of image with different origin and scale"""
        self.plot.setGraphTitle('origin and scale')

        tests = [  # (origin, scale)
            ((10, 20), (1, 1)),
            ((10, 20), (-1, -1)),
            ((-10, 20), (2, 1)),
            ((10, -20), (-1, -2)),
            (100, 2),
            (-100, (1, 1)),
            ((10, 20), 2),
            ]

        for origin, scale in tests:
            with self.subTest(origin=origin, scale=scale):
                self.plot.addImage(DATA_2D, origin=origin, scale=scale)

                try:
                    ox, oy = origin
                except TypeError:
                    ox, oy = origin, origin
                try:
                    sx, sy = scale
                except TypeError:
                    sx, sy = scale, scale
                xbounds = ox, ox + DATA_2D.shape[1] * sx
                ybounds = oy, oy + DATA_2D.shape[0] * sy

                # Check limits without aspect ratio
                xmin, xmax = self.plot.getXAxis().getLimits()
                ymin, ymax = self.plot.getYAxis().getLimits()
                self.assertEqual(xmin, min(xbounds))
                self.assertEqual(xmax, max(xbounds))
                self.assertEqual(ymin, min(ybounds))
                self.assertEqual(ymax, max(ybounds))

                # Check limits with aspect ratio
                self.plot.setKeepDataAspectRatio(True)
                xmin, xmax = self.plot.getXAxis().getLimits()
                ymin, ymax = self.plot.getYAxis().getLimits()
                self.assertTrue(round(xmin, 7) <= min(xbounds))
                self.assertTrue(round(xmax, 7) >= max(xbounds))
                self.assertTrue(round(ymin, 7) <= min(ybounds))
                self.assertTrue(round(ymax, 7) >= max(ybounds))

                self.plot.setKeepDataAspectRatio(False)  # Reset aspect ratio
                self.plot.clear()
                self.plot.resetZoom()

    def testPlotColormapDictAPI(self):
        """Test that the addImage API using a colormap dictionary is still
        working"""
        self.plot.setGraphTitle('Temp. Log')

        colormap = {
            'name': 'temperature',
            'normalization': 'log',
            'vmin': None,
            'vmax': None
        }
        self.plot.addImage(DATA_2D, legend="image 1", colormap=colormap)

    def testPlotComplexImage(self):
        """Test that a complex image is displayed as its absolute value."""
        data = numpy.linspace(1, 1j, 100).reshape(10, 10)
        self.plot.addImage(data, legend='complex')

        image = self.plot.getActiveImage()
        retrievedData = image.getData(copy=False)
        self.assertTrue(
            numpy.all(numpy.equal(retrievedData, numpy.absolute(data))))

    def testPlotBooleanImage(self):
        """Test that a boolean image is displayed and converted to int8."""
        data = numpy.zeros((10, 10), dtype=bool)
        data[::2, ::2] = True
        self.plot.addImage(data, legend='boolean')

        image = self.plot.getActiveImage()
        retrievedData = image.getData(copy=False)
        self.assertTrue(numpy.all(numpy.equal(retrievedData, data)))
        self.assertIs(retrievedData.dtype.type, numpy.int8)

    def testPlotAlphaImage(self):
        """Test with an alpha image layer"""
        data = numpy.random.random((10, 10))
        alpha = numpy.linspace(0, 1, 100).reshape(10, 10)
        self.plot.addImage(data, legend='image')
        image = self.plot.getActiveImage()
        image.setData(data, alpha=alpha)
        self.qapp.processEvents()
        self.assertTrue(numpy.array_equal(alpha, image.getAlphaData()))


class TestPlotCurve(PlotWidgetTestCase):
    """Basic tests for addCurve."""

    # Test data sets
    xData = numpy.arange(1000)
    yData = -500 + 100 * numpy.sin(xData)
    xData2 = xData + 1000
    yData2 = xData - 1000 + 200 * numpy.random.random(1000)

    def setUp(self):
        super(TestPlotCurve, self).setUp()
        self.plot.setGraphTitle('Curve')
        self.plot.getYAxis().setLabel('Rows')
        self.plot.getXAxis().setLabel('Columns')

        self.plot.setActiveCurveHandling(False)

    def testPlotCurveInfinite(self):
        """Test plot curves with not finite data"""
        tests = {
            'y all not finite': ([0, 1, 2], [numpy.inf, numpy.nan, -numpy.inf]),
            'x all not finite': ([numpy.inf, numpy.nan, -numpy.inf], [0, 1, 2]),
            'x some inf': ([0, numpy.inf, 2], [0, 1, 2]),
            'y some inf': ([0, 1, 2], [0, numpy.inf, 2])
        }
        for name, args in tests.items():
            with self.subTest(name):
                self.plot.addCurve(*args)
                self.plot.resetZoom()
                self.qapp.processEvents()
                self.plot.clear()

    def testPlotCurveColorFloat(self):
        color = numpy.array(numpy.random.random(3 * 1000),
                            dtype=numpy.float32).reshape(1000, 3)

        self.plot.addCurve(self.xData, self.yData,
                           legend="curve 1",
                           replace=False, resetzoom=False,
                           color=color,
                           linestyle="", symbol="s")
        self.plot.addCurve(self.xData2, self.yData2,
                           legend="curve 2",
                           replace=False, resetzoom=False,
                           color='green', linestyle="-", symbol='o')
        self.plot.resetZoom()

    def testPlotCurveColorByte(self):
        color = numpy.array(255 * numpy.random.random(3 * 1000),
                            dtype=numpy.uint8).reshape(1000, 3)

        self.plot.addCurve(self.xData, self.yData,
                           legend="curve 1",
                           replace=False, resetzoom=False,
                           color=color,
                           linestyle="", symbol="s")
        self.plot.addCurve(self.xData2, self.yData2,
                           legend="curve 2",
                           replace=False, resetzoom=False,
                           color='green', linestyle="-", symbol='o')
        self.plot.resetZoom()

    def testPlotCurveColors(self):
        color = numpy.array(numpy.random.random(3 * 1000),
                            dtype=numpy.float32).reshape(1000, 3)

        self.plot.addCurve(self.xData, self.yData,
                           legend="curve 2",
                           replace=False, resetzoom=False,
                           color=color, linestyle="-", symbol='o')
        self.plot.resetZoom()

        # Test updating color array

        # From array to array
        newColors = numpy.ones((len(self.xData), 3), dtype=numpy.float32)
        self.plot.addCurve(self.xData, self.yData,
                           legend="curve 2",
                           replace=False, resetzoom=False,
                           color=newColors, symbol='o')

        # Array to single color
        self.plot.addCurve(self.xData, self.yData,
                           legend="curve 2",
                           replace=False, resetzoom=False,
                           color='green', symbol='o')

        # single color to array
        self.plot.addCurve(self.xData, self.yData,
                           legend="curve 2",
                           replace=False, resetzoom=False,
                           color=color, symbol='o')

    def testPlotBaselineNumpyArray(self):
        """simple test of the API with baseline as a numpy array"""
        x = numpy.arange(0, 10, step=0.1)
        my_sin = numpy.sin(x)
        y = numpy.arange(-4, 6, step=0.1) + my_sin
        baseline = y - 1.0

        self.plot.addCurve(x=x, y=y, color='grey', legend='curve1', fill=True,
                           baseline=baseline)

    def testPlotBaselineScalar(self):
        """simple test of the API with baseline as an int"""
        x = numpy.arange(0, 10, step=0.1)
        my_sin = numpy.sin(x)
        y = numpy.arange(-4, 6, step=0.1) + my_sin

        self.plot.addCurve(x=x, y=y, color='grey', legend='curve1', fill=True,
                           baseline=0)

    def testPlotBaselineList(self):
        """simple test of the API with baseline as an int"""
        x = numpy.arange(0, 10, step=0.1)
        my_sin = numpy.sin(x)
        y = numpy.arange(-4, 6, step=0.1) + my_sin

        self.plot.addCurve(x=x, y=y, color='grey', legend='curve1', fill=True,
                           baseline=list(range(0, 100, 1)))

    def testPlotCurveComplexData(self):
        """Test curve with complex data"""
        data = numpy.arange(100.) + 1j
        self.plot.addCurve(x=data, y=data, xerror=data, yerror=data)


class TestPlotHistogram(PlotWidgetTestCase):
    """Basic tests for add Histogram"""
    def setUp(self):
        super(TestPlotHistogram, self).setUp()
        self.edges = numpy.arange(0, 10, step=1)
        self.histogram = numpy.random.random(len(self.edges))

    def testPlot(self):
        self.plot.addHistogram(histogram=self.histogram,
                               edges=self.edges,
                               legend='histogram1')

    def testPlotBaseline(self):
        self.plot.addHistogram(histogram=self.histogram,
                               edges=self.edges,
                               legend='histogram1',
                               color='blue',
                               baseline=-2,
                               z=2,
                               fill=True)


class TestPlotScatter(PlotWidgetTestCase, ParametricTestCase):
    """Basic tests for addScatter"""

    def testScatter(self):
        x = numpy.arange(100)
        y = numpy.arange(100)
        value = numpy.arange(100)
        self.plot.addScatter(x, y, value)
        self.plot.resetZoom()

    def testScatterComplexData(self):
        """Test scatter item with complex data"""
        data = numpy.arange(100.) + 1j
        self.plot.addScatter(
            x=data, y=data, value=data, xerror=data, yerror=data)
        self.plot.resetZoom()

    def testScatterVisualization(self):
        self.plot.addScatter((0, 1, 0, 1), (0, 0, 2, 2), (0, 1, 2, 3))
        self.plot.resetZoom()
        self.qapp.processEvents()

        scatter = self.plot.getItems()[0]

        for visualization in ('solid',
                              'points',
                              'regular_grid',
                              'irregular_grid',
                              'binned_statistic',
                              scatter.Visualization.SOLID,
                              scatter.Visualization.POINTS,
                              scatter.Visualization.REGULAR_GRID,
                              scatter.Visualization.IRREGULAR_GRID,
                              scatter.Visualization.BINNED_STATISTIC):
            with self.subTest(visualization=visualization):
                scatter.setVisualization(visualization)
                self.qapp.processEvents()

    def testGridVisualization(self):
        """Test regular and irregular grid mode with different points"""
        points = {  # name: (x, y, order)
            'single point': ((1.,), (1.,), 'row'),
            'horizontal line': ((0, 1, 2), (0, 0, 0), 'row'),
            'horizontal line backward': ((2, 1, 0), (0, 0, 0), 'row'),
            'vertical line': ((0, 0, 0), (0, 1, 2), 'row'),
            'vertical line backward': ((0, 0, 0), (2, 1, 0), 'row'),
            'grid fast x, +x +y': ((0, 1, 2, 0, 1, 2), (0, 0, 0, 1, 1, 1), 'row'),
            'grid fast x, +x -y': ((0, 1, 2, 0, 1, 2), (1, 1, 1, 0, 0, 0), 'row'),
            'grid fast x, -x -y': ((2, 1, 0, 2, 1, 0), (1, 1, 1, 0, 0, 0), 'row'),
            'grid fast x, -x +y': ((2, 1, 0, 2, 1, 0), (0, 0, 0, 1, 1, 1), 'row'),
            'grid fast y, +x +y': ((0, 0, 0, 1, 1, 1), (0, 1, 2, 0, 1, 2), 'column'),
            'grid fast y, +x -y': ((0, 0, 0, 1, 1, 1), (2, 1, 0, 2, 1, 0), 'column'),
            'grid fast y, -x -y': ((1, 1, 1, 0, 0, 0), (2, 1, 0, 2, 1, 0), 'column'),
            'grid fast y, -x +y': ((1, 1, 1, 0, 0, 0), (0, 1, 2, 0, 1, 2), 'column'),
            }

        self.plot.addScatter((), (), ())
        scatter = self.plot.getItems()[0]

        self.qapp.processEvents()

        for visualization in (scatter.Visualization.REGULAR_GRID,
                              scatter.Visualization.IRREGULAR_GRID):
            scatter.setVisualization(visualization)
            self.assertIs(scatter.getVisualization(), visualization)

            for name, (x, y, ref_order) in points.items():
                with self.subTest(name=name, visualization=visualization.name):
                    scatter.setData(x, y, numpy.arange(len(x)))
                    self.plot.setGraphTitle(name)
                    self.plot.resetZoom()
                    self.qapp.processEvents()

                    order = scatter.getCurrentVisualizationParameter(
                        scatter.VisualizationParameter.GRID_MAJOR_ORDER)
                    self.assertEqual(ref_order, order)

                    ref_bounds = (x[0], y[0]), (x[-1], y[-1])
                    bounds = scatter.getCurrentVisualizationParameter(
                        scatter.VisualizationParameter.GRID_BOUNDS)
                    self.assertEqual(ref_bounds, bounds)

                    shape = scatter.getCurrentVisualizationParameter(
                        scatter.VisualizationParameter.GRID_SHAPE)

                    self.plot.getXAxis().setLimits(numpy.min(x) - 1, numpy.max(x) + 1)
                    self.plot.getYAxis().setLimits(numpy.min(y) - 1, numpy.max(y) + 1)
                    self.qapp.processEvents()

                    for index, position in enumerate(zip(x, y)):
                        xpixel, ypixel = self.plot.dataToPixel(*position)
                        result = scatter.pick(xpixel, ypixel)
                        self.assertIsNotNone(result)
                        self.assertIs(result.getItem(), scatter)
                        self.assertEqual(result.getIndices(), (index,))

    def testBinnedStatisticVisualization(self):
        """Test binned display"""
        self.plot.addScatter((), (), ())
        scatter = self.plot.getItems()[0]
        scatter.setVisualization(scatter.Visualization.BINNED_STATISTIC)
        self.assertIs(scatter.getVisualization(),
                      scatter.Visualization.BINNED_STATISTIC)
        self.assertEqual(
            scatter.getVisualizationParameter(
                scatter.VisualizationParameter.BINNED_STATISTIC_FUNCTION),
            'mean')

        self.qapp.processEvents()

        scatter.setData(*numpy.random.random(300).reshape(3, -1))
        self.qapp.processEvents()

        # Update data
        scatter.setData(*numpy.random.random(3000).reshape(3, -1))
        self.qapp.processEvents()

        for reduction in ('count', 'sum', 'mean'):
            with self.subTest(reduction=reduction):
                scatter.setVisualizationParameter(
                    scatter.VisualizationParameter.BINNED_STATISTIC_FUNCTION,
                    reduction)
                self.assertEqual(
                    scatter.getVisualizationParameter(
                        scatter.VisualizationParameter.BINNED_STATISTIC_FUNCTION),
                    reduction)

                self.qapp.processEvents()


class TestPlotMarker(PlotWidgetTestCase):
    """Basic tests for add*Marker"""

    def setUp(self):
        super(TestPlotMarker, self).setUp()
        self.plot.getYAxis().setLabel('Rows')
        self.plot.getXAxis().setLabel('Columns')

        self.plot.getXAxis().setAutoScale(False)
        self.plot.getYAxis().setAutoScale(False)
        self.plot.setKeepDataAspectRatio(False)
        self.plot.setLimits(0., 100., -100., 100.)

    def testPlotMarkerX(self):
        self.plot.setGraphTitle('Markers X')

        markers = [
            (10., 'blue', False, False),
            (20., 'red', False, False),
            (40., 'green', True, False),
            (60., 'gray', True, True),
            (80., 'black', False, True),
        ]

        for x, color, select, drag in markers:
            name = str(x)
            if select:
                name += " sel."
            if drag:
                name += " drag"
            self.plot.addXMarker(x, name, name, color, select, drag)
        self.plot.resetZoom()

    def testPlotMarkerY(self):
        self.plot.setGraphTitle('Markers Y')

        markers = [
            (-50., 'blue', False, False),
            (-30., 'red', False, False),
            (0., 'green', True, False),
            (10., 'gray', True, True),
            (80., 'black', False, True),
        ]

        for y, color, select, drag in markers:
            name = str(y)
            if select:
                name += " sel."
            if drag:
                name += " drag"
            self.plot.addYMarker(y, name, name, color, select, drag)
        self.plot.resetZoom()

    def testPlotMarkerPt(self):
        self.plot.setGraphTitle('Markers Pt')

        markers = [
            (10., -50., 'blue', False, False),
            (40., -30., 'red', False, False),
            (50., 0., 'green', True, False),
            (50., 20., 'gray', True, True),
            (70., 50., 'black', False, True),
        ]
        for x, y, color, select, drag in markers:
            name = "{0},{1}".format(x, y)
            if select:
                name += " sel."
            if drag:
                name += " drag"
            self.plot.addMarker(x, y, name, name, color, select, drag)

        self.plot.resetZoom()

    def testPlotMarkerWithoutLegend(self):
        self.plot.setGraphTitle('Markers without legend')
        self.plot.getYAxis().setInverted(True)

        # Markers without legend
        self.plot.addMarker(10, 10)
        self.plot.addMarker(10, 20)
        self.plot.addMarker(40, 50, text='test', symbol=None)
        self.plot.addMarker(40, 50, text='test', symbol='+')
        self.plot.addXMarker(25)
        self.plot.addXMarker(35)
        self.plot.addXMarker(45, text='test')
        self.plot.addYMarker(55)
        self.plot.addYMarker(65)
        self.plot.addYMarker(75, text='test')

        self.plot.resetZoom()

    def testPlotMarkerYAxis(self):
        # Check only the API

        legend = self.plot.addMarker(10, 10)
        item = self.plot._getMarker(legend)
        self.assertEqual(item.getYAxis(), "left")

        legend = self.plot.addMarker(10, 10, yaxis="right")
        item = self.plot._getMarker(legend)
        self.assertEqual(item.getYAxis(), "right")

        legend = self.plot.addMarker(10, 10, yaxis="left")
        item = self.plot._getMarker(legend)
        self.assertEqual(item.getYAxis(), "left")

        legend = self.plot.addXMarker(10, yaxis="right")
        item = self.plot._getMarker(legend)
        self.assertEqual(item.getYAxis(), "right")

        legend = self.plot.addXMarker(10, yaxis="left")
        item = self.plot._getMarker(legend)
        self.assertEqual(item.getYAxis(), "left")

        legend = self.plot.addYMarker(10, yaxis="right")
        item = self.plot._getMarker(legend)
        self.assertEqual(item.getYAxis(), "right")

        legend = self.plot.addYMarker(10, yaxis="left")
        item = self.plot._getMarker(legend)
        self.assertEqual(item.getYAxis(), "left")

        self.plot.resetZoom()


# TestPlotItem ################################################################

class TestPlotItem(PlotWidgetTestCase):
    """Basic tests for addItem."""

    # Polygon coordinates and color
    POLYGONS = [  # legend, x coords, y coords, color
        ('triangle', numpy.array((10, 30, 50)),
         numpy.array((55, 70, 55)), 'red'),
        ('square', numpy.array((10, 10, 50, 50)),
         numpy.array((10, 50, 50, 10)), 'green'),
        ('star', numpy.array((60, 70, 80, 60, 80)),
         numpy.array((25, 50, 25, 40, 40)), 'blue'),
        ('2 triangles-simple',
         numpy.array((90., 95., 100., numpy.nan, 90., 95., 100.)),
         numpy.array((25., 5., 25., numpy.nan, 30., 50., 30.)),
         'pink'),
        ('2 triangles-extra NaN',
         numpy.array((numpy.nan, 90., 95., 100., numpy.nan, 0., 90., 95., 100., numpy.nan)),
         numpy.array((0., 55., 70., 55., numpy.nan, numpy.nan, 75., 90., 75., numpy.nan)),
         'black'),
    ]

    # Rectangle coordinantes and color
    RECTANGLES = [  # legend, x coords, y coords, color
        ('square 1', numpy.array((1., 10.)),
         numpy.array((1., 10.)), 'red'),
        ('square 2', numpy.array((10., 20.)),
         numpy.array((10., 20.)), 'green'),
        ('square 3', numpy.array((20., 30.)),
         numpy.array((20., 30.)), 'blue'),
        ('rect 1', numpy.array((1., 30.)),
         numpy.array((35., 40.)), 'black'),
        ('line h', numpy.array((1., 30.)),
         numpy.array((45., 45.)), 'darkRed'),
    ]

    SCALES = Axis.LINEAR, Axis.LOGARITHMIC

    def setUp(self):
        super(TestPlotItem, self).setUp()

        self.plot.getYAxis().setLabel('Rows')
        self.plot.getXAxis().setLabel('Columns')
        self.plot.getXAxis().setAutoScale(False)
        self.plot.getYAxis().setAutoScale(False)
        self.plot.setKeepDataAspectRatio(False)
        self.plot.setLimits(0., 100., -100., 100.)

    def testPlotItemPolygonFill(self):
        for scale in self.SCALES:
            with self.subTest(scale=scale):
                self.plot.clear()
                self.plot.getXAxis().setScale(scale)
                self.plot.getYAxis().setScale(scale)
                self.plot.setGraphTitle('Item Fill %s' % scale)

                for legend, xList, yList, color in self.POLYGONS:
                    self.plot.addShape(xList, yList, legend=legend,
                                       replace=False, linestyle='--',
                                       shape="polygon", fill=True, color=color)
                self.plot.resetZoom()

    def testPlotItemPolygonNoFill(self):
        for scale in self.SCALES:
            with self.subTest(scale=scale):
                self.plot.clear()
                self.plot.getXAxis().setScale(scale)
                self.plot.getYAxis().setScale(scale)
                self.plot.setGraphTitle('Item No Fill %s' % scale)

                for legend, xList, yList, color in self.POLYGONS:
                    self.plot.addShape(xList, yList, legend=legend,
                                       replace=False, linestyle='--',
                                       shape="polygon", fill=False, color=color)
                self.plot.resetZoom()

    def testPlotItemRectangleFill(self):
        for scale in self.SCALES:
            with self.subTest(scale=scale):
                self.plot.clear()
                self.plot.getXAxis().setScale(scale)
                self.plot.getYAxis().setScale(scale)
                self.plot.setGraphTitle('Rectangle Fill %s' % scale)

                for legend, xList, yList, color in self.RECTANGLES:
                    self.plot.addShape(xList, yList, legend=legend,
                                       replace=False,
                                       shape="rectangle", fill=True, color=color)
                self.plot.resetZoom()

    def testPlotItemRectangleNoFill(self):
        for scale in self.SCALES:
            with self.subTest(scale=scale):
                self.plot.clear()
                self.plot.getXAxis().setScale(scale)
                self.plot.getYAxis().setScale(scale)
                self.plot.setGraphTitle('Rectangle No Fill %s' % scale)

                for legend, xList, yList, color in self.RECTANGLES:
                    self.plot.addShape(xList, yList, legend=legend,
                                       replace=False,
                                       shape="rectangle", fill=False, color=color)
                self.plot.resetZoom()


class TestPlotActiveCurveImage(PlotWidgetTestCase):
    """Basic tests for active curve and image handling"""
    xData = numpy.arange(1000)
    yData = -500 + 100 * numpy.sin(xData)
    xData2 = xData + 1000
    yData2 = xData - 1000 + 200 * numpy.random.random(1000)

    def tearDown(self):
        self.plot.setActiveCurveHandling(False)
        super(TestPlotActiveCurveImage, self).tearDown()

    def testActiveCurveAndLabels(self):
        # Active curve handling off, no label change
        self.plot.setActiveCurveHandling(False)
        self.plot.getXAxis().setLabel('XLabel')
        self.plot.getYAxis().setLabel('YLabel')
        self.plot.addCurve((1, 2), (1, 2))
        self.assertEqual(self.plot.getXAxis().getLabel(), 'XLabel')
        self.assertEqual(self.plot.getYAxis().getLabel(), 'YLabel')

        self.plot.addCurve((1, 2), (2, 3), xlabel='x1', ylabel='y1')
        self.assertEqual(self.plot.getXAxis().getLabel(), 'XLabel')
        self.assertEqual(self.plot.getYAxis().getLabel(), 'YLabel')

        self.plot.clear()
        self.assertEqual(self.plot.getXAxis().getLabel(), 'XLabel')
        self.assertEqual(self.plot.getYAxis().getLabel(), 'YLabel')

        # Active curve handling on, label changes
        self.plot.setActiveCurveHandling(True)
        self.plot.getXAxis().setLabel('XLabel')
        self.plot.getYAxis().setLabel('YLabel')

        # labels changed as active curve
        self.plot.addCurve((1, 2), (1, 2), legend='1',
                           xlabel='x1', ylabel='y1')
        self.plot.setActiveCurve('1')
        self.assertEqual(self.plot.getXAxis().getLabel(), 'x1')
        self.assertEqual(self.plot.getYAxis().getLabel(), 'y1')

        # labels not changed as not active curve
        self.plot.addCurve((1, 2), (2, 3), legend='2')
        self.assertEqual(self.plot.getXAxis().getLabel(), 'x1')
        self.assertEqual(self.plot.getYAxis().getLabel(), 'y1')

        # labels changed
        self.plot.setActiveCurve('2')
        self.assertEqual(self.plot.getXAxis().getLabel(), 'XLabel')
        self.assertEqual(self.plot.getYAxis().getLabel(), 'YLabel')

        self.plot.setActiveCurve('1')
        self.assertEqual(self.plot.getXAxis().getLabel(), 'x1')
        self.assertEqual(self.plot.getYAxis().getLabel(), 'y1')

        self.plot.clear()
        self.assertEqual(self.plot.getXAxis().getLabel(), 'XLabel')
        self.assertEqual(self.plot.getYAxis().getLabel(), 'YLabel')

    def testPlotActiveCurveSelectionMode(self):
        self.plot.clear()
        self.plot.setActiveCurveHandling(True)
        legend = "curve 1"
        self.plot.addCurve(self.xData, self.yData,
                           legend=legend,
                           color="green")

        # active curve should be None
        self.assertEqual(self.plot.getActiveCurve(just_legend=True), None)

        # active curve should be None when None is set as active curve
        self.plot.setActiveCurve(legend)
        current = self.plot.getActiveCurve(just_legend=True)
        self.assertEqual(current, legend)
        self.plot.setActiveCurve(None)
        current = self.plot.getActiveCurve(just_legend=True)
        self.assertEqual(current, None)

        # testing it automatically toggles if there is only one
        self.plot.setActiveCurveSelectionMode("legacy")
        current = self.plot.getActiveCurve(just_legend=True)
        self.assertEqual(current, legend)
        
        # active curve should not change when None set as active curve
        self.assertEqual(self.plot.getActiveCurveSelectionMode(), "legacy")
        self.plot.setActiveCurve(None)
        current = self.plot.getActiveCurve(just_legend=True)
        self.assertEqual(current, legend)

        # situation where no curve is active
        self.plot.clear()
        self.plot.setActiveCurveHandling(True)
        self.assertEqual(self.plot.getActiveCurveSelectionMode(), "atmostone")
        self.plot.addCurve(self.xData, self.yData,
                           legend=legend,
                           color="green")
        self.assertEqual(self.plot.getActiveCurve(just_legend=True), None)
        self.plot.addCurve(self.xData2, self.yData2,
                           legend="curve 2",
                           color="red")
        self.assertEqual(self.plot.getActiveCurve(just_legend=True), None)
        self.plot.setActiveCurveSelectionMode("legacy")
        self.assertEqual(self.plot.getActiveCurve(just_legend=True), None)

        # the first curve added should be active
        self.plot.clear()
        self.plot.addCurve(self.xData, self.yData,
                           legend=legend,
                           color="green")
        self.assertEqual(self.plot.getActiveCurve(just_legend=True), legend)
        self.plot.addCurve(self.xData2, self.yData2,
                           legend="curve 2",
                           color="red")
        self.assertEqual(self.plot.getActiveCurve(just_legend=True), legend)

    def testActiveCurveStyle(self):
        """Test change of active curve style"""
        self.plot.setActiveCurveHandling(True)
        self.plot.setActiveCurveStyle(color='black')
        style = self.plot.getActiveCurveStyle()
        self.assertEqual(style.getColor(), (0., 0., 0., 1.))
        self.assertIsNone(style.getLineStyle())
        self.assertIsNone(style.getLineWidth())
        self.assertIsNone(style.getSymbol())
        self.assertIsNone(style.getSymbolSize())

        self.plot.addCurve(x=self.xData, y=self.yData, legend="curve1")
        curve = self.plot.getCurve("curve1")
        curve.setColor('blue')
        curve.setLineStyle('-')
        curve.setLineWidth(1)
        curve.setSymbol('o')
        curve.setSymbolSize(5)

        # Check default current style
        defaultStyle = curve.getCurrentStyle()
        self.assertEqual(defaultStyle, CurveStyle(color='blue',
                                                  linestyle='-',
                                                  linewidth=1,
                                                  symbol='o',
                                                  symbolsize=5))

        # Activate curve with highlight color=black
        self.plot.setActiveCurve("curve1")
        style = curve.getCurrentStyle()
        self.assertEqual(style.getColor(), (0., 0., 0., 1.))
        self.assertEqual(style.getLineStyle(), '-')
        self.assertEqual(style.getLineWidth(), 1)
        self.assertEqual(style.getSymbol(), 'o')
        self.assertEqual(style.getSymbolSize(), 5)

        # Change highlight to linewidth=2
        self.plot.setActiveCurveStyle(linewidth=2)
        style = curve.getCurrentStyle()
        self.assertEqual(style.getColor(), (0., 0., 1., 1.))
        self.assertEqual(style.getLineStyle(), '-')
        self.assertEqual(style.getLineWidth(), 2)
        self.assertEqual(style.getSymbol(), 'o')
        self.assertEqual(style.getSymbolSize(), 5)

        self.plot.setActiveCurve(None)
        self.assertEqual(curve.getCurrentStyle(), defaultStyle)

    def testActiveImageAndLabels(self):
        # Active image handling always on, no API for toggling it
        self.plot.getXAxis().setLabel('XLabel')
        self.plot.getYAxis().setLabel('YLabel')

        # labels changed as active curve
        self.plot.addImage(numpy.arange(100).reshape(10, 10),
                           legend='1', xlabel='x1', ylabel='y1')
        self.assertEqual(self.plot.getXAxis().getLabel(), 'x1')
        self.assertEqual(self.plot.getYAxis().getLabel(), 'y1')

        # labels not changed as not active curve
        self.plot.addImage(numpy.arange(100).reshape(10, 10),
                           legend='2')
        self.assertEqual(self.plot.getXAxis().getLabel(), 'x1')
        self.assertEqual(self.plot.getYAxis().getLabel(), 'y1')

        # labels changed
        self.plot.setActiveImage('2')
        self.assertEqual(self.plot.getXAxis().getLabel(), 'XLabel')
        self.assertEqual(self.plot.getYAxis().getLabel(), 'YLabel')

        self.plot.setActiveImage('1')
        self.assertEqual(self.plot.getXAxis().getLabel(), 'x1')
        self.assertEqual(self.plot.getYAxis().getLabel(), 'y1')

        self.plot.clear()
        self.assertEqual(self.plot.getXAxis().getLabel(), 'XLabel')
        self.assertEqual(self.plot.getYAxis().getLabel(), 'YLabel')


##############################################################################
# Log
##############################################################################

class TestPlotEmptyLog(PlotWidgetTestCase):
    """Basic tests for log plot"""
    def testEmptyPlotTitleLabelsLog(self):
        self.plot.setGraphTitle('Empty Log Log')
        self.plot.getXAxis().setLabel('X')
        self.plot.getYAxis().setLabel('Y')
        self.plot.getXAxis()._setLogarithmic(True)
        self.plot.getYAxis()._setLogarithmic(True)
        self.plot.resetZoom()


class TestPlotAxes(TestCaseQt, ParametricTestCase):

    # Test data
    xData = numpy.arange(1, 10)
    yData = xData ** 2

    def __init__(self, methodName='runTest', backend=None):
        unittest.TestCase.__init__(self, methodName)
        self.__backend = backend

    def setUp(self):
        super(TestPlotAxes, self).setUp()
        self.plot = PlotWidget(backend=self.__backend)
        # It is not needed to display the plot
        # It saves a lot of time
        # self.plot.show()
        # self.qWaitForWindowExposed(self.plot)

    def tearDown(self):
        self.qapp.processEvents()
        self.plot.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.plot.close()
        del self.plot
        super(TestPlotAxes, self).tearDown()

    def testDefaultAxes(self):
        axis = self.plot.getXAxis()
        self.assertEqual(axis.getScale(), axis.LINEAR)
        axis = self.plot.getYAxis()
        self.assertEqual(axis.getScale(), axis.LINEAR)
        axis = self.plot.getYAxis(axis="right")
        self.assertEqual(axis.getScale(), axis.LINEAR)

    def testOldPlotAxis_getterSetter(self):
        """Test silx API prior to silx 0.6"""
        x = self.plot.getXAxis()
        y = self.plot.getYAxis()
        p = self.plot

        tests = [
            # setters
            (p.setGraphXLimits, (10, 20), x.getLimits, (10, 20)),
            (p.setGraphYLimits, (10, 20), y.getLimits, (10, 20)),
            (p.setGraphXLabel, "foox", x.getLabel, "foox"),
            (p.setGraphYLabel, "fooy", y.getLabel, "fooy"),
            (p.setYAxisInverted, True, y.isInverted, True),
            (p.setXAxisLogarithmic, True, x.getScale, x.LOGARITHMIC),
            (p.setYAxisLogarithmic, True, y.getScale, y.LOGARITHMIC),
            (p.setXAxisAutoScale, False, x.isAutoScale, False),
            (p.setYAxisAutoScale, False, y.isAutoScale, False),
            # getters
            (x.setLimits, (11, 20), p.getGraphXLimits, (11, 20)),
            (y.setLimits, (11, 20), p.getGraphYLimits, (11, 20)),
            (x.setLabel, "fooxx", p.getGraphXLabel, "fooxx"),
            (y.setLabel, "fooyy", p.getGraphYLabel, "fooyy"),
            (y.setInverted, False, p.isYAxisInverted, False),
            (x.setScale, x.LINEAR, p.isXAxisLogarithmic, False),
            (y.setScale, y.LINEAR, p.isYAxisLogarithmic, False),
            (x.setAutoScale, True, p.isXAxisAutoScale, True),
            (y.setAutoScale, True, p.isYAxisAutoScale, True),
        ]
        for testCase in tests:
            setter, value, getter, expected = testCase
            with self.subTest():
                if setter is not None:
                    if not isinstance(value, tuple):
                        value = (value, )
                    setter(*value)
                if getter is not None:
                    self.assertEqual(getter(), expected)

    def testOldPlotAxis_Logarithmic(self):
        """Test silx API prior to silx 0.6"""
        x = self.plot.getXAxis()
        y = self.plot.getYAxis()
        yright = self.plot.getYAxis(axis="right")

        self.assertEqual(x.getScale(), x.LINEAR)
        self.assertEqual(y.getScale(), x.LINEAR)
        self.assertEqual(yright.getScale(), x.LINEAR)

        self.plot.setXAxisLogarithmic(True)
        self.assertEqual(x.getScale(), x.LOGARITHMIC)
        self.assertEqual(y.getScale(), x.LINEAR)
        self.assertEqual(yright.getScale(), x.LINEAR)
        self.assertEqual(self.plot.isXAxisLogarithmic(), True)
        self.assertEqual(self.plot.isYAxisLogarithmic(), False)

        self.plot.setYAxisLogarithmic(True)
        self.assertEqual(x.getScale(), x.LOGARITHMIC)
        self.assertEqual(y.getScale(), x.LOGARITHMIC)
        self.assertEqual(yright.getScale(), x.LOGARITHMIC)
        self.assertEqual(self.plot.isXAxisLogarithmic(), True)
        self.assertEqual(self.plot.isYAxisLogarithmic(), True)

        yright.setScale(yright.LINEAR)
        self.assertEqual(x.getScale(), x.LOGARITHMIC)
        self.assertEqual(y.getScale(), x.LINEAR)
        self.assertEqual(yright.getScale(), x.LINEAR)
        self.assertEqual(self.plot.isXAxisLogarithmic(), True)
        self.assertEqual(self.plot.isYAxisLogarithmic(), False)

    def testOldPlotAxis_AutoScale(self):
        """Test silx API prior to silx 0.6"""
        x = self.plot.getXAxis()
        y = self.plot.getYAxis()
        yright = self.plot.getYAxis(axis="right")

        self.assertEqual(x.isAutoScale(), True)
        self.assertEqual(y.isAutoScale(), True)
        self.assertEqual(yright.isAutoScale(), True)

        self.plot.setXAxisAutoScale(False)
        self.assertEqual(x.isAutoScale(), False)
        self.assertEqual(y.isAutoScale(), True)
        self.assertEqual(yright.isAutoScale(), True)
        self.assertEqual(self.plot.isXAxisAutoScale(), False)
        self.assertEqual(self.plot.isYAxisAutoScale(), True)

        self.plot.setYAxisAutoScale(False)
        self.assertEqual(x.isAutoScale(), False)
        self.assertEqual(y.isAutoScale(), False)
        self.assertEqual(yright.isAutoScale(), False)
        self.assertEqual(self.plot.isXAxisAutoScale(), False)
        self.assertEqual(self.plot.isYAxisAutoScale(), False)

        yright.setAutoScale(True)
        self.assertEqual(x.isAutoScale(), False)
        self.assertEqual(y.isAutoScale(), True)
        self.assertEqual(yright.isAutoScale(), True)
        self.assertEqual(self.plot.isXAxisAutoScale(), False)
        self.assertEqual(self.plot.isYAxisAutoScale(), True)

    def testOldPlotAxis_Inverted(self):
        """Test silx API prior to silx 0.6"""
        x = self.plot.getXAxis()
        y = self.plot.getYAxis()
        yright = self.plot.getYAxis(axis="right")

        self.assertEqual(x.isInverted(), False)
        self.assertEqual(y.isInverted(), False)
        self.assertEqual(yright.isInverted(), False)

        self.plot.setYAxisInverted(True)
        self.assertEqual(x.isInverted(), False)
        self.assertEqual(y.isInverted(), True)
        self.assertEqual(yright.isInverted(), True)
        self.assertEqual(self.plot.isYAxisInverted(), True)

        yright.setInverted(False)
        self.assertEqual(x.isInverted(), False)
        self.assertEqual(y.isInverted(), False)
        self.assertEqual(yright.isInverted(), False)
        self.assertEqual(self.plot.isYAxisInverted(), False)

    def testLogXWithData(self):
        self.plot.setGraphTitle('Curve X: Log Y: Linear')
        self.plot.addCurve(self.xData, self.yData,
                           legend="curve",
                           replace=False, resetzoom=True,
                           color='green', linestyle="-", symbol='o')
        axis = self.plot.getXAxis()
        axis.setScale(axis.LOGARITHMIC)

        self.assertEqual(axis.getScale(), axis.LOGARITHMIC)

    def testLogYWithData(self):
        self.plot.setGraphTitle('Curve X: Linear Y: Log')
        self.plot.addCurve(self.xData, self.yData,
                           legend="curve",
                           replace=False, resetzoom=True,
                           color='green', linestyle="-", symbol='o')
        axis = self.plot.getYAxis()
        axis.setScale(axis.LOGARITHMIC)

        self.assertEqual(axis.getScale(), axis.LOGARITHMIC)
        axis = self.plot.getYAxis(axis="right")
        self.assertEqual(axis.getScale(), axis.LOGARITHMIC)

    def testLogYRightWithData(self):
        self.plot.setGraphTitle('Curve X: Linear Y: Log')
        self.plot.addCurve(self.xData, self.yData,
                           legend="curve",
                           replace=False, resetzoom=True,
                           color='green', linestyle="-", symbol='o')
        axis = self.plot.getYAxis(axis="right")
        axis.setScale(axis.LOGARITHMIC)

        self.assertEqual(axis.getScale(), axis.LOGARITHMIC)
        axis = self.plot.getYAxis()
        self.assertEqual(axis.getScale(), axis.LOGARITHMIC)

    def testLimitsChanged_setLimits(self):
        self.plot.addCurve(self.xData, self.yData,
                           legend="curve",
                           replace=False, resetzoom=False,
                           color='green', linestyle="-", symbol='o')
        listener = SignalListener()
        self.plot.getXAxis().sigLimitsChanged.connect(listener.partial(axis="x"))
        self.plot.getYAxis().sigLimitsChanged.connect(listener.partial(axis="y"))
        self.plot.getYAxis(axis="right").sigLimitsChanged.connect(listener.partial(axis="y2"))
        self.plot.setLimits(0, 1, 0, 1, 0, 1)
        # at least one event per axis
        self.assertEqual(len(set(listener.karguments(argumentName="axis"))), 3)

    def testLimitsChanged_resetZoom(self):
        self.plot.addCurve(self.xData, self.yData,
                           legend="curve",
                           replace=False, resetzoom=False,
                           color='green', linestyle="-", symbol='o')
        listener = SignalListener()
        self.plot.getXAxis().sigLimitsChanged.connect(listener.partial(axis="x"))
        self.plot.getYAxis().sigLimitsChanged.connect(listener.partial(axis="y"))
        self.plot.getYAxis(axis="right").sigLimitsChanged.connect(listener.partial(axis="y2"))
        self.plot.resetZoom()
        # at least one event per axis
        self.assertEqual(len(set(listener.karguments(argumentName="axis"))), 3)

    def testLimitsChanged_setXLimit(self):
        self.plot.addCurve(self.xData, self.yData,
                           legend="curve",
                           replace=False, resetzoom=False,
                           color='green', linestyle="-", symbol='o')
        listener = SignalListener()
        axis = self.plot.getXAxis()
        axis.sigLimitsChanged.connect(listener)
        axis.setLimits(20, 30)
        # at least one event per axis
        self.assertEqual(listener.arguments(callIndex=-1), (20.0, 30.0))
        self.assertEqual(axis.getLimits(), (20.0, 30.0))

    def testLimitsChanged_setYLimit(self):
        self.plot.addCurve(self.xData, self.yData,
                           legend="curve",
                           replace=False, resetzoom=False,
                           color='green', linestyle="-", symbol='o')
        listener = SignalListener()
        axis = self.plot.getYAxis()
        axis.sigLimitsChanged.connect(listener)
        axis.setLimits(20, 30)
        # at least one event per axis
        self.assertEqual(listener.arguments(callIndex=-1), (20.0, 30.0))
        self.assertEqual(axis.getLimits(), (20.0, 30.0))

    def testLimitsChanged_setYRightLimit(self):
        self.plot.addCurve(self.xData, self.yData,
                           legend="curve",
                           replace=False, resetzoom=False,
                           color='green', linestyle="-", symbol='o')
        listener = SignalListener()
        axis = self.plot.getYAxis(axis="right")
        axis.sigLimitsChanged.connect(listener)
        axis.setLimits(20, 30)
        # at least one event per axis
        self.assertEqual(listener.arguments(callIndex=-1), (20.0, 30.0))
        self.assertEqual(axis.getLimits(), (20.0, 30.0))

    def testScaleProxy(self):
        listener = SignalListener()
        y = self.plot.getYAxis()
        yright = self.plot.getYAxis(axis="right")
        y.sigScaleChanged.connect(listener.partial("left"))
        yright.sigScaleChanged.connect(listener.partial("right"))
        yright.setScale(yright.LOGARITHMIC)

        self.assertEqual(y.getScale(), y.LOGARITHMIC)
        events = listener.arguments()
        self.assertEqual(len(events), 2)
        self.assertIn(("left", y.LOGARITHMIC), events)
        self.assertIn(("right", y.LOGARITHMIC), events)

    def testAutoScaleProxy(self):
        listener = SignalListener()
        y = self.plot.getYAxis()
        yright = self.plot.getYAxis(axis="right")
        y.sigAutoScaleChanged.connect(listener.partial("left"))
        yright.sigAutoScaleChanged.connect(listener.partial("right"))
        yright.setAutoScale(False)

        self.assertEqual(y.isAutoScale(), False)
        events = listener.arguments()
        self.assertEqual(len(events), 2)
        self.assertIn(("left", False), events)
        self.assertIn(("right", False), events)

    def testInvertedProxy(self):
        listener = SignalListener()
        y = self.plot.getYAxis()
        yright = self.plot.getYAxis(axis="right")
        y.sigInvertedChanged.connect(listener.partial("left"))
        yright.sigInvertedChanged.connect(listener.partial("right"))
        yright.setInverted(True)

        self.assertEqual(y.isInverted(), True)
        events = listener.arguments()
        self.assertEqual(len(events), 2)
        self.assertIn(("left", True), events)
        self.assertIn(("right", True), events)

    def testAxesDisplayedFalse(self):
        """Test coverage on setAxesDisplayed(False)"""
        self.plot.setAxesDisplayed(False)

    def testAxesDisplayedTrue(self):
        """Test coverage on setAxesDisplayed(True)"""
        self.plot.setAxesDisplayed(True)

    def testAxesMargins(self):
        """Test PlotWidget's getAxesMargins and setAxesMargins"""
        self.plot.show()
        self.qWaitForWindowExposed(self.plot)

        margins = self.plot.getAxesMargins()
        self.assertEqual(margins, (.15, .1, .1, .15))

        for margins in ((0., 0., 0., 0.), (.15, .1, .1, .15)):
            with self.subTest(margins=margins):
                self.plot.setAxesMargins(*margins)
                self.qapp.processEvents()
                self.assertEqual(self.plot.getAxesMargins(), margins)

    def testBoundingRectItem(self):
        item = BoundingRect()
        item.setBounds((-1000, 1000, -2000, 2000))
        self.plot.addItem(item)
        self.plot.resetZoom()
        limits = numpy.array(self.plot.getXAxis().getLimits())
        numpy.testing.assert_almost_equal(limits, numpy.array([-1000, 1000]))
        limits = numpy.array(self.plot.getYAxis().getLimits())
        numpy.testing.assert_almost_equal(limits, numpy.array([-2000, 2000]))

    def testBoundingRectRightItem(self):
        item = BoundingRect()
        item.setYAxis("right")
        item.setBounds((-1000, 1000, -2000, 2000))
        self.plot.addItem(item)
        self.plot.resetZoom()
        limits = numpy.array(self.plot.getXAxis().getLimits())
        numpy.testing.assert_almost_equal(limits, numpy.array([-1000, 1000]))
        limits = numpy.array(self.plot.getYAxis("right").getLimits())
        numpy.testing.assert_almost_equal(limits, numpy.array([-2000, 2000]))

    def testBoundingRectArguments(self):
        item = BoundingRect()
        with self.assertRaises(Exception):
            item.setBounds((1000, -1000, -2000, 2000))
        with self.assertRaises(Exception):
            item.setBounds((-1000, 1000, 2000, -2000))

    def testBoundingRectWithLog(self):
        item = BoundingRect()
        self.plot.addItem(item)

        item.setBounds((-1000, 1000, -2000, 2000))
        self.plot.getXAxis()._setLogarithmic(True)
        self.plot.getYAxis()._setLogarithmic(False)
        self.assertEqual(item.getBounds(), (1000, 1000, -2000, 2000))

        item.setBounds((-1000, 1000, -2000, 2000))
        self.plot.getXAxis()._setLogarithmic(False)
        self.plot.getYAxis()._setLogarithmic(True)
        self.assertEqual(item.getBounds(), (-1000, 1000, 2000, 2000))

        item.setBounds((-1000, 0, -2000, 2000))
        self.plot.getXAxis()._setLogarithmic(True)
        self.plot.getYAxis()._setLogarithmic(False)
        self.assertIsNone(item.getBounds())

    def testAxisExtent(self):
        """Test XAxisExtent and yAxisExtent"""
        for cls, axis in ((XAxisExtent, self.plot.getXAxis()),
                          (YAxisExtent, self.plot.getYAxis())):
            for range_, logRange in (((2, 3), (2, 3)),
                                     ((-2, -1), (1, 100)),
                                     ((-1, 3), (3. * 0.9, 3. * 1.1))):
                extent = cls()
                extent.setRange(*range_)
                self.plot.addItem(extent)

                for isLog, plotRange in ((False, range_), (True, logRange)):
                    with self.subTest(
                            cls=cls.__name__, range=range_, isLog=isLog):
                        axis._setLogarithmic(isLog)
                        self.plot.resetZoom()
                        self.qapp.processEvents()
                        self.assertEqual(axis.getLimits(), plotRange)

                axis._setLogarithmic(False)
                self.plot.clear()

    def testAxisLimitOverflow(self):
        """Test setting limis beyond supported range"""
        xaxis, yaxis = self.plot.getXAxis(), self.plot.getYAxis()
        for scale in ("linear", "log"):
            xaxis.setScale(scale)
            yaxis.setScale(scale)
            for limits in ((1e300, 1e308),
                           (-1e308, 1e308),
                           (1e-300, 2e-300)):
                with self.subTest(scale=scale, limits=limits):
                    xaxis.setLimits(*limits)
                    self.qapp.processEvents()
                    self.assertNotEqual(xaxis.getLimits(), limits)
                    yaxis.setLimits(*limits)
                    self.qapp.processEvents()
                    self.assertNotEqual(yaxis.getLimits(), limits)


class TestPlotCurveLog(PlotWidgetTestCase, ParametricTestCase):
    """Basic tests for addCurve with log scale axes"""

    # Test data
    xData = numpy.arange(1000) + 1
    yData = xData ** 2

    def _setLabels(self):
        self.plot.getXAxis().setLabel('X')
        self.plot.getYAxis().setLabel('X * X')

    def testPlotCurveLogX(self):
        self._setLabels()
        self.plot.getXAxis()._setLogarithmic(True)
        self.plot.setGraphTitle('Curve X: Log Y: Linear')

        self.plot.addCurve(self.xData, self.yData,
                           legend="curve",
                           replace=False, resetzoom=True,
                           color='green', linestyle="-", symbol='o')

    def testPlotCurveLogY(self):
        self._setLabels()
        self.plot.getYAxis()._setLogarithmic(True)

        self.plot.setGraphTitle('Curve X: Linear Y: Log')

        self.plot.addCurve(self.xData, self.yData,
                           legend="curve",
                           replace=False, resetzoom=True,
                           color='green', linestyle="-", symbol='o')

    def testPlotCurveLogXY(self):
        self._setLabels()
        self.plot.getXAxis()._setLogarithmic(True)
        self.plot.getYAxis()._setLogarithmic(True)

        self.plot.setGraphTitle('Curve X: Log Y: Log')

        self.plot.addCurve(self.xData, self.yData,
                           legend="curve",
                           replace=False, resetzoom=True,
                           color='green', linestyle="-", symbol='o')

    def testPlotCurveErrorLogXY(self):
        self.plot.getXAxis()._setLogarithmic(True)
        self.plot.getYAxis()._setLogarithmic(True)

        # Every second error leads to negative number
        errors = numpy.ones_like(self.xData)
        errors[::2] = self.xData[::2] + 1

        tests = [  # name, xerror, yerror
            ('xerror=3', 3, None),
            ('xerror=N array', errors, None),
            ('xerror=Nx1 array', errors.reshape(len(errors), 1), None),
            ('xerror=2xN array', numpy.array((errors, errors)), None),
            ('yerror=6', None, 6),
            ('yerror=N array', None, errors ** 2),
            ('yerror=Nx1 array', None, (errors ** 2).reshape(len(errors), 1)),
            ('yerror=2xN array', None, numpy.array((errors, errors)) ** 2),
        ]

        for name, xError, yError in tests:
            with self.subTest(name):
                self.plot.setGraphTitle(name)
                self.plot.addCurve(self.xData, self.yData,
                                   legend=name,
                                   xerror=xError, yerror=yError,
                                   replace=False, resetzoom=True,
                                   color='green', linestyle="-", symbol='o')

                self.qapp.processEvents()

                self.plot.clear()
                self.plot.resetZoom()
                self.qapp.processEvents()

    def testPlotCurveToggleLog(self):
        """Add a curve with negative data and toggle log axis"""
        arange = numpy.arange(1000) + 1
        tests = [  # name, xData, yData
            ('x>0, some negative y', arange, arange - 500),
            ('x>0, y<0', arange, -arange),
            ('some negative x, y>0', arange - 500, arange),
            ('x<0, y>0', -arange, arange),
            ('some negative x and y', arange - 500, arange - 500),
            ('x<0, y<0', -arange, -arange),
        ]

        for name, xData, yData in tests:
            with self.subTest(name):
                self.plot.addCurve(xData, yData, resetzoom=True)
                self.qapp.processEvents()

                # no log axis
                xLim = self.plot.getXAxis().getLimits()
                self.assertEqual(xLim, (min(xData), max(xData)))
                yLim = self.plot.getYAxis().getLimits()
                self.assertEqual(yLim, (min(yData), max(yData)))

                # x axis log
                self.plot.getXAxis()._setLogarithmic(True)
                self.qapp.processEvents()

                xLim = self.plot.getXAxis().getLimits()
                yLim = self.plot.getYAxis().getLimits()
                positives = xData > 0
                if numpy.any(positives):
                    self.assertTrue(numpy.allclose(
                        xLim, (min(xData[positives]), max(xData[positives]))))
                    self.assertEqual(
                        yLim, (min(yData[positives]), max(yData[positives])))
                else:  # No positive x in the curve
                    self.assertEqual(xLim, (1., 100.))
                    self.assertEqual(yLim, (1., 100.))

                # x axis and y axis log
                self.plot.getYAxis()._setLogarithmic(True)
                self.qapp.processEvents()

                xLim = self.plot.getXAxis().getLimits()
                yLim = self.plot.getYAxis().getLimits()
                positives = numpy.logical_and(xData > 0, yData > 0)
                if numpy.any(positives):
                    self.assertTrue(numpy.allclose(
                        xLim, (min(xData[positives]), max(xData[positives]))))
                    self.assertTrue(numpy.allclose(
                        yLim, (min(yData[positives]), max(yData[positives]))))
                else:  # No positive x and y in the curve
                    self.assertEqual(xLim, (1., 100.))
                    self.assertEqual(yLim, (1., 100.))

                # y axis log
                self.plot.getXAxis()._setLogarithmic(False)
                self.qapp.processEvents()

                xLim = self.plot.getXAxis().getLimits()
                yLim = self.plot.getYAxis().getLimits()
                positives = yData > 0
                if numpy.any(positives):
                    self.assertEqual(
                        xLim, (min(xData[positives]), max(xData[positives])))
                    self.assertTrue(numpy.allclose(
                        yLim, (min(yData[positives]), max(yData[positives]))))
                else:  # No positive y in the curve
                    self.assertEqual(xLim, (1., 100.))
                    self.assertEqual(yLim, (1., 100.))

                # no log axis
                self.plot.getYAxis()._setLogarithmic(False)
                self.qapp.processEvents()

                xLim = self.plot.getXAxis().getLimits()
                self.assertEqual(xLim, (min(xData), max(xData)))
                yLim = self.plot.getYAxis().getLimits()
                self.assertEqual(yLim, (min(yData), max(yData)))

                self.plot.clear()
                self.plot.resetZoom()
                self.qapp.processEvents()


class TestPlotImageLog(PlotWidgetTestCase):
    """Basic tests for addImage with log scale axes."""

    def setUp(self):
        super(TestPlotImageLog, self).setUp()

        self.plot.getXAxis().setLabel('Columns')
        self.plot.getYAxis().setLabel('Rows')

    def testPlotColormapGrayLogX(self):
        self.plot.getXAxis()._setLogarithmic(True)
        self.plot.setGraphTitle('CMap X: Log Y: Linear')

        colormap = Colormap(name='gray',
                            normalization='linear',
                            vmin=None,
                            vmax=None)
        self.plot.addImage(DATA_2D, legend="image 1",
                           origin=(1., 1.), scale=(1., 1.),
                           resetzoom=False, colormap=colormap)
        self.plot.resetZoom()

    def testPlotColormapGrayLogY(self):
        self.plot.getYAxis()._setLogarithmic(True)
        self.plot.setGraphTitle('CMap X: Linear Y: Log')

        colormap = Colormap(name='gray',
                            normalization='linear',
                            vmin=None,
                            vmax=None)
        self.plot.addImage(DATA_2D, legend="image 1",
                           origin=(1., 1.), scale=(1., 1.),
                           resetzoom=False, colormap=colormap)
        self.plot.resetZoom()

    def testPlotColormapGrayLogXY(self):
        self.plot.getXAxis()._setLogarithmic(True)
        self.plot.getYAxis()._setLogarithmic(True)
        self.plot.setGraphTitle('CMap X: Log Y: Log')

        colormap = Colormap(name='gray',
                            normalization='linear',
                            vmin=None,
                            vmax=None)
        self.plot.addImage(DATA_2D, legend="image 1",
                           origin=(1., 1.), scale=(1., 1.),
                           resetzoom=False, colormap=colormap)
        self.plot.resetZoom()

    def testPlotRgbRgbaLogXY(self):
        self.plot.getXAxis()._setLogarithmic(True)
        self.plot.getYAxis()._setLogarithmic(True)
        self.plot.setGraphTitle('RGB + RGBA X: Log Y: Log')

        rgb = numpy.array(
            (((0, 0, 0), (128, 0, 0), (255, 0, 0)),
             ((0, 128, 0), (0, 128, 128), (0, 128, 256))),
            dtype=numpy.uint8)

        self.plot.addImage(rgb, legend="rgb",
                           origin=(1, 1), scale=(10, 10),
                           resetzoom=False)

        rgba = numpy.array(
            (((0, 0, 0, .5), (.5, 0, 0, 1), (1, 0, 0, .5)),
             ((0, .5, 0, 1), (0, .5, .5, 1), (0, 1, 1, .5))),
            dtype=numpy.float32)

        self.plot.addImage(rgba, legend="rgba",
                           origin=(5., 5.), scale=(10., 10.),
                           resetzoom=False)
        self.plot.resetZoom()


class TestPlotMarkerLog(PlotWidgetTestCase):
    """Basic tests for markers on log scales"""

    # Test marker parameters
    markers = [  # x, y, color, selectable, draggable
        (10., 10., 'blue', False, False),
        (20., 20., 'red', False, False),
        (40., 100., 'green', True, False),
        (40., 500., 'gray', True, True),
        (60., 800., 'black', False, True),
    ]

    def setUp(self):
        super(TestPlotMarkerLog, self).setUp()

        self.plot.getYAxis().setLabel('Rows')
        self.plot.getXAxis().setLabel('Columns')
        self.plot.getXAxis().setAutoScale(False)
        self.plot.getYAxis().setAutoScale(False)
        self.plot.setKeepDataAspectRatio(False)
        self.plot.setLimits(1., 100., 1., 1000.)
        self.plot.getXAxis()._setLogarithmic(True)
        self.plot.getYAxis()._setLogarithmic(True)

    def testPlotMarkerXLog(self):
        self.plot.setGraphTitle('Markers X, Log axes')

        for x, _, color, select, drag in self.markers:
            name = str(x)
            if select:
                name += " sel."
            if drag:
                name += " drag"
            self.plot.addXMarker(x, name, name, color, select, drag)
        self.plot.resetZoom()

    def testPlotMarkerYLog(self):
        self.plot.setGraphTitle('Markers Y, Log axes')

        for _, y, color, select, drag in self.markers:
            name = str(y)
            if select:
                name += " sel."
            if drag:
                name += " drag"
            self.plot.addYMarker(y, name, name, color, select, drag)
        self.plot.resetZoom()

    def testPlotMarkerPtLog(self):
        self.plot.setGraphTitle('Markers Pt, Log axes')

        for x, y, color, select, drag in self.markers:
            name = "{0},{1}".format(x, y)
            if select:
                name += " sel."
            if drag:
                name += " drag"
            self.plot.addMarker(x, y, name, name, color, select, drag)
        self.plot.resetZoom()


@pytest.mark.usefixtures("test_options_class_attr")
class TestPlotWidgetSwitchBackend(PlotWidgetTestCase):
    """Test [get|set]Backend to switch backend"""

    @pytest.mark.usefixtures("test_options")
    def testSwitchBackend(self):
        """Test switching a plot with a few items"""
        backends = {'none': 'BackendBase', 'mpl': 'BackendMatplotlibQt'}
        if self.test_options.WITH_GL_TEST:
            backends['gl'] = 'BackendOpenGL'

        self.plot.addImage(numpy.arange(100).reshape(10, 10))
        self.plot.addCurve((-3, -2, -1), (1, 2, 3))
        self.plot.resetZoom()
        xlimits = self.plot.getXAxis().getLimits()
        ylimits = self.plot.getYAxis().getLimits()
        items = self.plot.getItems()
        self.assertEqual(len(items), 2)

        for backend, className in backends.items():
            with self.subTest(backend=backend):
                self.plot.setBackend(backend)
                self.plot.replot()

                retrievedBackend = self.plot.getBackend()
                self.assertEqual(type(retrievedBackend).__name__, className)
                self.assertEqual(self.plot.getXAxis().getLimits(), xlimits)
                self.assertEqual(self.plot.getYAxis().getLimits(), ylimits)
                self.assertEqual(self.plot.getItems(), items)


class TestPlotWidgetSelection(PlotWidgetTestCase):
    """Test PlotWidget.selection and active items handling"""

    def _checkSelection(self, selection, current=None, selected=()):
        """Check current item and selected items."""
        self.assertIs(selection.getCurrentItem(), current)
        self.assertEqual(selection.getSelectedItems(), selected)

    def testSyncWithActiveItems(self):
        """Test update of PlotWidgetSelection according to active items"""
        listener = SignalListener()

        selection = self.plot.selection()
        selection.sigCurrentItemChanged.connect(listener)
        self._checkSelection(selection)

        # Active item is current
        self.plot.addImage(((0, 1), (2, 3)), legend='image')
        image = self.plot.getActiveImage()
        self.assertEqual(listener.callCount(), 1)
        self._checkSelection(selection, image, (image,))

        # No active = no current
        self.plot.setActiveImage(None)
        self.assertEqual(listener.callCount(), 2)
        self._checkSelection(selection)

        # Active item is current
        self.plot.setActiveImage('image')
        self.assertEqual(listener.callCount(), 3)
        self._checkSelection(selection, image, (image,))

        # Mosted recently "actived" item is current
        self.plot.addScatter((3, 2, 1), (0, 1, 2), (0, 1, 2), legend='scatter')
        scatter = self.plot.getActiveScatter()
        self.assertEqual(listener.callCount(), 4)
        self._checkSelection(selection, scatter, (scatter, image))

        # Previously mosted recently "actived" item is current
        self.plot.setActiveScatter(None)
        self.assertEqual(listener.callCount(), 5)
        self._checkSelection(selection, image, (image,))

        # Mosted recently "actived" item is current
        self.plot.setActiveScatter('scatter')
        self.assertEqual(listener.callCount(), 6)
        self._checkSelection(selection, scatter, (scatter, image))

        # No active = no current
        self.plot.setActiveImage(None)
        self.plot.setActiveScatter(None)
        self.assertEqual(listener.callCount(), 7)
        self._checkSelection(selection)

        # Mosted recently "actived" item is current
        self.plot.setActiveScatter('scatter')
        self.assertEqual(listener.callCount(), 8)
        self.plot.setActiveImage('image')
        self.assertEqual(listener.callCount(), 9)
        self._checkSelection(selection, image, (image, scatter))

        # Add a curve which is not active by default
        self.plot.addCurve((0, 1, 2), (0, 1, 2), legend='curve')
        curve = self.plot.getCurve('curve')
        self.assertEqual(listener.callCount(), 9)
        self._checkSelection(selection, image, (image, scatter))

        # Mosted recently "actived" item is current
        self.plot.setActiveCurve('curve')
        self.assertEqual(listener.callCount(), 10)
        self._checkSelection(selection, curve, (curve, image, scatter))

        # Add a curve which is not active by default
        self.plot.addCurve((0, 1, 2), (0, 1, 2), legend='curve2')
        curve2 = self.plot.getCurve('curve2')
        self.assertEqual(listener.callCount(), 10)
        self._checkSelection(selection, curve, (curve, image, scatter))

        # Mosted recently "actived" item is current, previous curve is removed
        self.plot.setActiveCurve('curve2')
        self.assertEqual(listener.callCount(), 11)
        self._checkSelection(selection, curve2, (curve2, image, scatter))

        # No items = no current
        self.plot.clear()
        self.assertEqual(listener.callCount(), 12)
        self._checkSelection(selection)

    def testPlotWidgetWithItems(self):
        """Test init of selection on a plot with items"""
        self.plot.addImage(((0, 1), (2, 3)), legend='image')
        self.plot.addScatter((3, 2, 1), (0, 1, 2), (0, 1, 2), legend='scatter')
        self.plot.addCurve((0, 1, 2), (0, 1, 2), legend='curve')
        self.plot.setActiveCurve('curve')

        selection = self.plot.selection()
        self.assertIsNotNone(selection.getCurrentItem())
        selected = selection.getSelectedItems()
        self.assertEqual(len(selected), 3)
        self.assertIn(self.plot.getActiveCurve(), selected)
        self.assertIn(self.plot.getActiveImage(), selected)
        self.assertIn(self.plot.getActiveScatter(), selected)

    def testSetCurrentItem(self):
        """Test setCurrentItem"""
        # Add items to the plot
        self.plot.addImage(((0, 1), (2, 3)), legend='image')
        image = self.plot.getActiveImage()
        self.plot.addScatter((3, 2, 1), (0, 1, 2), (0, 1, 2), legend='scatter')
        scatter = self.plot.getActiveScatter()
        self.plot.addCurve((0, 1, 2), (0, 1, 2), legend='curve')
        self.plot.setActiveCurve('curve')
        curve = self.plot.getActiveCurve()

        selection = self.plot.selection()
        self.assertIsNotNone(selection.getCurrentItem())
        self.assertEqual(len(selection.getSelectedItems()), 3)

        # Set current to None reset all active items
        selection.setCurrentItem(None)
        self._checkSelection(selection)
        self.assertIsNone(self.plot.getActiveCurve())
        self.assertIsNone(self.plot.getActiveImage())
        self.assertIsNone(self.plot.getActiveScatter())

        # Set current to an item makes it active
        selection.setCurrentItem(image)
        self._checkSelection(selection, image, (image,))
        self.assertIsNone(self.plot.getActiveCurve())
        self.assertIs(self.plot.getActiveImage(), image)
        self.assertIsNone(self.plot.getActiveScatter())

        # Set current to an item makes it active and keeps other active
        selection.setCurrentItem(curve)
        self._checkSelection(selection, curve, (curve, image))
        self.assertIs(self.plot.getActiveCurve(), curve)
        self.assertIs(self.plot.getActiveImage(), image)
        self.assertIsNone(self.plot.getActiveScatter())

        # Set current to an item makes it active and keeps other active
        selection.setCurrentItem(scatter)
        self._checkSelection(selection, scatter, (scatter, curve, image))
        self.assertIs(self.plot.getActiveCurve(), curve)
        self.assertIs(self.plot.getActiveImage(), image)
        self.assertIs(self.plot.getActiveScatter(), scatter)


@pytest.mark.usefixtures("use_opengl")
class TestPlotWidget_Gl(TestPlotWidget):
    backend="gl"

@pytest.mark.usefixtures("use_opengl")
class TestPlotImage_Gl(TestPlotImage):
    backend="gl"

@pytest.mark.usefixtures("use_opengl")
class TestPlotCurve_Gl(TestPlotCurve):
    backend="gl"

@pytest.mark.usefixtures("use_opengl")
class TestPlotHistogram_Gl(TestPlotHistogram):
    backend="gl"

@pytest.mark.usefixtures("use_opengl")
class TestPlotScatter_Gl(TestPlotScatter):
    backend="gl"

@pytest.mark.usefixtures("use_opengl")
class TestPlotMarker_Gl(TestPlotMarker):
    backend="gl"

@pytest.mark.usefixtures("use_opengl")
class TestPlotItem_Gl(TestPlotItem):
    backend="gl"

@pytest.mark.usefixtures("use_opengl")
class TestPlotAxes_Gl(TestPlotAxes):
    backend="gl"

@pytest.mark.usefixtures("use_opengl")
class TestPlotActiveCurveImage_Gl(TestPlotActiveCurveImage):
    backend="gl"

@pytest.mark.usefixtures("use_opengl")
class TestPlotEmptyLog_Gl(TestPlotEmptyLog):
    backend="gl"

@pytest.mark.usefixtures("use_opengl")
class TestPlotCurveLog_Gl(TestPlotCurveLog):
    backend="gl"

@pytest.mark.usefixtures("use_opengl")
class TestPlotImageLog_Gl(TestPlotImageLog):
    backend="gl"

@pytest.mark.usefixtures("use_opengl")
class TestPlotMarkerLog_Gl(TestPlotMarkerLog):
    backend="gl"

@pytest.mark.usefixtures("use_opengl")
class TestPlotWidgetSelection_Gl(TestPlotWidgetSelection):
    backend="gl"

class TestSpecial_ExplicitMplBackend(TestSpecialBackend):
    backend="mpl"
