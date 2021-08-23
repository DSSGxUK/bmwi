import json
import pathlib
from typing import Optional
import sys

import geopandas as gpd
import pandas as pd
import streamlit as st
from bokeh.models import ColorBar, GeoJSONDataSource, LinearColorMapper
from bokeh.palettes import brewer  # pylint: disable=no-name-in-module
from bokeh.plotting import figure

from .utils import *

FILE_DIR = pathlib.Path.cwd()
SHAPEFILE = FILE_DIR / "georef-germany-kreis/georef-germany-kreis-millesime.shp"
JSONFILE = FILE_DIR / "georef-germany-kreis/georef-germany-kreis.geojson"
DATASET_FILE = FILE_DIR / "data/pred_output_full.csv"


INFO = """
    #### Ideas for improvement
    - Add tooltips to the map
    - Speed up the dashboard by not downloading each dataset from the source.
    - Add a seperate *tab* with a line or bar chart of the data
    - Add functionality to select between maps generated by Bokeh, HoloViews, HvPlot, Plotly and Vega
    in order to compare how they work.
    - Add a button to maximize the interactive part of the dashboard.
    - Change the year selection to a [player widget](https://panel.pyviz.org/reference/widgets/Player.html#gallery-player).
    - Add a button to download an interactive embedding of the plot.
    """


class MapDashboard:
    """A Dashboard showing the Owid World Data like 'Annual CO2 Emissions'

        Args:
            shape_data (Optional[gpd.geodataframe.GeoDataFrame], optional): The Map shape data.
            Defaults to None.
            merged_data_sets (Optional[pd.DataFrame], optional): A DataFrame listing the available
            datasets. Defaults to None.
    """

    def __init__(
        self,
        shape_data: Optional[gpd.geodataframe.GeoDataFrame] = None,
    ):

        if not shape_data:
            self.shape_data = self.get_shape_data()
        else:
            self.shape_data = shape_data

        self.year_range = (2007, 2021)
        self.year = 2021
        
        self.month_range = (1, 12)
        self.month = 1

    def map_plot(self):
        """The Bokeh Map"""
        return self._map_plot(self.year, self.month)

    def _map_plot(self, year:int, month:int):
        if year and month:
            merged = self.get_merged_data(self.shape_data, year=year, month=month)
            return self.get_map_plot(merged)
        return 'IM NOT WORKING'
        # return None

    @staticmethod
    @st.cache
    def get_shape_data() -> gpd.geodataframe.GeoDataFrame:
        """Loads the shape data of the map"""
        shape_data = gpd.read_file(SHAPEFILE)[["krs_name_s", "krs_code", "geometry"]]
        shape_data.columns = ["krs_name", "ags5", "geometry"]
        return shape_data

    @staticmethod
    @st.cache
    def get_df(data_path) -> pd.DataFrame:
        """The DataFrame of data from Owid"""
        return pd.read_csv(data_path)

    @classmethod
    def get_merged_data(  # pylint: disable=too-many-arguments
        cls,
        shape_data: gpd.geodataframe.GeoDataFrame,
        year: Optional[int] = None,
        month: Optional[int] = None,
        # key: Optional[str] = None,
    ) -> gpd.geodataframe.GeoDataFrame:
        """Data Set combined with the shape_data

        Args:
            shape_data (gpd.geodataframe.GeoDataFrame): The shape data for the map
            key (Optional[str], optional): The name of column containing the values.
            Defaults to None.

        Returns:
            gpd.geodataframe.GeoDataFrame: The Owid Data Sets merged with the shape data
        """
        df = cls.get_df(DATASET_FILE)
        if (year is not None) and (month is not None):
            if len(str(month))==1:
                month = '0'+str(month)
            date_col = df.filter(like=f'{year}-{month}').columns
            df = df[['ags5']+list(date_col)]
        
        df['ags5'] = df['ags5'].apply(fix_ags5)    
        merged = pd.merge(df, shape_data, on="ags5")
        return merged

    @staticmethod
    def to_geojson(
        data: gpd.geodataframe.GeoDataFrame) -> GeoJSONDataSource:
        """Convert the data to a GeoJSONDataSource

        Args:
            data (gpd.geodataframe.GeoDataFrame): The data

        Returns:
            GeoJSONDataSource: The resulting GeoJson Data
        """
        data.columns = [str(col) for col in data.columns]
        try:
            json_data = data.to_json()
            json_data = json.dumps(json.loads(json_data))
        except:
            with open(JSONFILE) as response:
                json_data = json.load(response)
            json_data = json.dumps(json_data)
        return GeoJSONDataSource(geojson=json_data)

    @classmethod
    def get_map_plot(
        cls,
        shape_data: gpd.geodataframe.GeoDataFrame,
        value_column: Optional[str] = None,
        title: str = "",
    ):
        """Plot GeoDataFrame as a map
        """
        geosource = cls.to_geojson(shape_data)
        if value_column is None:
            value_column = shape_data.columns[1]
        vals = shape_data[value_column]
        
        palette = brewer["OrRd"][8]
        palette = palette[::-1]
        color_mapper = LinearColorMapper(palette=palette, 
                                         low=vals.min(), high=vals.max())
        color_bar = ColorBar(
            color_mapper=color_mapper,
            label_standoff=8,
            height=20,
            location=(0, 0),
            orientation="horizontal",
        )

        plot = figure(title=title, plot_height=500, tools="", sizing_mode="stretch_width")
        plot.xgrid.grid_line_color = None
        plot.ygrid.grid_line_color = None
        plot.patches(
            "xs",
            "ys",
            source=geosource,
            fill_alpha=1,
            line_width=0.5,
            line_color="black",
            fill_color={"field": value_column, "transform": color_mapper},
        )
        plot.add_layout(color_bar, "below")
        plot.toolbar.logo = None
        return plot

    def view(self):
        """Map dashboard"""
        st.markdown(__doc__)
        
        self.year = st.slider(
            "Select Year",
            min_value=self.year_range[0],
            max_value=self.year_range[1],
            value=self.year)
        self.month = st.slider(
            "Select Month",
            min_value=self.month_range[0],
            max_value=self.month_range[1],
            value=self.month)
        
        st.bokeh_chart(self.map_plot())
        # st.markdown(INFO)


def app():
    MapDashboard().view()