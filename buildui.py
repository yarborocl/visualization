from pyxley.charts.mg import Figure, Histogram, LineChart, ScatterPlot, barchart
from pyxley.filters import SelectButton
from pyxley import UILayout, register_layouts
import pandas as pd
import numpy as np

from os import path

from collections import OrderedDict
from flask import request, jsonify

def readCSVtoDF(filename):
    df = pd.read_csv(filename, header=0, sep='\t')
    dfPointsMotivNA = df.replace(np.nan, 'N/A', regex=True)
    return dfPointsMotivNA

def create_barchart(df, value):
    """ create a mg histogram

        Args:
            df (pandas.DataFrame): data to plot
    """
    fig = Figure("/mg/barplot/" + value, "mg_barplot_" + value)
    fig.graphics.transition_on_update(True)
    fig.layout.set_size(width=650, height=300)
    fig.layout.set_margin(left=40, right=40)
    fig.graphics.animate_on_load()

    # Make sentiment bar chart
    if value == 'sentiment':
        return barchart.BarChart(df, fig, "Sentiment", "Sentiment Count", title="A Healthier You - Sentiment Count", description="A Healthier You - Sentiment Count")
    elif value == 'emotion':
        return barchart.BarChart(df, fig, "Top Emotion", "TE Count", title="A Healthier You - Top Emotion Count", description="A Healthier You - Top Emotion Count")
    elif value == 'keywords':
        return barchart.BarChart(df, fig, "Keyword", "Count", title="A Healthier You - Keyword Count", description="A Healthier You - Keyword Count")
    else:
        return "ERROR"

def make_mg_layout(filename):
    here = path.abspath(path.dirname(__file__))
    # load a dataframe
    dfSentiment = readCSVtoDF(filename)

    dfKeywords = readCSVtoDF(here+"/files/keywordsAHY.txt")

    dfEmotion = readCSVtoDF(here+"/files/emotionAHY.txt")
    # Make a UI
    ui = UILayout("FilterChart")

    # Make a Figure, add some settings, make a line plot
    ui.add_chart(create_barchart(dfSentiment, "sentiment"))
    ui.add_chart(create_barchart(dfKeywords, "keywords"))
    ui.add_chart(create_barchart(dfEmotion, "emotion"))
    #ui.add_chart(create_histogram(_stack2))
    #ui.add_chart(create_scatterplot(df))

    return ui

def get_layouts(mod, filename):

    # metrics graphics
    mg_ui = make_mg_layout(filename)
    mg_ui.assign_routes(mod)
    mg_props = mg_ui.build_props()

    _layouts = OrderedDict()
    _layouts["mg"] = {"layout": [mg_props], "title": "Emotional Analysis - BCBS"}

    register_layouts(_layouts, mod)
