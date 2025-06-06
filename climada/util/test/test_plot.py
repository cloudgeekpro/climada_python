"""
This file is part of CLIMADA.

Copyright (C) 2017 ETH Zurich, CLIMADA contributors listed in AUTHORS.

CLIMADA is free software: you can redistribute it and/or modify it under the
terms of the GNU General Public License as published by the Free
Software Foundation, version 3.

CLIMADA is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with CLIMADA. If not, see <https://www.gnu.org/licenses/>.

---

Test plot module.
"""

import unittest

import cartopy
import cartopy.crs as ccrs
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colormaps as cm
from shapely import Point

import climada.util.plot as u_plot


class TestFuncs(unittest.TestCase):

    def test_get_transform_4326_pass(self):
        """Check _get_transformation for 4326 epsg."""
        res, unit = u_plot.get_transformation("epsg:4326")
        self.assertIsInstance(res, cartopy.crs.PlateCarree)
        self.assertEqual(unit, "°")

    def test_get_transform_3395_pass(self):
        """Check that assigned attribute is correctly set."""
        res, unit = u_plot.get_transformation("epsg:3395")
        self.assertIsInstance(res, cartopy.crs.Mercator)
        self.assertEqual(unit, "m")

    def test_get_transform_3035_pass(self):
        """Check that assigned attribute is correctly set."""
        res, unit = u_plot.get_transformation("epsg:3035")
        self.assertIsInstance(res, cartopy.crs.Projection)
        self.assertEqual(res.epsg_code, 3035)
        self.assertEqual(unit, "m")


