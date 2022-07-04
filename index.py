import matplotlib.pyplot as plt;
import numpy as np;
import pandas as pd;
import streamlit as st;
from sklearn import linear_model;
from sklearn.preprocessing import PolynomialFeatures;
from PIL import Image;
from bokeh.plotting import figure;
import os;

def upload():
    data: any
    if file is not None:
        file_head = os.path.splitext(file.name);
        file_name = file_head[0];
        file_extens = file_head[1];
       
        data = getData(file_extens);
        
    else:
        st.text('Seleccione un archivo valido antes de querer realizar cualquier operacion');
    
    if data is not None:       
        st.write(data);
        col1, col2, col3 = st.columns(3);
        with col1:
            x = st.selectbox('Variable X:', data.columns);
        with col2:
            y = st.selectbox('Variable Y:', data.columns);
        with col3:
            btnPredict = st.button('Predecir');       
                
        if btnPredict:
            predictParamXY(data, x, y);

def predictParamXY(data, xParam, yParam):
    #Realize lineral prediction
    x = np.asarray(data[xParam]).reshape(-1,1);
    y = data[yParam];
    regr = linear_model.LinearRegression();
    regr.fit(x,y);
    yPred = regr.predict(x);    
   
    y1 = regr.predict([[0]]);
    y2 = regr.predict([[2]]);

    m = (y2 - y1)/(2-0);
    strEcuation = str(m).replace('[','').replace(']','') + 'x' + ' + (' + str(y1).replace('[','').replace(']','') +')';
    #Graph
    plot(x.flatten(), y, yPred, xParam, yParam, strEcuation);

def getData(file_extens):
    #Gete extension and read data
        if file_extens == '.csv':
            data = pd.read_csv(file);
        elif file_extens == '.json':
            data = pd.read_json(file);
        elif file_extens == '.xlsx' or file_extens == '.xls':
            data = pd.read_excel(file);
        else:
            st.text('Archivo de extension invalida');
            return None;
        return data;

def plot(x, y, y1, xTitle, yTitle, ecuation):
    # create a plot
    p = figure(
        title="Regresion lineal de: " + yTitle,
        sizing_mode="stretch_width",
        max_width=1200,
        max_height=800,
    );

    # activate toolbar autohide
    p.toolbar.autohide = True;
    p.toolbar.logo = None;

    # add a renderer
    p.circle(x, y, size=10);
    p.line(x, y1, legend_label = ecuation, line_color = "red");
    p.circle(x, y1, legend_label = ecuation, fill_color = "red", line_color = "red", size = 6);

    # change some things about the x-axis
    p.xaxis.axis_label = xTitle;
    p.xaxis.axis_line_width = 3;
    p.xaxis.axis_line_color = "cyan";

    # change some things about the y-axis
    p.yaxis.axis_label = yTitle;
    p.yaxis.major_label_text_color = "black";
    p.yaxis.major_label_orientation = "vertical";

    # change things on all axes
    p.axis.minor_tick_in = -3;
    p.axis.minor_tick_out = 6;
    st.bokeh_chart(p, use_container_width=True);

#Execution
st.title('Regresión Lineal');
file = st.file_uploader('Eliga un fichero: ', type=['csv','json','xlsx','xls']);

if file is not None:
    upload();