class TestPlots(unittest.TestCase):

    def test_geo_scatter_categorical(self):
        """Plots ones with geo_scatteR_categorical"""
        # test default with one plot
        values = np.array([1, 2.0, 1, "a"])
        coord = np.array([[26, 0], [26, 1], [28, 0], [29, 1]])
        u_plot.geo_scatter_categorical(
            values, coord, "value", "test plot", pop_name=True
        )
        plt.close()

        # test multiple plots with non default kwargs
        values = np.array([[1, 2.0, 1, "a"], [0, 0, 0, 0]])
        coord = np.array([[26, 0], [26, 1], [28, 0], [29, 1]])
        u_plot.geo_scatter_categorical(
            values,
            coord,
            "value",
            "test plot",
            cat_name={0: "zero", 1: "int", 2.0: "float", "a": "string"},
            pop_name=False,
            cmap=cm.get_cmap("Set1"),
        )
        plt.close()

        # test colormap warning
        values = np.array(
            [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]
        )
        coord = np.array([[26, 0], [26, 4], [28, 0], [29, 1]])
        u_plot.geo_scatter_categorical(
            values, coord, "value", "test plot", pop_name=False, cmap="viridis"
        )

        plt.close()

        # test colormap warning with 256 colors
        values = np.array(
            [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]
        )
        coord = np.array([[26, 0], [26, 1], [28, 0], [29, 1]])
        u_plot.geo_scatter_categorical(
            values, coord, "value", "test plot", pop_name=False, cmap="tab20c"
        )
        plt.close()

    def test_geo_scatter_from_array(self):
        values = np.array([1, 2.0, 1, 1])
        coord = np.array([[-17, 178], [-10, 180], [-27, 175], [-16, 186]])
        var_name = "test"
        title = "test"
        projection = ccrs.PlateCarree()
        cmap = "viridis"
        ax = u_plot.geo_scatter_from_array(
            values,
            coord,
            var_name,
            title,
            pop_name=True,
            extend="neither",
            shapes=True,
            axes=None,
            proj=projection,
            figsize=(9, 13),
            cmap=cmap,
        )
        self.assertEqual(var_name, ax.get_title())
        colorbar = next(x.colorbar for x in ax.collections if x.colorbar)
        self.assertAlmostEqual(np.max(values), colorbar.vmax)
        self.assertAlmostEqual(np.min(values), colorbar.vmin)
        self.assertEqual(cmap, ax.collections[0].cmap.name)
        plt.close()

    def test_geo_bin_from_array(self):
        values = np.array([1, 2.0, 5, 1])
        coord = np.array([[-10, 17], [-30, 20], [5, 75], [-16, 20]])
        var_name = "test"
        title = "test"
        projection = ccrs.PlateCarree()
        cmap = "viridis"
        ax = u_plot.geo_bin_from_array(
            values,
            coord,
            var_name,
            title,
            pop_name=True,
            extend="neither",
            shapes=True,
            axes=None,
            proj=projection,
            figsize=(9, 13),
            cmap=cmap,
        )
        self.assertEqual(var_name, ax.get_title())
        colorbar = next(x.colorbar for x in ax.collections if x.colorbar)
        self.assertAlmostEqual(np.max(values), colorbar.vmax)
        self.assertAlmostEqual(np.min(values), colorbar.vmin)
        self.assertEqual(cmap, ax.collections[0].cmap.name)
        plt.close()

    def test_geo_im_from_array(self):
        values = np.array([1, 2.0, 5, np.nan])
        coord = np.array([[-17, 178], [-10, 180], [-27, 175], [-16, 186]])
        var_name = "test"
        title = "test"
        projection = ccrs.PlateCarree()
        cmap = "viridis"
        ax = u_plot.geo_im_from_array(
            values,
            coord,
            var_name,
            title,
            proj=projection,
            smooth=True,
            axes=None,
            figsize=(9, 13),
            cmap=cmap,
        )
        self.assertEqual(var_name, ax.get_title())
        colorbar = next(x.colorbar for x in ax.collections if x.colorbar)
        self.assertAlmostEqual(np.nanmax(values), colorbar.vmax)
        self.assertAlmostEqual(np.nanmin(values), colorbar.vmin)
        self.assertEqual(cmap, ax.collections[0].cmap.name)
        plt.close()

        projection = ccrs.AzimuthalEquidistant()
        ax = u_plot.geo_im_from_array(
            values,
            coord,
            var_name,
            title,
            proj=projection,
            smooth=True,
            axes=None,
            figsize=(9, 13),
            cmap=cmap,
        )
        self.assertEqual(var_name, ax.get_title())
        colorbar = next(x.colorbar for x in ax.collections if x.colorbar)
        self.assertAlmostEqual(np.nanmax(values), colorbar.vmax)
        self.assertAlmostEqual(np.nanmin(values), colorbar.vmin)
        self.assertEqual(cmap, ax.collections[0].cmap.name)
        plt.close()

    def test_plot_from_gdf_no_log(self):
        """test plot_from_gdf() with linear color bar (because there is a 0 in data)"""
        return_periods = gpd.GeoDataFrame(
            data=((2.0, 5.0), (0.0, 6.0), (None, 2.0), (1.0, 1000.0)),
            columns=("10.0", "20.0"),
        )
        return_periods["geometry"] = (
            Point(45.0, 26.0),
            Point(46.0, 26.0),
            Point(45.0, 27.0),
            Point(46.0, 27.0),
        )
        colorbar_name = "Return Periods (Years)"
        title_subplots = lambda cols: [
            f"Threshold Intensity: {col} m/s" for col in cols
        ]
        (axis1, axis2) = u_plot.plot_from_gdf(
            return_periods, colorbar_name=colorbar_name, title_subplots=title_subplots
        )
        self.assertEqual("Threshold Intensity: 10.0 m/s", axis1.get_title())
        self.assertEqual("Threshold Intensity: 20.0 m/s", axis2.get_title())
        plt.close()

    def test_plot_from_gdf_log(self):
        """test plot_from_gdf() with log color bar)"""
        return_periods = gpd.GeoDataFrame(
            data=((2.0, 5.0), (3.0, 6.0), (None, 2.0), (1.0, 1000.0)),
            columns=("10.0", "20.0"),
        )
        return_periods["geometry"] = (
            Point(45.0, 26.0),
            Point(46.0, 26.0),
            Point(45.0, 27.0),
            Point(46.0, 27.0),
        )
        colorbar_name = "Return Periods (Years)"
        title_subplots = lambda cols: [
            f"Threshold Intensity: {col} m/s" for col in cols
        ]
        (axis1, axis2) = u_plot.plot_from_gdf(
            return_periods, colorbar_name=colorbar_name, title_subplots=title_subplots
        )
        self.assertEqual("Threshold Intensity: 10.0 m/s", axis1.get_title())
        self.assertEqual("Threshold Intensity: 20.0 m/s", axis2.get_title())
        plt.close()


# Execute Tests
if __name__ == "__main__":
    TESTS = unittest.TestLoader().loadTestsFromTestCase(TestFuncs)
    TESTS.addTests(unittest.TestLoader().loadTestsFromTestCase(TestPlots))
    unittest.TextTestRunner(verbosity=2).run(TESTS)
