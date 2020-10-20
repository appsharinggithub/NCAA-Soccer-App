#!/usr/bin/env python
# coding: utf-8

import os
from natsort import natsorted
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
from streamlit.hashing import _CodeHasher
import matplotlib.font_manager as fm
import numpy as np
import matplotlib.cm as cm
import matplotlib.colors as colors 
from matplotlib.colors import TwoSlopeNorm
import matplotlib.cbook as cbook
import matplotlib.image as image
import matplotlib.gridspec as gridspec
import matplotlib as mpl
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib.projections import get_projection_class
from scipy.spatial import ConvexHull
import vaex




try:
    # Before Streamlit 0.65
    from streamlit.ReportThread import get_report_ctx
    from streamlit.server.Server import Server
except ModuleNotFoundError:
    # After Streamlit 0.65
    from streamlit.report_thread import get_report_ctx
    from streamlit.server.server import Server


@st.cache
def load_defense_data(season, team):
    url = 'https://drive.google.com/file/d/1KD5nxMlZZImiArxLXg4N43uiUkJ4taQP/view?usp=sharing'
    path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
    df = pd.read_csv(path)
    df = df[(df.Team.isin(team)) & (df.Season.isin(season))]
    return df

@st.cache
def load_pass_data(season, team, opp):
    url = 'https://drive.google.com/file/d/17FNbkRCZCb_Ue77AbzgBv36SxvD4MTg_/view?usp=sharing'
    path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
    df = pd.read_csv(path)
    if opp == 'yes':
        df = df[((df['HomeTeam'].isin(team)) | (df['AwayTeam'].isin(team))) & (~df['Team'].isin(team)) & (df.Season.isin(season))]
    else:
        df = df[(df.Team.isin(team)) & (df.Season.isin(season))]
    return df

@st.cache
def load_carry_data(season, team):
    url = 'https://drive.google.com/file/d/1KD5nxMlZZImiArxLXg4N43uiUkJ4taQP/view?usp=sharing'
    path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
    df = pd.read_csv(path)
    df = df[(df.Team.isin(team)) & (df.Season.isin(season))]
    return df

@st.cache
def load_shot_data(season, team, opp):
    url = 'https://drive.google.com/file/d/1egyoOVcul4IazeNmRzko1ZTovmlEzKrD/view?usp=sharing'
    path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
    df = pd.read_csv(path)
    if opp == 'yes':
        df = df[((df['HomeTeam'].isin(team)) | (df['AwayTeam'].isin(team))) & (~df['Team'].isin(team)) & (df.Season.isin(season))]
    else:
        df = df[(df.Team.isin(team)) & (df.Season.isin(season))]
    return df

@st.cache
def load_sm_data():
    #return pd.read_csv('/Users/michael/Documents/Python/CSV/NCAA Season and Team.csv')
    url = 'https://drive.google.com/file/d/1ygw0v6eTNppkSAQ4ZSVm2nouJYEfbYPD/view?usp=sharing'
    path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
    return pd.read_csv(path)

#df = load_data()
#df1 = pd.read_csv('/Users/michael/Documents/Python/CSV/NCAA All Matches.csv')

fontPathBold = "./EBGaramond-Bold.ttf"
fontPathNBold = "./EBGaramond-Medium.ttf"
headers = fm.FontProperties(fname=fontPathBold, size=46)
footers = fm.FontProperties(fname=fontPathNBold, size=24)
Labels = fm.FontProperties(fname=fontPathNBold, size=20)
PitchNumbers = fm.FontProperties(fname=fontPathBold, size=54)
Head = fm.FontProperties(fname=fontPathBold, size=60)
Subtitle = fm.FontProperties(fname=fontPathBold, size=34)
TableSummary = fm.FontProperties(fname=fontPathNBold, size=40)
Annotate = fm.FontProperties(fname=fontPathBold, size=24)
SmallTitle = fm.FontProperties(fname=fontPathBold, size=30)

TeamHead = fm.FontProperties(fname=fontPathBold, size=60)
GoalandxG = fm.FontProperties(fname=fontPathBold, size=48)
Summary = fm.FontProperties(fname=fontPathNBold, size=36)
TableHead = fm.FontProperties(fname=fontPathBold, size=34)
TableNum = fm.FontProperties(fname=fontPathNBold, size=30)





zo=12
def draw_pitch(pitch, line, orientation,view):
    
    orientation = orientation
    view = view
    line = line
    pitch = pitch
    
    if orientation.lower().startswith("h"):
        
        if view.lower().startswith("h"):
            fig,ax = plt.subplots(figsize=(32,18), facecolor=pitch)
            plt.xlim(40,110)
            plt.ylim(-5,73)
        else:
            fig,ax = plt.subplots(figsize=(32,18), facecolor=pitch)
            plt.xlim(-5,110)
            plt.ylim(-5,73)
        ax.axis('off') # this hides the x and y ticks
    
        # side and goal lines #
        ly1 = [0,0,68,68,0]
        lx1 = [0,105,105,0,0]

        plt.plot(lx1,ly1,color=line,zorder=5)


        # boxes, 6 yard box and goals

            #outer boxes#
        ly2 = [15.3,15.3,52.7,52.7] 
        lx2 = [105,89.25,89.25,105]
        plt.plot(lx2,ly2,color=line,zorder=5)

        ly3 = [15.3,15.3,52.7,52.7]  
        lx3 = [0,15.75,15.75,0]
        plt.plot(lx3,ly3,color=line,zorder=5)

            #goals#
        ly4 = [30.6,30.6,37.4,37.4]
        lx4 = [105,105.2,105.2,105]
        plt.plot(lx4,ly4,color=line,zorder=5)

        ly5 = [30.6,30.6,37.4,37.4]
        lx5 = [0,-0.2,-0.2,0]
        plt.plot(lx5,ly5,color=line,zorder=5)


           #6 yard boxes#
        ly6 = [25.5,25.5,42.5,42.5]
        lx6 = [105,99.75,99.75,105]
        plt.plot(lx6,ly6,color=line,zorder=5)

        ly7 = [25.5,25.5,42.5,42.5]
        lx7 = [0,5.25,5.25,0]
        plt.plot(lx7,ly7,color=line,zorder=5)

        #Halfway line, penalty spots, and kickoff spot
        ly8 = [0,68] 
        lx8 = [52.5,52.5]
        plt.plot(lx8,ly8,color=line,zorder=5)


        plt.scatter(94.5,34,color=line,zorder=5, s=12)
        plt.scatter(10.5,34,color=line,zorder=5, s=12)
        plt.scatter(52.5,34,color=line,zorder=5, s=12)

        arc1 =  Arc((95.25,34),height=18.3,width=18.3,angle=0,theta1=130,theta2=230,color=line,zorder=2)
        arc2 = Arc((9.75,34),height=18.3,width=18.3,angle=0,theta1=310,theta2=50,color=line,zorder=2)
        circle1 = plt.Circle((52.5, 34), 9.15,ls='solid',lw=1.5,color=line, fill=False, zorder=2,alpha=1)

        ## Rectangles in boxes
        rec1 = plt.Rectangle((89.25,20), 16,30,ls='-',color=pitch, zorder=1,alpha=1)
        rec2 = plt.Rectangle((0, 20), 16.5,30,ls='-',color=pitch, zorder=1,alpha=1)

        ## Pitch rectangle
        rec3 = plt.Rectangle((-5, -5), 115,78,ls='-',color=pitch, zorder=1,alpha=1)
        
        ## Add Direction of Play Arrow
        DoP = plt.arrow(0, -2.5, 18-2, 1-1, head_width=1.2,
            head_length=1.2,
            color=line,
            alpha=1,
            length_includes_head=True, zorder=12, width=.3)

        ax.add_artist(rec3)
        ax.add_artist(arc1)
        ax.add_artist(arc2)
        ax.add_artist(rec1)
        ax.add_artist(rec2)
        ax.add_artist(circle1)
        ax.add_artist(DoP)
        
    else:
        if view.lower().startswith("h"):
            fig,ax = plt.subplots(figsize=(32,18), facecolor=pitch)
            plt.ylim(40,110)
            plt.xlim(-5,73)
        else:
            fig,ax = plt.subplots(figsize=(32,18), facecolor=pitch)
            plt.ylim(-5,110)
            plt.xlim(-5,73)
        ax.axis('off') # this hides the x and y ticks

        # side and goal lines #
        lx1 = [0,0,68,68,0]
        ly1 = [0,105,105,0,0]

        plt.plot(lx1,ly1,color=line,zorder=5)


        # boxes, 6 yard box and goals

            #outer boxes#
        lx2 = [15.3,15.3,52.7,52.7] 
        ly2 = [105,89.25,89.25,105]
        plt.plot(lx2,ly2,color=line,zorder=5)

        lx3 = [15.3,15.3,52.7,52.7] 
        ly3 = [0,15.75,15.75,0]
        plt.plot(lx3,ly3,color=line,zorder=5)

            #goals#
        lx4 = [30.6,30.6,37.4,37.4]
        ly4 = [105,105.2,105.2,105]
        plt.plot(lx4,ly4,color=line,zorder=5)

        lx5 = [30.6,30.6,37.4,37.4]
        ly5 = [0,-0.2,-0.2,0]
        plt.plot(lx5,ly5,color=line,zorder=5)


           #6 yard boxes#
        lx6 = [25.5,25.5,42.5,42.5]
        ly6 = [105,99.75,99.75,105]
        plt.plot(lx6,ly6,color=line,zorder=5)

        lx7 = [25.5,25.5,42.5,42.5]
        ly7 = [0,5.25,5.25,0]
        plt.plot(lx7,ly7,color=line,zorder=5)

        #Halfway line, penalty spots, and kickoff spot
        lx8 = [0,68] 
        ly8 = [52.5,52.5]
        plt.plot(lx8,ly8,color=line,zorder=5)


        plt.scatter(34,94.5,color=line,zorder=5,s=12)
        plt.scatter(34,10.5,color=line,zorder=5,s=12)
        plt.scatter(34,52.5,color=line,zorder=5,s=12)

        arc1 =  Arc((34,95.25),height=18.3,width=18.3,angle=0,theta1=220,theta2=-40,color=line, zorder=2)
        arc2 = Arc((34,9.75),height=18.3,width=18.3,angle=0,theta1=40,theta2=-220,color=line, zorder=2)
        circle1 = plt.Circle((34,52.5), 9.15,ls='solid',lw=1.5,color=line, fill=False, zorder=2,alpha=1)


        ## Rectangles in boxes
        rec1 = plt.Rectangle((20, 89.25), 30,16.5,ls='-',color=pitch, zorder=1,alpha=1)
        rec2 = plt.Rectangle((20, 0), 30,16.5,ls='-',color=pitch, zorder=1,alpha=1)

        ## Pitch rectangle
        rec3 = plt.Rectangle((-5, -5), 78, 115,ls='-',color=pitch, zorder=1,alpha=1)
        
        ## Add Direction of Play Arrow
        DoP = plt.arrow(70.5, 0, 2-2, 18-1, head_width=1.2,
            head_length=1.2,
            color=line,
            alpha=1,
            length_includes_head=True, zorder=12, width=.3)

        ax.add_artist(rec3)
        ax.add_artist(arc1)
        ax.add_artist(arc2)
        ax.add_artist(rec1)
        ax.add_artist(rec2)
        ax.add_artist(circle1)
        ax.add_artist(DoP)

def vertfull_pitch(pitch, line, ax): 
    # side and goal lines #
    ax = ax
    
    
    lx1 = [0,0,68,68,0]
    ly1 = [0,105,105,0,0]

    plt.plot(lx1,ly1,color=line,zorder=5)


    # boxes, 6 yard box and goals

        #outer boxes#
    lx2 = [15.3,15.3,52.7,52.7] 
    ly2 = [105,89.25,89.25,105]
    ax.plot(lx2,ly2,color=line,zorder=5)

    lx3 = [15.3,15.3,52.7,52.7] 
    ly3 = [0,15.75,15.75,0]
    ax.plot(lx3,ly3,color=line,zorder=5)

        #goals#
    lx4 = [30.6,30.6,37.4,37.4]
    ly4 = [105,105.2,105.2,105]
    ax.plot(lx4,ly4,color=line,zorder=5)

    lx5 = [30.6,30.6,37.4,37.4]
    ly5 = [0,-0.2,-0.2,0]
    ax.plot(lx5,ly5,color=line,zorder=5)


       #6 yard boxes#
    lx6 = [25.5,25.5,42.5,42.5]
    ly6 = [105,99.75,99.75,105]
    ax.plot(lx6,ly6,color=line,zorder=5)

    lx7 = [25.5,25.5,42.5,42.5]
    ly7 = [0,5.25,5.25,0]
    ax.plot(lx7,ly7,color=line,zorder=5)

    #Halfway line, penalty spots, and kickoff spot
    lx8 = [0,68] 
    ly8 = [52.5,52.5]
    ax.plot(lx8,ly8,color=line,zorder=5)


    ax.scatter(34,94.5,color=line,zorder=5,s=12)
    ax.scatter(34,10.5,color=line,zorder=5,s=12)
    ax.scatter(34,52.5,color=line,zorder=5,s=12)

    arc1 =  Arc((34,95.25),height=18.3,width=18.3,angle=0,theta1=220,theta2=-40,color=line, zorder=zo-8)
    arc2 = Arc((34,9.75),height=18.3,width=18.3,angle=0,theta1=40,theta2=-220,color=line, zorder=zo-8)
    circle1 = plt.Circle((34,52.5), 9.15,ls='solid',lw=1.5,color=line, fill=False, zorder=2,alpha=1)


    ## Rectangles in boxes
    rec1 = plt.Rectangle((20, 89.25), 30,16.5,ls='-',color=pitch, zorder=1,alpha=1)
    rec2 = plt.Rectangle((20, 0), 30,16.5,ls='-',color=pitch, zorder=1,alpha=1)

    ## Pitch rectangle
    rec3 = plt.Rectangle((-5, -5), 78, 115,ls='-',color=pitch, zorder=1,alpha=1)
    
    ## Add Direction of Play Arrow
    DoP = plt.arrow(70.5, 0, 2-2, 18-1, head_width=1.2,
        head_length=1.2,
        color=line,
        alpha=1,
        length_includes_head=True, zorder=12, width=.3)

    ax.add_artist(rec3)
    ax.add_artist(arc1)
    ax.add_artist(arc2)
    ax.add_artist(rec1)
    ax.add_artist(rec2)
    ax.add_artist(circle1)
    ax.add_artist(DoP)
    ax.axis('off')
    
def horizfull_pitch(pitch, line, ax): 
# side and goal lines #
    ax = ax
    
    ly1 = [0,0,68,68,0]
    lx1 = [0,105,105,0,0]
    
    ax.plot(lx1,ly1,color=line,zorder=5)
    
    
    # boxes, 6 yard box and goals
    
        #outer boxes#
    ly2 = [15.3,15.3,52.7,52.7] 
    lx2 = [105,89.25,89.25,105]
    ax.plot(lx2,ly2,color=line,zorder=5)
    
    ly3 = [15.3,15.3,52.7,52.7]  
    lx3 = [0,15.75,15.75,0]
    ax.plot(lx3,ly3,color=line,zorder=5)
    
        #goals#
    ly4 = [30.6,30.6,37.4,37.4]
    lx4 = [105,105.2,105.2,105]
    ax.plot(lx4,ly4,color=line,zorder=5)
    
    ly5 = [30.6,30.6,37.4,37.4]
    lx5 = [0,-0.2,-0.2,0]
    ax.plot(lx5,ly5,color=line,zorder=5)
    
    
       #6 yard boxes#
    ly6 = [25.5,25.5,42.5,42.5]
    lx6 = [105,99.75,99.75,105]
    ax.plot(lx6,ly6,color=line,zorder=5)
    
    ly7 = [25.5,25.5,42.5,42.5]
    lx7 = [0,5.25,5.25,0]
    ax.plot(lx7,ly7,color=line,zorder=5)
    
    #Halfway line, penalty spots, and kickoff spot
    ly8 = [0,68] 
    lx8 = [52.5,52.5]
    ax.plot(lx8,ly8,color=line,zorder=5)
    
    
    ax.scatter(94.5,34,color=line,zorder=5, s=12)
    ax.scatter(10.5,34,color=line,zorder=5, s=12)
    ax.scatter(52.5,34,color=line,zorder=5, s=12)
    
    arc1 =  Arc((95.25,34),height=18.3,width=18.3,angle=0,theta1=130,theta2=230,color=line,zorder=zo+1)
    arc2 = Arc((9.75,34),height=18.3,width=18.3,angle=0,theta1=310,theta2=50,color=line,zorder=zo+1)
    circle1 = plt.Circle((52.5, 34), 9.15,ls='solid',lw=1.5,color=line, fill=False, zorder=2,alpha=1)
    
    ## Rectangles in boxes
    rec1 = plt.Rectangle((89.25,20), 16,30,ls='-',color=pitch, zorder=1,alpha=1)
    rec2 = plt.Rectangle((0, 20), 16.5,30,ls='-',color=pitch, zorder=1,alpha=1)
    
    ## Pitch rectangle
    rec3 = plt.Rectangle((-5, -5), 115,78,ls='-',color=pitch, zorder=1,alpha=1)
    
    ## Add Direction of Play Arrow
    DoP = ax.arrow(0, -2.5, 18-2, 1-1, head_width=1.2,
        head_length=1.2,
        color=line,
        alpha=1,
        length_includes_head=True, zorder=12, width=.3)
    
    ax.add_artist(rec3)
    ax.add_artist(arc1)
    ax.add_artist(arc2)
    ax.add_artist(rec1)
    ax.add_artist(rec2)
    ax.add_artist(circle1)
    ax.add_artist(DoP)
    ax.axis('off')


def verthalf_pitch(pitch, line, ax): 
        # side and goal lines #
        ax = ax
        
        plt.ylim(40,106)
        plt.xlim(-5,73)
        
        lx1 = [0,0,68,68,0]
        ly1 = [0,105,105,0,0]
    
        plt.plot(lx1,ly1,color=line,zorder=5)
    
    
        # boxes, 6 yard box and goals
    
            #outer boxes#
        lx2 = [15.3,15.3,52.7,52.7] 
        ly2 = [105,89.25,89.25,105]
        ax.plot(lx2,ly2,color=line,zorder=5)
    
        lx3 = [15.3,15.3,52.7,52.7] 
        ly3 = [0,15.75,15.75,0]
        ax.plot(lx3,ly3,color=line,zorder=5)
    
            #goals#
        lx4 = [30.6,30.6,37.4,37.4]
        ly4 = [105,105.2,105.2,105]
        ax.plot(lx4,ly4,color=line,zorder=5)
    
        lx5 = [30.6,30.6,37.4,37.4]
        ly5 = [0,-0.2,-0.2,0]
        ax.plot(lx5,ly5,color=line,zorder=5)
    
    
           #6 yard boxes#
        lx6 = [25.5,25.5,42.5,42.5]
        ly6 = [105,99.75,99.75,105]
        ax.plot(lx6,ly6,color=line,zorder=5)
    
        lx7 = [25.5,25.5,42.5,42.5]
        ly7 = [0,5.25,5.25,0]
        ax.plot(lx7,ly7,color=line,zorder=5)
    
        #Halfway line, penalty spots, and kickoff spot
        lx8 = [0,68] 
        ly8 = [52.5,52.5]
        ax.plot(lx8,ly8,color=line,zorder=5)
    
    
        ax.scatter(34,94.5,color=line,zorder=5,s=12)
        ax.scatter(34,10.5,color=line,zorder=5,s=12)
        ax.scatter(34,52.5,color=line,zorder=5,s=12)
    
        arc1 =  Arc((34,95.25),height=18.3,width=18.3,angle=0,theta1=220,theta2=-40,color=line, zorder=zo-8)
        arc2 = Arc((34,9.75),height=18.3,width=18.3,angle=0,theta1=40,theta2=-220,color=line, zorder=zo-8)
        circle1 = plt.Circle((34,52.5), 9.15,ls='solid',lw=1.5,color=line, fill=False, zorder=2,alpha=1)
    
    
        ## Rectangles in boxes
        rec1 = plt.Rectangle((20, 89.25), 30,16.5,ls='-',color=pitch, zorder=1,alpha=1)
        rec2 = plt.Rectangle((20, 0), 30,16.5,ls='-',color=pitch, zorder=1,alpha=1)
    
        ## Pitch rectangle
        rec3 = plt.Rectangle((-5, -5), 78, 115,ls='-',color=pitch, zorder=1,alpha=1)
        
        ## Add Direction of Play Arrow
        DoP = plt.arrow(70.5, 0, 2-2, 18-1, head_width=1.2,
            head_length=1.2,
            color=line,
            alpha=1,
            length_includes_head=True, zorder=12, width=.3)
    
        ax.add_artist(rec3)
        ax.add_artist(arc1)
        ax.add_artist(arc2)
        ax.add_artist(rec1)
        ax.add_artist(rec2)
        ax.add_artist(circle1)
        ax.add_artist(DoP)
        ax.axis('off')

def main():
    state = _get_state()
    pages = {
        "Team Shots": TeamShot,
        "Team Shots Against": TeamShotD,
        "Team Pass Network": TeamMatchPN,
        "Team PassSonar": TeamPassSonar,
        "Team Passing From/To Zones": TeamPassingEngine,
        "Team Passing Attacking Third": PassDash,
        "Team Defense": TeamDefensive,
        "Team Attacking Corners": AttCorner,
        "Team Defensive Corners": DefCorner,
        "Player Shots": PlayerShot,
        "Goalkeeper Shot Map": GKShotMap,
        "Player Pass": PlayerPass,
        "Player Carry": PlayerCarry,
        "Player Pass Network": PlayerMatchPN,
        "Player PassSonar": PlayerPassSonar,
        "Player Passing From/To Zones": PlayerPassingEngine,
        "Player Defense": PlayerDefensive,
    }

    #st.sidebar.title("Page Filters")
    page = st.sidebar.radio("Select Page", tuple(pages.keys()))

    # Display the selected page with the session state
    pages[page](state)

    # Mandatory to avoid rollbacks with widgets, must be called at the end of your app
    state.sync()



def display_state_values(state):
    st.write("Input state:", state.input)
    st.write("Slider state:", state.slider)
    #st.write("Radio state:", state.radio)
    st.write("Checkbox state:", state.checkbox)
    st.write("Selectbox state:", state.selectbox)
    st.write("Multiselect state:", state.multiselect)
    
    for i in range(3):
        st.write(f"Value {i}:", state[f"State value {i}"])

    if st.button("Clear state"):
        state.clear()

def multiselect(label, options, default, format_func=str):
    """multiselect extension that enables default to be a subset list of the list of objects
     - not a list of strings

     Assumes that options have unique format_func representations

     cf. https://github.com/streamlit/streamlit/issues/352
     """
    options_ = {format_func(option): option for option in options}
    default_ = [format_func(option) for option in default]
    selections = st.multiselect(
        label, options=list(options_.keys()), default=default_, format_func=format_func
    )
    return [options_[format_func(selection)] for selection in selections]


#selections = multiselect("Select", options=[Option1, Option2], default=[Option2])


class _SessionState:

    def __init__(self, session, hash_funcs):
        """Initialize SessionState instance."""
        self.__dict__["_state"] = {
            "data": {},
            "hash": None,
            "hasher": _CodeHasher(hash_funcs),
            "is_rerun": False,
            "session": session,
        }

    def __call__(self, **kwargs):
        """Initialize state data once."""
        for item, value in kwargs.items():
            if item not in self._state["data"]:
                self._state["data"][item] = value

    def __getitem__(self, item):
        """Return a saved state value, None if item is undefined."""
        return self._state["data"].get(item, None)
        
    def __getattr__(self, item):
        """Return a saved state value, None if item is undefined."""
        return self._state["data"].get(item, None)

    def __setitem__(self, item, value):
        """Set state value."""
        self._state["data"][item] = value

    def __setattr__(self, item, value):
        """Set state value."""
        self._state["data"][item] = value
    
    def clear(self):
        """Clear session state and request a rerun."""
        self._state["data"].clear()
        self._state["session"].request_rerun()
    
    def sync(self):
        """Rerun the app with all state values up to date from the beginning to fix rollbacks."""

        # Ensure to rerun only once to avoid infinite loops
        # caused by a constantly changing state value at each run.
        #
        # Example: state.value += 1
        if self._state["is_rerun"]:
            self._state["is_rerun"] = False
        
        elif self._state["hash"] is not None:
            if self._state["hash"] != self._state["hasher"].to_bytes(self._state["data"], None):
                self._state["is_rerun"] = True
                self._state["session"].request_rerun()

        self._state["hash"] = self._state["hasher"].to_bytes(self._state["data"], None)

def _get_session():
    session_id = get_report_ctx().session_id
    session_info = Server.get_current()._get_session_info(session_id)

    if session_info is None:
        raise RuntimeError("Couldn't get your Streamlit Session object.")
    
    return session_info.session

def _get_state(hash_funcs=None):
    session = _get_session()

    if not hasattr(session, "_custom_session_state"):
        session._custom_session_state = _SessionState(session, hash_funcs)

    return session._custom_session_state


#df = load_defense_data()

    
def PlayerDefensive(state):
    sm_df = load_sm_data()
    
    team = st.sidebar.multiselect('Select Team(s)', natsorted(sm_df.Team.unique()))
    sm_df = sm_df[sm_df['Team'].isin(team)]
    
    
    season = st.sidebar.multiselect('Select Season(s)',natsorted(sm_df.Season.unique()))  
    sm_df = sm_df[sm_df['Season'].isin(season)]
    
    defense_df = load_defense_data(season, team)
    
    player = st.sidebar.multiselect("Select Player(s)", natsorted(defense_df.Player.unique()))
    player_df = defense_df[defense_df['Player'].isin(player)]
    

    matches = (player_df.MatchName.unique()).tolist()
    
    match = st.sidebar.multiselect("Select Match(es)", natsorted(player_df.MatchName.unique()), default=matches)
    match_df = player_df[player_df['MatchName'].isin(match)]
    
    #st.text(f"Selected Season: {season} / Selected Team: {team} / Player: {player}")
    

    
    st.header("Defensive Maps")
    draw_pitch('none', 'black', 'horizontal', 'full')
    #player_events = player_df[(player_df.Player == player)]
    plt.title(str(season)+' - '+str(player)+' Heat Map', fontproperties=headers, color="black")
    sns.kdeplot(match_df.X, match_df.Y, cmap="RdYlBu_r",shade=True,n_levels=25, shade_lowest=False, alpha=.45, zorder=zo)

    plt.arrow(0.5, 2.5, 18-2, 1-1, head_width=1.2,
            head_length=1.2,
            color='black',
            alpha=1,
            length_includes_head=True, zorder=12, width=.3)
    plt.xlim(-.5,105.5)
    plt.ylim(-.5,68.5)
    st.pyplot()
    
    
    draw_pitch('none', 'black', 'horizontal', 'full')
    plt.title(str(season)+' - '+str(player)+' GPA Map', fontproperties=headers, color="black")
    norm=TwoSlopeNorm(vmin=-.04, vcenter=0, vmax=.04)

    plt.scatter(match_df.X,match_df.Y,marker='o',c=match_df.GPA, facecolors="none", s=120,
            edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
    sm = plt.cm.ScalarMappable(cmap='RdYlBu_r', norm=TwoSlopeNorm(vmin=-.03, vcenter=0, vmax=.03))
    sm.A = []
    cbar = plt.colorbar(sm,orientation='horizontal', fraction=0.02, pad=0.01, ticks=[-.03, 0, .03])
    cbar.set_label('GPA', fontproperties=footers)

    st.pyplot()
    
def TeamDefensive(state):
    sm_df = load_sm_data()
    
    team = st.sidebar.multiselect('Select Team(s)', natsorted(sm_df.Team.unique()))
    sm_df = sm_df[sm_df['Team'].isin(team)]
    
    #pass_df1 = pass_df.to_pandas_df()
    
    season = st.sidebar.multiselect('Select Season(s)',natsorted(sm_df.Season.unique()))  
    sm_df = sm_df[sm_df['Season'].isin(season)]
    
    defense_df = load_defense_data(season, team)
    
    matches = (defense_df.MatchName.unique()).tolist()
    
    match = st.sidebar.multiselect("Select Match(es)", natsorted(defense_df.MatchName.unique()), default=matches)
    match_df = defense_df[defense_df['MatchName'].isin(match)]

    st.header("Team Defensive Maps")  
    st.subheader("Heat Map, GPA Map, & Coverage Map")    
    st.text("")
    
    
    draw_pitch('none', 'black', 'horizontal', 'full')
    #player_events = player_df[(player_df.Player == player)]
    plt.title(str(season)+' - '+str(team)+' Heat Map', fontproperties=headers, color="black")
    sns.kdeplot(match_df.X, match_df.Y, cmap="RdYlBu_r",shade=True,n_levels=25, shade_lowest=False, alpha=.45, zorder=zo)

    plt.arrow(0.5, 2.5, 18-2, 1-1, head_width=1.2,
            head_length=1.2,
            color='black',
            alpha=1,
            length_includes_head=True, zorder=12, width=.3)
    plt.xlim(-.5,105.5)
    plt.ylim(-.5,68.5)
    st.pyplot()
    
    
    draw_pitch('none', 'black', 'horizontal', 'full')
    plt.title(str(season)+' - '+str(team)+' GPA Map', fontproperties=headers, color="black")
    norm=TwoSlopeNorm(vmin=-.04, vcenter=0, vmax=.04)

    plt.scatter(match_df.X,match_df.Y,marker='o',c=match_df.GPA, facecolors="none", s=120,
            edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
    sm = plt.cm.ScalarMappable(cmap='RdYlBu_r', norm=TwoSlopeNorm(vmin=-.03, vcenter=0, vmax=.03))
    sm.A = []
    cbar = plt.colorbar(sm,orientation='horizontal', fraction=0.02, pad=0.01, ticks=[-.03, 0, .03])
    cbar.set_label('GPA', fontproperties=footers)

    st.pyplot()
    
    st.markdown("Map below will be best with a single or a couple matches selected")
    
    match1 = st.sidebar.multiselect("Select Match(es) for Coverage Map", natsorted(match_df.MatchName.unique()))
    match_df1 = match_df[match_df['MatchName'].isin(match1)]

    st.text(f"Selected Matches {match1}")

    Title = fm.FontProperties(fname=fontPathBold, size=32)
    Annotate = fm.FontProperties(fname=fontPathBold, size=30)
    Legend = fm.FontProperties(fname=fontPathBold, size=28)

    action = st.sidebar.multiselect('Select Action(s)', natsorted(match_df1.Action.unique()))
    action_df = match_df1[match_df1['Action'].isin(action)]
    
    players = (action_df.Player.unique()).tolist()
    
    player = st.sidebar.multiselect("Select Player(s)", natsorted(action_df.Player.unique()), default=players)
    player_df = action_df[action_df['Player'].isin(player)]


    defdata = player_df

    players = defdata['Player'].unique()
    #players
    
    players = defdata['Player'].tolist()
    
    
    x = defdata['X'].tolist()
    y = defdata['Y'].tolist()
    
    fig,ax = plt.subplots(figsize=(22,32))
    vertfull_pitch('#B2B2B2', 'white', ax)

    #draw_pitch("#B2B2B2", "black", "vertical", "full")
    
    #For each player in our players variable
    for player in players:
        
        #Create a new dataframe for the player
        df = defdata[(defdata.Player == player)]
        
        x1 = df.X.mean()
        y1 = df.Y.mean()
        
        distx = abs(df.X - x1)
        disty = abs(df.Y - x1)
        
        df1 = df.drop(df[abs(df['X'] - x1) > .7 * distx].index)
        df1 = df.drop(df[abs(df['Y'] - y1) > .7 * disty].index)
        
        xm = df1.X.mean()
        ym = df1.Y.mean()
        
        #Create an array of the x/y coordinate groups
        points = df1[['Y', 'X']].values
    
        #If there are enough points for a hull, create it. If there's an error, forget about it
        try:
            hull = ConvexHull(df1[['Y','X']])
            
        except:
            pass
        
        #If we created the hull, draw the lines and fill with 5% transparent red. If there's an error, forget about it
        try:     
            for simplex in hull.simplices:
                plt.plot(68-points[simplex, 0], points[simplex, 1], 'k-', color='white')
                plt.fill(68-points[hull.vertices,0], points[hull.vertices,1], color='black', alpha=0.025, zorder=zo+4)
                           
        except:
            pass
        
        plt.scatter(68-ym,xm, zorder=zo+5, color='white')
        plt.annotate(player,(68-ym,xm), color='white',fontproperties=Annotate, zorder=zo+5)
        plt.title(str(season)+' - '+str(team)+' - '+str(action)+' Coverage Map',fontproperties=Title)
        plt.annotate("Convex Hulls of "+str(action), xy=(5, 108), fontproperties=Legend, color='black')
        plt.annotate("Name and Point is Avg Location of "+str(action), xy=(5, 106.5), fontproperties=Legend, color='black')

    st.pyplot()

def PlayerPass(state):
    sm_df = load_sm_data()
    
    team = st.sidebar.multiselect('Select Team(s)', natsorted(sm_df.Team.unique()))
    sm_df = sm_df[sm_df['Team'].isin(team)]
    
    
    season = st.sidebar.multiselect('Select Season(s)',natsorted(sm_df.Season.unique()))  
    sm_df = sm_df[sm_df['Season'].isin(season)]
    
    pass_df = load_pass_data(season, team, 'no')
    
    player = st.sidebar.multiselect("Select Player(s)", natsorted(pass_df.Player.unique()))
    player_df = pass_df[pass_df['Player'].isin(player)]
    

    matches = (player_df.MatchName.unique()).tolist()
    
    match = st.sidebar.multiselect("Select Match(es)", natsorted(player_df.MatchName.unique()), default=matches)
    match_df = player_df[player_df['MatchName'].isin(match)]
    
        
    
    st.header("Player Pass Maps")  
    st.subheader("GPA Map, xA Map, & OP Map")    
    st.text("")

    df = match_df
    progdf = df[(df['ProgPass'] == 1) & (df['ifSP'] != 1)]
    deepdf = df[(df['DeepProg'] == 1) & (df['ifSP'] != 1)]
    crossdf = df[((df['ifCross'] == 1)|(df['in18'] == 1)) & (df['ifSP'] != 1)]
    startdf = df[(df['ifStart'] == 1) & (df['ifSP'] != 1)]
    
    xS = df["X"]
    yS = df["Y"]
    xE = df["DestX"]
    yE = df["DestY"]
    xSP = progdf["X"]
    ySP = progdf["Y"]
    xEP = progdf["DestX"]
    yEP = progdf["DestY"]
    xSD = deepdf["X"]
    ySD = deepdf["Y"]
    xED = deepdf["DestX"]
    yED = deepdf["DestY"]
    xSC = crossdf["X"]
    ySC = crossdf["Y"]
    xEC = crossdf["DestX"]
    yEC = crossdf["DestY"]
    xSS = startdf["X"]
    ySS = startdf["Y"]
    xES = startdf["DestX"]
    yES = startdf["DestY"]
    
    figsize1 = 32
    figsize2 = 18
    widths = [3.13, 1.25]
    heights = [1, 2]
    fig = plt.figure(figsize=(figsize1, figsize2)) 
    gs = gridspec.GridSpec(2, 3, left=.15, right=1, wspace=0.05)    
    
    ax1 = plt.subplot(gs[0, 0])
    plt.title('Progressive Passes', color='black',fontproperties=Subtitle)
    #plt.title(str(Season)+' - '+str(Player)+' - xA Map', color='white', size=30, weight='bold')
    horizfull_pitch('white', 'black', ax1)
    plt.text(42.5, -4, 'GPA: '+str(round(sum(progdf.GPA),2)), color='black',fontproperties=footers)

    
    for i in range(len(progdf)):
        z = progdf.GPA.values
        cmap = mpl.cm.get_cmap('bwr')
        norm_range = mpl.colors.Normalize(vmin=-.02, vmax=0.04)
        c_vals = [cmap(norm_range(value)) for value in z]
        #plt.plot([68-ySA.iloc[i],68-yEA.iloc[i]],
         #   [xSA.iloc[i],xEA.iloc[i]],zorder=zo, color="dodgerblue", lw=5)
        #plt.annotate('',xy=(xSP.iloc[i], ySP.iloc[i]), xycoords='data', xytext=(xEP.iloc[i], yEP.iloc[i]),textcoords='data',
         #           arrowprops=dict(arrowstyle='wedge', connectionstyle='arc3',
          #                          color='red' if progdf.LostAfterCarry.iloc[i]==1 else 'dodgerblue', lw=2))
        plt.arrow(xSP.iloc[i], ySP.iloc[i], (xEP.iloc[i])-(xSP.iloc[i]), yEP.iloc[i]-ySP.iloc[i], head_width=1.2,
            head_length=1.2, color=c_vals[i],length_includes_head=True, zorder=zo if progdf.GPA.iloc[i] <= 0 else 15, alpha= .35 if progdf.GPA.iloc[i] <= 0 else 1)
        plt.scatter(xSP.iloc[i], ySP.iloc[i],zorder=zo+6 if progdf.GPA.iloc[i] <= 0 else 21, color=c_vals[i], alpha= .35 if progdf.GPA.iloc[i] <= 0 else 1,
                    edgecolor='black', marker='o', linewidths=2, s=120)
    
    ax2 = plt.subplot(gs[0, 1])
    plt.title('Deep Progressions', color='black', fontproperties=Subtitle)
    #plt.title(str(Season)+' - '+str(Player)+' - xA Map', color='white', size=30, weight='bold')
    horizfull_pitch('white', 'black', ax2)
    plt.text(42.5, -4, 'GPA: '+str(round(sum(deepdf.GPA),2)), color='black',fontproperties=footers)

    
    for i in range(len(deepdf)):
        z = deepdf.GPA.values
        cmap = mpl.cm.get_cmap('bwr')
        norm_range = mpl.colors.Normalize(vmin=-.02, vmax=0.04)
        c_vals = [cmap(norm_range(value)) for value in z]
        #plt.plot([68-ySA.iloc[i],68-yEA.iloc[i]],
         #   [xSA.iloc[i],xEA.iloc[i]],zorder=zo, color="dodgerblue", lw=5)
        #plt.annotate('',xy=(xSP.iloc[i], ySP.iloc[i]), xycoords='data', xytext=(xEP.iloc[i], yEP.iloc[i]),textcoords='data',
         #           arrowprops=dict(arrowstyle='wedge', connectionstyle='arc3',
          #                          color='red' if progdf.LostAfterCarry.iloc[i]==1 else 'dodgerblue', lw=2))
        plt.arrow(xSD.iloc[i], ySD.iloc[i], (xED.iloc[i])-(xSD.iloc[i]), yED.iloc[i]-ySD.iloc[i], head_width=1.2,
            head_length=1.2, color=c_vals[i],length_includes_head=True, zorder=zo if deepdf.GPA.iloc[i] <= 0 else 15, alpha= .35 if deepdf.GPA.iloc[i] <= 0 else 1)
        plt.scatter(xSD.iloc[i], ySD.iloc[i],zorder=zo+6 if deepdf.GPA.iloc[i] <= 0 else 21, color=c_vals[i], alpha= .35 if deepdf.GPA.iloc[i] <= 0 else 1,
                    edgecolor='black', marker='o', linewidths=2, s=120)

    ax3 = plt.subplot(gs[1, 0])
    plt.title('Crosses and Passes into Penalty Area', color='black', fontproperties=Subtitle)
    #plt.title(str(Season)+' - '+str(Player)+' - xA Map', color='white', size=30, weight='bold')
    horizfull_pitch('white', 'black', ax3)
    plt.text(42.5, -4, 'GPA: '+str(round(sum(crossdf.GPA),2)), color='black', fontproperties=footers)
    
    for i in range(len(crossdf)):
        z = crossdf.GPA.values
        cmap = mpl.cm.get_cmap('bwr')
        norm_range = mpl.colors.Normalize(vmin=-.02, vmax=0.04)
        c_vals = [cmap(norm_range(value)) for value in z]
        #plt.plot([68-ySA.iloc[i],68-yEA.iloc[i]],
         #   [xSA.iloc[i],xEA.iloc[i]],zorder=zo, color="dodgerblue", lw=5)
        #plt.annotate('',xy=(xSP.iloc[i], ySP.iloc[i]), xycoords='data', xytext=(xEP.iloc[i], yEP.iloc[i]),textcoords='data',
         #           arrowprops=dict(arrowstyle='wedge', connectionstyle='arc3',
          #                          color='red' if progdf.LostAfterCarry.iloc[i]==1 else 'dodgerblue', lw=2))
        plt.arrow(xSC.iloc[i], ySC.iloc[i], (xEC.iloc[i])-(xSC.iloc[i]), yEC.iloc[i]-ySC.iloc[i], head_width=1.2,
            head_length=1.2, color=c_vals[i],length_includes_head=True, zorder=zo if crossdf.GPA.iloc[i] <= 0 else 15, alpha= .35 if crossdf.GPA.iloc[i] <= 0 else 1)
        plt.scatter(xSC.iloc[i], ySC.iloc[i],zorder=zo+6 if crossdf.GPA.iloc[i] <= 0 else 21, color=c_vals[i], alpha= .35 if crossdf.GPA.iloc[i] <= 0 else 1,
                    edgecolor='black', marker='o', linewidths=2, s=120)
        
    ax4 = plt.subplot(gs[1, 1])
    plt.title('Passes To Start Possession', color='black', fontproperties=Subtitle)
    #plt.title(str(Season)+' - '+str(Player)+' - xA Map', color='white', size=30, weight='bold')
    horizfull_pitch('white', 'black', ax4)
    plt.text(42.5, -4, 'GPA: '+str(round(sum(startdf.GPA),2)), color='black', fontproperties=footers)
    
    for i in range(len(startdf)):
        z = startdf.GPA.values
        cmap = mpl.cm.get_cmap('bwr')
        norm_range = mpl.colors.Normalize(vmin=-.02, vmax=0.04)
        c_vals = [cmap(norm_range(value)) for value in z]
        #plt.plot([68-ySA.iloc[i],68-yEA.iloc[i]],
         #   [xSA.iloc[i],xEA.iloc[i]],zorder=zo, color="dodgerblue", lw=5)
        #plt.annotate('',xy=(xSP.iloc[i], ySP.iloc[i]), xycoords='data', xytext=(xEP.iloc[i], yEP.iloc[i]),textcoords='data',
         #           arrowprops=dict(arrowstyle='wedge', connectionstyle='arc3',
          #                          color='red' if progdf.LostAfterCarry.iloc[i]==1 else 'dodgerblue', lw=2))
        plt.arrow(xSS.iloc[i], ySS.iloc[i], (xES.iloc[i])-(xSS.iloc[i]), yES.iloc[i]-ySS.iloc[i], head_width=1.2,
            head_length=1.2, color=c_vals[i],length_includes_head=True, zorder=zo if startdf.GPA.iloc[i] <= 0 else 15, alpha= .35 if startdf.GPA.iloc[i] <= 0 else 1)
        plt.scatter(xSS.iloc[i], ySS.iloc[i],zorder=zo+6 if startdf.GPA.iloc[i] <= 0 else 21, color=c_vals[i], alpha= .35 if startdf.GPA.iloc[i] <= 0 else 1,
                    edgecolor='black', marker='o', linewidths=2, s=120)

    ax5 = plt.subplot(gs[:,2])
    plt.title('Heat Map of\nAll Passes', color='black', fontproperties=Subtitle)
    vertfull_pitch('none', 'black', ax5)
    #passdata = df[(df['Team'].str.contains(Team))]
    #pasd = passdata.groupby("MatchID").agg({"Team": 'nunique'})
    #mp = pasd.sum()
    #plt.hist2d(68-df['Y'], df['X'], bins=12, cmap='RdYlBu_r', zorder=12, alpha=.35, cmin=mp.sum()*.09, range=([-.1,68.1], [-.1,105.1]))
    #plt.hexbin(68-df['Y'], df['X'], cmap='RdYlBu_r', gridsize=10, C=df.CarrySum, reduce_C_function=np.sum, zorder=12, alpha=.35, mincnt=mp.sum()*.09)    
    sns.kdeplot(68-df['Y'], df['X'], shade=True, shade_lowest=False, cmap='RdYlBu_r', n_levels=100, alpha=.35)
    plt.xlim(0,68)
    plt.ylim(0,105)

    #ax4 = plt.subplot(gs[1,1])
    #ax4.scatter(0,0, alpha=0)
    #ax4.scatter(1,1,alpha=0)
    #ax4.axis('off')
    cax = plt.axes([0.325, 0.075, 0.2, 0.025])
    sm = plt.cm.ScalarMappable(cmap='bwr', norm=TwoSlopeNorm(vmin=-.02,vcenter=0, vmax=.04))
    sm.A = []
    cbar = fig.colorbar(sm, cax=cax, orientation='horizontal', fraction=0.046, pad=0.04)
    cbar.set_label('GPA', color='black', fontproperties=footers)
    cbar.ax.tick_params(labelsize=20,labelcolor='black')
    cbar.set_ticks([-.02, -.01, 0, .01, .01, .02, .03, .04])
    cbar.ax.set_xticklabels([-.02, -.01, 0, .01, .01, .02, .03, .04])
    
    #ax3.text(0.50,0.65,'Progressive Passes colored by:',fontproperties=TableHead,color='white',
     #     horizontalalignment='center', verticalalignment='center')
    
    statsdf = match_df.groupby(["Season","Player"]).agg({'GPA':'sum','ProgPass':'sum', 'ifPass':'sum'})
    
    possessions = match_df.groupby(["MatchName","Team", "Player"]).agg({'Possession':'nunique','Action':'count'}).reset_index()
    totalpos = possessions.groupby(["Team", "Player"]).agg({'Possession':'sum','Action':'sum','MatchName':'nunique'}).reset_index()

    perpos = pd.merge(statsdf, totalpos, on=["Player"])
    perpos['GPAper100Pos'] = (perpos['GPA'] / (perpos['Possession'] / 100))
    perpos['Carryper100Pos'] = (perpos['ifPass'] / (perpos['Possession'] / 100))
    perpos['ProgPassper100Pos'] = (perpos['ProgPass'] / (perpos['Possession'] / 100))
    perpos['PosInv'] = (perpos['Possession'] / (perpos['MatchName']))

    
    fig.text(.475, .96,'Goal Probability Added\nper 100 Possessions -', color='black', fontproperties=Summary)
    fig.text(.615, .96, str(round(sum(perpos.GPAper100Pos),2)), color='dodgerblue', fontproperties=Summary)

    fig.text(.67, .96,'Possession Involvements\nper Match -', color='black', fontproperties=Summary)
    fig.text(.76, .96, str(round(sum(perpos.PosInv),2)), color='dodgerblue', fontproperties=Summary)

    fig.text(.84, .96,'Progressive Passes\nper 100 Possessions -', color='black', fontproperties=Summary)
    fig.text(.98, .96, str(round(sum(perpos.ProgPassper100Pos),2)), color='dodgerblue', fontproperties=Summary)

    fig.text(0.15,0.96,str(player),fontsize=58,  color='black', fontproperties=Head)
    fig.text(0.15,0.925,str(season)+' - '+str(team)+' - Passes', color='black',fontproperties=Subtitle)
    #fig.text(0.15,0.1,'az',fontsize=12, weight='bold', color='black', family='fantasy', alpha=0)

    st.pyplot()


    df = match_df[match_df['ifSP'] != 1]
    assist = df[df['ifAssist'] == 1]
    xA = df[(df['xA'] >= .075) & (df['ifAssist'] != 1)]
    ShotAssist = df[(df['ShotAssist'] == 1) & (df['ifAssist'] != 1) & (df['xA'] < .075)] 
    
    xS = df["X"]
    yS = df["Y"]
    xE = df["DestX"]
    yE = df["DestY"]
    xSA = assist["X"]
    ySA = assist["Y"]
    xEA = assist["DestX"]
    yEA = assist["DestY"]
    xSxA = xA["X"]
    ySxA = xA["Y"]
    xExA = xA["DestX"]
    yExA = xA["DestY"]
    xSSA = ShotAssist["X"]
    ySSA = ShotAssist["Y"]
    xESA = ShotAssist["DestX"]
    yESA = ShotAssist["DestY"]

    #opta/mckeever blue hex code #2f3653 & #82868f
    figsize1 = 32
    figsize2 = 18
    fig = plt.figure(figsize=(figsize1, figsize2),facecolor='white') 
    gs = gridspec.GridSpec(3, 2, width_ratios=[3.13, 1.25])

    ax1 = plt.subplot(gs[:, 0])
    #plt.title(str(Season)+' - '+str(Player)+' - xA Map', color='white', size=30, weight='bold')
    verthalf_pitch('white', 'black', ax1)
    plt.scatter(68-yS, xS, marker='o',s=125, facecolor="#333333", linewidths=2,
        zorder=zo+5, alpha=.5)
    
    for i in range(len(assist)):
        #plt.plot([68-ySA.iloc[i],68-yEA.iloc[i]],
         #   [xSA.iloc[i],xEA.iloc[i]],zorder=zo, color="dodgerblue", lw=5)
        plt.annotate('',xy=(68-ySA.iloc[i], xSA.iloc[i]), xycoords='data', xytext=(68-yEA.iloc[i], xEA.iloc[i]),textcoords='data',
                    arrowprops=dict(arrowstyle='wedge', connectionstyle='arc3', color='gold', lw=2))
        plt.scatter(68-yEA.iloc[i], xEA.iloc[i],zorder=zo+6,
            color="gold", edgecolor='black', marker='o', linewidths=3.5, s=200)
    for i in range(len(xA)):
        #plt.plot([68-ySxA.iloc[i],68-yExA.iloc[i]],
         #   [xSxA.iloc[i],xExA.iloc[i]],zorder=zo, color="dodgerblue", lw=5)
        plt.annotate('',xy=(68-ySxA.iloc[i], xSxA.iloc[i]), xycoords='data', xytext=(68-yExA.iloc[i], xExA.iloc[i]),textcoords='data',
                    arrowprops=dict(arrowstyle='wedge', connectionstyle='arc3', color="crimson" if xA.xA.iloc[i]>=.1 else 'aqua', lw=2))
        plt.scatter(68-yExA.iloc[i], xExA.iloc[i],zorder=zo+4,
            color="crimson" if xA.xA.iloc[i]>=.1 else 'aqua', edgecolor='black', marker='o', linewidths=3.5, s=200)
    for i in range(len(ShotAssist)):
        #plt.plot([68-ySA.iloc[i],68-yEA.iloc[i]],
         #   [xSA.iloc[i],xEA.iloc[i]],zorder=zo, color="dodgerblue", lw=5)
        plt.annotate('',xy=(68-ySSA.iloc[i], xSSA.iloc[i]), xycoords='data', xytext=(68-yESA.iloc[i], xESA.iloc[i]),textcoords='data',
                    arrowprops=dict(arrowstyle='wedge', connectionstyle='arc3', color='dodgerblue', lw=2))
        plt.scatter(68-yESA.iloc[i], xESA.iloc[i],zorder=zo+3,
            color="dodgerblue", edgecolor='black', marker='o', linewidths=3.5, s=200)
    
    ax2 = plt.subplot(gs[0, 1])
    ax2.axis('off')
    ax2.set_xticks([0,1])
    ax2.set_yticks([0,1])
    ax2.scatter(0,0, alpha=0)
    ax2.scatter(1,1,alpha=0)
    ax2.scatter(0.05, .45, marker='o', s=200, color='gold', edgecolor='black', linewidths=3.5, zorder=zo+5)
    ax2.scatter(0.325, .45, marker='o', s=200, color='crimson', edgecolor='black', linewidths=3.5, zorder=zo+5)
    ax2.scatter(0.625, .45, marker='o', s=200, color='aqua', edgecolor='black', linewidths=3.5, zorder=zo+5)
    ax2.scatter(0.9, .45, marker='o', s=200, color='dodgerblue', edgecolor='black', linewidths=3.5, zorder=zo+5)
    ax2.text(0.05, 0.35, 'Assist', color='black', fontproperties=Annotate, horizontalalignment='center', verticalalignment='center')
    ax2.text(0.325, 0.35, 'xA >= .1', color='black', fontproperties=Annotate, horizontalalignment='center', verticalalignment='center')
    ax2.text(0.625, 0.35, 'xA >= .075', color='black', fontproperties=Annotate, horizontalalignment='center', verticalalignment='center')
    ax2.text(0.9, 0.35, 'Shot Assist', color='black', fontproperties=Annotate, horizontalalignment='center', verticalalignment='center')

    ax2.text(0.30,0.85,str(round(sum(df.ifAssist),))+" Assists",fontsize=28, color='white', fontproperties=TableSummary,
              horizontalalignment='center', verticalalignment='center', bbox=dict(facecolor='black',edgecolor='#B2B2B2', lw=5))
    ax2.text(0.69,0.85,str(round(sum(df.xA),2))+" xA",fontsize=28, color='white', fontproperties=TableSummary,
             horizontalalignment='center', verticalalignment='center', bbox=dict(facecolor='black', edgecolor='#B2B2B2', lw=5))
    
    ax2.text(0.5,0.1,str(round(sum(df.AttThird)),)+" Completed Attacking 1/3 Passes",fontproperties=Summary,color='black', horizontalalignment='center', verticalalignment='center')
    ax2.text(0.5,0.01,str(round(sum(df.Cin18)),)+" Completed Passes into 18",fontproperties=Summary, color='black', horizontalalignment='center', verticalalignment='center')    

    
    
    ax3 = plt.subplot(gs[1, 1])
    plt.title('Assists & High xA Passes & Shot Assists', color='black', fontproperties=SmallTitle)
    verthalf_pitch('white', 'black', ax3)
    for i in range(len(assist)):
        #plt.plot([68-ySA.iloc[i],68-yEA.iloc[i]],
         #   [xSA.iloc[i],xEA.iloc[i]],zorder=zo, color="dodgerblue", lw=5)
        plt.annotate('',xy=(68-ySA.iloc[i], xSA.iloc[i]), xycoords='data', xytext=(68-yEA.iloc[i], xEA.iloc[i]),textcoords='data',
                    arrowprops=dict(arrowstyle='wedge', connectionstyle='arc3', color='gold', lw=2))
        plt.scatter(68-yEA.iloc[i], xEA.iloc[i],zorder=zo+6,
            color="gold", edgecolor='black', marker='o', linewidths=2, s=120)
    for i in range(len(xA)):
        #plt.plot([68-ySxA.iloc[i],68-yExA.iloc[i]],
         #   [xSxA.iloc[i],xExA.iloc[i]],zorder=zo, color="dodgerblue", lw=5)
        plt.annotate('',xy=(68-ySxA.iloc[i], xSxA.iloc[i]), xycoords='data', xytext=(68-yExA.iloc[i], xExA.iloc[i]),textcoords='data',
                    arrowprops=dict(arrowstyle='wedge', connectionstyle='arc3', color="crimson" if xA.xA.iloc[i]>=.1 else 'aqua', lw=2))
        plt.scatter(68-yExA.iloc[i], xExA.iloc[i],zorder=zo+4,
            color="crimson" if xA.xA.iloc[i]>=.1 else 'aqua', edgecolor='black', marker='o', linewidths=2, s=120)
    for i in range(len(ShotAssist)):
        #plt.plot([68-ySA.iloc[i],68-yEA.iloc[i]],
         #   [xSA.iloc[i],xEA.iloc[i]],zorder=zo, color="dodgerblue", lw=5)
        plt.annotate('',xy=(68-ySSA.iloc[i], xSSA.iloc[i]), xycoords='data', xytext=(68-yESA.iloc[i], xESA.iloc[i]),textcoords='data',
                    arrowprops=dict(arrowstyle='wedge', connectionstyle='arc3', color='dodgerblue', lw=2))
        plt.scatter(68-yESA.iloc[i], xESA.iloc[i],zorder=zo+3,
            color="dodgerblue", edgecolor='black', marker='o', linewidths=2, s=120)

        
    ax4 = plt.subplot(gs[2, 1])
    plt.title('Pass Start Locations', color='black', fontproperties=SmallTitle)
    verthalf_pitch('white', 'black', ax4)
    plt.scatter(68-yS, xS, marker='o',s=50, facecolor="#333333", linewidths=2,
        zorder=zo+5, alpha=.5)
   
    
    fig.text(0.15,0.93,str(player),fontsize=58, color='black', fontproperties=Head)
    fig.text(0.15,0.9,str(season)+' - '+str(team)+' - OP Passes',fontproperties=Subtitle,color='black')
    
    st.pyplot()
    
    st.markdown("Map below will be best with a single or a couple matches selected")
    
    match1 = st.sidebar.multiselect("Select Match(es) for OP Pass Map", natsorted(player_df.MatchName.unique()))
    match_df1 = player_df[player_df['MatchName'].isin(match1)]

    st.text(f"Selected Matches {match1}")
    
    retain = match_df1[(match_df1['ifRetain'] == 1) & (match_df1['ifSP'] != 1)]
    incornret = match_df1[(match_df1['ifRetain'] != 1) & (match_df1['ifSP'] != 1)]


    xS = retain["X"]
    yS = retain["Y"]
    xE = retain["DestX"]
    yE = retain["DestY"]
    xS1 = incornret["X"]
    yS1 = incornret["Y"]
    xE1 = incornret["DestX"]
    yE1 = incornret["DestY"]
    xP = player_df['xP']

    draw_pitch('none', 'black', 'horizontal', 'full')
   
    for i in range(len(retain)):
        plt.arrow(xS.iloc[i], yS.iloc[i],  xE.iloc[i]-xS.iloc[i], (yE.iloc[i])-(yS.iloc[i]),  width=xP.iloc[i], head_width=xP.iloc[i]*2,
           head_length=xP.iloc[i]*2,
           color='lime',
           alpha=1,
           length_includes_head=True, zorder=zo)
    for i in range(len(incornret)):
        plt.arrow(xS1.iloc[i], yS1.iloc[i],  xE1.iloc[i]-xS1.iloc[i], (yE1.iloc[i])-(yS1.iloc[i]),  width=xP.iloc[i], head_width=xP.iloc[i]*2,
           head_length=xP.iloc[i]*2,
           color="dodgerblue" if incornret.iloc[i]["ifComplete"] == 1
           else "red", alpha=1,length_includes_head=True, zorder=zo)

    plt.title(str(season)+' - '+str(player)+" OP Passes", fontproperties=headers, color="black")
    #plt.annotate(str(round(sum(pass_data.PP),2))+" Progressive Passes",color="white", xy=(44, -2), size = 10, ha="center", weight="bold", zorder=zo)
    #plt.annotate(str(round(sum(pass_data.DP),2))+" Deep Progressions",color="white", xy=(44, -4), size = 10, ha="center", weight="bold", zorder=zo)
    #plt.annotate(str(round(sum(pass_data.xP),2))+" xP",color="white", xy=(24, -2), size = 10, ha="center", weight="bold", zorder=zo)
    #plt.annotate(str(round(sum(pass_data.ifComplete),))+' / '+str(round(sum(pass_data.PassesAttempted),))+" Passes",color="white", xy=(24, -4), size = 10, ha="center", weight="bold", zorder=zo)     
    #plt.annotate("Bigger Arrow  = Higher xP",color="white", xy=(6, 107.5), size = 10, ha="center", weight="bold", zorder=zo)              
    plt.plot(-2,color="lime",label="Retain",zorder=0)
    plt.plot(-2,color="dodgerblue",label="Complete",zorder=0)
    plt.plot(-2,color="red",label="Incomplete",zorder=0)
    #plt.plot(-2,color="gold",label="Assist",zorder=0)
    leg = plt.legend(loc=0, ncol=3,frameon=False)
    plt.setp(leg.get_texts(), color='black', fontproperties=Labels)
    st.pyplot()

    
def PlayerCarry(state):
    sm_df = load_sm_data()
    
    team = st.sidebar.multiselect('Select Team(s)', natsorted(sm_df.Team.unique()))
    sm_df = sm_df[sm_df['Team'].isin(team)]
    
    
    season = st.sidebar.multiselect('Select Season(s)',natsorted(sm_df.Season.unique()))  
    sm_df = sm_df[sm_df['Season'].isin(season)]
    
    carry_df = load_carry_data(season, team)
    
    player = st.sidebar.multiselect("Select Player(s)", natsorted(carry_df.Player.unique()))
    player_df = carry_df[carry_df['Player'].isin(player)]
    

    matches = (player_df.MatchName.unique()).tolist()
    
    match = st.sidebar.multiselect("Select Match(es)", natsorted(player_df.MatchName.unique()), default=matches)
    match_df = player_df[player_df['MatchName'].isin(match)]

    
    st.header("Player Carry Maps")  
    st.subheader("Carry Dashboard, By Next Action, & GPA Map")    
    st.text("")
        
    progdf = match_df[match_df['ProgCarry'] == 1]
    
    xS = match_df["X"]
    yS = match_df["Y"]
    xE = match_df["DestX"]
    yE = match_df["DestY"]
    xSP = progdf["X"]
    ySP = progdf["Y"]
    xEP = progdf["DestX"]
    yEP = progdf["DestY"]
    
    figsize1 = 32
    figsize2 = 18
    widths = [3.13, 1.25]
    heights = [1, 2]
    fig = plt.figure(figsize=(figsize1, figsize2)) 
    gs = gridspec.GridSpec(2, 2, width_ratios=widths, height_ratios=heights,left=.15, right=1, wspace=0.05)    

    ax1 = plt.subplot(gs[:, 0])
    #plt.title(str(Season)+' - '+str(Player)+' - xA Map', color='white', size=30, weight='bold')
    horizfull_pitch('white', 'black', ax1)
    for i in range(len(progdf)):
        #plt.plot([68-ySA.iloc[i],68-yEA.iloc[i]],
         #   [xSA.iloc[i],xEA.iloc[i]],zorder=zo, color="dodgerblue", lw=5)
        #plt.annotate('',xy=(xSP.iloc[i], ySP.iloc[i]), xycoords='data', xytext=(xEP.iloc[i], yEP.iloc[i]),textcoords='data',
         #           arrowprops=dict(arrowstyle='wedge', connectionstyle='arc3',
          #                          color='red' if progdf.LostAfterCarry.iloc[i]==1 else 'dodgerblue', lw=2))
        plt.arrow(xSP.iloc[i], ySP.iloc[i], (xEP.iloc[i])-(xSP.iloc[i]), yEP.iloc[i]-ySP.iloc[i], head_width=1.2,
            head_length=1.2, color="red" if progdf.iloc[i]["LostAfterCarry"] == 1
            else "dodgerblue",alpha=1, length_includes_head=True, zorder=zo, linestyle='--')
        plt.scatter(xSP.iloc[i], ySP.iloc[i],zorder=zo+6,
            color='red' if progdf.LostAfterCarry.iloc[i]==1 else 'dodgerblue', edgecolor='black', marker='o', linewidths=2, s=120)

    ax2 = plt.subplot(gs[1,1])
    plt.title('Heat Map of\nAll Carries', color='black', fontproperties=Subtitle)
    vertfull_pitch('none', 'black', ax2)
    #passdata = df[(df['Team'].str.contains(Team))]
    #pasd = passdata.groupby("Match").agg({"Team": 'nunique'})
    #mp = pasd.sum()
    #plt.hist2d(68-df['Y'], df['X'], bins=12, cmap='RdYlBu_r', zorder=12, alpha=.35, cmin=mp.sum()*.09, range=([-.1,68.1], [-.1,105.1]))
    #plt.hexbin(68-df['Y'], df['X'], cmap='RdYlBu_r', gridsize=10, C=df.ifCarry, reduce_C_function=np.sum, zorder=12, alpha=.35, mincnt=mp.sum()*.09)    
    sns.kdeplot(68-match_df['Y'], match_df['X'], shade=True, shade_lowest=False, cmap='RdYlBu_r', n_levels=100, alpha=.35)
    plt.xlim(0,68)
    plt.ylim(0,105)

    ax3 = plt.subplot(gs[0,1])
    ax3.scatter(0,0, alpha=0)
    ax3.scatter(1,1,alpha=0)
    ax3.axis('off')
    ax3.text(0.50,0.65,'Progressive Carries colored by:', color='black',fontproperties=TableHead,
          horizontalalignment='center', verticalalignment='center')
    ax3.text(0.50,0.475,'Successful Action After Carry', color='dodgerblue', fontproperties=Summary,
          horizontalalignment='center', verticalalignment='center')
    ax3.text(0.50,0.3,'Unsuccessful Action After Carry', color='red', fontproperties=Summary,
          horizontalalignment='center', verticalalignment='center')

    #df['Match1'] = df['Match']
    statsdf = match_df.groupby(["Season","Player"]).agg({'GPA':'sum','ProgCarry':'sum', 'ifCarry':'sum'})
    
    possessions = match_df.groupby(["MatchName","Team", "Player"]).agg({'Possession':'nunique','Action':'count'}).reset_index()
    totalpos = possessions.groupby(["Team", "Player"]).agg({'Possession':'sum','Action':'sum','MatchName':'nunique'}).reset_index()
    
    perpos = pd.merge(statsdf, totalpos, on=["Player"])
    perpos['GPAper100Pos'] = (perpos['GPA'] / (perpos['Possession'] / 100))
    perpos['Carryper100Pos'] = (perpos['ifCarry'] / (perpos['Possession'] / 100))
    perpos['ProgCarryper100Pos'] = (perpos['ProgCarry'] / (perpos['Possession'] / 100))
    perpos['PosInv'] = (perpos['Possession'] / (perpos['MatchName']))

    fig.text(.175, .86,'GPA\nper 100 Possessions -',  color='black', fontproperties=Summary)
    fig.text(.315, .86, str(round(sum(perpos.GPAper100Pos),2)), color='dodgerblue', fontproperties=Summary)

    fig.text(.37, .86,'Possession Involvements\nper Match -', color='black', fontproperties=Summary)
    fig.text(.46, .86, str(round(sum(perpos.PosInv),2)), color='dodgerblue', fontproperties=Summary)

    fig.text(.54, .86,'Progressive Carries\nper 100 Possessions -', color='black', fontproperties=Summary)
    fig.text(.68, .86, str(round(sum(perpos.ProgCarryper100Pos),2)), color='dodgerblue', fontproperties=Summary)

    fig.text(.75, .875, str(season)+' - '+str(player), color='black', fontproperties=headers)
    
    st.pyplot()
    
    df = match_df
    xS = df["X"]
    yS = df["Y"]
    xE = df["DestX"]
    yE = df["DestY"]
    

    draw_pitch('none', 'black', 'horizontal', 'full')
    plt.title(str(season)+' - '+str(player)+" Carries by Next Action", fontproperties=headers, color="black")

    for i in range(len(df)):
        #plt.plot([68-ySA.iloc[i],68-yEA.iloc[i]],
         #   [xSA.iloc[i],xEA.iloc[i]],zorder=zo, color="dodgerblue", lw=5)
        #plt.annotate('',xy=(xSP.iloc[i], ySP.iloc[i]), xycoords='data', xytext=(xEP.iloc[i], yEP.iloc[i]),textcoords='data',
         #           arrowprops=dict(arrowstyle='wedge', connectionstyle='arc3',
          #                          color='red' if progdf.LostAfterCarry.iloc[i]==1 else 'dodgerblue', lw=2))
        plt.arrow(xS.iloc[i], yS.iloc[i], (xE.iloc[i])-(xS.iloc[i]), yE.iloc[i]-yS.iloc[i], head_width=1.2,
            head_length=1.2, color="red" if df.iloc[i]["LostAfterCarry"] == 1
            else "dodgerblue",alpha=1, length_includes_head=True, zorder=zo, linestyle='--')
        plt.scatter(xS.iloc[i], yS.iloc[i],zorder=zo+6,
            color='red' if df.LostAfterCarry.iloc[i]==1 else 'dodgerblue', edgecolor='black', marker='o', linewidths=2, s=120)
    
    plt.plot(-2,color="dodgerblue",label="Completed After Carry",zorder=0)
    plt.plot(-2,color="red",label="Lost After Carry",zorder=0)
    leg = plt.legend(loc=0, ncol=2,frameon=False)
    plt.setp(leg.get_texts(), color='black', fontproperties=Labels)
    st.pyplot()
    
    st.markdown("Map below will be best with a single or a couple matches selected")

    
    match1 = st.sidebar.multiselect("Select Match(es) for GPA Carry Map", natsorted(player_df.MatchName.unique()))
    match_df1 = player_df[player_df['MatchName'].isin(match1)]
    
    st.text(f"Selected Matches {match1}")
    

    xS = match_df1["X"]
    yS = match_df1["Y"]
    xE = match_df1["DestX"]
    yE = match_df1["DestY"]

    draw_pitch('none', 'black', 'horizontal', 'full')
    plt.title(str(season)+' - '+str(player)+" Carries by GPA", fontproperties=headers, color="black")
    for i in range(len(match_df1)):
        z = match_df1.GPA.values
        cmap = mpl.cm.get_cmap('bwr')
        norm_range = mpl.colors.Normalize(vmin=-.02, vmax=0.04)
        c_vals = [cmap(norm_range(value)) for value in z]
        #plt.plot([68-ySA.iloc[i],68-yEA.iloc[i]],
         #   [xSA.iloc[i],xEA.iloc[i]],zorder=zo, color="dodgerblue", lw=5)
        #plt.annotate('',xy=(xSP.iloc[i], ySP.iloc[i]), xycoords='data', xytext=(xEP.iloc[i], yEP.iloc[i]),textcoords='data',
         #           arrowprops=dict(arrowstyle='wedge', connectionstyle='arc3',
          #                          color='red' if progdf.LostAfterCarry.iloc[i]==1 else 'dodgerblue', lw=2))
        plt.arrow(xS.iloc[i], yS.iloc[i], (xE.iloc[i])-(xS.iloc[i]), yE.iloc[i]-yS.iloc[i], head_width=1.2,
            head_length=1.2, color=c_vals[i],length_includes_head=True, zorder=zo if match_df1.GPA.iloc[i] <= 0 else 15, alpha= .35 if match_df1.GPA.iloc[i] <= 0 else 1)
        plt.scatter(xS.iloc[i], yS.iloc[i],zorder=zo+6 if match_df1.GPA.iloc[i] <= 0 else 21, color=c_vals[i], alpha= .35 if match_df1.GPA.iloc[i] <= 0 else 1,
                    edgecolor='black', marker='o', linewidths=2, s=120)

    sm = plt.cm.ScalarMappable(cmap='bwr', norm=TwoSlopeNorm(vmin=-.02, vcenter=0, vmax=.04))
    sm.A = []
    cbar = plt.colorbar(sm,orientation='horizontal', fraction=0.02, pad=0.01, ticks=[-.02, 0, .04])
    cbar.set_label('GPA', fontproperties=footers)

    st.pyplot()

def PlayerPassSonar(state):    
    sm_df = load_sm_data()
    
    team = st.sidebar.multiselect('Select Team(s)', natsorted(sm_df.Team.unique()))
    sm_df = sm_df[sm_df['Team'].isin(team)]
    
    
    season = st.sidebar.multiselect('Select Season(s)',natsorted(sm_df.Season.unique()))  
    sm_df = sm_df[sm_df['Season'].isin(season)]
    
    pass_df = load_pass_data(season, team, 'no')
    
    player = st.sidebar.multiselect("Select Player(s)", natsorted(pass_df.Player.unique()))
    player_df = pass_df[pass_df['Player'].isin(player)]
    

    matches = (player_df.MatchName.unique()).tolist()
    
    match = st.sidebar.multiselect("Select Match(es)", natsorted(player_df.MatchName.unique()), default=matches)
    match_df = player_df[player_df['MatchName'].isin(match)]


    st.header("Player PassSonar")  
    st.subheader("By xPR, By Length of Pass, Pass Map within Zone")    
    st.text("")

    
    def AdvPassSonar(match_df):
        Passes = match_df[match_df['ifSP'] != 1]
        def Pass(zone):
    
            #local_df = Pass.copy(deep=True)
            local_df = Passes[(Passes["Zone"]==zone)]
            #local_df['Angle'] = np.arctan2((local_df['DestY'] - local_df['Y']), (local_df['DestX'] - local_df['X']))
            local_df = pd.DataFrame(data=local_df, columns=['Angle', 'Length', 'ifPass', 'Player', 'Zone', 'ifComplete', 'xP'])
            local_df = local_df.dropna(axis=1, how="all")
    
            for i in range(25):
                local_df = local_df.append({'Angle': 0,'Length': 15,'ifPass': 0, 'Zone': i, 'ifComplete':0, 'xP':0}, ignore_index=True)
            
            df1 = local_df[['Angle','Length', 'ifPass', 'ifComplete', 'xP']].copy()
            
            bins = np.linspace(-np.pi,np.pi,24)
            df1['binned'] = pd.cut(local_df['Angle'], bins, include_lowest=True, right = True)
            df1["Bin"] = df1["binned"].apply(lambda x: x.mid)
            df1 = df1[:-1]
 
           
            A= df1.groupby("Bin", as_index=False)["ifComplete"].mean()
            A = df1.groupby('Bin', as_index=False).agg({'ifComplete': 'mean', 'ifPass' : 'sum', 'xP':'mean', 'Length':'mean'}) 
            A['xPR'] = A['ifComplete'] / A['xP']
            A = A.dropna(0)
            
            return A
        
      
        fig,ax = plt.subplots(figsize=(32,18))
        plt.title(str(season)+' - '+str(player)+" PassSonar Color by xPR", fontproperties=headers, color="black")
        norm = plt.Normalize(0.9, 1.1) 
        cmap = plt.cm.RdYlBu
        sm = mpl.cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])
        cbar = fig.colorbar(sm, orientation="horizontal", fraction=0.046, pad=0.04)
        cbar.ax.set_title('xPR', fontproperties=footers, color='black')
        
        def plot_inset(width, axis_main, data, x,y):
             ax_sub= inset_axes(axis_main, width=width, height=width, loc=10,
                               bbox_to_anchor=(x,y),
                               bbox_transform=axis_main.transData, 
                               borderpad=0.0, axes_class=get_projection_class("polar"))
             
             #passdata = Passes[(Passes['Player'].str.contains(player))]
             pasd = Passes.groupby("MatchID").agg({"Player": 'nunique'})
             mp = pasd.sum()
             totp = Passes.groupby("MatchID").agg({'ifPass':'sum'})
             tp = totp.max()
             
             theta = data["Bin"]
             radii = data["ifPass"]
             length = np.array(data["xPR"])
             #data['xPR'] = data['ifComplete'] / data['xP']
             cma = cmap(norm(length))
             bars = ax_sub.bar(theta, radii, width=.265, edgecolor='black', linewidth=1.5, bottom=0)
             ax_sub.set_xticklabels([])
             ax_sub.set_yticklabels([])
             #ax_sub.set_ylim(0,mp.sum()/1.75)
             ax_sub.set_ylim(0,tp.sum()/4.25)
             ax_sub.yaxis.grid(False)
             ax_sub.xaxis.grid(False)
             ax_sub.spines['polar'].set_visible(False)
             ax_sub.patch.set_facecolor("none")
             ax_sub.patch.set_alpha(0.1)
             for r,bar in zip(cma,bars):
                    bar.set_facecolor(r)
        def plotzones():
            plot_inset(2,ax, Pass(25), 94.5, 64)
            plot_inset(2, ax, Pass(24), 94.5, 49)
            plot_inset(2,ax, Pass(23), 94.5, 34)
            plot_inset(2, ax, Pass(22), 94.5, 20)
            plot_inset(2, ax, Pass(21), 94.5, 4)
            plot_inset(2,ax, Pass(20), 73.5, 64)
            plot_inset(2, ax, Pass(19), 73.5, 49)
            plot_inset(2,ax, Pass(18), 73.5, 34)
            plot_inset(2, ax, Pass(17), 73.5, 20)
            plot_inset(2, ax, Pass(16), 73.5, 4)
            plot_inset(2,ax, Pass(15), 52.5, 64)
            plot_inset(2, ax, Pass(14), 52.5, 49)
            plot_inset(2,ax, Pass(13), 52.5, 34)
            plot_inset(2, ax, Pass(12), 52.5, 20)
            plot_inset(2, ax, Pass(11), 52.5, 4)
            plot_inset(2,ax, Pass(10), 31.5, 64)
            plot_inset(2, ax, Pass(9), 31.5, 49)
            plot_inset(2,ax, Pass(8), 31.5, 34)
            plot_inset(2, ax, Pass(7), 31.5, 20)
            plot_inset(2, ax, Pass(6), 31.5, 4)
            plot_inset(2,ax, Pass(5), 10.5, 64)
            plot_inset(2, ax, Pass(4), 10.5, 49)
            plot_inset(2,ax, Pass(3), 10.5, 34)
            plot_inset(2, ax, Pass(2), 10.5, 20)
            plot_inset(2, ax, Pass(1), 10.5, 4)
        plotzones()
        
        def numbers():
            ax.annotate(25 ,xy=(94.5, 64), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(24 ,xy=(94.5, 49), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(23 ,xy=(94.5, 34), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(22 ,xy=(94.5, 20), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(21 ,xy=(94.5, 4), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(20 ,xy=(73.5, 64), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(19 ,xy=(73.5, 49), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(18 ,xy=(73.5, 34), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(17 ,xy=(73.5, 20), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(16 ,xy=(73.5, 4), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(15 ,xy=(52.5, 64), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(14 ,xy=(52.5, 49), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(13 ,xy=(52.5, 34), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(12 ,xy=(52.5, 20), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(11 ,xy=(52.5, 4), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(10 ,xy=(31.5, 64), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(9 ,xy=(31.5, 49), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(8 ,xy=(31.5, 34), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(7 ,xy=(31.5, 20), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(6 ,xy=(31.5, 4), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(5 ,xy=(10.5, 64), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(4 ,xy=(10.5, 49), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(3 ,xy=(10.5, 34), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(2 ,xy=(10.5, 20), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(1 ,xy=(10.5, 4), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
    
        numbers()
        
        zo=12
        def draw_pitch(pitch, line): 
        # side and goal lines #
            ly1 = [0,0,68,68,0]
            lx1 = [0,105,105,0,0]
            
            ax.plot(lx1,ly1,color=line,zorder=5)
            
            
            # boxes, 6 yard box and goals
            
                #outer boxes#
            ly2 = [15.3,15.3,52.7,52.7] 
            lx2 = [105,89.25,89.25,105]
            ax.plot(lx2,ly2,color=line,zorder=5)
            
            ly3 = [15.3,15.3,52.7,52.7]  
            lx3 = [0,15.75,15.75,0]
            ax.plot(lx3,ly3,color=line,zorder=5)
            
                #goals#
            ly4 = [30.6,30.6,37.4,37.4]
            lx4 = [105,105.2,105.2,105]
            ax.plot(lx4,ly4,color=line,zorder=5)
            
            ly5 = [30.6,30.6,37.4,37.4]
            lx5 = [0,-0.2,-0.2,0]
            ax.plot(lx5,ly5,color=line,zorder=5)
            
            
               #6 yard boxes#
            ly6 = [25.5,25.5,42.5,42.5]
            lx6 = [105,99.75,99.75,105]
            ax.plot(lx6,ly6,color=line,zorder=5)
            
            ly7 = [25.5,25.5,42.5,42.5]
            lx7 = [0,5.25,5.25,0]
            ax.plot(lx7,ly7,color=line,zorder=5)
            
            #Halfway line, penalty spots, and kickoff spot
            ly8 = [0,68] 
            lx8 = [52.5,52.5]
            ax.plot(lx8,ly8,color=line,zorder=5)
            
            
            ax.scatter(94.5,34,color=line,zorder=5, s=12)
            ax.scatter(10.5,34,color=line,zorder=5, s=12)
            ax.scatter(52.5,34,color=line,zorder=5, s=12)
            
            arc1 =  Arc((95.25,34),height=18.3,width=18.3,angle=0,theta1=130,theta2=230,color=line,zorder=zo+1)
            arc2 = Arc((9.75,34),height=18.3,width=18.3,angle=0,theta1=310,theta2=50,color=line,zorder=zo+1)
            circle1 = plt.Circle((52.5, 34), 9.15,ls='solid',lw=1.5,color=line, fill=False, zorder=2,alpha=1)
            
            ## Rectangles in boxes
            rec1 = plt.Rectangle((89.25,20), 16,30,ls='-',color=pitch, zorder=1,alpha=1)
            rec2 = plt.Rectangle((0, 20), 16.5,30,ls='-',color=pitch, zorder=1,alpha=1)
            
            ## Pitch rectangle
            rec3 = plt.Rectangle((-0.5, -0.5), 106,69,ls='-',color=pitch, zorder=1,alpha=1)
            
            ## Add Direction of Play Arrow
            DoP = ax.arrow(1.5, 1.5, 18-2, 1-1, head_width=1.2,
                head_length=1.2,
                color=line,
                alpha=1,
                length_includes_head=True, zorder=12, width=.3)
            
            ax.add_artist(rec3)
            ax.add_artist(arc1)
            ax.add_artist(arc2)
            ax.add_artist(rec1)
            ax.add_artist(rec2)
            ax.add_artist(circle1)
            ax.add_artist(DoP)
            ax.axis('off')
        draw_pitch('#B2B2B2', 'black')
        ax.annotate('Bar Length =  # of Passes',xy=(95, 1), fontproperties=Annotate, color="black", ha="center", zorder=zo)
        #ax.annotate('Wider Bar = Completing to Expectation',xy=(10, 68.5),fontproperties=Labels, color="black", ha="center", zorder=zo)
    AdvPassSonar(match_df)
    st.pyplot()
    
    def BasicPassSonar(match_df):
        Passes = match_df[match_df['ifSP'] != 1]
        def Pass(zone):
    
            #local_df = Pass.copy(deep=True)
            local_df = Passes[(Passes["Zone"]==zone)]
            #local_df['Angle'] = np.arctan2((local_df['DestY'] - local_df['Y']), (local_df['DestX'] - local_df['X']))
            local_df = pd.DataFrame(data=local_df, columns=['Angle', 'Length', 'ifPass', 'Player', 'Zone', 'ifComplete', 'xP'])
            local_df = local_df.dropna(axis=1, how="all")
    
            for i in range(25):
                local_df = local_df.append({'Angle': 0,'Length': 15,'ifPass': 0, 'Zone': i, 'ifComplete':0, 'xP':0}, ignore_index=True)
            
            df1 = local_df[['Angle','Length', 'ifPass']].copy()
            
            bins = np.linspace(-np.pi,np.pi,24)
            df1['binned'] = pd.cut(local_df['Angle'], bins, include_lowest=True, right = True)
            df1["Bin"] = df1["binned"].apply(lambda x: x.mid)
            df1 = df1[:-1]
 
            A= df1.groupby("Bin", as_index=False)["Length"].mean()
            A = df1.groupby('Bin', as_index=False).agg({'ifPass' : 'sum', 'Length':'mean'}) 
            A = A.dropna(0)
            
            return A
        
      
        fig,ax = plt.subplots(figsize=(32,18))
        plt.title(str(season)+' - '+str(player)+" PassSonar Color by Length", fontproperties=headers, color="black")
        norm = plt.Normalize(0, 35) 
        cmap = plt.cm.RdYlBu_r
        sm = mpl.cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])
        cbar = fig.colorbar(sm, orientation="horizontal", fraction=0.046, pad=0.04)
        cbar.ax.set_title('Mean Pass Length', fontproperties=footers, color='black')
        
        def plot_inset(width, axis_main, data, x,y):
             ax_sub= inset_axes(axis_main, width=width, height=width, loc=10,
                               bbox_to_anchor=(x,y),
                               bbox_transform=axis_main.transData, 
                               borderpad=0.0, axes_class=get_projection_class("polar"))
             
             #passdata = Passes[(Passes['Player'].str.contains(player))]
             pasd = Passes.groupby("MatchID").agg({"Player": 'nunique'})
             mp = pasd.sum()
             totp = Passes.groupby("MatchID").agg({'ifPass':'sum'})
             tp = totp.max()
             
             theta = data["Bin"]
             radii = data["ifPass"]
             length = np.array(data["Length"])
             #data['xPR'] = data['ifComplete'] / data['xP']
             cma = cmap(norm(length))
             bars = ax_sub.bar(theta, radii, width=.265, edgecolor='black', linewidth=1.5, bottom=0)
             ax_sub.set_xticklabels([])
             ax_sub.set_yticklabels([])
             #ax_sub.set_ylim(0,mp.sum()/1.75)
             ax_sub.set_ylim(0,tp.sum()/4.25)
             ax_sub.yaxis.grid(False)
             ax_sub.xaxis.grid(False)
             ax_sub.spines['polar'].set_visible(False)
             ax_sub.patch.set_facecolor("none")
             ax_sub.patch.set_alpha(0.1)
             for r,bar in zip(cma,bars):
                    bar.set_facecolor(r)
        def plotzones():
            plot_inset(2,ax, Pass(25), 94.5, 64)
            plot_inset(2, ax, Pass(24), 94.5, 49)
            plot_inset(2,ax, Pass(23), 94.5, 34)
            plot_inset(2, ax, Pass(22), 94.5, 20)
            plot_inset(2, ax, Pass(21), 94.5, 4)
            plot_inset(2,ax, Pass(20), 73.5, 64)
            plot_inset(2, ax, Pass(19), 73.5, 49)
            plot_inset(2,ax, Pass(18), 73.5, 34)
            plot_inset(2, ax, Pass(17), 73.5, 20)
            plot_inset(2, ax, Pass(16), 73.5, 4)
            plot_inset(2,ax, Pass(15), 52.5, 64)
            plot_inset(2, ax, Pass(14), 52.5, 49)
            plot_inset(2,ax, Pass(13), 52.5, 34)
            plot_inset(2, ax, Pass(12), 52.5, 20)
            plot_inset(2, ax, Pass(11), 52.5, 4)
            plot_inset(2,ax, Pass(10), 31.5, 64)
            plot_inset(2, ax, Pass(9), 31.5, 49)
            plot_inset(2,ax, Pass(8), 31.5, 34)
            plot_inset(2, ax, Pass(7), 31.5, 20)
            plot_inset(2, ax, Pass(6), 31.5, 4)
            plot_inset(2,ax, Pass(5), 10.5, 64)
            plot_inset(2, ax, Pass(4), 10.5, 49)
            plot_inset(2,ax, Pass(3), 10.5, 34)
            plot_inset(2, ax, Pass(2), 10.5, 20)
            plot_inset(2, ax, Pass(1), 10.5, 4)
        plotzones()
        
        def numbers():
            ax.annotate(25 ,xy=(94.5, 64), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(24 ,xy=(94.5, 49), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(23 ,xy=(94.5, 34), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(22 ,xy=(94.5, 20), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(21 ,xy=(94.5, 4), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(20 ,xy=(73.5, 64), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(19 ,xy=(73.5, 49), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(18 ,xy=(73.5, 34), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(17 ,xy=(73.5, 20), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(16 ,xy=(73.5, 4), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(15 ,xy=(52.5, 64), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(14 ,xy=(52.5, 49), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(13 ,xy=(52.5, 34), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(12 ,xy=(52.5, 20), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(11 ,xy=(52.5, 4), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(10 ,xy=(31.5, 64), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(9 ,xy=(31.5, 49), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(8 ,xy=(31.5, 34), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(7 ,xy=(31.5, 20), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(6 ,xy=(31.5, 4), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(5 ,xy=(10.5, 64), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(4 ,xy=(10.5, 49), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(3 ,xy=(10.5, 34), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(2 ,xy=(10.5, 20), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(1 ,xy=(10.5, 4), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
    
        numbers()
        
        zo=12
        def draw_pitch(pitch, line): 
        # side and goal lines #
            ly1 = [0,0,68,68,0]
            lx1 = [0,105,105,0,0]
            
            ax.plot(lx1,ly1,color=line,zorder=5)
            
            
            # boxes, 6 yard box and goals
            
                #outer boxes#
            ly2 = [15.3,15.3,52.7,52.7] 
            lx2 = [105,89.25,89.25,105]
            ax.plot(lx2,ly2,color=line,zorder=5)
            
            ly3 = [15.3,15.3,52.7,52.7]  
            lx3 = [0,15.75,15.75,0]
            ax.plot(lx3,ly3,color=line,zorder=5)
            
                #goals#
            ly4 = [30.6,30.6,37.4,37.4]
            lx4 = [105,105.2,105.2,105]
            ax.plot(lx4,ly4,color=line,zorder=5)
            
            ly5 = [30.6,30.6,37.4,37.4]
            lx5 = [0,-0.2,-0.2,0]
            ax.plot(lx5,ly5,color=line,zorder=5)
            
            
               #6 yard boxes#
            ly6 = [25.5,25.5,42.5,42.5]
            lx6 = [105,99.75,99.75,105]
            ax.plot(lx6,ly6,color=line,zorder=5)
            
            ly7 = [25.5,25.5,42.5,42.5]
            lx7 = [0,5.25,5.25,0]
            ax.plot(lx7,ly7,color=line,zorder=5)
            
            #Halfway line, penalty spots, and kickoff spot
            ly8 = [0,68] 
            lx8 = [52.5,52.5]
            ax.plot(lx8,ly8,color=line,zorder=5)
            
            
            ax.scatter(94.5,34,color=line,zorder=5, s=12)
            ax.scatter(10.5,34,color=line,zorder=5, s=12)
            ax.scatter(52.5,34,color=line,zorder=5, s=12)
            
            arc1 =  Arc((95.25,34),height=18.3,width=18.3,angle=0,theta1=130,theta2=230,color=line,zorder=zo+1)
            arc2 = Arc((9.75,34),height=18.3,width=18.3,angle=0,theta1=310,theta2=50,color=line,zorder=zo+1)
            circle1 = plt.Circle((52.5, 34), 9.15,ls='solid',lw=1.5,color=line, fill=False, zorder=2,alpha=1)
            
            ## Rectangles in boxes
            rec1 = plt.Rectangle((89.25,20), 16,30,ls='-',color=pitch, zorder=1,alpha=1)
            rec2 = plt.Rectangle((0, 20), 16.5,30,ls='-',color=pitch, zorder=1,alpha=1)
            
            ## Pitch rectangle
            rec3 = plt.Rectangle((-0.5, -0.5), 106,69,ls='-',color=pitch, zorder=1,alpha=1)
            
            ## Add Direction of Play Arrow
            DoP = ax.arrow(1.5, 1.5, 18-2, 1-1, head_width=1.2,
                head_length=1.2,
                color=line,
                alpha=1,
                length_includes_head=True, zorder=12, width=.3)
            
            ax.add_artist(rec3)
            ax.add_artist(arc1)
            ax.add_artist(arc2)
            ax.add_artist(rec1)
            ax.add_artist(rec2)
            ax.add_artist(circle1)
            ax.add_artist(DoP)
            ax.axis('off')
        draw_pitch('#B2B2B2', 'black')
        ax.annotate('Bar Length =  # of Passes',xy=(95, 1), fontproperties=Annotate, color="black", ha="center", zorder=zo)
    BasicPassSonar(match_df)
    st.pyplot()
    
    
    zone = st.sidebar.multiselect('Select Zone', natsorted(match_df.Zone.unique()))  
    zone_df = match_df[match_df['Zone'].isin(zone)]


    retain = zone_df[(zone_df['ifRetain'] == 1) & (zone_df['ifSP'] != 1)]
    incornret = zone_df[(zone_df['ifRetain'] != 1) & (zone_df['ifSP'] != 1)]


    xS = retain["X"]
    yS = retain["Y"]
    xE = retain["DestX"]
    yE = retain["DestY"]
    xS1 = incornret["X"]
    yS1 = incornret["Y"]
    xE1 = incornret["DestX"]
    yE1 = incornret["DestY"]
    xP = player_df['xP']

    draw_pitch('none', 'black', 'horizontal', 'full')
   
    for i in range(len(retain)):
        plt.arrow(xS.iloc[i], yS.iloc[i],  xE.iloc[i]-xS.iloc[i], (yE.iloc[i])-(yS.iloc[i]),  width=xP.iloc[i], head_width=xP.iloc[i]*2,
           head_length=xP.iloc[i]*2,
           color='lime',
           alpha=1,
           length_includes_head=True, zorder=zo)
    for i in range(len(incornret)):
        plt.arrow(xS1.iloc[i], yS1.iloc[i],  xE1.iloc[i]-xS1.iloc[i], (yE1.iloc[i])-(yS1.iloc[i]),  width=xP.iloc[i], head_width=xP.iloc[i]*2,
           head_length=xP.iloc[i]*2,
           color="dodgerblue" if incornret.iloc[i]["ifComplete"] == 1
           else "red", alpha=1,length_includes_head=True, zorder=zo)

    plt.title(str(season)+' - '+str(player)+" Passes in Zone "+str(zone), fontproperties=headers, color="black")
    #plt.annotate(str(round(sum(pass_data.PP),2))+" Progressive Passes",color="white", xy=(44, -2), size = 10, ha="center", weight="bold", zorder=zo)
    #plt.annotate(str(round(sum(pass_data.DP),2))+" Deep Progressions",color="white", xy=(44, -4), size = 10, ha="center", weight="bold", zorder=zo)
    #plt.annotate(str(round(sum(pass_data.xP),2))+" xP",color="white", xy=(24, -2), size = 10, ha="center", weight="bold", zorder=zo)
    #plt.annotate(str(round(sum(pass_data.ifComplete),))+' / '+str(round(sum(pass_data.PassesAttempted),))+" Passes",color="white", xy=(24, -4), size = 10, ha="center", weight="bold", zorder=zo)     
    #plt.annotate("Bigger Arrow  = Higher xP",color="white", xy=(6, 107.5), size = 10, ha="center", weight="bold", zorder=zo)              
    plt.plot(-2,color="lime",label="Retain",zorder=0)
    plt.plot(-2,color="dodgerblue",label="Complete",zorder=0)
    plt.plot(-2,color="red",label="Incomplete",zorder=0)
    #plt.plot(-2,color="gold",label="Assist",zorder=0)
    leg = plt.legend(loc=0, ncol=3,frameon=False)
    plt.setp(leg.get_texts(), color='black', fontproperties=Labels)
    st.pyplot()
    
def TeamPassSonar(state):    
    sm_df = load_sm_data()
    
    team = st.sidebar.multiselect('Select Team(s)', natsorted(sm_df.Team.unique()))
    sm_df = sm_df[sm_df['Team'].isin(team)]
    
    
    season = st.sidebar.multiselect('Select Season(s)',natsorted(sm_df.Season.unique()))  
    sm_df = sm_df[sm_df['Season'].isin(season)]
    
    pass_df = load_pass_data(season, team, 'no')
        

    matches = (pass_df.MatchName.unique()).tolist()
    
    match = st.sidebar.multiselect("Select Match(es)", natsorted(pass_df.MatchName.unique()), default=matches)
    match_df = pass_df[pass_df['MatchName'].isin(match)]


    st.header("Team PassSonar")  
    st.subheader("By xPR, By Length of Pass, Pass Map within Zone")    
    st.text("")

    
    def AdvPassSonar(match_df):
        Passes = match_df[match_df['ifSP'] != 1]
        def Pass(zone):
    
            #local_df = Pass.copy(deep=True)
            local_df = Passes[(Passes["Zone"]==zone)]
            #local_df['Angle'] = np.arctan2((local_df['DestY'] - local_df['Y']), (local_df['DestX'] - local_df['X']))
            local_df = pd.DataFrame(data=local_df, columns=['Angle', 'Length', 'ifPass', 'Team', 'Zone', 'ifComplete', 'xP'])
            local_df = local_df.dropna(axis=1, how="all")
    
            for i in range(25):
                local_df = local_df.append({'Angle': 0,'Length': 15,'ifPass': 0, 'Zone': i, 'ifComplete':0, 'xP':0}, ignore_index=True)
            
            df1 = local_df[['Angle','Length', 'ifPass', 'ifComplete', 'xP']].copy()
            
            bins = np.linspace(-np.pi,np.pi,24)
            df1['binned'] = pd.cut(local_df['Angle'], bins, include_lowest=True, right = True)
            df1["Bin"] = df1["binned"].apply(lambda x: x.mid)
            df1 = df1[:-1]
 
           
            A= df1.groupby("Bin", as_index=False)["ifComplete"].mean()
            A = df1.groupby('Bin', as_index=False).agg({'ifComplete': 'mean', 'ifPass' : 'sum', 'xP':'mean', 'Length':'mean'}) 
            A['xPR'] = A['ifComplete'] / A['xP']
            A = A.dropna(0)
            
            return A
        
      
        fig,ax = plt.subplots(figsize=(32,18))
        plt.title(str(season)+' - '+str(team)+" PassSonar Color by xPR", fontproperties=headers, color="black")
        norm = plt.Normalize(0.9, 1.1) 
        cmap = plt.cm.RdYlBu
        sm = mpl.cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])
        cbar = fig.colorbar(sm, orientation="horizontal", fraction=0.046, pad=0.04)
        cbar.ax.set_title('xPR', fontproperties=footers, color='black')
        
        def plot_inset(width, axis_main, data, x,y):
             ax_sub= inset_axes(axis_main, width=width, height=width, loc=10,
                               bbox_to_anchor=(x,y),
                               bbox_transform=axis_main.transData, 
                               borderpad=0.0, axes_class=get_projection_class("polar"))
             
             #passdata = Passes[(Passes['Player'].str.contains(player))]
             pasd = Passes.groupby("MatchID").agg({"Team": 'nunique'})
             mp = pasd.sum()
             totp = Passes.groupby("MatchID").agg({'ifPass':'sum'})
             tp = totp.max()

             
             theta = data["Bin"]
             radii = data["ifPass"]
             length = np.array(data["xPR"])
             #data['xPR'] = data['ifComplete'] / data['xP']
             cma = cmap(norm(length))
             bars = ax_sub.bar(theta, radii, width=.265, edgecolor='black', linewidth=1.5, bottom=0)
             ax_sub.set_xticklabels([])
             ax_sub.set_yticklabels([])
             #ax_sub.set_ylim(0,mp.sum()*3.5)
             ax_sub.set_ylim(0,tp.sum()/50)
             ax_sub.yaxis.grid(False)
             ax_sub.xaxis.grid(False)
             ax_sub.spines['polar'].set_visible(False)
             ax_sub.patch.set_facecolor("none")
             ax_sub.patch.set_alpha(0.1)
             for r,bar in zip(cma,bars):
                    bar.set_facecolor(r)
        def plotzones():
            plot_inset(2,ax, Pass(25), 94.5, 64)
            plot_inset(2, ax, Pass(24), 94.5, 49)
            plot_inset(2,ax, Pass(23), 94.5, 34)
            plot_inset(2, ax, Pass(22), 94.5, 20)
            plot_inset(2, ax, Pass(21), 94.5, 4)
            plot_inset(2,ax, Pass(20), 73.5, 64)
            plot_inset(2, ax, Pass(19), 73.5, 49)
            plot_inset(2,ax, Pass(18), 73.5, 34)
            plot_inset(2, ax, Pass(17), 73.5, 20)
            plot_inset(2, ax, Pass(16), 73.5, 4)
            plot_inset(2,ax, Pass(15), 52.5, 64)
            plot_inset(2, ax, Pass(14), 52.5, 49)
            plot_inset(2,ax, Pass(13), 52.5, 34)
            plot_inset(2, ax, Pass(12), 52.5, 20)
            plot_inset(2, ax, Pass(11), 52.5, 4)
            plot_inset(2,ax, Pass(10), 31.5, 64)
            plot_inset(2, ax, Pass(9), 31.5, 49)
            plot_inset(2,ax, Pass(8), 31.5, 34)
            plot_inset(2, ax, Pass(7), 31.5, 20)
            plot_inset(2, ax, Pass(6), 31.5, 4)
            plot_inset(2,ax, Pass(5), 10.5, 64)
            plot_inset(2, ax, Pass(4), 10.5, 49)
            plot_inset(2,ax, Pass(3), 10.5, 34)
            plot_inset(2, ax, Pass(2), 10.5, 20)
            plot_inset(2, ax, Pass(1), 10.5, 4)
        plotzones()
        
        def numbers():
            ax.annotate(25 ,xy=(94.5, 64), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(24 ,xy=(94.5, 49), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(23 ,xy=(94.5, 34), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(22 ,xy=(94.5, 20), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(21 ,xy=(94.5, 4), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(20 ,xy=(73.5, 64), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(19 ,xy=(73.5, 49), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(18 ,xy=(73.5, 34), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(17 ,xy=(73.5, 20), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(16 ,xy=(73.5, 4), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(15 ,xy=(52.5, 64), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(14 ,xy=(52.5, 49), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(13 ,xy=(52.5, 34), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(12 ,xy=(52.5, 20), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(11 ,xy=(52.5, 4), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(10 ,xy=(31.5, 64), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(9 ,xy=(31.5, 49), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(8 ,xy=(31.5, 34), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(7 ,xy=(31.5, 20), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(6 ,xy=(31.5, 4), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(5 ,xy=(10.5, 64), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(4 ,xy=(10.5, 49), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(3 ,xy=(10.5, 34), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(2 ,xy=(10.5, 20), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(1 ,xy=(10.5, 4), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
    
        numbers()
        
        zo=12
        def draw_pitch(pitch, line): 
        # side and goal lines #
            ly1 = [0,0,68,68,0]
            lx1 = [0,105,105,0,0]
            
            ax.plot(lx1,ly1,color=line,zorder=5)
            
            
            # boxes, 6 yard box and goals
            
                #outer boxes#
            ly2 = [15.3,15.3,52.7,52.7] 
            lx2 = [105,89.25,89.25,105]
            ax.plot(lx2,ly2,color=line,zorder=5)
            
            ly3 = [15.3,15.3,52.7,52.7]  
            lx3 = [0,15.75,15.75,0]
            ax.plot(lx3,ly3,color=line,zorder=5)
            
                #goals#
            ly4 = [30.6,30.6,37.4,37.4]
            lx4 = [105,105.2,105.2,105]
            ax.plot(lx4,ly4,color=line,zorder=5)
            
            ly5 = [30.6,30.6,37.4,37.4]
            lx5 = [0,-0.2,-0.2,0]
            ax.plot(lx5,ly5,color=line,zorder=5)
            
            
               #6 yard boxes#
            ly6 = [25.5,25.5,42.5,42.5]
            lx6 = [105,99.75,99.75,105]
            ax.plot(lx6,ly6,color=line,zorder=5)
            
            ly7 = [25.5,25.5,42.5,42.5]
            lx7 = [0,5.25,5.25,0]
            ax.plot(lx7,ly7,color=line,zorder=5)
            
            #Halfway line, penalty spots, and kickoff spot
            ly8 = [0,68] 
            lx8 = [52.5,52.5]
            ax.plot(lx8,ly8,color=line,zorder=5)
            
            
            ax.scatter(94.5,34,color=line,zorder=5, s=12)
            ax.scatter(10.5,34,color=line,zorder=5, s=12)
            ax.scatter(52.5,34,color=line,zorder=5, s=12)
            
            arc1 =  Arc((95.25,34),height=18.3,width=18.3,angle=0,theta1=130,theta2=230,color=line,zorder=zo+1)
            arc2 = Arc((9.75,34),height=18.3,width=18.3,angle=0,theta1=310,theta2=50,color=line,zorder=zo+1)
            circle1 = plt.Circle((52.5, 34), 9.15,ls='solid',lw=1.5,color=line, fill=False, zorder=2,alpha=1)
            
            ## Rectangles in boxes
            rec1 = plt.Rectangle((89.25,20), 16,30,ls='-',color=pitch, zorder=1,alpha=1)
            rec2 = plt.Rectangle((0, 20), 16.5,30,ls='-',color=pitch, zorder=1,alpha=1)
            
            ## Pitch rectangle
            rec3 = plt.Rectangle((-0.5, -0.5), 106,69,ls='-',color=pitch, zorder=1,alpha=1)
            
            ## Add Direction of Play Arrow
            DoP = ax.arrow(1.5, 1.5, 18-2, 1-1, head_width=1.2,
                head_length=1.2,
                color=line,
                alpha=1,
                length_includes_head=True, zorder=12, width=.3)
            
            ax.add_artist(rec3)
            ax.add_artist(arc1)
            ax.add_artist(arc2)
            ax.add_artist(rec1)
            ax.add_artist(rec2)
            ax.add_artist(circle1)
            ax.add_artist(DoP)
            ax.axis('off')
        draw_pitch('#B2B2B2', 'black')
        ax.annotate('Bar Length =  # of Passes',xy=(95, 1), fontproperties=Annotate, color="black", ha="center", zorder=zo)
        #ax.annotate('Wider Bar = Completing to Expectation',xy=(10, 68.5),fontproperties=Labels, color="black", ha="center", zorder=zo)
    AdvPassSonar(match_df)
    st.pyplot()
    
    def BasicPassSonar(match_df):
        Passes = match_df[match_df['ifSP'] != 1]
        def Pass(zone):
    
            #local_df = Pass.copy(deep=True)
            local_df = Passes[(Passes["Zone"]==zone)]
            #local_df['Angle'] = np.arctan2((local_df['DestY'] - local_df['Y']), (local_df['DestX'] - local_df['X']))
            local_df = pd.DataFrame(data=local_df, columns=['Angle', 'Length', 'ifPass', 'Team', 'Zone', 'ifComplete', 'xP'])
            local_df = local_df.dropna(axis=1, how="all")
    
            for i in range(25):
                local_df = local_df.append({'Angle': 0,'Length': 15,'ifPass': 0, 'Zone': i, 'ifComplete':0, 'xP':0}, ignore_index=True)
            
            df1 = local_df[['Angle','Length', 'ifPass']].copy()
            
            bins = np.linspace(-np.pi,np.pi,24)
            df1['binned'] = pd.cut(local_df['Angle'], bins, include_lowest=True, right = True)
            df1["Bin"] = df1["binned"].apply(lambda x: x.mid)
            df1 = df1[:-1]
 
            A= df1.groupby("Bin", as_index=False)["Length"].mean()
            A = df1.groupby('Bin', as_index=False).agg({'ifPass' : 'sum', 'Length':'mean'}) 
            A = A.dropna(0)
            
            return A
        
      
        fig,ax = plt.subplots(figsize=(32,18))
        plt.title(str(season)+' - '+str(team)+" PassSonar Color by Length", fontproperties=headers, color="black")
        norm = plt.Normalize(0, 35) 
        cmap = plt.cm.RdYlBu_r
        sm = mpl.cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])
        cbar = fig.colorbar(sm, orientation="horizontal", fraction=0.046, pad=0.04)
        cbar.ax.set_title('Mean Pass Length', fontproperties=footers, color='black')
        
        def plot_inset(width, axis_main, data, x,y):
             ax_sub= inset_axes(axis_main, width=width, height=width, loc=10,
                               bbox_to_anchor=(x,y),
                               bbox_transform=axis_main.transData, 
                               borderpad=0.0, axes_class=get_projection_class("polar"))
             
             #passdata = Passes[(Passes['Player'].str.contains(player))]
             pasd = Passes.groupby("MatchID").agg({"Team": 'nunique'})
             mp = pasd.sum()
             totp = Passes.groupby("MatchID").agg({'ifPass':'sum'})
             tp = totp.max()

             
             theta = data["Bin"]
             radii = data["ifPass"]
             length = np.array(data["Length"])
             #data['xPR'] = data['ifComplete'] / data['xP']
             cma = cmap(norm(length))
             bars = ax_sub.bar(theta, radii, width=.265, edgecolor='black', linewidth=1.5, bottom=0)
             ax_sub.set_xticklabels([])
             ax_sub.set_yticklabels([])
             #ax_sub.set_ylim(0,mp.sum()*3.5)
             ax_sub.set_ylim(0,tp.sum()/50)
             ax_sub.yaxis.grid(False)
             ax_sub.xaxis.grid(False)
             ax_sub.spines['polar'].set_visible(False)
             ax_sub.patch.set_facecolor("none")
             ax_sub.patch.set_alpha(0.1)
             for r,bar in zip(cma,bars):
                    bar.set_facecolor(r)
        def plotzones():
            plot_inset(2,ax, Pass(25), 94.5, 64)
            plot_inset(2, ax, Pass(24), 94.5, 49)
            plot_inset(2,ax, Pass(23), 94.5, 34)
            plot_inset(2, ax, Pass(22), 94.5, 20)
            plot_inset(2, ax, Pass(21), 94.5, 4)
            plot_inset(2,ax, Pass(20), 73.5, 64)
            plot_inset(2, ax, Pass(19), 73.5, 49)
            plot_inset(2,ax, Pass(18), 73.5, 34)
            plot_inset(2, ax, Pass(17), 73.5, 20)
            plot_inset(2, ax, Pass(16), 73.5, 4)
            plot_inset(2,ax, Pass(15), 52.5, 64)
            plot_inset(2, ax, Pass(14), 52.5, 49)
            plot_inset(2,ax, Pass(13), 52.5, 34)
            plot_inset(2, ax, Pass(12), 52.5, 20)
            plot_inset(2, ax, Pass(11), 52.5, 4)
            plot_inset(2,ax, Pass(10), 31.5, 64)
            plot_inset(2, ax, Pass(9), 31.5, 49)
            plot_inset(2,ax, Pass(8), 31.5, 34)
            plot_inset(2, ax, Pass(7), 31.5, 20)
            plot_inset(2, ax, Pass(6), 31.5, 4)
            plot_inset(2,ax, Pass(5), 10.5, 64)
            plot_inset(2, ax, Pass(4), 10.5, 49)
            plot_inset(2,ax, Pass(3), 10.5, 34)
            plot_inset(2, ax, Pass(2), 10.5, 20)
            plot_inset(2, ax, Pass(1), 10.5, 4)
        plotzones()
        
        def numbers():
            ax.annotate(25 ,xy=(94.5, 64), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(24 ,xy=(94.5, 49), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(23 ,xy=(94.5, 34), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(22 ,xy=(94.5, 20), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(21 ,xy=(94.5, 4), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(20 ,xy=(73.5, 64), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(19 ,xy=(73.5, 49), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(18 ,xy=(73.5, 34), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(17 ,xy=(73.5, 20), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(16 ,xy=(73.5, 4), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(15 ,xy=(52.5, 64), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(14 ,xy=(52.5, 49), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(13 ,xy=(52.5, 34), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(12 ,xy=(52.5, 20), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(11 ,xy=(52.5, 4), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(10 ,xy=(31.5, 64), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(9 ,xy=(31.5, 49), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(8 ,xy=(31.5, 34), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(7 ,xy=(31.5, 20), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(6 ,xy=(31.5, 4), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(5 ,xy=(10.5, 64), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(4 ,xy=(10.5, 49), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(3 ,xy=(10.5, 34), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(2 ,xy=(10.5, 20), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
            ax.annotate(1 ,xy=(10.5, 4), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
    
        numbers()
        
        zo=12
        def draw_pitch(pitch, line): 
        # side and goal lines #
            ly1 = [0,0,68,68,0]
            lx1 = [0,105,105,0,0]
            
            ax.plot(lx1,ly1,color=line,zorder=5)
            
            
            # boxes, 6 yard box and goals
            
                #outer boxes#
            ly2 = [15.3,15.3,52.7,52.7] 
            lx2 = [105,89.25,89.25,105]
            ax.plot(lx2,ly2,color=line,zorder=5)
            
            ly3 = [15.3,15.3,52.7,52.7]  
            lx3 = [0,15.75,15.75,0]
            ax.plot(lx3,ly3,color=line,zorder=5)
            
                #goals#
            ly4 = [30.6,30.6,37.4,37.4]
            lx4 = [105,105.2,105.2,105]
            ax.plot(lx4,ly4,color=line,zorder=5)
            
            ly5 = [30.6,30.6,37.4,37.4]
            lx5 = [0,-0.2,-0.2,0]
            ax.plot(lx5,ly5,color=line,zorder=5)
            
            
               #6 yard boxes#
            ly6 = [25.5,25.5,42.5,42.5]
            lx6 = [105,99.75,99.75,105]
            ax.plot(lx6,ly6,color=line,zorder=5)
            
            ly7 = [25.5,25.5,42.5,42.5]
            lx7 = [0,5.25,5.25,0]
            ax.plot(lx7,ly7,color=line,zorder=5)
            
            #Halfway line, penalty spots, and kickoff spot
            ly8 = [0,68] 
            lx8 = [52.5,52.5]
            ax.plot(lx8,ly8,color=line,zorder=5)
            
            
            ax.scatter(94.5,34,color=line,zorder=5, s=12)
            ax.scatter(10.5,34,color=line,zorder=5, s=12)
            ax.scatter(52.5,34,color=line,zorder=5, s=12)
            
            arc1 =  Arc((95.25,34),height=18.3,width=18.3,angle=0,theta1=130,theta2=230,color=line,zorder=zo+1)
            arc2 = Arc((9.75,34),height=18.3,width=18.3,angle=0,theta1=310,theta2=50,color=line,zorder=zo+1)
            circle1 = plt.Circle((52.5, 34), 9.15,ls='solid',lw=1.5,color=line, fill=False, zorder=2,alpha=1)
            
            ## Rectangles in boxes
            rec1 = plt.Rectangle((89.25,20), 16,30,ls='-',color=pitch, zorder=1,alpha=1)
            rec2 = plt.Rectangle((0, 20), 16.5,30,ls='-',color=pitch, zorder=1,alpha=1)
            
            ## Pitch rectangle
            rec3 = plt.Rectangle((-0.5, -0.5), 106,69,ls='-',color=pitch, zorder=1,alpha=1)
            
            ## Add Direction of Play Arrow
            DoP = ax.arrow(1.5, 1.5, 18-2, 1-1, head_width=1.2,
                head_length=1.2,
                color=line,
                alpha=1,
                length_includes_head=True, zorder=12, width=.3)
            
            ax.add_artist(rec3)
            ax.add_artist(arc1)
            ax.add_artist(arc2)
            ax.add_artist(rec1)
            ax.add_artist(rec2)
            ax.add_artist(circle1)
            ax.add_artist(DoP)
            ax.axis('off')
        draw_pitch('#B2B2B2', 'black')
        ax.annotate('Bar Length =  # of Passes',xy=(95, 1), fontproperties=Annotate, color="black", ha="center", zorder=zo)
    BasicPassSonar(match_df)
    st.pyplot()
    
    
    zone = st.sidebar.multiselect('Select Zone', natsorted(match_df.Zone.unique()))
    zone_df = match_df[match_df['Zone'].isin(zone)]


    retain = zone_df[(zone_df['ifRetain'] == 1) & (zone_df['ifSP'] != 1)]
    incornret = zone_df[(zone_df['ifRetain'] != 1) & (zone_df['ifSP'] != 1)]


    xS = retain["X"]
    yS = retain["Y"]
    xE = retain["DestX"]
    yE = retain["DestY"]
    xS1 = incornret["X"]
    yS1 = incornret["Y"]
    xE1 = incornret["DestX"]
    yE1 = incornret["DestY"]
    xP = match_df['xP']

    draw_pitch('none', 'black', 'horizontal', 'full')
   
    for i in range(len(retain)):
        plt.arrow(xS.iloc[i], yS.iloc[i],  xE.iloc[i]-xS.iloc[i], (yE.iloc[i])-(yS.iloc[i]),  width=xP.iloc[i], head_width=xP.iloc[i]*2,
           head_length=xP.iloc[i]*2,
           color='lime',
           alpha=1,
           length_includes_head=True, zorder=zo)
    for i in range(len(incornret)):
        plt.arrow(xS1.iloc[i], yS1.iloc[i],  xE1.iloc[i]-xS1.iloc[i], (yE1.iloc[i])-(yS1.iloc[i]),  width=xP.iloc[i], head_width=xP.iloc[i]*2,
           head_length=xP.iloc[i]*2,
           color="dodgerblue" if incornret.iloc[i]["ifComplete"] == 1
           else "red", alpha=1,length_includes_head=True, zorder=zo)

    plt.title(str(season)+' - '+str(team)+" Passes in Zone "+str(zone), fontproperties=headers, color="black")
    #plt.annotate(str(round(sum(pass_data.PP),2))+" Progressive Passes",color="white", xy=(44, -2), size = 10, ha="center", weight="bold", zorder=zo)
    #plt.annotate(str(round(sum(pass_data.DP),2))+" Deep Progressions",color="white", xy=(44, -4), size = 10, ha="center", weight="bold", zorder=zo)
    #plt.annotate(str(round(sum(pass_data.xP),2))+" xP",color="white", xy=(24, -2), size = 10, ha="center", weight="bold", zorder=zo)
    #plt.annotate(str(round(sum(pass_data.ifComplete),))+' / '+str(round(sum(pass_data.PassesAttempted),))+" Passes",color="white", xy=(24, -4), size = 10, ha="center", weight="bold", zorder=zo)     
    #plt.annotate("Bigger Arrow  = Higher xP",color="white", xy=(6, 107.5), size = 10, ha="center", weight="bold", zorder=zo)              
    plt.plot(-2,color="lime",label="Retain",zorder=0)
    plt.plot(-2,color="dodgerblue",label="Complete",zorder=0)
    plt.plot(-2,color="red",label="Incomplete",zorder=0)
    #plt.plot(-2,color="gold",label="Assist",zorder=0)
    leg = plt.legend(loc=0, ncol=3,frameon=False)
    plt.setp(leg.get_texts(), color='black', fontproperties=Labels)
    st.pyplot()

def TeamShot(state):
    sm_df = load_sm_data()
    
    team = st.sidebar.multiselect('Select Team(s)', natsorted(sm_df.Team.unique()))
    sm_df = sm_df[sm_df['Team'].isin(team)]
    
    
    season = st.sidebar.multiselect('Select Season(s)',natsorted(sm_df.Season.unique()))  
    sm_df = sm_df[sm_df['Season'].isin(season)]
    
    shot_df = load_shot_data(season, team, 'no')
    
    ToPs = (shot_df.TypeofPossession.unique()).tolist()
    
    ToP = st.sidebar.multiselect('Select Type of Possession(s)', natsorted(shot_df.TypeofPossession.unique()), default=ToPs)  
    ToP_df = shot_df[shot_df['TypeofPossession'].isin(ToP)]

    Actions = (ToP_df.Action.unique()).tolist()
    
    Action = st.sidebar.multiselect('Select Outcome of Shot(s)', natsorted(ToP_df.Action.unique()), default=Actions)  
    Action_df = ToP_df[ToP_df['Action'].isin(Action)]
    
    ToSs = (Action_df.TypeofShot.unique()).tolist()

    TypeofShot = st.sidebar.multiselect('Select Type of Shot(s)', natsorted(Action_df.TypeofShot.unique()), default=ToSs)  
    ToS_df = Action_df[Action_df['TypeofShot'].isin(TypeofShot)]
    
    matches = (ToS_df.MatchName.unique()).tolist()
    
    match = st.sidebar.multiselect("Select Match(es)", natsorted(ToS_df.MatchName.unique()), default=matches)
    match_df = ToS_df[ToS_df['MatchName'].isin(match)]
    

        

    st.header("Team Shot Maps")  
    st.subheader("By Matches, By Type of Possession, By Outcome of Shot, By Type of Shot")    
    st.text("")
 
    
    def TeamShotMap(data):
        Shots = match_df
        figsize1 = 36
        figsize2 = 18
        fig = plt.figure(figsize=(figsize1, figsize2)) 
        gs = gridspec.GridSpec(2, 2, width_ratios=[2., 1.25], wspace=0.05, right=.85)
    
        ax1 = plt.subplot(gs[:, 0])
        verthalf_pitch('#E6E6E6', 'black', ax1)
        def team_shot_map(data):
             shot_data = Shots[(Shots['TypeofPossession'] != 'Penalty attack')]
             stat_data = Shots
             OP_data = shot_data[(shot_data['TypeofPossession'] == 'Positional attack')]
             CR_data = shot_data[(shot_data['TypeofPossession'] == 'Corner attack')]
             FK_data = shot_data[ (shot_data['TypeofPossession'] == 'Free-kick attack')]
             T_data = shot_data[(shot_data['TypeofPossession'] == 'Throw-in attack')]
             CO_data = shot_data[(shot_data['TypeofPossession'] == 'Counter-attack')]
            
            
             Head = shot_data[(shot_data["Body"] == 'Header') & ((shot_data['ifShotFromCarry'] != 1) | ((shot_data['ifShotFromCarry'] == 1) & (shot_data['ifCA'] != 1)))]
             Foot = shot_data[(shot_data["Body"] != 'Header') & ((shot_data['ifShotFromCarry'] != 1) | ((shot_data['ifShotFromCarry'] == 1) & (shot_data['ifCA'] != 1)))]
             Carry = shot_data[(shot_data['ifShotFromCarry'] == 1) & (shot_data['ifCA'] == 1)]
             
             HGoal = Head[Head['Action'] == "Goal"]
             HMissed = Head[Head['Action'] == "Wide shot"]
             HSaved = Head[Head['Action'] == "Shot on target"]
             HBlocked = Head[(Head['Action'] == "Shot blocked by field player")]
             HSave = Head[(Head['Action'] == "Shot blocked")]
             HPost = Head[(Head)['Action'] == "Shot into the bar/post"]
             
             FGoal = Foot[(Foot['Action'] == "Goal")&(Foot['TypeofAttack'] != 'Free-kick attack')]
             FMissed = Foot[(Foot['Action'] == "Wide shot")&(Foot['TypeofAttack'] != 'Free-kick attack')]
             FSaved = Foot[(Foot['Action'] == "Shot on target")&(Foot['TypeofAttack'] != 'Free-kick attack')]
             FBlocked = Foot[(Foot['Action'] == "Shot blocked by field player")&(Foot['TypeofAttack'] != 'Free-kick attack')]
             FSave = Foot[(Foot['Action'] == "Shot blocked")&(Foot['TypeofAttack'] != 'Free-kick attack')]
             FPost = Foot[(Foot['Action'] == "Shot into the bar/post")]
             
             FKGoal = Foot[(Foot['Action'] == "Goal")&(Foot['TypeofAttack'] == 'Free-kick attack')]
             FKMissed = Foot[(Foot['Action'] == "Wide shot")&(Foot['TypeofAttack'] == 'Free-kick attack')]
             FKSaved = Foot[(Foot['Action'] == "Shot on target")&(Foot['TypeofAttack'] == 'Free-kick attack')]
             FKBlocked = Foot[(Foot['Action'] == "Shot blocked by field player")&(Foot['TypeofAttack'] == 'Free-kick attack')]
             FKSave = Foot[(Foot['Action'] == "Shot blocked")&(Foot['TypeofAttack'] == 'Free-kick attack')]
             FKPost = Foot[(Foot['Action'] == "Shot into the bar/post")&(Foot['TypeofAttack'] == 'Free-kick attack')]
             
             CGoal = Carry[(Carry['Action'] == "Goal")&(Carry['TypeofAttack'] != 'Free-kick attack')]
             CMissed = Carry[(Carry['Action'] == "Wide shot")&(Carry['TypeofAttack'] != 'Free-kick attack')]
             CSaved = Carry[(Carry['Action'] == "Shot on target")&(Carry['TypeofAttack'] != 'Free-kick attack')]
             CBlocked = Carry[(Carry['Action'] == "Shot blocked by field player")&(Carry['TypeofAttack'] != 'Free-kick attack')]
             CSave = Carry[(Carry['Action'] == "Shot blocked")&(Carry['TypeofAttack'] != 'Free-kick attack')]
             CPost = Carry[(Carry['Action'] == "Shot into the bar/post")]
    
             
             #draw_pitch("#B2B2B2","white","vertical","half")
             #plt.title(str(Season)+" - "+str(Team)+ " - " +str(Player)+" \n"+str((sum(shot_data.ifGoal)))+" Goals" " - "+str(round(sum(shot_data.xG),2))+" xG \n "+str(sum(stat_data.PenGoal))+" Goals / "+str(sum(stat_data.ifPen))+" Penalties \n "+str((sum(stat_data.Shots)))+" Shots"" - "+str(round(sum(shot_data.xG/sum(shot_data.Shots)),2))+" xG/shot", fontsize=20, weight="bold")
             
             norm = TwoSlopeNorm(vmin=0,vcenter=.2,vmax=.7)
             if len(FGoal) > 0:
                plt.scatter(68-FGoal.Y,FGoal.X,
                marker='H',c=FGoal.xG, s=500,
                edgecolors="black",zorder=zo+2, cmap='RdYlBu_r', norm=norm, linewidth=.5)
                plt.scatter(68-FGoal.Y,FGoal.X,marker='H',c="white",
                s=750,edgecolors="black",zorder=zo+1, linewidth=.5, norm=norm)
             if len(FMissed) > 0:
                plt.scatter(68-FMissed.Y,FMissed.X,marker='H',c=FMissed.xG, facecolors="none", s=500,
                edgecolors="none",zorder=zo, cmap='RdYlBu_r', norm=norm)
             if len(FSaved) > 0:
                plt.scatter(68-FSaved.Y,FSaved.X,
                marker='H',c=FSaved.xG, s=500,linewidths=2,
                edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
             if len(FSave) > 0:
                plt.scatter(68-FSave.Y,FSave.X,
                marker='H',c=FSave.xG, s=500, linewidths=2,
                edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
             if len(FBlocked) > 0:
                plt.scatter(68-FBlocked.Y,FBlocked.X,marker='H',c=FBlocked.xG, facecolors="none", s=500,
                edgecolors="black",zorder=zo, cmap='RdYlBu_r', alpha=.15, norm=norm)
                plt.scatter(68-FBlocked.Y,FBlocked.X,marker='H',facecolors="gray",
                s=500,edgecolors="black",zorder=zo+1, alpha=.15, norm=norm)
             if len(FPost) > 0:
                plt.scatter(68-FPost.Y,FPost.X,marker='H',c=FPost.xG, facecolors="none", s=500,
                edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
             if len(CGoal) > 0:
                plt.scatter(68-CGoal.Y,CGoal.X,
                marker='^',c=CGoal.xG, s=500,
                edgecolors="black",zorder=zo+2, cmap='RdYlBu_r', norm=norm, linewidth=.5)
                plt.scatter(68-CGoal.Y,CGoal.X,marker='^',facecolors="none",
                s=750,edgecolors="black",zorder=zo+1, linewidth=.5, norm=norm)
             if len(CMissed) > 0:
                plt.scatter(68-CMissed.Y,CMissed.X,marker='^',c=CMissed.xG, facecolors="none", s=500,
                edgecolors="none",zorder=zo, cmap='RdYlBu_r', norm=norm)
             if len(CSaved) > 0:
                plt.scatter(68-CSaved.Y,CSaved.X,
                marker='^',c=CSaved.xG, s=500,linewidths=2,
                edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
             if len(CSave) > 0:
                plt.scatter(68-CSave.Y,CSave.X,
                marker='^',c=CSave.xG, s=500, linewidths=2,
                edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
             if len(CBlocked) > 0:
                plt.scatter(68-CBlocked.Y,CBlocked.X,marker='^',c=CBlocked.xG, facecolors="none", s=500,
                edgecolors="black",zorder=zo, cmap='RdYlBu_r', alpha=.15, norm=norm)
                plt.scatter(68-CBlocked.Y,CBlocked.X,marker='^',facecolors="gray",
                s=500,edgecolors="black",zorder=zo+1, alpha=.15, norm=norm)
             if len(CPost) > 0:
                plt.scatter(68-CPost.Y,CPost.X,marker='^',c=CPost.xG, facecolors="none", s=500,
                edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
             if len(HGoal) > 0:
                plt.scatter(68-HGoal.Y,HGoal.X,
                marker='o',c=HGoal.xG, s=500,
                edgecolors="black",zorder=zo+2, cmap='RdYlBu_r', linewidth=.5, norm=norm)
                plt.scatter(68-HGoal.Y,HGoal.X,marker='o',facecolors="none",
                s=750,edgecolors="black",zorder=zo+1, linewidth=.5, norm=norm)
             if len(HMissed) > 0:
                plt.scatter(68-HMissed.Y,HMissed.X,marker='o',c=HMissed.xG, facecolors="none", s=500,
                edgecolors="none",zorder=zo, cmap='RdYlBu_r', norm=norm)
             if len(HSaved) > 0:
                plt.scatter(68-HSaved.Y,HSaved.X,
                marker='o',c=HSaved.xG, s=500, linewidths=2,
                edgecolors="black",zorder=zo, cmap='RdYlBu_r',  norm=norm)
             if len(HSave) > 0:
                plt.scatter(68-HSave.Y,HSave.X,
                marker='o',c=HSave.xG, s=500, linewidths=2,
                edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
             if len(HBlocked) > 0:
                plt.scatter(68-HBlocked.Y,HBlocked.X,marker='H',c=HBlocked.xG, facecolors="none", s=500,
                edgecolors="black",zorder=zo, cmap='RdYlBu_r', alpha=.15, norm=norm)
                plt.scatter(68-HBlocked.Y,HBlocked.X,marker='H',facecolors="gray",
                s=500,edgecolors="black",zorder=zo+1, alpha=.15, norm=norm)
             if len(HPost) > 0:
                plt.scatter(68-HPost.Y,HPost.X,marker='H',c=HPost.xG, facecolors="none", s=500,
                edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
             if len(FKGoal) > 0:
                plt.scatter(68-FKGoal.Y,FKGoal.X,
                marker='s',c=FKGoal.xG, s=500,
                edgecolors="black",zorder=zo+2, cmap='RdYlBu_r', linewidth=.5, norm=norm)
                plt.scatter(68-FKGoal.Y,FKGoal.X,marker='s',facecolors="none",
                s=750,edgecolors="black",zorder=zo+1, linewidth=.5, norm=norm)
             if len(FKMissed) > 0:
                plt.scatter(68-FKMissed.Y,FKMissed.X,marker='s',c=FKMissed.xG, facecolors="none", s=500,
                edgecolors="none",zorder=zo, cmap='RdYlBu_r', norm=norm)
             if len(FKSaved) > 0:
                plt.scatter(68-FKSaved.Y,FKSaved.X,
                marker='s',c=FKSaved.xG, s=500, linewidths=2,
                edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
             if len(FKSave) > 0:
                plt.scatter(68-FKSave.Y,FKSave.X, 
                marker='s',c=FKSave.xG, s=500, linewidths=2,
                edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
             if len(FKBlocked) > 0:
                plt.scatter(68-FKBlocked.Y,FKBlocked.X,marker='s',c=FKBlocked.xG, facecolors="none", s=500,
                edgecolors="black",zorder=zo, cmap='RdYlBu_r',  alpha=.15, norm=norm)
                plt.scatter(68-FKBlocked.Y,FKBlocked.X,marker='s',facecolors="gray",
                s=500,edgecolors="black",zorder=zo+1, alpha=.15, norm=norm)
             if len(FKPost) > 0:
                plt.scatter(68-FKPost.Y,FKPost.X,marker='s',c=FKPost.xG, facecolors="none", s=500,
                edgecolors="black",zorder=zo, cmap='RdYlBu_r', vmin=0, vmax=.7, norm=norm)
               
             plt.scatter(3.5,45, marker='H', facecolor="white", edgecolors="black", s=500, zorder=12)
             plt.scatter(11, 45, marker='o', facecolor="white", edgecolors="black", s=500, zorder=12)
             plt.scatter(18.5, 45, marker='^', facecolor="white", edgecolors="black", s=500, zorder=12)
             plt.scatter(26, 45, marker='s', facecolor="white", edgecolors="black", s=500, zorder=12)
             ax1.text(3.5,42.5,"Foot", color='black', fontproperties=Labels,
                      horizontalalignment='center', verticalalignment='center', zorder=12)
             ax1.text(11,42.5,"Header", color='black', fontproperties=Labels,
                      horizontalalignment='center', verticalalignment='center', zorder=12)
             ax1.text(18.5,42.5,"Carry",color='black', fontproperties=Labels,
                      horizontalalignment='center', verticalalignment='center', zorder=12)
             ax1.text(26,42.5,"FK", color='black', fontproperties=Labels,
                      horizontalalignment='center', verticalalignment='center', zorder=12)
            
             plt.scatter(45,45,marker='H',c='white', s=500,
                    edgecolors="black",zorder=zo+2, linewidth=.5)
             plt.scatter(45,45,marker='H',c="white",s=750,
                    edgecolors="black",zorder=zo+1, linewidth=.5)
             plt.scatter(50.5,45, marker='H', c='white', s=500, linewidths=2,
                edgecolors="black",zorder=zo)
             plt.scatter(56,45,marker='H', facecolors="none", s=500,
                edgecolors="black",zorder=zo, alpha=.15)
             plt.scatter(56,45,marker='H',facecolors="gray",
                s=500,edgecolors="black",zorder=zo+1, alpha=.15)
             plt.scatter(61.5,45,marker='H',c='white', facecolors="none", s=500,
                edgecolors="black", linewidths=.25, zorder=zo)
             ax1.text(45,42.5,"Goal",fontproperties=Labels,
                      horizontalalignment='center', verticalalignment='center', zorder=12)
             ax1.text(50.5,42.5,"Save",fontproperties=Labels,
                      horizontalalignment='center', verticalalignment='center', zorder=12)
             ax1.text(56,42.5,"Block",fontproperties=Labels,
                      horizontalalignment='center', verticalalignment='center', zorder=12)
             ax1.text(61.5,42.5,"OffT",fontproperties=Labels,
                      horizontalalignment='center', verticalalignment='center', zorder=12)
             plt.ylim(40,105.5)
             plt.xlim(-.5,68.5)
        
             #a = plt.scatter(-10,-10, marker='H', facecolor="white", edgecolors="black", s=500)
             #b = plt.scatter(-10, -10, marker='o', facecolor="white", edgecolors="black", s=500)
             #c = plt.scatter(-10, -10, marker='^', facecolor="white", edgecolors="black", s=500)
             #plt.legend((a, b, c),("Foot", "Header", "Direct Free Kick"), loc='lower left', title="Types of Shots")
             #plt.annotate('Double Ring = Goal', xy=(18, 47), size = 12, color="black",ha="center")
             #plt.annotate('Black Edge = On Target', xy=(18, 45), size = 12, color="black",ha="center")
             #plt.annotate('No Edge = Off Target', xy=(18, 43), size = 12, color="black",ha="center")
             #plt.annotate('Gray Fill = Blocked', xy=(18, 41), size = 12, color="black",ha="center")
    
        team_shot_map(data)
            
        ax2 = plt.subplot(gs[0, 1])
        def GKMap(data, ax):
            df = Shots[(Shots['ifPen'] != 1) & (Shots['OnT'] == 1)]
            
            ly1 = [-0.1,-0.1,2.5,2.5,-0.1]
            lx1 = [-3.8,3.8,3.8,-3.8,-3.8]
            ax.plot(lx1,ly1,color='black',zorder=5, lw=6)
            ax.plot([-3.8,3.8], [-0.1,-0.1], color='white', zorder=6, lw=8)
            ax.axis('off')
            
            
            Head = df[(df["Body"] == 'Header') & ((df['ifShotFromCarry'] != 1) | ((df['ifShotFromCarry'] == 1) & (df['ifCA'] != 1)))]
            Foot = df[(df["Body"] != 'Header') & ((df['ifShotFromCarry'] != 1) | ((df['ifShotFromCarry'] == 1) & (df['ifCA'] != 1)))]
            Carry = df[(df['ifShotFromCarry'] == 1) & (df['ifCA'] == 1)]
              
            HGoal = Head[Head['Action'] == "Goal"]
            HSaved = Head[Head['Action'] == "Shot on target"]
            HSave = Head[(Head['Action'] == "Shot blocked")]
            CGoal = Carry[Carry['Action'] == "Goal"]
            CSaved = Carry[Carry['Action'] == "Shot on target"]
            CSave = Carry[(Carry['Action'] == "Shot blocked")]
            FGoal = Foot[(Foot['Action'] == "Goal")&(Foot['TypeofAttack'] != 'Free-kick attack')]
            FSaved = Foot[(Foot['Action'] == "Shot on target")&(Foot['TypeofAttack'] != 'Free-kick attack')]
            FSave = Foot[(Foot['Action'] == "Shot blocked")&(Foot['TypeofAttack'] != 'Free-kick attack')]
            FKGoal = Foot[(Foot['Action'] == "Goal")&(Foot['TypeofAttack'] == 'Free-kick attack')]
            FKSaved = Foot[(Foot['Action'] == "Shot on target")&(Foot['TypeofAttack'] == 'Free-kick attack')]
            FKSave = Foot[(Foot['Action'] == "Shot blocked")&(Foot['TypeofAttack'] == 'Free-kick attack')]
            
            norm = TwoSlopeNorm(vmin=0,vcenter=.2,vmax=.7)
            if len(FGoal) > 0:
               plt.scatter(FGoal.GoalX,FGoal.GoalY,
               marker='H',c=FGoal.PSxG, s=500,
               edgecolors="black",zorder=zo+2, cmap='RdYlBu_r', norm=norm, linewidth=.5)
               plt.scatter(FGoal.GoalX,FGoal.GoalY,marker='H',facecolors="none",
               s=750,edgecolors="black",zorder=zo+1, linewidth=.5, norm=norm)
            if len(FSaved) > 0:
               plt.scatter(FSaved.GoalX,FSaved.GoalY,
               marker='H',c=FSaved.PSxG, s=500,linewidths=2,
               edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
            if len(FSave) > 0:
               plt.scatter(FSave.GoalX,FSave.GoalY,
               marker='H',c=FSave.PSxG, s=500, linewidths=2,
               edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
            if len(CGoal) > 0:
               plt.scatter(CGoal.GoalX,CGoal.GoalY,
               marker='^',c=CGoal.PSxG, s=500,
               edgecolors="black",zorder=zo+2, cmap='RdYlBu_r', norm=norm, linewidth=.5)
               plt.scatter(CGoal.GoalX,CGoal.GoalY,marker='^',facecolors="none",
               s=750,edgecolors="black",zorder=zo+1, linewidth=.5, norm=norm)
            if len(CSaved) > 0:
               plt.scatter(CSaved.GoalX,CSaved.GoalY,
               marker='^',c=CSaved.PSxG, s=500,linewidths=2,
               edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
            if len(CSave) > 0:
               plt.scatter(CSave.GoalX,CSave.GoalY,
               marker='^',c=CSave.PSxG, s=500, linewidths=2,
               edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)           
            if len(HGoal) > 0:
               plt.scatter(HGoal.GoalX,HGoal.GoalY,
               marker='o',c=HGoal.PSxG, s=500,
               edgecolors="white",zorder=zo+2, cmap='RdYlBu_r', linewidth=.5, norm=norm)
               plt.scatter(HGoal.GoalX,HGoal.GoalY,marker='o',facecolors="none",
               s=750,edgecolors="black",zorder=zo+1, linewidth=.5, norm=norm)
            if len(HSaved) > 0:
               plt.scatter(HSaved.GoalX,HSaved.GoalY,
               marker='o',c=HSaved.PSxG, s=500, linewidths=2,
               edgecolors="black",zorder=zo, cmap='RdYlBu_r',  norm=norm)
            if len(HSave) > 0:
               plt.scatter(HSave.GoalX,HSave.GoalY,
               marker='o',c=HSave.PSxG, s=500, linewidths=2,
               edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
            if len(FKGoal) > 0:
               plt.scatter(FKGoal.GoalX,FKGoal.GoalY,
               marker='s',c=FKGoal.PSxG, s=500,
               edgecolors="black",zorder=zo+2, cmap='RdYlBu_r', linewidth=.5, norm=norm)
               plt.scatter(FKGoal.GoalX,FKGoal.GoalY,marker='s',facecolors="none",
               s=500,edgecolors="black",zorder=zo+1, linewidth=.5, norm=norm)
            if len(FKSaved) > 0:
               plt.scatter(FKSaved.GoalX,FKSaved.GoalY,
               marker='s',c=FKSaved.PSxG, s=500, linewidths=2,
               edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
            if len(FKSave) > 0:
               plt.scatter(FKSave.GoalX,FKSave.GoalY, 
               marker='s',c=FKSave.PSxG, s=500, linewidths=2,
               edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
               
        GKMap(data, ax2)
        
        
        
        shot_data = Shots[(Shots['ifPen'] != 1)]
        pen_data = Shots[ (Shots['ifPen'] == 1)]
        OP_data = shot_data[(shot_data['TypeofPossession'] == 'Positional attack')]
        CR_data = shot_data[(shot_data['TypeofPossession'] == 'Corner attack')]
        FK_data = shot_data[(shot_data['TypeofPossession'] == 'Free-kick attack')]
        T_data = shot_data[(shot_data['TypeofPossession'] == 'Throw-in attack')]
        CO_data = shot_data[(shot_data['TypeofPossession'] == 'Counter-attack')]
        sog_data = Shots[(Shots['ifPen'] != 1) ]
        sOP_data = sog_data[(sog_data['TypeofPossession'] == 'Positional attack')]
        sCR_data = sog_data[(sog_data['TypeofPossession'] == 'Corner attack')]
        sFK_data = sog_data[(sog_data['TypeofPossession'] == 'Free-kick attack')]
        sT_data = sog_data[(sog_data['TypeofPossession'] == 'Throw-in attack')]
        sCO_data = sog_data[(sog_data['TypeofPossession'] == 'Counter-attack')]
        SP_data = sog_data[(sog_data['ifSP'] == 1)]        
        #SP_data = shot_data[(shot_data['TypeofPossession'] == 'Free-kick attack')or(shot_data['TypeofPossession'] == 'Throw-in attack')or(shot_data['TypeofPossession'] == 'Corner attack')]
        
        ax3 = plt.subplot(gs[1, 1])
        ax3.axis('off')
        ax3.set_xticks([0,1])
        ax3.set_yticks([0,1])
        ax3.scatter(0,0, alpha=0)
        ax3.scatter(1,1,alpha=0)
    
        #ax3.text(0.10,0.85,"Open Play",fontproperties=TableHead,color='white',
         #         horizontalalignment='center', verticalalignment='center', bbox=dict(facecolor='black', alpha=0.5, edgecolor='white', lw=3.5))
        #ax3.text(0.425,0.85,"Counter Attack",fontproperties=TableHead,color='white',
         #        horizontalalignment='center', verticalalignment='center', bbox=dict(facecolor='black', alpha=0.5, edgecolor='white', lw=3.5))
        #ax3.text(0.750,0.85,"Set Pieces",fontproperties=TableHead,color='white',
         #        horizontalalignment='center', verticalalignment='center', bbox=dict(facecolor='black', alpha=0.5, edgecolor='white', lw=3.5))
        #ax3.text(0.10,0.725,str(round(sum(OP_data.xG),2))+' xG\n'+str(round(sum(OP_data.ifGoal),))+' G - '+str(round(sum(OP_data.Shots),))+' S',fontproperties=Labels,
         #         horizontalalignment='center', verticalalignment='center', bbox=dict(facecolor='white', alpha=0.5, edgecolor='white', lw=3.5))
        ax3.text(0.475,1,"Post-Shot xG",fontproperties=TableHead, color='white',
                  horizontalalignment='center', verticalalignment='center', zorder=12)
        ax3.text(0.10,0.9,"Open Play",fontproperties=TableHead, color='white', 
                  horizontalalignment='center', verticalalignment='center', zorder=12)
        ax3.text(0.475,0.9,"Counter Attack",fontproperties=TableHead, color='white',
                  horizontalalignment='center', verticalalignment='center', zorder=12)
        ax3.text(0.85,0.9,"Set Pieces",fontproperties=TableHead, color='white', 
                  horizontalalignment='center', verticalalignment='center', zorder=12)
        ax3.text(0.10,0.725,str(round(sum(sOP_data.PSxG),2))+' PSxG\n'+str(round(sum(sOP_data.ifGoal),))+' G - '+str(round(sum(sOP_data.OnT),))+' S\n'+str(round(sum(sOP_data.PSxG/sum(sOP_data.OnT)),2))+" PSxGpShot",
                 fontproperties=TableNum, color='black',  horizontalalignment='center', verticalalignment='center', zorder=12)
        ax3.text(0.475,0.725,str(round(sum(sCO_data.PSxG),2))+' PSxG\n'+str(round(sum(sCO_data.ifGoal),))+' G - '+str(round(sum(sCO_data.OnT),))+' S\n'+str(round(sum(sCO_data.PSxG/sum(sCO_data.OnT)),2))+" PSxGpShot",
                 fontproperties=TableNum, color='black', horizontalalignment='center', verticalalignment='center', zorder=12)
        ax3.text(0.85,0.725,str(round(sum(SP_data.PSxG),2))+' PSxG\n'+str(round(sum(SP_data.ifGoal),))+' G - '+str(round(sum(SP_data.OnT),))+' S\n'+str(round(sum(SP_data.PSxG/sum(SP_data.OnT)),2))+" PSxGpShot",
                 fontproperties=TableNum, color='black', horizontalalignment='center', verticalalignment='center', zorder=12)

        rec1 = plt.Rectangle((-0.1, .85),1.1,.15,ls='-',color='black',zorder=6,alpha=1)
        rec2 = plt.Rectangle((-0.1, .95),1.1,.15,ls='-',color='black',zorder=6,alpha=1)
        rec3 = plt.Rectangle((-0.1, .6),1.1,.3,ls='-',color='white',zorder=5,alpha=.5)
        ax3.add_artist(rec1)
        ax3.add_artist(rec2)
        ax3.add_artist(rec3)
    
        
        
        
        
        
        ax3.text(0.475,0.35,"Normal xG",fontproperties=TableHead, color='white',
                  horizontalalignment='center', verticalalignment='center', zorder=12)
        ax3.text(0.10,0.25,"Open Play",fontproperties=TableHead, color='white', 
                  horizontalalignment='center', verticalalignment='center', zorder=12)
        ax3.text(0.475,0.25,"Counter Attack",fontproperties=TableHead, color='white', 
                  horizontalalignment='center', verticalalignment='center', zorder=12)
        ax3.text(0.85,0.25,"Set Pieces",fontproperties=TableHead, color='white', 
                  horizontalalignment='center', verticalalignment='center', zorder=12)
        ax3.text(0.10,0.07,str(round(sum(OP_data.xG),2))+' xG\n'+str(round(sum(OP_data.ifGoal),))+' G - '+str(round(sum(OP_data.ifShot),))+' S\n'+str(round(sum(OP_data.xG/sum(OP_data.ifShot)),2))+" xGpShot",
                 fontproperties=TableNum, color='black', horizontalalignment='center', verticalalignment='center', zorder=12)
        ax3.text(0.475,0.07,str(round(sum(CO_data.xG),2))+' xG\n'+str(round(sum(CO_data.ifGoal),))+' G - '+str(round(sum(CO_data.ifShot),))+' S\n'+str(round(sum(CO_data.xG/sum(CO_data.ifShot)),2))+" xGpShot",
                 fontproperties=TableNum, color='black',  horizontalalignment='center', verticalalignment='center', zorder=12)
        ax3.text(0.85,0.07,str(round(sum(SP_data.xG),2))+' xG\n'+str(round(sum(SP_data.ifGoal),))+' G - '+str(round(sum(SP_data.ifShot),))+' S\n'+str(round(sum(SP_data.xG/sum(SP_data.ifShot)),2))+" xGpShot",
                 fontproperties=TableNum, color='black', horizontalalignment='center', verticalalignment='center', zorder=12)
        
        rec1 = plt.Rectangle((-0.1, .2),1.1,.1,ls='-',color='black',zorder=6,alpha=1)
        rec2 = plt.Rectangle((-0.1, .3),1.1,.1,ls='-',color='black',zorder=6,alpha=1)
        rec3 = plt.Rectangle((-0.1, -0.1),1.1,.4,ls='-',color='white',zorder=5,alpha=.5)
        ax3.add_artist(rec1)
        ax3.add_artist(rec2)
        ax3.add_artist(rec3)
    
        
        cax = plt.axes([0.15, 0.065, 0.7, 0.025])
        sm = plt.cm.ScalarMappable(cmap='RdYlBu_r', norm=TwoSlopeNorm(vmin=0,vcenter=.2, vmax=.7))
        sm.A = []
        cbar = fig.colorbar(sm, cax=cax, orientation='horizontal', fraction=0.046, pad=0.04)
        cbar.set_label('xG', fontproperties=TableHead)
        cbar.set_ticks([0, .03, .1, .2, .3, .4, .5, .6, .7])
        cbar.ax.set_xticklabels([0, .03, .1, .2, .3, .4, .5, .6, .7])
        cbar.ax.tick_params(labelsize=20)
        
        fig.text(0.125,0.9,str(season)+' - '+str(team), fontproperties=TeamHead, color='black')
        #fig.text(0.125,0.875,str(season), fontproperties=GoalandxG, color='black')
        fig.text(0.625,0.925,str(round(sum(shot_data.ifGoal),))+" Goals - "+str(round(sum(shot_data.xG),2))+' xG - '+str(round(sum(sog_data.PSxG),2))+' PSxG',
                 fontproperties=GoalandxG, color='black')
        fig.text(0.7,0.905,str(round(sum(pen_data.xG),2))+' xG - '+str(round(sum(pen_data.ifGoal),))+" Goals - "+str(round(sum(pen_data.ifPen),))+" Penalties",fontproperties=Summary, color='black')
        fig.text(0.7,0.88,str(round(sum(shot_data.ifShot),))+'|'+str(round(sum(shot_data.OnT),))+' S|OnT - '+str(round(sum(shot_data.xG/sum(shot_data.ifShot)),2))+" xGpShot",fontproperties=Summary,color='black')
    
    TeamShotMap(match_df)
    st.pyplot()
    
    st.subheader("Shot Data")    
    st.text("")

    
    AllShots = match_df
    
    test = AllShots[(AllShots['ifPen'] != 1) & (AllShots['Player'] != 'Noname Noname')]
    test = test.groupby(["Player"], as_index=False).agg({"xG": 'sum', 'PSxG': 'sum', 'ifShot':'sum','ifGoal':'sum', 'GPA':'sum'}).sort_values(by='xG', ascending=False)
    test['xG/Shot'] = test['xG'] / test['ifShot']
    test = test.sort_values(by='PSxG', ascending=False).head(25)
    st.dataframe(test)
    

def TeamShotD(state):
    sm_df = load_sm_data()
    
    team = st.sidebar.multiselect('Select Team(s)', natsorted(sm_df.Team.unique()))
    sm_df = sm_df[(sm_df['Team'].isin(team))]
    
    
    season = st.sidebar.multiselect('Select Season(s)',natsorted(sm_df.Season.unique()))  
    sm_df = sm_df[sm_df['Season'].isin(season)]
    
    shot_df = load_shot_data(season, team, 'yes')
    
    ToPs = (shot_df.TypeofPossession.unique()).tolist()
    
    ToP = st.sidebar.multiselect('Select Type of Possession(s)', natsorted(shot_df.TypeofPossession.unique()), default=ToPs)  
    ToP_df = shot_df[shot_df['TypeofPossession'].isin(ToP)]

    Actions = (ToP_df.Action.unique()).tolist()
    
    Action = st.sidebar.multiselect('Select Outcome of Shot(s)', natsorted(ToP_df.Action.unique()), default=Actions)  
    Action_df = ToP_df[ToP_df['Action'].isin(Action)]
    
    ToSs = (Action_df.TypeofShot.unique()).tolist()

    TypeofShot = st.sidebar.multiselect('Select Type of Shot(s)', natsorted(Action_df.TypeofShot.unique()), default=ToSs)  
    ToS_df = Action_df[Action_df['TypeofShot'].isin(TypeofShot)]
    
    matches = (ToS_df.MatchName.unique()).tolist()
    
    match = st.sidebar.multiselect("Select Match(es)", natsorted(ToS_df.MatchName.unique()), default=matches)
    match_df = ToS_df[ToS_df['MatchName'].isin(match)]

    
    st.header("Team Defensive Shot Maps")  
    st.subheader("By Matches, By Type of Possession, By Outcome of Shot, By Type of Shot")    
    st.text("")

    
    def TeamShotMap(data):
        Shots = match_df
        figsize1 = 36
        figsize2 = 18
        fig = plt.figure(figsize=(figsize1, figsize2)) 
        gs = gridspec.GridSpec(2, 2, width_ratios=[2., 1.25], wspace=0.05, right=.85)
    
        ax1 = plt.subplot(gs[:, 0])
        verthalf_pitch('#E6E6E6', 'black', ax1)
        def team_shot_map(data):
             shot_data = Shots[(Shots['TypeofPossession'] != 'Penalty attack')]
             stat_data = Shots
             OP_data = shot_data[(shot_data['TypeofPossession'] == 'Positional attack')]
             CR_data = shot_data[(shot_data['TypeofPossession'] == 'Corner attack')]
             FK_data = shot_data[ (shot_data['TypeofPossession'] == 'Free-kick attack')]
             T_data = shot_data[(shot_data['TypeofPossession'] == 'Throw-in attack')]
             CO_data = shot_data[(shot_data['TypeofPossession'] == 'Counter-attack')]
            
            
             Head = shot_data[(shot_data["Body"] == 'Header') & ((shot_data['ifShotFromCarry'] != 1) | ((shot_data['ifShotFromCarry'] == 1) & (shot_data['ifCA'] != 1)))]
             Foot = shot_data[(shot_data["Body"] != 'Header') & ((shot_data['ifShotFromCarry'] != 1) | ((shot_data['ifShotFromCarry'] == 1) & (shot_data['ifCA'] != 1)))]
             Carry = shot_data[(shot_data['ifShotFromCarry'] == 1) & (shot_data['ifCA'] == 1)]
             
             HGoal = Head[Head['Action'] == "Goal"]
             HMissed = Head[Head['Action'] == "Wide shot"]
             HSaved = Head[Head['Action'] == "Shot on target"]
             HBlocked = Head[(Head['Action'] == "Shot blocked by field player")]
             HSave = Head[(Head['Action'] == "Shot blocked")]
             HPost = Head[(Head)['Action'] == "Shot into the bar/post"]
             
             FGoal = Foot[(Foot['Action'] == "Goal")&(Foot['TypeofAttack'] != 'Free-kick attack')]
             FMissed = Foot[(Foot['Action'] == "Wide shot")&(Foot['TypeofAttack'] != 'Free-kick attack')]
             FSaved = Foot[(Foot['Action'] == "Shot on target")&(Foot['TypeofAttack'] != 'Free-kick attack')]
             FBlocked = Foot[(Foot['Action'] == "Shot blocked by field player")&(Foot['TypeofAttack'] != 'Free-kick attack')]
             FSave = Foot[(Foot['Action'] == "Shot blocked")&(Foot['TypeofAttack'] != 'Free-kick attack')]
             FPost = Foot[(Foot['Action'] == "Shot into the bar/post")]
             
             FKGoal = Foot[(Foot['Action'] == "Goal")&(Foot['TypeofAttack'] == 'Free-kick attack')]
             FKMissed = Foot[(Foot['Action'] == "Wide shot")&(Foot['TypeofAttack'] == 'Free-kick attack')]
             FKSaved = Foot[(Foot['Action'] == "Shot on target")&(Foot['TypeofAttack'] == 'Free-kick attack')]
             FKBlocked = Foot[(Foot['Action'] == "Shot blocked by field player")&(Foot['TypeofAttack'] == 'Free-kick attack')]
             FKSave = Foot[(Foot['Action'] == "Shot blocked")&(Foot['TypeofAttack'] == 'Free-kick attack')]
             FKPost = Foot[(Foot['Action'] == "Shot into the bar/post")&(Foot['TypeofAttack'] == 'Free-kick attack')]
             
             CGoal = Carry[(Carry['Action'] == "Goal")&(Carry['TypeofAttack'] != 'Free-kick attack')]
             CMissed = Carry[(Carry['Action'] == "Wide shot")&(Carry['TypeofAttack'] != 'Free-kick attack')]
             CSaved = Carry[(Carry['Action'] == "Shot on target")&(Carry['TypeofAttack'] != 'Free-kick attack')]
             CBlocked = Carry[(Carry['Action'] == "Shot blocked by field player")&(Carry['TypeofAttack'] != 'Free-kick attack')]
             CSave = Carry[(Carry['Action'] == "Shot blocked")&(Carry['TypeofAttack'] != 'Free-kick attack')]
             CPost = Carry[(Carry['Action'] == "Shot into the bar/post")]
    
             
             #draw_pitch("#B2B2B2","white","vertical","half")
             #plt.title(str(Season)+" - "+str(Team)+ " - " +str(Player)+" \n"+str((sum(shot_data.ifGoal)))+" Goals" " - "+str(round(sum(shot_data.xG),2))+" xG \n "+str(sum(stat_data.PenGoal))+" Goals / "+str(sum(stat_data.ifPen))+" Penalties \n "+str((sum(stat_data.Shots)))+" Shots"" - "+str(round(sum(shot_data.xG/sum(shot_data.Shots)),2))+" xG/shot", fontsize=20, weight="bold")
             
             norm = TwoSlopeNorm(vmin=0,vcenter=.2,vmax=.7)
             if len(FGoal) > 0:
                plt.scatter(68-FGoal.Y,FGoal.X,
                marker='H',c=FGoal.xG, s=500,
                edgecolors="black",zorder=zo+2, cmap='RdYlBu_r', norm=norm, linewidth=.5)
                plt.scatter(68-FGoal.Y,FGoal.X,marker='H',c="white",
                s=750,edgecolors="black",zorder=zo+1, linewidth=.5, norm=norm)
             if len(FMissed) > 0:
                plt.scatter(68-FMissed.Y,FMissed.X,marker='H',c=FMissed.xG, facecolors="none", s=500,
                edgecolors="none",zorder=zo, cmap='RdYlBu_r', norm=norm)
             if len(FSaved) > 0:
                plt.scatter(68-FSaved.Y,FSaved.X,
                marker='H',c=FSaved.xG, s=500,linewidths=2,
                edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
             if len(FSave) > 0:
                plt.scatter(68-FSave.Y,FSave.X,
                marker='H',c=FSave.xG, s=500, linewidths=2,
                edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
             if len(FBlocked) > 0:
                plt.scatter(68-FBlocked.Y,FBlocked.X,marker='H',c=FBlocked.xG, facecolors="none", s=500,
                edgecolors="black",zorder=zo, cmap='RdYlBu_r', alpha=.15, norm=norm)
                plt.scatter(68-FBlocked.Y,FBlocked.X,marker='H',facecolors="gray",
                s=500,edgecolors="black",zorder=zo+1, alpha=.15, norm=norm)
             if len(FPost) > 0:
                plt.scatter(68-FPost.Y,FPost.X,marker='H',c=FPost.xG, facecolors="none", s=500,
                edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
             if len(CGoal) > 0:
                plt.scatter(68-CGoal.Y,CGoal.X,
                marker='^',c=CGoal.xG, s=500,
                edgecolors="black",zorder=zo+2, cmap='RdYlBu_r', norm=norm, linewidth=.5)
                plt.scatter(68-CGoal.Y,CGoal.X,marker='^',facecolors="none",
                s=750,edgecolors="black",zorder=zo+1, linewidth=.5, norm=norm)
             if len(CMissed) > 0:
                plt.scatter(68-CMissed.Y,CMissed.X,marker='^',c=CMissed.xG, facecolors="none", s=500,
                edgecolors="none",zorder=zo, cmap='RdYlBu_r', norm=norm)
             if len(CSaved) > 0:
                plt.scatter(68-CSaved.Y,CSaved.X,
                marker='^',c=CSaved.xG, s=500,linewidths=2,
                edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
             if len(CSave) > 0:
                plt.scatter(68-CSave.Y,CSave.X,
                marker='^',c=CSave.xG, s=500, linewidths=2,
                edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
             if len(CBlocked) > 0:
                plt.scatter(68-CBlocked.Y,CBlocked.X,marker='^',c=CBlocked.xG, facecolors="none", s=500,
                edgecolors="black",zorder=zo, cmap='RdYlBu_r', alpha=.15, norm=norm)
                plt.scatter(68-CBlocked.Y,CBlocked.X,marker='^',facecolors="gray",
                s=500,edgecolors="black",zorder=zo+1, alpha=.15, norm=norm)
             if len(CPost) > 0:
                plt.scatter(68-CPost.Y,CPost.X,marker='^',c=CPost.xG, facecolors="none", s=500,
                edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
             if len(HGoal) > 0:
                plt.scatter(68-HGoal.Y,HGoal.X,
                marker='o',c=HGoal.xG, s=500,
                edgecolors="black",zorder=zo+2, cmap='RdYlBu_r', linewidth=.5, norm=norm)
                plt.scatter(68-HGoal.Y,HGoal.X,marker='o',facecolors="none",
                s=750,edgecolors="black",zorder=zo+1, linewidth=.5, norm=norm)
             if len(HMissed) > 0:
                plt.scatter(68-HMissed.Y,HMissed.X,marker='o',c=HMissed.xG, facecolors="none", s=500,
                edgecolors="none",zorder=zo, cmap='RdYlBu_r', norm=norm)
             if len(HSaved) > 0:
                plt.scatter(68-HSaved.Y,HSaved.X,
                marker='o',c=HSaved.xG, s=500, linewidths=2,
                edgecolors="black",zorder=zo, cmap='RdYlBu_r',  norm=norm)
             if len(HSave) > 0:
                plt.scatter(68-HSave.Y,HSave.X,
                marker='o',c=HSave.xG, s=500, linewidths=2,
                edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
             if len(HBlocked) > 0:
                plt.scatter(68-HBlocked.Y,HBlocked.X,marker='H',c=HBlocked.xG, facecolors="none", s=500,
                edgecolors="black",zorder=zo, cmap='RdYlBu_r', alpha=.15, norm=norm)
                plt.scatter(68-HBlocked.Y,HBlocked.X,marker='H',facecolors="gray",
                s=500,edgecolors="black",zorder=zo+1, alpha=.15, norm=norm)
             if len(HPost) > 0:
                plt.scatter(68-HPost.Y,HPost.X,marker='H',c=HPost.xG, facecolors="none", s=500,
                edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
             if len(FKGoal) > 0:
                plt.scatter(68-FKGoal.Y,FKGoal.X,
                marker='s',c=FKGoal.xG, s=500,
                edgecolors="black",zorder=zo+2, cmap='RdYlBu_r', linewidth=.5, norm=norm)
                plt.scatter(68-FKGoal.Y,FKGoal.X,marker='s',facecolors="none",
                s=750,edgecolors="black",zorder=zo+1, linewidth=.5, norm=norm)
             if len(FKMissed) > 0:
                plt.scatter(68-FKMissed.Y,FKMissed.X,marker='s',c=FKMissed.xG, facecolors="none", s=500,
                edgecolors="none",zorder=zo, cmap='RdYlBu_r', norm=norm)
             if len(FKSaved) > 0:
                plt.scatter(68-FKSaved.Y,FKSaved.X,
                marker='s',c=FKSaved.xG, s=500, linewidths=2,
                edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
             if len(FKSave) > 0:
                plt.scatter(68-FKSave.Y,FKSave.X, 
                marker='s',c=FKSave.xG, s=500, linewidths=2,
                edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
             if len(FKBlocked) > 0:
                plt.scatter(68-FKBlocked.Y,FKBlocked.X,marker='s',c=FKBlocked.xG, facecolors="none", s=500,
                edgecolors="black",zorder=zo, cmap='RdYlBu_r',  alpha=.15, norm=norm)
                plt.scatter(68-FKBlocked.Y,FKBlocked.X,marker='s',facecolors="gray",
                s=500,edgecolors="black",zorder=zo+1, alpha=.15, norm=norm)
             if len(FKPost) > 0:
                plt.scatter(68-FKPost.Y,FKPost.X,marker='s',c=FKPost.xG, facecolors="none", s=500,
                edgecolors="black",zorder=zo, cmap='RdYlBu_r', vmin=0, vmax=.7, norm=norm)
               
             plt.scatter(3.5,45, marker='H', facecolor="white", edgecolors="black", s=500, zorder=12)
             plt.scatter(11, 45, marker='o', facecolor="white", edgecolors="black", s=500, zorder=12)
             plt.scatter(18.5, 45, marker='^', facecolor="white", edgecolors="black", s=500, zorder=12)
             plt.scatter(26, 45, marker='s', facecolor="white", edgecolors="black", s=500, zorder=12)
             ax1.text(3.5,42.5,"Foot",fontproperties=Labels,
                      horizontalalignment='center', verticalalignment='center', zorder=12)
             ax1.text(11,42.5,"Header",fontproperties=Labels,
                      horizontalalignment='center', verticalalignment='center', zorder=12)
             ax1.text(18.5,42.5,"Carry",fontproperties=Labels,
                      horizontalalignment='center', verticalalignment='center', zorder=12)
             ax1.text(26,42.5,"FK",fontproperties=Labels,
                      horizontalalignment='center', verticalalignment='center', zorder=12)
            
             plt.scatter(45,45,marker='H',c='white', s=500,
                    edgecolors="black",zorder=zo+2, linewidth=.5)
             plt.scatter(45,45,marker='H',c="white",s=750,
                    edgecolors="black",zorder=zo+1, linewidth=.5)
             plt.scatter(50.5,45, marker='H', c='white', s=500, linewidths=2,
                edgecolors="black",zorder=zo)
             plt.scatter(56,45,marker='H', facecolors="none", s=500,
                edgecolors="black",zorder=zo, alpha=.15)
             plt.scatter(56,45,marker='H',facecolors="gray",
                s=500,edgecolors="black",zorder=zo+1, alpha=.15)
             plt.scatter(61.5,45,marker='H',c='white', facecolors="none", s=500,
                edgecolors="black", linewidths=.25, zorder=zo)
             ax1.text(45,42.5,"Goal",fontproperties=Labels,
                      horizontalalignment='center', verticalalignment='center', zorder=12)
             ax1.text(50.5,42.5,"Save",fontproperties=Labels,
                      horizontalalignment='center', verticalalignment='center', zorder=12)
             ax1.text(56,42.5,"Block",fontproperties=Labels,
                      horizontalalignment='center', verticalalignment='center', zorder=12)
             ax1.text(61.5,42.5,"OffT",fontproperties=Labels,
                      horizontalalignment='center', verticalalignment='center', zorder=12)
             plt.ylim(40,105.5)
             plt.xlim(-.5,68.5)
        
             #a = plt.scatter(-10,-10, marker='H', facecolor="white", edgecolors="black", s=500)
             #b = plt.scatter(-10, -10, marker='o', facecolor="white", edgecolors="black", s=500)
             #c = plt.scatter(-10, -10, marker='^', facecolor="white", edgecolors="black", s=500)
             #plt.legend((a, b, c),("Foot", "Header", "Direct Free Kick"), loc='lower left', title="Types of Shots")
             #plt.annotate('Double Ring = Goal', xy=(18, 47), size = 12, color="black",ha="center")
             #plt.annotate('Black Edge = On Target', xy=(18, 45), size = 12, color="black",ha="center")
             #plt.annotate('No Edge = Off Target', xy=(18, 43), size = 12, color="black",ha="center")
             #plt.annotate('Gray Fill = Blocked', xy=(18, 41), size = 12, color="black",ha="center")
    
        team_shot_map(data)
            
        ax2 = plt.subplot(gs[0, 1])
        def GKMap(data, ax):
            df = Shots[(Shots['ifPen'] != 1) & (Shots['OnT'] == 1)]
            
            ly1 = [-0.1,-0.1,2.5,2.5,-0.1]
            lx1 = [-3.8,3.8,3.8,-3.8,-3.8]
            ax.plot(lx1,ly1,color='black',zorder=5, lw=6)
            ax.plot([-3.8,3.8], [-0.1,-0.1], color='white', zorder=6, lw=8)
            ax.axis('off')
            
            
            Head = df[(df["Body"] == 'Header') & ((df['ifShotFromCarry'] != 1) | ((df['ifShotFromCarry'] == 1) & (df['ifCA'] != 1)))]
            Foot = df[(df["Body"] != 'Header') & ((df['ifShotFromCarry'] != 1) | ((df['ifShotFromCarry'] == 1) & (df['ifCA'] != 1)))]
            Carry = df[(df['ifShotFromCarry'] == 1) & (df['ifCA'] == 1)]
              
            HGoal = Head[Head['Action'] == "Goal"]
            HSaved = Head[Head['Action'] == "Shot on target"]
            HSave = Head[(Head['Action'] == "Shot blocked")]
            CGoal = Carry[Carry['Action'] == "Goal"]
            CSaved = Carry[Carry['Action'] == "Shot on target"]
            CSave = Carry[(Carry['Action'] == "Shot blocked")]
            FGoal = Foot[(Foot['Action'] == "Goal")&(Foot['TypeofAttack'] != 'Free-kick attack')]
            FSaved = Foot[(Foot['Action'] == "Shot on target")&(Foot['TypeofAttack'] != 'Free-kick attack')]
            FSave = Foot[(Foot['Action'] == "Shot blocked")&(Foot['TypeofAttack'] != 'Free-kick attack')]
            FKGoal = Foot[(Foot['Action'] == "Goal")&(Foot['TypeofAttack'] == 'Free-kick attack')]
            FKSaved = Foot[(Foot['Action'] == "Shot on target")&(Foot['TypeofAttack'] == 'Free-kick attack')]
            FKSave = Foot[(Foot['Action'] == "Shot blocked")&(Foot['TypeofAttack'] == 'Free-kick attack')]
            
            norm = TwoSlopeNorm(vmin=0,vcenter=.2,vmax=.7)
            if len(FGoal) > 0:
               plt.scatter(FGoal.GoalX,FGoal.GoalY,
               marker='H',c=FGoal.PSxG, s=500,
               edgecolors="black",zorder=zo+2, cmap='RdYlBu_r', norm=norm, linewidth=.5)
               plt.scatter(FGoal.GoalX,FGoal.GoalY,marker='H',facecolors="none",
               s=750,edgecolors="black",zorder=zo+1, linewidth=.5, norm=norm)
            if len(FSaved) > 0:
               plt.scatter(FSaved.GoalX,FSaved.GoalY,
               marker='H',c=FSaved.PSxG, s=500,linewidths=2,
               edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
            if len(FSave) > 0:
               plt.scatter(FSave.GoalX,FSave.GoalY,
               marker='H',c=FSave.PSxG, s=500, linewidths=2,
               edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
            if len(CGoal) > 0:
               plt.scatter(CGoal.GoalX,CGoal.GoalY,
               marker='^',c=CGoal.PSxG, s=500,
               edgecolors="black",zorder=zo+2, cmap='RdYlBu_r', norm=norm, linewidth=.5)
               plt.scatter(CGoal.GoalX,CGoal.GoalY,marker='^',facecolors="none",
               s=750,edgecolors="black",zorder=zo+1, linewidth=.5, norm=norm)
            if len(CSaved) > 0:
               plt.scatter(CSaved.GoalX,CSaved.GoalY,
               marker='^',c=CSaved.PSxG, s=500,linewidths=2,
               edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
            if len(CSave) > 0:
               plt.scatter(CSave.GoalX,CSave.GoalY,
               marker='^',c=CSave.PSxG, s=500, linewidths=2,
               edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)           
            if len(HGoal) > 0:
               plt.scatter(HGoal.GoalX,HGoal.GoalY,
               marker='o',c=HGoal.PSxG, s=500,
               edgecolors="white",zorder=zo+2, cmap='RdYlBu_r', linewidth=.5, norm=norm)
               plt.scatter(HGoal.GoalX,HGoal.GoalY,marker='o',facecolors="none",
               s=750,edgecolors="black",zorder=zo+1, linewidth=.5, norm=norm)
            if len(HSaved) > 0:
               plt.scatter(HSaved.GoalX,HSaved.GoalY,
               marker='o',c=HSaved.PSxG, s=500, linewidths=2,
               edgecolors="black",zorder=zo, cmap='RdYlBu_r',  norm=norm)
            if len(HSave) > 0:
               plt.scatter(HSave.GoalX,HSave.GoalY,
               marker='o',c=HSave.PSxG, s=500, linewidths=2,
               edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
            if len(FKGoal) > 0:
               plt.scatter(FKGoal.GoalX,FKGoal.GoalY,
               marker='s',c=FKGoal.PSxG, s=500,
               edgecolors="black",zorder=zo+2, cmap='RdYlBu_r', linewidth=.5, norm=norm)
               plt.scatter(FKGoal.GoalX,FKGoal.GoalY,marker='s',facecolors="none",
               s=500,edgecolors="black",zorder=zo+1, linewidth=.5, norm=norm)
            if len(FKSaved) > 0:
               plt.scatter(FKSaved.GoalX,FKSaved.GoalY,
               marker='s',c=FKSaved.PSxG, s=500, linewidths=2,
               edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
            if len(FKSave) > 0:
               plt.scatter(FKSave.GoalX,FKSave.GoalY, 
               marker='s',c=FKSave.PSxG, s=500, linewidths=2,
               edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
               
        GKMap(data, ax2)
        
        
        
        shot_data = Shots[(Shots['ifPen'] != 1)]
        pen_data = Shots[ (Shots['ifPen'] == 1)]
        OP_data = shot_data[(shot_data['TypeofPossession'] == 'Positional attack')]
        CR_data = shot_data[(shot_data['TypeofPossession'] == 'Corner attack')]
        FK_data = shot_data[(shot_data['TypeofPossession'] == 'Free-kick attack')]
        T_data = shot_data[(shot_data['TypeofPossession'] == 'Throw-in attack')]
        CO_data = shot_data[(shot_data['TypeofPossession'] == 'Counter-attack')]
        sog_data = Shots[(Shots['ifPen'] != 1) ]
        sOP_data = sog_data[(sog_data['TypeofPossession'] == 'Positional attack')]
        sCR_data = sog_data[(sog_data['TypeofPossession'] == 'Corner attack')]
        sFK_data = sog_data[(sog_data['TypeofPossession'] == 'Free-kick attack')]
        sT_data = sog_data[(sog_data['TypeofPossession'] == 'Throw-in attack')]
        sCO_data = sog_data[(sog_data['TypeofPossession'] == 'Counter-attack')]
        SP_data = sog_data[(sog_data['ifSP'] == 1)]        
        #SP_data = shot_data[(shot_data['TypeofPossession'] == 'Free-kick attack')or(shot_data['TypeofPossession'] == 'Throw-in attack')or(shot_data['TypeofPossession'] == 'Corner attack')]
        
        ax3 = plt.subplot(gs[1, 1])
        ax3.axis('off')
        ax3.set_xticks([0,1])
        ax3.set_yticks([0,1])
        ax3.scatter(0,0, alpha=0)
        ax3.scatter(1,1,alpha=0)
    
        #ax3.text(0.10,0.85,"Open Play",fontproperties=TableHead,color='white',
         #         horizontalalignment='center', verticalalignment='center', bbox=dict(facecolor='black', alpha=0.5, edgecolor='white', lw=3.5))
        #ax3.text(0.425,0.85,"Counter Attack",fontproperties=TableHead,color='white',
         #        horizontalalignment='center', verticalalignment='center', bbox=dict(facecolor='black', alpha=0.5, edgecolor='white', lw=3.5))
        #ax3.text(0.750,0.85,"Set Pieces",fontproperties=TableHead,color='white',
         #        horizontalalignment='center', verticalalignment='center', bbox=dict(facecolor='black', alpha=0.5, edgecolor='white', lw=3.5))
        #ax3.text(0.10,0.725,str(round(sum(OP_data.xG),2))+' xG\n'+str(round(sum(OP_data.ifGoal),))+' G - '+str(round(sum(OP_data.Shots),))+' S',fontproperties=Labels,
         #         horizontalalignment='center', verticalalignment='center', bbox=dict(facecolor='white', alpha=0.5, edgecolor='white', lw=3.5))
        ax3.text(0.475,1,"Post-Shot xG",fontproperties=TableHead, color='white',
                  horizontalalignment='center', verticalalignment='center', zorder=12)
        ax3.text(0.10,0.9,"Open Play",fontproperties=TableHead, color='white', 
                  horizontalalignment='center', verticalalignment='center', zorder=12)
        ax3.text(0.475,0.9,"Counter Attack",fontproperties=TableHead, color='white',
                  horizontalalignment='center', verticalalignment='center', zorder=12)
        ax3.text(0.85,0.9,"Set Pieces",fontproperties=TableHead, color='white', 
                  horizontalalignment='center', verticalalignment='center', zorder=12)
        ax3.text(0.10,0.725,str(round(sum(sOP_data.PSxG),2))+' PSxG\n'+str(round(sum(sOP_data.ifGoal),))+' G - '+str(round(sum(sOP_data.OnT),))+' S\n'+str(round(sum(sOP_data.PSxG/sum(sOP_data.OnT)),2))+" PSxGpShot",
                 fontproperties=TableNum, color='black',  horizontalalignment='center', verticalalignment='center', zorder=12)
        ax3.text(0.475,0.725,str(round(sum(sCO_data.PSxG),2))+' PSxG\n'+str(round(sum(sCO_data.ifGoal),))+' G - '+str(round(sum(sCO_data.OnT),))+' S\n'+str(round(sum(sCO_data.PSxG/sum(sCO_data.OnT)),2))+" PSxGpShot",
                 fontproperties=TableNum, color='black', horizontalalignment='center', verticalalignment='center', zorder=12)
        ax3.text(0.85,0.725,str(round(sum(SP_data.PSxG),2))+' PSxG\n'+str(round(sum(SP_data.ifGoal),))+' G - '+str(round(sum(SP_data.OnT),))+' S\n'+str(round(sum(SP_data.PSxG/sum(SP_data.OnT)),2))+" PSxGpShot",
                 fontproperties=TableNum, color='black', horizontalalignment='center', verticalalignment='center', zorder=12)

        rec1 = plt.Rectangle((-0.1, .85),1.1,.15,ls='-',color='black',zorder=6,alpha=1)
        rec2 = plt.Rectangle((-0.1, .95),1.1,.15,ls='-',color='black',zorder=6,alpha=1)
        rec3 = plt.Rectangle((-0.1, .6),1.1,.3,ls='-',color='white',zorder=5,alpha=.5)
        ax3.add_artist(rec1)
        ax3.add_artist(rec2)
        ax3.add_artist(rec3)
    
        
        
        
        
        
        ax3.text(0.475,0.35,"Normal xG",fontproperties=TableHead, color='white',
                  horizontalalignment='center', verticalalignment='center', zorder=12)
        ax3.text(0.10,0.25,"Open Play",fontproperties=TableHead, color='white', 
                  horizontalalignment='center', verticalalignment='center', zorder=12)
        ax3.text(0.475,0.25,"Counter Attack",fontproperties=TableHead, color='white', 
                  horizontalalignment='center', verticalalignment='center', zorder=12)
        ax3.text(0.85,0.25,"Set Pieces",fontproperties=TableHead, color='white', 
                  horizontalalignment='center', verticalalignment='center', zorder=12)
        ax3.text(0.10,0.07,str(round(sum(OP_data.xG),2))+' xG\n'+str(round(sum(OP_data.ifGoal),))+' G - '+str(round(sum(OP_data.ifShot),))+' S\n'+str(round(sum(OP_data.xG/sum(OP_data.ifShot)),2))+" xGpShot",
                 fontproperties=TableNum, color='black', horizontalalignment='center', verticalalignment='center', zorder=12)
        ax3.text(0.475,0.07,str(round(sum(CO_data.xG),2))+' xG\n'+str(round(sum(CO_data.ifGoal),))+' G - '+str(round(sum(CO_data.ifShot),))+' S\n'+str(round(sum(CO_data.xG/sum(CO_data.ifShot)),2))+" xGpShot",
                 fontproperties=TableNum, color='black',  horizontalalignment='center', verticalalignment='center', zorder=12)
        ax3.text(0.85,0.07,str(round(sum(SP_data.xG),2))+' xG\n'+str(round(sum(SP_data.ifGoal),))+' G - '+str(round(sum(SP_data.ifShot),))+' S\n'+str(round(sum(SP_data.xG/sum(SP_data.ifShot)),2))+" xGpShot",
                 fontproperties=TableNum, color='black', horizontalalignment='center', verticalalignment='center', zorder=12)
        
        rec1 = plt.Rectangle((-0.1, .2),1.1,.1,ls='-',color='black',zorder=6,alpha=1)
        rec2 = plt.Rectangle((-0.1, .3),1.1,.1,ls='-',color='black',zorder=6,alpha=1)
        rec3 = plt.Rectangle((-0.1, -0.1),1.1,.4,ls='-',color='white',zorder=5,alpha=.5)
        ax3.add_artist(rec1)
        ax3.add_artist(rec2)
        ax3.add_artist(rec3)
    
        
        cax = plt.axes([0.15, 0.065, 0.7, 0.025])
        sm = plt.cm.ScalarMappable(cmap='RdYlBu_r', norm=TwoSlopeNorm(vmin=0,vcenter=.2, vmax=.7))
        sm.A = []
        cbar = fig.colorbar(sm, cax=cax, orientation='horizontal', fraction=0.046, pad=0.04)
        cbar.set_label('xG', fontproperties=TableHead)
        cbar.set_ticks([0, .03, .1, .2, .3, .4, .5, .6, .7])
        cbar.ax.set_xticklabels([0, .03, .1, .2, .3, .4, .5, .6, .7])
        cbar.ax.tick_params(labelsize=20)
        
        fig.text(0.125,0.925,str(season)+' - '+str(team)+' Defending', fontproperties=TeamHead, color='black')
        #fig.text(0.125,0.885,str(match), fontproperties=TableHead, color='black')
        fig.text(0.625,0.925,str(round(sum(shot_data.ifGoal),))+" Goals - "+str(round(sum(shot_data.xG),2))+' xG - '+str(round(sum(sog_data.PSxG),2))+' PSxG',
                 fontproperties=GoalandxG, color='black')
        fig.text(0.7,0.905,str(round(sum(pen_data.xG),2))+' xG - '+str(round(sum(pen_data.ifGoal),))+" Goals - "+str(round(sum(pen_data.ifPen),))+" Penalties",fontproperties=Summary, color='black')
        fig.text(0.7,0.88,str(round(sum(shot_data.ifShot),))+'|'+str(round(sum(shot_data.OnT),))+' S|OnT - '+str(round(sum(shot_data.xG/sum(shot_data.ifShot)),2))+" xGpShot",fontproperties=Summary,color='black')
    
    TeamShotMap(match_df)
    st.pyplot()
    

def PlayerShot(state):
    sm_df = load_sm_data()
    
    team = st.sidebar.multiselect('Select Team(s)', natsorted(sm_df.Team.unique()))
    sm_df = sm_df[(sm_df['Team'].isin(team))]
    
    
    season = st.sidebar.multiselect('Select Season(s)',natsorted(sm_df.Season.unique()))  
    sm_df = sm_df[sm_df['Season'].isin(season)]
    
    shot_df = load_shot_data(season, team, 'no')
    
    player = st.sidebar.multiselect('Select Player(s)', natsorted(shot_df.Player.unique()))
    player_df = shot_df[shot_df['Player'].isin(player)]

    ToPs = (player_df.TypeofPossession.unique()).tolist()
    
    ToP = st.sidebar.multiselect('Select Type of Possession(s)', natsorted(player_df.TypeofPossession.unique()), default=ToPs)  
    ToP_df = player_df[player_df['TypeofPossession'].isin(ToP)]

    Actions = (ToP_df.Action.unique()).tolist()
    
    Action = st.sidebar.multiselect('Select Outcome of Shot(s)', natsorted(ToP_df.Action.unique()), default=Actions)  
    Action_df = ToP_df[ToP_df['Action'].isin(Action)]
    
    ToSs = (Action_df.TypeofShot.unique()).tolist()

    TypeofShot = st.sidebar.multiselect('Select Type of Shot(s)', natsorted(Action_df.TypeofShot.unique()), default=ToSs)  
    ToS_df = Action_df[Action_df['TypeofShot'].isin(TypeofShot)]
    
    matches = (ToS_df.MatchName.unique()).tolist()
    
    match = st.sidebar.multiselect("Select Match(es)", natsorted(ToS_df.MatchName.unique()), default=matches)
    match_df = ToS_df[ToS_df['MatchName'].isin(match)]

    
    st.header("Player Shot Maps")  
    st.subheader("By Matches, By Type of Possession, By Outcome of Shot, By Type of Shot")    
    st.text("")

    
    def TeamShotMap(data):
        Shots = match_df
        figsize1 = 36
        figsize2 = 18
        fig = plt.figure(figsize=(figsize1, figsize2)) 
        gs = gridspec.GridSpec(2, 2, width_ratios=[2., 1.25], wspace=0.05, right=.85)
    
        ax1 = plt.subplot(gs[:, 0])
        verthalf_pitch('#E6E6E6', 'black', ax1)
        def team_shot_map(data):
             shot_data = Shots[(Shots['TypeofPossession'] != 'Penalty attack')]
             stat_data = Shots
             OP_data = shot_data[(shot_data['TypeofPossession'] == 'Positional attack')]
             CR_data = shot_data[(shot_data['TypeofPossession'] == 'Corner attack')]
             FK_data = shot_data[ (shot_data['TypeofPossession'] == 'Free-kick attack')]
             T_data = shot_data[(shot_data['TypeofPossession'] == 'Throw-in attack')]
             CO_data = shot_data[(shot_data['TypeofPossession'] == 'Counter-attack')]
            
            
             Head = shot_data[(shot_data["Body"] == 'Header') & ((shot_data['ifShotFromCarry'] != 1) | ((shot_data['ifShotFromCarry'] == 1) & (shot_data['ifCA'] != 1)))]
             Foot = shot_data[(shot_data["Body"] != 'Header') & ((shot_data['ifShotFromCarry'] != 1) | ((shot_data['ifShotFromCarry'] == 1) & (shot_data['ifCA'] != 1)))]
             Carry = shot_data[(shot_data['ifShotFromCarry'] == 1) & (shot_data['ifCA'] == 1)]
             
             HGoal = Head[Head['Action'] == "Goal"]
             HMissed = Head[Head['Action'] == "Wide shot"]
             HSaved = Head[Head['Action'] == "Shot on target"]
             HBlocked = Head[(Head['Action'] == "Shot blocked by field player")]
             HSave = Head[(Head['Action'] == "Shot blocked")]
             HPost = Head[(Head)['Action'] == "Shot into the bar/post"]
             
             FGoal = Foot[(Foot['Action'] == "Goal")&(Foot['TypeofAttack'] != 'Free-kick attack')]
             FMissed = Foot[(Foot['Action'] == "Wide shot")&(Foot['TypeofAttack'] != 'Free-kick attack')]
             FSaved = Foot[(Foot['Action'] == "Shot on target")&(Foot['TypeofAttack'] != 'Free-kick attack')]
             FBlocked = Foot[(Foot['Action'] == "Shot blocked by field player")&(Foot['TypeofAttack'] != 'Free-kick attack')]
             FSave = Foot[(Foot['Action'] == "Shot blocked")&(Foot['TypeofAttack'] != 'Free-kick attack')]
             FPost = Foot[(Foot['Action'] == "Shot into the bar/post")]
             
             FKGoal = Foot[(Foot['Action'] == "Goal")&(Foot['TypeofAttack'] == 'Free-kick attack')]
             FKMissed = Foot[(Foot['Action'] == "Wide shot")&(Foot['TypeofAttack'] == 'Free-kick attack')]
             FKSaved = Foot[(Foot['Action'] == "Shot on target")&(Foot['TypeofAttack'] == 'Free-kick attack')]
             FKBlocked = Foot[(Foot['Action'] == "Shot blocked by field player")&(Foot['TypeofAttack'] == 'Free-kick attack')]
             FKSave = Foot[(Foot['Action'] == "Shot blocked")&(Foot['TypeofAttack'] == 'Free-kick attack')]
             FKPost = Foot[(Foot['Action'] == "Shot into the bar/post")&(Foot['TypeofAttack'] == 'Free-kick attack')]
             
             CGoal = Carry[(Carry['Action'] == "Goal")&(Carry['TypeofAttack'] != 'Free-kick attack')]
             CMissed = Carry[(Carry['Action'] == "Wide shot")&(Carry['TypeofAttack'] != 'Free-kick attack')]
             CSaved = Carry[(Carry['Action'] == "Shot on target")&(Carry['TypeofAttack'] != 'Free-kick attack')]
             CBlocked = Carry[(Carry['Action'] == "Shot blocked by field player")&(Carry['TypeofAttack'] != 'Free-kick attack')]
             CSave = Carry[(Carry['Action'] == "Shot blocked")&(Carry['TypeofAttack'] != 'Free-kick attack')]
             CPost = Carry[(Carry['Action'] == "Shot into the bar/post")]
    
             
             #draw_pitch("#B2B2B2","white","vertical","half")
             #plt.title(str(Season)+" - "+str(Team)+ " - " +str(Player)+" \n"+str((sum(shot_data.ifGoal)))+" Goals" " - "+str(round(sum(shot_data.xG),2))+" xG \n "+str(sum(stat_data.PenGoal))+" Goals / "+str(sum(stat_data.ifPen))+" Penalties \n "+str((sum(stat_data.Shots)))+" Shots"" - "+str(round(sum(shot_data.xG/sum(shot_data.Shots)),2))+" xG/shot", fontsize=20, weight="bold")
             
             norm = TwoSlopeNorm(vmin=0,vcenter=.2,vmax=.7)
             if len(FGoal) > 0:
                plt.scatter(68-FGoal.Y,FGoal.X,
                marker='H',c=FGoal.xG, s=500,
                edgecolors="black",zorder=zo+2, cmap='RdYlBu_r', norm=norm, linewidth=.5)
                plt.scatter(68-FGoal.Y,FGoal.X,marker='H',c="white",
                s=750,edgecolors="black",zorder=zo+1, linewidth=.5, norm=norm)
             if len(FMissed) > 0:
                plt.scatter(68-FMissed.Y,FMissed.X,marker='H',c=FMissed.xG, facecolors="none", s=500,
                edgecolors="none",zorder=zo, cmap='RdYlBu_r', norm=norm)
             if len(FSaved) > 0:
                plt.scatter(68-FSaved.Y,FSaved.X,
                marker='H',c=FSaved.xG, s=500,linewidths=2,
                edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
             if len(FSave) > 0:
                plt.scatter(68-FSave.Y,FSave.X,
                marker='H',c=FSave.xG, s=500, linewidths=2,
                edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
             if len(FBlocked) > 0:
                plt.scatter(68-FBlocked.Y,FBlocked.X,marker='H',c=FBlocked.xG, facecolors="none", s=500,
                edgecolors="black",zorder=zo, cmap='RdYlBu_r', alpha=.15, norm=norm)
                plt.scatter(68-FBlocked.Y,FBlocked.X,marker='H',facecolors="gray",
                s=500,edgecolors="black",zorder=zo+1, alpha=.15, norm=norm)
             if len(FPost) > 0:
                plt.scatter(68-FPost.Y,FPost.X,marker='H',c=FPost.xG, facecolors="none", s=500,
                edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
             if len(CGoal) > 0:
                plt.scatter(68-CGoal.Y,CGoal.X,
                marker='^',c=CGoal.xG, s=500,
                edgecolors="black",zorder=zo+2, cmap='RdYlBu_r', norm=norm, linewidth=.5)
                plt.scatter(68-CGoal.Y,CGoal.X,marker='^',facecolors="none",
                s=750,edgecolors="black",zorder=zo+1, linewidth=.5, norm=norm)
             if len(CMissed) > 0:
                plt.scatter(68-CMissed.Y,CMissed.X,marker='^',c=CMissed.xG, facecolors="none", s=500,
                edgecolors="none",zorder=zo, cmap='RdYlBu_r', norm=norm)
             if len(CSaved) > 0:
                plt.scatter(68-CSaved.Y,CSaved.X,
                marker='^',c=CSaved.xG, s=500,linewidths=2,
                edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
             if len(CSave) > 0:
                plt.scatter(68-CSave.Y,CSave.X,
                marker='^',c=CSave.xG, s=500, linewidths=2,
                edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
             if len(CBlocked) > 0:
                plt.scatter(68-CBlocked.Y,CBlocked.X,marker='^',c=CBlocked.xG, facecolors="none", s=500,
                edgecolors="black",zorder=zo, cmap='RdYlBu_r', alpha=.15, norm=norm)
                plt.scatter(68-CBlocked.Y,CBlocked.X,marker='^',facecolors="gray",
                s=500,edgecolors="black",zorder=zo+1, alpha=.15, norm=norm)
             if len(CPost) > 0:
                plt.scatter(68-CPost.Y,CPost.X,marker='^',c=CPost.xG, facecolors="none", s=500,
                edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
             if len(HGoal) > 0:
                plt.scatter(68-HGoal.Y,HGoal.X,
                marker='o',c=HGoal.xG, s=500,
                edgecolors="black",zorder=zo+2, cmap='RdYlBu_r', linewidth=.5, norm=norm)
                plt.scatter(68-HGoal.Y,HGoal.X,marker='o',facecolors="none",
                s=750,edgecolors="black",zorder=zo+1, linewidth=.5, norm=norm)
             if len(HMissed) > 0:
                plt.scatter(68-HMissed.Y,HMissed.X,marker='o',c=HMissed.xG, facecolors="none", s=500,
                edgecolors="none",zorder=zo, cmap='RdYlBu_r', norm=norm)
             if len(HSaved) > 0:
                plt.scatter(68-HSaved.Y,HSaved.X,
                marker='o',c=HSaved.xG, s=500, linewidths=2,
                edgecolors="black",zorder=zo, cmap='RdYlBu_r',  norm=norm)
             if len(HSave) > 0:
                plt.scatter(68-HSave.Y,HSave.X,
                marker='o',c=HSave.xG, s=500, linewidths=2,
                edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
             if len(HBlocked) > 0:
                plt.scatter(68-HBlocked.Y,HBlocked.X,marker='H',c=HBlocked.xG, facecolors="none", s=500,
                edgecolors="black",zorder=zo, cmap='RdYlBu_r', alpha=.15, norm=norm)
                plt.scatter(68-HBlocked.Y,HBlocked.X,marker='H',facecolors="gray",
                s=500,edgecolors="black",zorder=zo+1, alpha=.15, norm=norm)
             if len(HPost) > 0:
                plt.scatter(68-HPost.Y,HPost.X,marker='H',c=HPost.xG, facecolors="none", s=500,
                edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
             if len(FKGoal) > 0:
                plt.scatter(68-FKGoal.Y,FKGoal.X,
                marker='s',c=FKGoal.xG, s=500,
                edgecolors="black",zorder=zo+2, cmap='RdYlBu_r', linewidth=.5, norm=norm)
                plt.scatter(68-FKGoal.Y,FKGoal.X,marker='s',facecolors="none",
                s=750,edgecolors="black",zorder=zo+1, linewidth=.5, norm=norm)
             if len(FKMissed) > 0:
                plt.scatter(68-FKMissed.Y,FKMissed.X,marker='s',c=FKMissed.xG, facecolors="none", s=500,
                edgecolors="none",zorder=zo, cmap='RdYlBu_r', norm=norm)
             if len(FKSaved) > 0:
                plt.scatter(68-FKSaved.Y,FKSaved.X,
                marker='s',c=FKSaved.xG, s=500, linewidths=2,
                edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
             if len(FKSave) > 0:
                plt.scatter(68-FKSave.Y,FKSave.X, 
                marker='s',c=FKSave.xG, s=500, linewidths=2,
                edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
             if len(FKBlocked) > 0:
                plt.scatter(68-FKBlocked.Y,FKBlocked.X,marker='s',c=FKBlocked.xG, facecolors="none", s=500,
                edgecolors="black",zorder=zo, cmap='RdYlBu_r',  alpha=.15, norm=norm)
                plt.scatter(68-FKBlocked.Y,FKBlocked.X,marker='s',facecolors="gray",
                s=500,edgecolors="black",zorder=zo+1, alpha=.15, norm=norm)
             if len(FKPost) > 0:
                plt.scatter(68-FKPost.Y,FKPost.X,marker='s',c=FKPost.xG, facecolors="none", s=500,
                edgecolors="black",zorder=zo, cmap='RdYlBu_r', vmin=0, vmax=.7, norm=norm)
               
             plt.scatter(3.5,45, marker='H', facecolor="white", edgecolors="black", s=500, zorder=12)
             plt.scatter(11, 45, marker='o', facecolor="white", edgecolors="black", s=500, zorder=12)
             plt.scatter(18.5, 45, marker='^', facecolor="white", edgecolors="black", s=500, zorder=12)
             plt.scatter(26, 45, marker='s', facecolor="white", edgecolors="black", s=500, zorder=12)
             ax1.text(3.5,42.5,"Foot",fontproperties=Labels,
                      horizontalalignment='center', verticalalignment='center', zorder=12)
             ax1.text(11,42.5,"Header",fontproperties=Labels,
                      horizontalalignment='center', verticalalignment='center', zorder=12)
             ax1.text(18.5,42.5,"Carry",fontproperties=Labels,
                      horizontalalignment='center', verticalalignment='center', zorder=12)
             ax1.text(26,42.5,"FK",fontproperties=Labels,
                      horizontalalignment='center', verticalalignment='center', zorder=12)
            
             plt.scatter(45,45,marker='H',c='white', s=500,
                    edgecolors="black",zorder=zo+2, linewidth=.5)
             plt.scatter(45,45,marker='H',c="white",s=750,
                    edgecolors="black",zorder=zo+1, linewidth=.5)
             plt.scatter(50.5,45, marker='H', c='white', s=500, linewidths=2,
                edgecolors="black",zorder=zo)
             plt.scatter(56,45,marker='H', facecolors="none", s=500,
                edgecolors="black",zorder=zo, alpha=.15)
             plt.scatter(56,45,marker='H',facecolors="gray",
                s=500,edgecolors="black",zorder=zo+1, alpha=.15)
             plt.scatter(61.5,45,marker='H',c='white', facecolors="none", s=500,
                edgecolors="black", linewidths=.25, zorder=zo)
             ax1.text(45,42.5,"Goal",fontproperties=Labels,
                      horizontalalignment='center', verticalalignment='center', zorder=12)
             ax1.text(50.5,42.5,"Save",fontproperties=Labels,
                      horizontalalignment='center', verticalalignment='center', zorder=12)
             ax1.text(56,42.5,"Block",fontproperties=Labels,
                      horizontalalignment='center', verticalalignment='center', zorder=12)
             ax1.text(61.5,42.5,"OffT",fontproperties=Labels,
                      horizontalalignment='center', verticalalignment='center', zorder=12)
             plt.ylim(40,105.5)
             plt.xlim(-.5,68.5)
        
             #a = plt.scatter(-10,-10, marker='H', facecolor="white", edgecolors="black", s=500)
             #b = plt.scatter(-10, -10, marker='o', facecolor="white", edgecolors="black", s=500)
             #c = plt.scatter(-10, -10, marker='^', facecolor="white", edgecolors="black", s=500)
             #plt.legend((a, b, c),("Foot", "Header", "Direct Free Kick"), loc='lower left', title="Types of Shots")
             #plt.annotate('Double Ring = Goal', xy=(18, 47), size = 12, color="black",ha="center")
             #plt.annotate('Black Edge = On Target', xy=(18, 45), size = 12, color="black",ha="center")
             #plt.annotate('No Edge = Off Target', xy=(18, 43), size = 12, color="black",ha="center")
             #plt.annotate('Gray Fill = Blocked', xy=(18, 41), size = 12, color="black",ha="center")
    
        team_shot_map(data)
            
        ax2 = plt.subplot(gs[0, 1])
        def GKMap(data, ax):
            df = Shots[(Shots['ifPen'] != 1) & (Shots['OnT'] == 1)]
            
            ly1 = [-0.1,-0.1,2.5,2.5,-0.1]
            lx1 = [-3.8,3.8,3.8,-3.8,-3.8]
            ax.plot(lx1,ly1,color='black',zorder=5, lw=6)
            ax.plot([-3.8,3.8], [-0.1,-0.1], color='white', zorder=6, lw=8)
            ax.axis('off')
            
            
            Head = df[(df["Body"] == 'Header') & ((df['ifShotFromCarry'] != 1) | ((df['ifShotFromCarry'] == 1) & (df['ifCA'] != 1)))]
            Foot = df[(df["Body"] != 'Header') & ((df['ifShotFromCarry'] != 1) | ((df['ifShotFromCarry'] == 1) & (df['ifCA'] != 1)))]
            Carry = df[(df['ifShotFromCarry'] == 1) & (df['ifCA'] == 1)]
              
            HGoal = Head[Head['Action'] == "Goal"]
            HSaved = Head[Head['Action'] == "Shot on target"]
            HSave = Head[(Head['Action'] == "Shot blocked")]
            CGoal = Carry[Carry['Action'] == "Goal"]
            CSaved = Carry[Carry['Action'] == "Shot on target"]
            CSave = Carry[(Carry['Action'] == "Shot blocked")]
            FGoal = Foot[(Foot['Action'] == "Goal")&(Foot['TypeofAttack'] != 'Free-kick attack')]
            FSaved = Foot[(Foot['Action'] == "Shot on target")&(Foot['TypeofAttack'] != 'Free-kick attack')]
            FSave = Foot[(Foot['Action'] == "Shot blocked")&(Foot['TypeofAttack'] != 'Free-kick attack')]
            FKGoal = Foot[(Foot['Action'] == "Goal")&(Foot['TypeofAttack'] == 'Free-kick attack')]
            FKSaved = Foot[(Foot['Action'] == "Shot on target")&(Foot['TypeofAttack'] == 'Free-kick attack')]
            FKSave = Foot[(Foot['Action'] == "Shot blocked")&(Foot['TypeofAttack'] == 'Free-kick attack')]
            
            norm = TwoSlopeNorm(vmin=0,vcenter=.2,vmax=.7)
            if len(FGoal) > 0:
               plt.scatter(FGoal.GoalX,FGoal.GoalY,
               marker='H',c=FGoal.PSxG, s=500,
               edgecolors="black",zorder=zo+2, cmap='RdYlBu_r', norm=norm, linewidth=.5)
               plt.scatter(FGoal.GoalX,FGoal.GoalY,marker='H',facecolors="none",
               s=750,edgecolors="black",zorder=zo+1, linewidth=.5, norm=norm)
            if len(FSaved) > 0:
               plt.scatter(FSaved.GoalX,FSaved.GoalY,
               marker='H',c=FSaved.PSxG, s=500,linewidths=2,
               edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
            if len(FSave) > 0:
               plt.scatter(FSave.GoalX,FSave.GoalY,
               marker='H',c=FSave.PSxG, s=500, linewidths=2,
               edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
            if len(CGoal) > 0:
               plt.scatter(CGoal.GoalX,CGoal.GoalY,
               marker='^',c=CGoal.PSxG, s=500,
               edgecolors="black",zorder=zo+2, cmap='RdYlBu_r', norm=norm, linewidth=.5)
               plt.scatter(CGoal.GoalX,CGoal.GoalY,marker='^',facecolors="none",
               s=750,edgecolors="black",zorder=zo+1, linewidth=.5, norm=norm)
            if len(CSaved) > 0:
               plt.scatter(CSaved.GoalX,CSaved.GoalY,
               marker='^',c=CSaved.PSxG, s=500,linewidths=2,
               edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
            if len(CSave) > 0:
               plt.scatter(CSave.GoalX,CSave.GoalY,
               marker='^',c=CSave.PSxG, s=500, linewidths=2,
               edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)           
            if len(HGoal) > 0:
               plt.scatter(HGoal.GoalX,HGoal.GoalY,
               marker='o',c=HGoal.PSxG, s=500,
               edgecolors="white",zorder=zo+2, cmap='RdYlBu_r', linewidth=.5, norm=norm)
               plt.scatter(HGoal.GoalX,HGoal.GoalY,marker='o',facecolors="none",
               s=750,edgecolors="black",zorder=zo+1, linewidth=.5, norm=norm)
            if len(HSaved) > 0:
               plt.scatter(HSaved.GoalX,HSaved.GoalY,
               marker='o',c=HSaved.PSxG, s=500, linewidths=2,
               edgecolors="black",zorder=zo, cmap='RdYlBu_r',  norm=norm)
            if len(HSave) > 0:
               plt.scatter(HSave.GoalX,HSave.GoalY,
               marker='o',c=HSave.PSxG, s=500, linewidths=2,
               edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
            if len(FKGoal) > 0:
               plt.scatter(FKGoal.GoalX,FKGoal.GoalY,
               marker='s',c=FKGoal.PSxG, s=500,
               edgecolors="black",zorder=zo+2, cmap='RdYlBu_r', linewidth=.5, norm=norm)
               plt.scatter(FKGoal.GoalX,FKGoal.GoalY,marker='s',facecolors="none",
               s=500,edgecolors="black",zorder=zo+1, linewidth=.5, norm=norm)
            if len(FKSaved) > 0:
               plt.scatter(FKSaved.GoalX,FKSaved.GoalY,
               marker='s',c=FKSaved.PSxG, s=500, linewidths=2,
               edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
            if len(FKSave) > 0:
               plt.scatter(FKSave.GoalX,FKSave.GoalY, 
               marker='s',c=FKSave.PSxG, s=500, linewidths=2,
               edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
               
        GKMap(data, ax2)
        
        
        
        shot_data = Shots[(Shots['ifPen'] != 1)]
        pen_data = Shots[ (Shots['ifPen'] == 1)]
        OP_data = shot_data[(shot_data['TypeofPossession'] == 'Positional attack')]
        CR_data = shot_data[(shot_data['TypeofPossession'] == 'Corner attack')]
        FK_data = shot_data[(shot_data['TypeofPossession'] == 'Free-kick attack')]
        T_data = shot_data[(shot_data['TypeofPossession'] == 'Throw-in attack')]
        CO_data = shot_data[(shot_data['TypeofPossession'] == 'Counter-attack')]
        sog_data = Shots[(Shots['ifPen'] != 1) ]
        sOP_data = sog_data[(sog_data['TypeofPossession'] == 'Positional attack')]
        sCR_data = sog_data[(sog_data['TypeofPossession'] == 'Corner attack')]
        sFK_data = sog_data[(sog_data['TypeofPossession'] == 'Free-kick attack')]
        sT_data = sog_data[(sog_data['TypeofPossession'] == 'Throw-in attack')]
        sCO_data = sog_data[(sog_data['TypeofPossession'] == 'Counter-attack')]
        SP_data = sog_data[(sog_data['ifSP'] == 1)]        
        #SP_data = shot_data[(shot_data['TypeofPossession'] == 'Free-kick attack')or(shot_data['TypeofPossession'] == 'Throw-in attack')or(shot_data['TypeofPossession'] == 'Corner attack')]
        
        ax3 = plt.subplot(gs[1, 1])
        ax3.axis('off')
        ax3.set_xticks([0,1])
        ax3.set_yticks([0,1])
        ax3.scatter(0,0, alpha=0)
        ax3.scatter(1,1,alpha=0)
    
        #ax3.text(0.10,0.85,"Open Play",fontproperties=TableHead,color='white',
         #         horizontalalignment='center', verticalalignment='center', bbox=dict(facecolor='black', alpha=0.5, edgecolor='white', lw=3.5))
        #ax3.text(0.425,0.85,"Counter Attack",fontproperties=TableHead,color='white',
         #        horizontalalignment='center', verticalalignment='center', bbox=dict(facecolor='black', alpha=0.5, edgecolor='white', lw=3.5))
        #ax3.text(0.750,0.85,"Set Pieces",fontproperties=TableHead,color='white',
         #        horizontalalignment='center', verticalalignment='center', bbox=dict(facecolor='black', alpha=0.5, edgecolor='white', lw=3.5))
        #ax3.text(0.10,0.725,str(round(sum(OP_data.xG),2))+' xG\n'+str(round(sum(OP_data.ifGoal),))+' G - '+str(round(sum(OP_data.Shots),))+' S',fontproperties=Labels,
         #         horizontalalignment='center', verticalalignment='center', bbox=dict(facecolor='white', alpha=0.5, edgecolor='white', lw=3.5))
        ax3.text(0.475,1,"Post-Shot xG",fontproperties=TableHead, color='white',
                  horizontalalignment='center', verticalalignment='center', zorder=12)
        ax3.text(0.10,0.9,"Open Play",fontproperties=TableHead, color='white', 
                  horizontalalignment='center', verticalalignment='center', zorder=12)
        ax3.text(0.475,0.9,"Counter Attack",fontproperties=TableHead, color='white',
                  horizontalalignment='center', verticalalignment='center', zorder=12)
        ax3.text(0.85,0.9,"Set Pieces",fontproperties=TableHead, color='white', 
                  horizontalalignment='center', verticalalignment='center', zorder=12)
        ax3.text(0.10,0.725,str(round(sum(sOP_data.PSxG),2))+' PSxG\n'+str(round(sum(sOP_data.ifGoal),))+' G - '+str(round(sum(sOP_data.OnT),))+' S\n'+str(round(sum(sOP_data.PSxG/sum(sOP_data.OnT)),2))+" PSxGpShot",
                 fontproperties=TableNum, color='black',  horizontalalignment='center', verticalalignment='center', zorder=12)
        ax3.text(0.475,0.725,str(round(sum(sCO_data.PSxG),2))+' PSxG\n'+str(round(sum(sCO_data.ifGoal),))+' G - '+str(round(sum(sCO_data.OnT),))+' S\n'+str(round(sum(sCO_data.PSxG/sum(sCO_data.OnT)),2))+" PSxGpShot",
                 fontproperties=TableNum, color='black', horizontalalignment='center', verticalalignment='center', zorder=12)
        ax3.text(0.85,0.725,str(round(sum(SP_data.PSxG),2))+' PSxG\n'+str(round(sum(SP_data.ifGoal),))+' G - '+str(round(sum(SP_data.OnT),))+' S\n'+str(round(sum(SP_data.PSxG/sum(SP_data.OnT)),2))+" PSxGpShot",
                 fontproperties=TableNum, color='black', horizontalalignment='center', verticalalignment='center', zorder=12)

        rec1 = plt.Rectangle((-0.1, .85),1.1,.15,ls='-',color='black',zorder=6,alpha=1)
        rec2 = plt.Rectangle((-0.1, .95),1.1,.15,ls='-',color='black',zorder=6,alpha=1)
        rec3 = plt.Rectangle((-0.1, .6),1.1,.3,ls='-',color='white',zorder=5,alpha=.5)
        ax3.add_artist(rec1)
        ax3.add_artist(rec2)
        ax3.add_artist(rec3)
    
        
        
        
        
        
        ax3.text(0.475,0.35,"Normal xG",fontproperties=TableHead, color='white',
                  horizontalalignment='center', verticalalignment='center', zorder=12)
        ax3.text(0.10,0.25,"Open Play",fontproperties=TableHead, color='white', 
                  horizontalalignment='center', verticalalignment='center', zorder=12)
        ax3.text(0.475,0.25,"Counter Attack",fontproperties=TableHead, color='white', 
                  horizontalalignment='center', verticalalignment='center', zorder=12)
        ax3.text(0.85,0.25,"Set Pieces",fontproperties=TableHead, color='white', 
                  horizontalalignment='center', verticalalignment='center', zorder=12)
        ax3.text(0.10,0.07,str(round(sum(OP_data.xG),2))+' xG\n'+str(round(sum(OP_data.ifGoal),))+' G - '+str(round(sum(OP_data.ifShot),))+' S\n'+str(round(sum(OP_data.xG/sum(OP_data.ifShot)),2))+" xGpShot",
                 fontproperties=TableNum, color='black', horizontalalignment='center', verticalalignment='center', zorder=12)
        ax3.text(0.475,0.07,str(round(sum(CO_data.xG),2))+' xG\n'+str(round(sum(CO_data.ifGoal),))+' G - '+str(round(sum(CO_data.ifShot),))+' S\n'+str(round(sum(CO_data.xG/sum(CO_data.ifShot)),2))+" xGpShot",
                 fontproperties=TableNum, color='black',  horizontalalignment='center', verticalalignment='center', zorder=12)
        ax3.text(0.85,0.07,str(round(sum(SP_data.xG),2))+' xG\n'+str(round(sum(SP_data.ifGoal),))+' G - '+str(round(sum(SP_data.ifShot),))+' S\n'+str(round(sum(SP_data.xG/sum(SP_data.ifShot)),2))+" xGpShot",
                 fontproperties=TableNum, color='black', horizontalalignment='center', verticalalignment='center', zorder=12)
        
        rec1 = plt.Rectangle((-0.1, .2),1.1,.1,ls='-',color='black',zorder=6,alpha=1)
        rec2 = plt.Rectangle((-0.1, .3),1.1,.1,ls='-',color='black',zorder=6,alpha=1)
        rec3 = plt.Rectangle((-0.1, -0.1),1.1,.4,ls='-',color='white',zorder=5,alpha=.5)
        ax3.add_artist(rec1)
        ax3.add_artist(rec2)
        ax3.add_artist(rec3)
    
        
        cax = plt.axes([0.15, 0.065, 0.7, 0.025])
        sm = plt.cm.ScalarMappable(cmap='RdYlBu_r', norm=TwoSlopeNorm(vmin=0,vcenter=.2, vmax=.7))
        sm.A = []
        cbar = fig.colorbar(sm, cax=cax, orientation='horizontal', fraction=0.046, pad=0.04)
        cbar.set_label('xG', fontproperties=TableHead)
        cbar.set_ticks([0, .03, .1, .2, .3, .4, .5, .6, .7])
        cbar.ax.set_xticklabels([0, .03, .1, .2, .3, .4, .5, .6, .7])
        cbar.ax.tick_params(labelsize=20)
        
        fig.text(0.125,0.925,str(player), fontproperties=TeamHead, color='black')
        fig.text(0.125,0.9,str(season)+' - '+str(team), color='black',fontproperties=Subtitle)
        #fig.text(0.125,0.875,str(season), fontproperties=GoalandxG, color='black')
        fig.text(0.625,0.925,str(round(sum(shot_data.ifGoal),))+" Goals - "+str(round(sum(shot_data.xG),2))+' xG - '+str(round(sum(sog_data.PSxG),2))+' PSxG',
                 fontproperties=GoalandxG, color='black')
        fig.text(0.7,0.905,str(round(sum(pen_data.xG),2))+' xG - '+str(round(sum(pen_data.ifGoal),))+" Goals - "+str(round(sum(pen_data.ifPen),))+" Penalties",fontproperties=Summary, color='black')
        fig.text(0.7,0.88,str(round(sum(shot_data.ifShot),))+'|'+str(round(sum(shot_data.OnT),))+' S|OnT - '+str(round(sum(shot_data.xG/sum(shot_data.ifShot)),2))+" xGpShot",fontproperties=Summary,color='black')
    
    TeamShotMap(match_df)
    st.pyplot()
    
    
def GKShotMap(state):
    sm_df = load_sm_data()
    
    team = st.sidebar.multiselect('Select Team(s)', natsorted(sm_df.Team.unique()))
    sm_df = sm_df[(sm_df['Team'].isin(team))]
    
    
    season = st.sidebar.multiselect('Select Season(s)',natsorted(sm_df.Season.unique()))  
    sm_df = sm_df[sm_df['Season'].isin(season)]
    
    shot_df = load_shot_data(season, team, 'yes')
    
    player = st.sidebar.multiselect('Select Player(s)', natsorted(shot_df.Teammate.unique()))
    player_df = shot_df[(shot_df['Teammate'].isin(player)) & (shot_df['OnT'] == 1)]

    ToPs = (player_df.TypeofPossession.unique()).tolist()
    
    ToP = st.sidebar.multiselect('Select Type of Possession(s)', natsorted(player_df.TypeofPossession.unique()), default=ToPs)  
    ToP_df = player_df[player_df['TypeofPossession'].isin(ToP)]

    Actions = (ToP_df.Action.unique()).tolist()
    
    Action = st.sidebar.multiselect('Select Outcome of Shot(s)', natsorted(ToP_df.Action.unique()), default=Actions)  
    Action_df = ToP_df[ToP_df['Action'].isin(Action)]
    
    ToSs = (Action_df.TypeofShot.unique()).tolist()

    TypeofShot = st.sidebar.multiselect('Select Type of Shot(s)', natsorted(Action_df.TypeofShot.unique()), default=ToSs)  
    ToS_df = Action_df[Action_df['TypeofShot'].isin(TypeofShot)]
    
    matches = (ToS_df.MatchName.unique()).tolist()
    
    match = st.sidebar.multiselect("Select Match(es)", natsorted(ToS_df.MatchName.unique()), default=matches)
    match_df = ToS_df[ToS_df['MatchName'].isin(match)]

    st.header("Goalkeeper Shot Maps")  
    #st.subheader("Heat Maps by Zones")    
    st.text("")

 
    figsize1 = 36
    figsize2 = 18
    fig = plt.figure(figsize=(figsize1, figsize2)) 
    gs = gridspec.GridSpec(2, 2, width_ratios=[2., 1.25], left=.15, right=1, wspace=0.05)

    ax1 = plt.subplot(gs[:, 0])
    verthalf_pitch('#E6E6E6', 'black', ax1)
    def player_shot_map(data):
         shot_data = match_df[(match_df['TypeofPossession'] != 'Penalty attack') & (match_df['OnT'] == 1)]
         stat_data = match_df[(match_df['OnT'] == 1)]
         OP_data = shot_data[ (shot_data['TypeofPossession'] == 'Positional attack')]
         CR_data = shot_data[(shot_data['TypeofPossession'] == 'Corner attack')]
         FK_data = shot_data[ (shot_data['TypeofPossession'] == 'Free-kick attack')]
         T_data = shot_data[(shot_data['TypeofPossession'] == 'Throw-in attack')]
         CO_data = shot_data[(shot_data['TypeofPossession'] == 'Counter-attack')]
        
        
         Head = shot_data[(shot_data["Body"] == 'Header') & ((shot_data['ifShotFromCarry'] != 1) | ((shot_data['ifShotFromCarry'] == 1) & (shot_data['ifCA'] != 1)))]
         Foot = shot_data[(shot_data["Body"] != 'Header') & ((shot_data['ifShotFromCarry'] != 1) | ((shot_data['ifShotFromCarry'] == 1) & (shot_data['ifCA'] != 1)))]
         Carry = shot_data[(shot_data['ifShotFromCarry'] == 1) & (shot_data['ifCA'] == 1)]
         
         HGoal = Head[Head['Action'] == "Goal"]
         HMissed = Head[Head['Action'] == "Wide shot"]
         HSaved = Head[Head['Action'] == "Shot on target"]
         HBlocked = Head[(Head['Action'] == "Shot blocked by field player")]
         HSave = Head[(Head['Action'] == "Shot blocked")]
         HPost = Head[(Head)['Action'] == "Shot into the bar/post"]
         
         FGoal = Foot[(Foot['Action'] == "Goal")&(Foot['TypeofAttack'] != 'Free-kick attack')]
         FMissed = Foot[(Foot['Action'] == "Wide shot")&(Foot['TypeofAttack'] != 'Free-kick attack')]
         FSaved = Foot[(Foot['Action'] == "Shot on target")&(Foot['TypeofAttack'] != 'Free-kick attack')]
         FBlocked = Foot[(Foot['Action'] == "Shot blocked by field player")&(Foot['TypeofAttack'] != 'Free-kick attack')]
         FSave = Foot[(Foot['Action'] == "Shot blocked")&(Foot['TypeofAttack'] != 'Free-kick attack')]
         FPost = Foot[(Foot['Action'] == "Shot into the bar/post")]
         
         FKGoal = Foot[(Foot['Action'] == "Goal")&(Foot['TypeofAttack'] == 'Free-kick attack')]
         FKMissed = Foot[(Foot['Action'] == "Wide shot")&(Foot['TypeofAttack'] == 'Free-kick attack')]
         FKSaved = Foot[(Foot['Action'] == "Shot on target")&(Foot['TypeofAttack'] == 'Free-kick attack')]
         FKBlocked = Foot[(Foot['Action'] == "Shot blocked by field player")&(Foot['TypeofAttack'] == 'Free-kick attack')]
         FKSave = Foot[(Foot['Action'] == "Shot blocked")&(Foot['TypeofAttack'] == 'Free-kick attack')]
         FKPost = Foot[(Foot['Action'] == "Shot into the bar/post")&(Foot['TypeofAttack'] == 'Free-kick attack')]
         
         CGoal = Carry[(Carry['Action'] == "Goal")&(Carry['TypeofAttack'] != 'Free-kick attack')]
         CMissed = Carry[(Carry['Action'] == "Wide shot")&(Carry['TypeofAttack'] != 'Free-kick attack')]
         CSaved = Carry[(Carry['Action'] == "Shot on target")&(Carry['TypeofAttack'] != 'Free-kick attack')]
         CBlocked = Carry[(Carry['Action'] == "Shot blocked by field player")&(Carry['TypeofAttack'] != 'Free-kick attack')]
         CSave = Carry[(Carry['Action'] == "Shot blocked")&(Carry['TypeofAttack'] != 'Free-kick attack')]
         CPost = Carry[(Carry['Action'] == "Shot into the bar/post")]

         
         #draw_pitch("#B2B2B2","white","vertical","half")
         #plt.title(str(Season)+" - "+str(Team)+ " - " +str(Player)+" \n"+str((sum(shot_data.ifGoal)))+" Goals" " - "+str(round(sum(shot_data.xG),2))+" xG \n "+str(sum(stat_data.PenGoal))+" Goals / "+str(sum(stat_data.ifPen))+" Penalties \n "+str((sum(stat_data.Shots)))+" Shots"" - "+str(round(sum(shot_data.xG/sum(shot_data.Shots)),2))+" xG/shot", fontsize=20, weight="bold")
         
         norm = TwoSlopeNorm(vmin=0,vcenter=.2,vmax=.7)
         if len(FGoal) > 0:
           plt.scatter(68-FGoal.Y,FGoal.X,
           marker='H',c=FGoal.xG, s=500,
           edgecolors="black",zorder=zo+2, cmap='RdYlBu_r', norm=norm, linewidth=.5)
           plt.scatter(68-FGoal.Y,FGoal.X,marker='H',c="white",
           s=750,edgecolors="black",zorder=zo+1, linewidth=.5, norm=norm)
         if len(FMissed) > 0:
            plt.scatter(68-FMissed.Y,FMissed.X,marker='H',c=FMissed.xG, facecolors="none", s=500,
            edgecolors="none",zorder=zo, cmap='RdYlBu_r', norm=norm)
         if len(FSaved) > 0:
            plt.scatter(68-FSaved.Y,FSaved.X,
            marker='H',c=FSaved.xG, s=500,linewidths=2,
            edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
         if len(FSave) > 0:
            plt.scatter(68-FSave.Y,FSave.X,
            marker='H',c=FSave.xG, s=500, linewidths=2,
            edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
         if len(FBlocked) > 0:
            plt.scatter(68-FBlocked.Y,FBlocked.X,marker='H',c=FBlocked.xG, facecolors="none", s=500,
            edgecolors="black",zorder=zo, cmap='RdYlBu_r', alpha=.15, norm=norm)
            plt.scatter(68-FBlocked.Y,FBlocked.X,marker='H',facecolors="gray",
            s=500,edgecolors="black",zorder=zo+1, alpha=.15, norm=norm)
         if len(FPost) > 0:
            plt.scatter(68-FPost.Y,FPost.X,marker='H',c=FPost.xG, facecolors="none", s=500,
            edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
         if len(CGoal) > 0:
           plt.scatter(68-CGoal.Y,CGoal.X,
           marker='^',c=CGoal.xG, s=500,
           edgecolors="black",zorder=zo+2, cmap='RdYlBu_r', norm=norm, linewidth=1.5)
           plt.scatter(68-CGoal.Y,CGoal.X,marker='^',facecolors="none",
           s=750,edgecolors="black",zorder=zo+1, linewidth=.5, norm=norm)
         if len(CMissed) > 0:
            plt.scatter(68-CMissed.Y,CMissed.X,marker='^',c=CMissed.xG, facecolors="none", s=500,
            edgecolors="none",zorder=zo, cmap='RdYlBu_r', norm=norm)
         if len(CSaved) > 0:
            plt.scatter(68-CSaved.Y,CSaved.X,
            marker='^',c=CSaved.xG, s=500,linewidths=2,
            edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
         if len(CSave) > 0:
            plt.scatter(68-CSave.Y,CSave.X,
            marker='^',c=CSave.xG, s=500, linewidths=2,
            edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
         if len(CBlocked) > 0:
            plt.scatter(68-CBlocked.Y,CBlocked.X,marker='^',c=CBlocked.xG, facecolors="none", s=500,
            edgecolors="black",zorder=zo, cmap='RdYlBu_r', alpha=.15, norm=norm)
            plt.scatter(68-CBlocked.Y,CBlocked.X,marker='^',facecolors="gray",
            s=500,edgecolors="black",zorder=zo+1, alpha=.15, norm=norm)
         if len(CPost) > 0:
            plt.scatter(68-CPost.Y,CPost.X,marker='^',c=CPost.xG, facecolors="none", s=500,
            edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
         if len(HGoal) > 0:
           plt.scatter(68-HGoal.Y,HGoal.X,
           marker='o',c=HGoal.xG, s=500,
           edgecolors="black",zorder=zo+2, cmap='RdYlBu_r', linewidth=.5, norm=norm)
           plt.scatter(68-HGoal.Y,HGoal.X,marker='o',facecolors="none",
           s=750,edgecolors="black",zorder=zo+1, linewidth=.5, norm=norm)
         if len(HMissed) > 0:
            plt.scatter(68-HMissed.Y,HMissed.X,marker='o',c=HMissed.xG, facecolors="none", s=500,
            edgecolors="none",zorder=zo, cmap='RdYlBu_r', norm=norm)
         if len(HSaved) > 0:
            plt.scatter(68-HSaved.Y,HSaved.X,
            marker='o',c=HSaved.xG, s=500, linewidths=2,
            edgecolors="black",zorder=zo, cmap='RdYlBu_r',  norm=norm)
         if len(HSave) > 0:
            plt.scatter(68-HSave.Y,HSave.X,
            marker='o',c=HSave.xG, s=500, linewidths=2,
            edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
         if len(HBlocked) > 0:
            plt.scatter(68-HBlocked.Y,HBlocked.X,marker='H',c=HBlocked.xG, facecolors="none", s=500,
            edgecolors="black",zorder=zo, cmap='RdYlBu_r', alpha=.15, norm=norm)
            plt.scatter(68-HBlocked.Y,HBlocked.X,marker='H',facecolors="gray",
            s=500,edgecolors="black",zorder=zo+1, alpha=.15, norm=norm)
         if len(HPost) > 0:
            plt.scatter(68-HPost.Y,HPost.X,marker='H',c=HPost.xG, facecolors="none", s=500,
            edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
         if len(FKGoal) > 0:
           plt.scatter(68-FKGoal.Y,FKGoal.X,
           marker='s',c=FKGoal.xG, s=500,
           edgecolors="black",zorder=zo+2, cmap='RdYlBu_r', linewidth=.5, norm=norm)
           plt.scatter(68-FKGoal.Y,FKGoal.X,marker='s',facecolors="none",
           s=750,edgecolors="black",zorder=zo+1, linewidth=.5, norm=norm)
         if len(FKMissed) > 0:
            plt.scatter(68-FKMissed.Y,FKMissed.X,marker='s',c=FKMissed.xG, facecolors="none", s=500,
            edgecolors="none",zorder=zo, cmap='RdYlBu_r', norm=norm)
         if len(FKSaved) > 0:
            plt.scatter(68-FKSaved.Y,FKSaved.X,
            marker='s',c=FKSaved.xG, s=500, linewidths=2,
            edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
         if len(FKSave) > 0:
            plt.scatter(68-FKSave.Y,FKSave.X, 
            marker='s',c=FKSave.xG, s=500, linewidths=2,
            edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
         if len(FKBlocked) > 0:
            plt.scatter(68-FKBlocked.Y,FKBlocked.X,marker='s',c=FKBlocked.xG, facecolors="none", s=500,
            edgecolors="black",zorder=zo, cmap='RdYlBu_r',  alpha=.15, norm=norm)
            plt.scatter(68-FKBlocked.Y,FKBlocked.X,marker='s',facecolors="gray",
            s=500,edgecolors="black",zorder=zo+1, alpha=.15, norm=norm)
         if len(FKPost) > 0:
            plt.scatter(68-FKPost.Y,FKPost.X,marker='s',c=FKPost.xG, facecolors="none", s=500,
            edgecolors="black",zorder=zo, cmap='RdYlBu_r', vmin=0, vmax=.7, norm=norm)
           
         plt.scatter(3.5,45, marker='H', facecolor="white", edgecolors="black", s=500, zorder=12)
         plt.scatter(11, 45, marker='o', facecolor="white", edgecolors="black", s=500, zorder=12)
         plt.scatter(18.5, 45, marker='^', facecolor="white", edgecolors="black", s=500, zorder=12)
         plt.scatter(26, 45, marker='s', facecolor="white", edgecolors="black", s=500, zorder=12)
         ax1.text(3.5,42.5,"Foot",fontproperties=Labels,
                  horizontalalignment='center', verticalalignment='center', zorder=12)
         ax1.text(11,42.5,"Header",fontproperties=Labels,
                  horizontalalignment='center', verticalalignment='center', zorder=12)
         ax1.text(18.5,42.5,"Carry",fontproperties=Labels,
                  horizontalalignment='center', verticalalignment='center', zorder=12)
         ax1.text(26,42.5,"FK",fontproperties=Labels,
                  horizontalalignment='center', verticalalignment='center', zorder=12)

        
         plt.scatter(45,45,marker='H',c='white', s=500,
                edgecolors="white",zorder=zo+2, linewidth=3.5)
         plt.scatter(45,45,marker='H',facecolors="none",
                s=500,edgecolors="black",zorder=zo+3, linewidth=.5)
         plt.scatter(50.5,45, marker='H', c='white', s=500, linewidths=2,
            edgecolors="black",zorder=zo)
         plt.scatter(56,45,marker='H', facecolors="none", s=500,
            edgecolors="black",zorder=zo, alpha=.15)
         plt.scatter(56,45,marker='H',facecolors="gray",
            s=500,edgecolors="black",zorder=zo+1, alpha=.15)
         plt.scatter(61.5,45,marker='H',c='white', facecolors="none", s=500,
            edgecolors="none",zorder=zo)
         ax1.text(45,42.5,"Goal",fontproperties=Labels,
                  horizontalalignment='center', verticalalignment='center', zorder=12)
         ax1.text(50.5,42.5,"Save",fontproperties=Labels,
                  horizontalalignment='center', verticalalignment='center', zorder=12)
         ax1.text(56,42.5,"Block",fontproperties=Labels,
                  horizontalalignment='center', verticalalignment='center', zorder=12)
         ax1.text(61.5,42.5,"OffT",fontproperties=Labels,
                  horizontalalignment='center', verticalalignment='center', zorder=12)
         plt.ylim(40,105.5)
         plt.xlim(-.5,68.5)



         #a = plt.scatter(-10,-10, marker='H', facecolor="white", edgecolors="black", s=500)
         #b = plt.scatter(-10, -10, marker='o', facecolor="white", edgecolors="black", s=500)
         #c = plt.scatter(-10, -10, marker='^', facecolor="white", edgecolors="black", s=500)
         #plt.legend((a, b, c),("Foot", "Header", "Direct Free Kick"), loc='lower left', title="Types of Shots")
         #plt.annotate('Double Ring = Goal', xy=(18, 47), size = 12, color="black",ha="center")
         #plt.annotate('Black Edge = On Target', xy=(18, 45), size = 12, color="black",ha="center")
         #plt.annotate('No Edge = Off Target', xy=(18, 43), size = 12, color="black",ha="center")
         #plt.annotate('Gray Fill = Blocked', xy=(18, 41), size = 12, color="black",ha="center")

    player_shot_map(match_df)
        
    ax2 = plt.subplot(gs[1, 1])
    def GKMap(data):
        df = match_df[(match_df['ifPen'] != 1) & (match_df['OnT'] == 1)]
        
        ly1 = [-0.1,-0.1,2.5,2.5,-0.1]
        lx1 = [-3.8,3.8,3.8,-3.8,-3.8]
        ax2.plot(lx1,ly1,color='black',zorder=5, lw=4)
        ax2.plot([-3.8,3.8], [-0.1,-0.1], color='white', zorder=6, lw=5)
        ax2.axis('off')
        
        Head = df[(df["Body"] == 'Header') & ((df['ifShotFromCarry'] != 1) | ((df['ifShotFromCarry'] == 1) & (df['ifCA'] != 1)))]
        Foot = df[(df["Body"] != 'Header') & ((df['ifShotFromCarry'] != 1) | ((df['ifShotFromCarry'] == 1) & (df['ifCA'] != 1)))]
        Carry = df[(df['ifShotFromCarry'] == 1) & (df['ifCA'] == 1)]
         
        HGoal = Head[Head['Action'] == "Goal"]
        HSaved = Head[Head['Action'] == "Shot on target"]
        HSave = Head[(Head['Action'] == "Shot blocked")]
        CGoal = Carry[Carry['Action'] == "Goal"]
        CSaved = Carry[Carry['Action'] == "Shot on target"]
        CSave = Carry[(Carry['Action'] == "Shot blocked")]
        FGoal = Foot[(Foot['Action'] == "Goal")&(Foot['TypeofAttack'] != 'Free-kick attack')]
        FSaved = Foot[(Foot['Action'] == "Shot on target")&(Foot['TypeofAttack'] != 'Free-kick attack')]
        FSave = Foot[(Foot['Action'] == "Shot blocked")&(Foot['TypeofAttack'] != 'Free-kick attack')]
        FKGoal = Foot[(Foot['Action'] == "Goal")&(Foot['TypeofAttack'] == 'Free-kick attack')]
        FKSaved = Foot[(Foot['Action'] == "Shot on target")&(Foot['TypeofAttack'] == 'Free-kick attack')]
        FKSave = Foot[(Foot['Action'] == "Shot blocked")&(Foot['TypeofAttack'] == 'Free-kick attack')]
        
        norm = TwoSlopeNorm(vmin=0,vcenter=.2,vmax=.7)
        if len(FGoal) > 0:
          plt.scatter(FGoal.GoalX,FGoal.GoalY,
          marker='H',c=FGoal.xG, s=500,
          edgecolors="black",zorder=zo+2, cmap='RdYlBu_r', norm=norm, linewidth=.5)
          plt.scatter(FGoal.GoalX,FGoal.GoalY,marker='H',c="white",
          s=750,edgecolors="black",zorder=zo+1, linewidth=.5, norm=norm)
        if len(FSaved) > 0:
           plt.scatter(FSaved.GoalX,FSaved.GoalY,
           marker='H',c=FSaved.xG, s=500,linewidths=2,
           edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
        if len(FSave) > 0:
           plt.scatter(FSave.GoalX,FSave.GoalY,
           marker='H',c=FSave.xG, s=500, linewidths=2,
           edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
        if len(CGoal) > 0:
          plt.scatter(CGoal.GoalX,CGoal.GoalY,
          marker='^',c=CGoal.xG, s=500,
          edgecolors="black",zorder=zo+2, cmap='RdYlBu_r', norm=norm, linewidth=.5)
          plt.scatter(CGoal.GoalX,CGoal.GoalY,marker='^',facecolors="none",
          s=750,edgecolors="black",zorder=zo+1, linewidth=.5, norm=norm)
        if len(CSaved) > 0:
           plt.scatter(CSaved.GoalX,CSaved.GoalY,
           marker='^',c=CSaved.xG, s=500,linewidths=2,
           edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
        if len(CSave) > 0:
           plt.scatter(CSave.GoalX,CSave.GoalY,
           marker='^',c=CSave.xG, s=500, linewidths=2,
           edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
        if len(HGoal) > 0:
          plt.scatter(HGoal.GoalX,HGoal.GoalY,
          marker='o',c=HGoal.xG, s=500,
          edgecolors="black",zorder=zo+2, cmap='RdYlBu_r', linewidth=.5, norm=norm)
          plt.scatter(HGoal.GoalX,HGoal.GoalY,marker='o',facecolors="none",
          s=750,edgecolors="black",zorder=zo+1, linewidth=.5, norm=norm)
        if len(HSaved) > 0:
           plt.scatter(HSaved.GoalX,HSaved.GoalY,
           marker='o',c=HSaved.xG, s=500, linewidths=2,
           edgecolors="black",zorder=zo, cmap='RdYlBu_r',  norm=norm)
        if len(HSave) > 0:
           plt.scatter(HSave.GoalX,HSave.GoalY,
           marker='o',c=HSave.xG, s=500, linewidths=2,
           edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
        if len(FKGoal) > 0:
          plt.scatter(FKGoal.GoalX,FKGoal.GoalY,
          marker='s',c=FKGoal.xG, s=500,
          edgecolors="black",zorder=zo+2, cmap='RdYlBu_r', linewidth=.5, norm=norm)
          plt.scatter(FKGoal.GoalX,FKGoal.GoalY,marker='s',facecolors="none",
          s=750,edgecolors="black",zorder=zo+1, linewidth=.5, norm=norm)
        if len(FKSaved) > 0:
           plt.scatter(FKSaved.GoalX,FKSaved.GoalY,
           marker='s',c=FKSaved.xG, s=500, linewidths=2,
           edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
        if len(FKSave) > 0:
           plt.scatter(FKSave.GoalX,FKSave.GoalY, 
           marker='s',c=FKSave.xG, s=500, linewidths=2,
           edgecolors="black",zorder=zo, cmap='RdYlBu_r', norm=norm)
    GKMap(match_df)
    
    
    
    shot_data = match_df[(match_df['ifPen'] != 1) & (match_df['OnT'] == 1)]
    pen_data = match_df[(match_df['ifPen'] == 1)]
    OP_data = shot_data[ (shot_data['TypeofPossession'] == 'Positional attack')]
    CR_data = shot_data[(shot_data['TypeofPossession'] == 'Corner attack')]
    FK_data = shot_data[(shot_data['TypeofPossession'] == 'Free-kick attack')]
    T_data = shot_data[(shot_data['TypeofPossession'] == 'Throw-in attack')]
    CO_data = shot_data[(shot_data['TypeofPossession'] == 'Counter-attack')]
    sog_data = match_df[(match_df['ifPen'] != 1)]
    sOP_data = sog_data[(sog_data['TypeofPossession'] == 'Positional attack')]
    sCR_data = sog_data[(sog_data['TypeofPossession'] == 'Corner attack')]
    sFK_data = sog_data[(sog_data['TypeofPossession'] == 'Free-kick attack')]
    sT_data = sog_data[(sog_data['TypeofPossession'] == 'Throw-in attack')]
    sCO_data = sog_data[ (sog_data['TypeofPossession'] == 'Counter-attack')]
    #SP_data = shot_data[(shot_data['TypeofPossession'] == 'Free-kick attack')or(shot_data['TypeofPossession'] == 'Throw-in attack')or(shot_data['TypeofPossession'] == 'Corner attack')]
    
    ax3 = plt.subplot(gs[0, 1])
    ax3.axis('off')
    ax3.set_xticks([0,1])
    ax3.set_yticks([0,1])
    ax3.scatter(0,0, alpha=0)
    ax3.scatter(1,1,alpha=0)

    #ax3.text(0.10,0.85,"Open Play",fontproperties=TableHead,color='white',
     #         horizontalalignment='center', verticalalignment='center', bbox=dict(facecolor='black', alpha=0.5, edgecolor='white', lw=3.5))
    #ax3.text(0.425,0.85,"Counter Attack",fontproperties=TableHead,color='white',
     #        horizontalalignment='center', verticalalignment='center', bbox=dict(facecolor='black', alpha=0.5, edgecolor='white', lw=3.5))
    #ax3.text(0.750,0.85,"Set Pieces",fontproperties=TableHead,color='white',
     #        horizontalalignment='center', verticalalignment='center', bbox=dict(facecolor='black', alpha=0.5, edgecolor='white', lw=3.5))
    #ax3.text(0.10,0.725,str(round(sum(OP_data.xG),2))+' xG\n'+str(round(sum(OP_data.ifGoal),))+' G - '+str(round(sum(OP_data.Shots),))+' S',fontproperties=Labels,
     #         horizontalalignment='center', verticalalignment='center', bbox=dict(facecolor='white', alpha=0.5, edgecolor='white', lw=3.5))
    ax3.text(0.475,.35,"Post-Shot xG",fontproperties=TableHead,color='white',
              horizontalalignment='center', verticalalignment='center', zorder=12)
    ax3.text(0.10,.25,"Open Play",fontproperties=TableHead,color='white',
              horizontalalignment='center', verticalalignment='center', zorder=12)
    ax3.text(0.475,0.25,"Counter Attack",fontproperties=TableHead,color='white',
              horizontalalignment='center', verticalalignment='center', zorder=12)
    ax3.text(0.85,0.25,"Set Pieces",fontproperties=TableHead,color='white',
              horizontalalignment='center', verticalalignment='center', zorder=12)
    ax3.text(0.10,0.07,str(round(sum(sOP_data.PSxG),2))+' xG\n'+str(round(sum(sOP_data.ifGoal),))+' G - '+str(round(sum(sOP_data.OnT),))+' S\n'+str(round(sum(sOP_data.xG/sum(sOP_data.OnT)),2))+" xG/shot",
             fontproperties=TableNum, horizontalalignment='center', verticalalignment='center', zorder=12)
    ax3.text(0.475,0.07,str(round(sum(sCO_data.PSxG),2))+' xG\n'+str(round(sum(sCO_data.ifGoal),))+' G - '+str(round(sum(sCO_data.OnT),))+' S\n'+str(round(sum(CO_data.xG/sum(sCO_data.OnT)),2))+" xG/shot",
             fontproperties=TableNum, horizontalalignment='center', verticalalignment='center', zorder=12)
    ax3.text(0.85,0.07,str(round(sum(sCR_data.PSxG)+sum(sFK_data.PSxG)+sum(sT_data.PSxG),2))+" xG\n"+str(sum(sCR_data.ifGoal)+sum(sFK_data.ifGoal)+sum(sT_data.ifGoal))+" G - "+str(round(sum(sCR_data.OnT)+sum(sFK_data.OnT)+sum(sT_data.OnT),))+" S\n"+str(round(sum((sCR_data.PSxG+sum(sFK_data.PSxG)+sum(sT_data.PSxG))/sum(sCR_data.OnT+sum(sFK_data.OnT)+sum(sT_data.OnT))),2))+" xG/shot",
             fontproperties=TableNum, horizontalalignment='center', verticalalignment='center', zorder=12)
    
    rec1 = plt.Rectangle((-0.1, .2),1.1,.1,ls='-',color='black',zorder=6,alpha=1)
    rec2 = plt.Rectangle((-0.1, .3),1.1,.1,ls='-',color='black',zorder=6,alpha=1)
    rec3 = plt.Rectangle((-0.1, -0.1),1.1,.4,ls='-',color='white',zorder=5,alpha=.5)
    ax3.add_artist(rec1)
    ax3.add_artist(rec2)
    ax3.add_artist(rec3)

    
    
    

    cax = plt.axes([0.2, 0.05, 0.75, 0.025])
    sm = plt.cm.ScalarMappable(cmap='RdYlBu_r', norm=TwoSlopeNorm(vmin=0,vcenter=.2, vmax=.7))
    sm.A = []
    cbar = fig.colorbar(sm, cax=cax, orientation='horizontal', fraction=0.046, pad=0.04)
    cbar.set_label('xG', weight="bold", size=30, family='fantasy')
    cbar.set_ticks([0, .03, .1, .2, .3, .4, .5, .6, .7])
    cbar.ax.set_xticklabels([0, .03, .1, .2, .3, .4, .5, .6, .7])
    cbar.ax.tick_params(labelsize=20)
    
    fig.text(0.15,0.93,str(player),fontproperties=TeamHead)
    fig.text(0.15,0.9,str(season)+' - '+str(team),fontproperties=TableHead)
    
    fig.text(0.725,0.93,str(round(sum(shot_data.PSxG) - (sum(shot_data.ifGoal)),2))+' GSAA - '+str(round(((sum(shot_data.Save) / (sum(shot_data.OnT)))- (sum(shot_data.xS)) / (sum(shot_data.OnT))),2)*100)+" aSV%", fontproperties=GoalandxG)
    fig.text(0.77,0.90,str(round(sum(shot_data.Save),2))+' Saves - '+str(round(sum(shot_data.xS),2))+' xS',fontproperties=Summary)
    fig.text(0.78,0.87,str(round(sum(shot_data.PSxG),2))+' PSxG - '+str(round(sum(shot_data.ifGoal),2))+' G',fontproperties=Summary)
    fig.text(0.74,0.84,str(round(sum(pen_data.PSxG),2))+' xG - '+str(sum(pen_data.ifGoal))+" Goals - "+str(sum(pen_data.ifPen))+" Penalties",fontproperties=Summary)
    fig.text(0.77,0.81,str(round(sum(shot_data.ifShot),2))+' S - '+str(round(sum(shot_data.xG/sum(shot_data.ifShot)),2))+" xG/shot",fontproperties=Summary)

    st.pyplot()
    
    
def TeamPassingEngine(state):
    sm_df = load_sm_data()
    
    team = st.sidebar.multiselect('Select Team(s)', natsorted(sm_df.Team.unique()))
    sm_df = sm_df[sm_df['Team'].isin(team)]
    
    
    season = st.sidebar.multiselect('Select Season(s)',natsorted(sm_df.Season.unique()))  
    sm_df = sm_df[sm_df['Season'].isin(season)]
    
    pass_df = load_pass_data(season, team, 'no')
    
    matches = (pass_df.MatchName.unique()).tolist()
    
    match = st.sidebar.multiselect("Select Match(es)", natsorted(pass_df.MatchName.unique()), default=matches)
    match_df = pass_df[pass_df['MatchName'].isin(match)]
    
    zone = st.sidebar.selectbox('Select Start Zone', natsorted(match_df.Zone.unique()))  
    zone_df = match_df[match_df['Zone'] == zone]


    st.header("Team Passes From/To Pitch Zones")  
    st.subheader("Passes From Zone, Passes to Zones")    
    st.text("")


    fig,ax = plt.subplots(figsize=(32,18))
    plt.title(str(season)+' - '+str(team)+" Passing from Start Zone "+str(zone), fontproperties=headers, color="black")

    def numbers():
        ax.annotate(25 ,xy=(94.5, 64), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(24 ,xy=(94.5, 49), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(23 ,xy=(94.5, 34), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(22 ,xy=(94.5, 20), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(21 ,xy=(94.5, 4), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(20 ,xy=(73.5, 64), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(19 ,xy=(73.5, 49), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(18 ,xy=(73.5, 34), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(17 ,xy=(73.5, 20), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(16 ,xy=(73.5, 4), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(15 ,xy=(52.5, 64), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(14 ,xy=(52.5, 49), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(13 ,xy=(52.5, 34), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(12 ,xy=(52.5, 20), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(11 ,xy=(52.5, 4), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(10 ,xy=(31.5, 64), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(9 ,xy=(31.5, 49), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(8 ,xy=(31.5, 34), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(7 ,xy=(31.5, 20), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(6 ,xy=(31.5, 4), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(5 ,xy=(10.5, 64), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(4 ,xy=(10.5, 49), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(3 ,xy=(10.5, 34), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(2 ,xy=(10.5, 20), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(1 ,xy=(10.5, 4), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)

    numbers()
    
    zo=12
    def draw_pitch(pitch, line): 
    # side and goal lines #
        ly1 = [0,0,68,68,0]
        lx1 = [0,105,105,0,0]
        
        ax.plot(lx1,ly1,color=line,zorder=5)
        
        
        # boxes, 6 yard box and goals
        
            #outer boxes#
        ly2 = [15.3,15.3,52.7,52.7] 
        lx2 = [105,89.25,89.25,105]
        ax.plot(lx2,ly2,color=line,zorder=5)
        
        ly3 = [15.3,15.3,52.7,52.7]  
        lx3 = [0,15.75,15.75,0]
        ax.plot(lx3,ly3,color=line,zorder=5)
        
            #goals#
        ly4 = [30.6,30.6,37.4,37.4]
        lx4 = [105,105.2,105.2,105]
        ax.plot(lx4,ly4,color=line,zorder=5)
        
        ly5 = [30.6,30.6,37.4,37.4]
        lx5 = [0,-0.2,-0.2,0]
        ax.plot(lx5,ly5,color=line,zorder=5)
        
        
           #6 yard boxes#
        ly6 = [25.5,25.5,42.5,42.5]
        lx6 = [105,99.75,99.75,105]
        ax.plot(lx6,ly6,color=line,zorder=5)
        
        ly7 = [25.5,25.5,42.5,42.5]
        lx7 = [0,5.25,5.25,0]
        ax.plot(lx7,ly7,color=line,zorder=5)
        
        #Halfway line, penalty spots, and kickoff spot
        ly8 = [0,68] 
        lx8 = [52.5,52.5]
        ax.plot(lx8,ly8,color=line,zorder=5)
        
        
        ax.scatter(94.5,34,color=line,zorder=5, s=12)
        ax.scatter(10.5,34,color=line,zorder=5, s=12)
        ax.scatter(52.5,34,color=line,zorder=5, s=12)
        
        arc1 =  Arc((95.25,34),height=18.3,width=18.3,angle=0,theta1=130,theta2=230,color=line,zorder=zo+1)
        arc2 = Arc((9.75,34),height=18.3,width=18.3,angle=0,theta1=310,theta2=50,color=line,zorder=zo+1)
        circle1 = plt.Circle((52.5, 34), 9.15,ls='solid',lw=1.5,color=line, fill=False, zorder=2,alpha=1)
        
        ## Rectangles in boxes
        rec1 = plt.Rectangle((89.25,20), 16,30,ls='-',color=pitch, zorder=1,alpha=1)
        rec2 = plt.Rectangle((0, 20), 16.5,30,ls='-',color=pitch, zorder=1,alpha=1)
        
        ## Pitch rectangle
        rec3 = plt.Rectangle((-5, -5), 115,78,ls='-',color=pitch, zorder=1,alpha=1)
        
        ## Add Direction of Play Arrow
        DoP = ax.arrow(1.5, 1.5, 18-2, 1-1, head_width=1.2,
            head_length=1.2,
            color=line,
            alpha=1,
            length_includes_head=True, zorder=12, width=.3)
        
        ax.add_artist(rec3)
        ax.add_artist(arc1)
        ax.add_artist(arc2)
        ax.add_artist(rec1)
        ax.add_artist(rec2)
        ax.add_artist(circle1)
        ax.add_artist(DoP)
        ax.axis('off')
    draw_pitch('#B2B2B2', 'black')
    plt.xlim(-.5,105.5)
    plt.ylim(-.5,68.5)
    
    #df = season_df
    df = zone_df[zone_df['ifSP'] != 1]
    df = df.groupby(["Zone", "DestZone"], as_index=False).agg({
        "ifPass": 'sum', 'ifComplete': 'sum', 'xP':'sum', 'MatchID':'nunique',
        "X":'mean', 'Y':'mean', 'DestX':'mean', 'DestY':'mean'}).sort_values(by='ifPass', ascending=False)

    xS = df["X"]
    yS = df["Y"]
    xE = df["DestX"]
    yE = df["DestY"]

    #opta/mckeever blue hex code #2f3653 & #82868f
    #plt.title(str(Season)+' - '+str(Player)+' - xA Map', color='white', size=30, weight='bold')
    
    norm = TwoSlopeNorm(vmin=df.ifPass.min(),vcenter=df.ifPass.mean(),vmax=df.ifPass.max())
    for i in range(len(df)):
        plt.annotate('',xy=(xS.iloc[i], yS.iloc[i]), xycoords='data', xytext=(xE.iloc[i], yE.iloc[i]),textcoords='data',
                   arrowprops=dict(arrowstyle='wedge', connectionstyle='arc3', color='#333333', lw=5))
        plt.scatter(xE.iloc[i], yE.iloc[i],zorder=zo+2,c=df.ifPass.iloc[i], 
                    cmap="RdYlBu_r", edgecolor='white', marker='o', linewidths=7.5, 
                    s=df.ifPass.iloc[i]*75, norm=norm)
        plt.scatter(xE.iloc[i],yE.iloc[i],marker='o',facecolors="none",
            s=df.ifPass.iloc[i]*75,edgecolors="black",zorder=zo+3, linewidth=1.5, norm=norm)

    
    cax = plt.axes([0.175, 0.065, 0.675, 0.025])
    sm = plt.cm.ScalarMappable(cmap='RdYlBu_r', norm=TwoSlopeNorm(vmin=df.ifPass.min(),vcenter=df.ifPass.mean(),vmax=df.ifPass.max()))
    sm.A = []
    cbar = fig.colorbar(sm, cax=cax, orientation='horizontal', fraction=0.046, pad=0.04)
    cbar.set_label('Number of Pases', fontproperties=TableHead)
    cbar.ax.tick_params(labelsize=20)

        
    st.pyplot()
    
    destzone = st.sidebar.selectbox('Select Destination Zone', natsorted(match_df.DestZone.unique()))  
    destzone_df = match_df[match_df['DestZone'] == destzone]


    fig,ax = plt.subplots(figsize=(32,18))
    plt.title(str(season)+' - '+str(team)+" Passing to Destination Zone "+str(destzone), fontproperties=headers, color="black")

    def numbers():
        ax.annotate(25 ,xy=(94.5, 64), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(24 ,xy=(94.5, 49), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(23 ,xy=(94.5, 34), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(22 ,xy=(94.5, 20), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(21 ,xy=(94.5, 4), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(20 ,xy=(73.5, 64), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(19 ,xy=(73.5, 49), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(18 ,xy=(73.5, 34), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(17 ,xy=(73.5, 20), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(16 ,xy=(73.5, 4), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(15 ,xy=(52.5, 64), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(14 ,xy=(52.5, 49), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(13 ,xy=(52.5, 34), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(12 ,xy=(52.5, 20), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(11 ,xy=(52.5, 4), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(10 ,xy=(31.5, 64), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(9 ,xy=(31.5, 49), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(8 ,xy=(31.5, 34), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(7 ,xy=(31.5, 20), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(6 ,xy=(31.5, 4), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(5 ,xy=(10.5, 64), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(4 ,xy=(10.5, 49), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(3 ,xy=(10.5, 34), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(2 ,xy=(10.5, 20), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(1 ,xy=(10.5, 4), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)

    numbers()
    
    zo=12
    def draw_pitch(pitch, line): 
    # side and goal lines #
        ly1 = [0,0,68,68,0]
        lx1 = [0,105,105,0,0]
        
        ax.plot(lx1,ly1,color=line,zorder=5)
        
        
        # boxes, 6 yard box and goals
        
            #outer boxes#
        ly2 = [15.3,15.3,52.7,52.7] 
        lx2 = [105,89.25,89.25,105]
        ax.plot(lx2,ly2,color=line,zorder=5)
        
        ly3 = [15.3,15.3,52.7,52.7]  
        lx3 = [0,15.75,15.75,0]
        ax.plot(lx3,ly3,color=line,zorder=5)
        
            #goals#
        ly4 = [30.6,30.6,37.4,37.4]
        lx4 = [105,105.2,105.2,105]
        ax.plot(lx4,ly4,color=line,zorder=5)
        
        ly5 = [30.6,30.6,37.4,37.4]
        lx5 = [0,-0.2,-0.2,0]
        ax.plot(lx5,ly5,color=line,zorder=5)
        
        
           #6 yard boxes#
        ly6 = [25.5,25.5,42.5,42.5]
        lx6 = [105,99.75,99.75,105]
        ax.plot(lx6,ly6,color=line,zorder=5)
        
        ly7 = [25.5,25.5,42.5,42.5]
        lx7 = [0,5.25,5.25,0]
        ax.plot(lx7,ly7,color=line,zorder=5)
        
        #Halfway line, penalty spots, and kickoff spot
        ly8 = [0,68] 
        lx8 = [52.5,52.5]
        ax.plot(lx8,ly8,color=line,zorder=5)
        
        
        ax.scatter(94.5,34,color=line,zorder=5, s=12)
        ax.scatter(10.5,34,color=line,zorder=5, s=12)
        ax.scatter(52.5,34,color=line,zorder=5, s=12)
        
        arc1 =  Arc((95.25,34),height=18.3,width=18.3,angle=0,theta1=130,theta2=230,color=line,zorder=zo+1)
        arc2 = Arc((9.75,34),height=18.3,width=18.3,angle=0,theta1=310,theta2=50,color=line,zorder=zo+1)
        circle1 = plt.Circle((52.5, 34), 9.15,ls='solid',lw=1.5,color=line, fill=False, zorder=2,alpha=1)
        
        ## Rectangles in boxes
        rec1 = plt.Rectangle((89.25,20), 16,30,ls='-',color=pitch, zorder=1,alpha=1)
        rec2 = plt.Rectangle((0, 20), 16.5,30,ls='-',color=pitch, zorder=1,alpha=1)
        
        ## Pitch rectangle
        rec3 = plt.Rectangle((-5, -5), 115,78,ls='-',color=pitch, zorder=1,alpha=1)
        
        ## Add Direction of Play Arrow
        DoP = ax.arrow(1.5, 1.5, 18-2, 1-1, head_width=1.2,
            head_length=1.2,
            color=line,
            alpha=1,
            length_includes_head=True, zorder=12, width=.3)
        
        ax.add_artist(rec3)
        ax.add_artist(arc1)
        ax.add_artist(arc2)
        ax.add_artist(rec1)
        ax.add_artist(rec2)
        ax.add_artist(circle1)
        ax.add_artist(DoP)
        ax.axis('off')
    draw_pitch('#B2B2B2', 'black')
    plt.xlim(-.5,105.5)
    plt.ylim(-.5,68.5)
    
    #df = season_df
    df = destzone_df[destzone_df['ifSP'] != 1]
    df = df.groupby(["Zone", "DestZone"], as_index=False).agg({
        "ifPass": 'sum', 'ifComplete': 'sum', 'xP':'sum', 'MatchID':'nunique',
        "X":'mean', 'Y':'mean', 'DestX':'mean', 'DestY':'mean'}).sort_values(by='ifPass', ascending=False)

    xS = df["X"]
    yS = df["Y"]
    xE = df["DestX"]
    yE = df["DestY"]

    #opta/mckeever blue hex code #2f3653 & #82868f
    #plt.title(str(Season)+' - '+str(Player)+' - xA Map', color='white', size=30, weight='bold')
    
    norm = TwoSlopeNorm(vmin=df.ifPass.min(),vcenter=df.ifPass.mean(),vmax=df.ifPass.max())
    for i in range(len(df)):
        plt.annotate('',xy=(xS.iloc[i], yS.iloc[i]), xycoords='data', xytext=(xE.iloc[i], yE.iloc[i]),textcoords='data',
                   arrowprops=dict(arrowstyle='wedge', connectionstyle='arc3', color='#333333', lw=5))
        plt.scatter(xS.iloc[i], yS.iloc[i],zorder=zo+2,c=df.ifPass.iloc[i], 
                    cmap="RdYlBu_r", edgecolor='white', marker='o', linewidths=7.5, 
                    s=df.ifPass.iloc[i]*75, norm=norm)
        plt.scatter(xS.iloc[i],yS.iloc[i],marker='o',facecolors="none",
            s=df.ifPass.iloc[i]*75,edgecolors="black",zorder=zo+3, linewidth=1.5, norm=norm)

    
    cax = plt.axes([0.175, 0.065, 0.675, 0.025])
    sm = plt.cm.ScalarMappable(cmap='RdYlBu_r', norm=TwoSlopeNorm(vmin=df.ifPass.min(),vcenter=df.ifPass.mean(),vmax=df.ifPass.max()))
    sm.A = []
    cbar = fig.colorbar(sm, cax=cax, orientation='horizontal', fraction=0.046, pad=0.04)
    cbar.set_label('Number of Pases', fontproperties=TableHead)
    cbar.ax.tick_params(labelsize=20)

        
    st.pyplot()

def PlayerPassingEngine(state):
    sm_df = load_sm_data()
    
    team = st.sidebar.multiselect('Select Team(s)', natsorted(sm_df.Team.unique()))
    sm_df = sm_df[sm_df['Team'].isin(team)]
    
    
    season = st.sidebar.multiselect('Select Season(s)',natsorted(sm_df.Season.unique()))  
    sm_df = sm_df[sm_df['Season'].isin(season)]
    
    pass_df = load_pass_data(season, team, 'no')
    
    player = st.sidebar.multiselect('Select Player(s)', natsorted(pass_df.Player.unique()))
    player_df = pass_df[pass_df['Player'].isin(player)]

    matches = (player_df.MatchName.unique()).tolist()
    
    match = st.sidebar.multiselect("Select Match(es)", natsorted(player_df.MatchName.unique()), default=matches)
    match_df = player_df[player_df['MatchName'].isin(match)]
    
    zone = st.sidebar.selectbox('Select Start Zone', natsorted(match_df.Zone.unique()))  
    zone_df = match_df[match_df['Zone'] == zone]


    st.header("Player Passes From/To Pitch Zones")  
    st.subheader("Passes From Zone, Passes to Zones")    
    st.text("")


    fig,ax = plt.subplots(figsize=(32,18))
    plt.title(str(season)+' - '+str(player)+" Passing from Start Zone "+str(zone), fontproperties=headers, color="black")

    def numbers():
        ax.annotate(25 ,xy=(94.5, 64), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(24 ,xy=(94.5, 49), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(23 ,xy=(94.5, 34), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(22 ,xy=(94.5, 20), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(21 ,xy=(94.5, 4), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(20 ,xy=(73.5, 64), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(19 ,xy=(73.5, 49), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(18 ,xy=(73.5, 34), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(17 ,xy=(73.5, 20), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(16 ,xy=(73.5, 4), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(15 ,xy=(52.5, 64), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(14 ,xy=(52.5, 49), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(13 ,xy=(52.5, 34), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(12 ,xy=(52.5, 20), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(11 ,xy=(52.5, 4), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(10 ,xy=(31.5, 64), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(9 ,xy=(31.5, 49), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(8 ,xy=(31.5, 34), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(7 ,xy=(31.5, 20), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(6 ,xy=(31.5, 4), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(5 ,xy=(10.5, 64), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(4 ,xy=(10.5, 49), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(3 ,xy=(10.5, 34), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(2 ,xy=(10.5, 20), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(1 ,xy=(10.5, 4), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)

    numbers()
    
    zo=12
    def draw_pitch(pitch, line): 
    # side and goal lines #
        ly1 = [0,0,68,68,0]
        lx1 = [0,105,105,0,0]
        
        ax.plot(lx1,ly1,color=line,zorder=5)
        
        
        # boxes, 6 yard box and goals
        
            #outer boxes#
        ly2 = [15.3,15.3,52.7,52.7] 
        lx2 = [105,89.25,89.25,105]
        ax.plot(lx2,ly2,color=line,zorder=5)
        
        ly3 = [15.3,15.3,52.7,52.7]  
        lx3 = [0,15.75,15.75,0]
        ax.plot(lx3,ly3,color=line,zorder=5)
        
            #goals#
        ly4 = [30.6,30.6,37.4,37.4]
        lx4 = [105,105.2,105.2,105]
        ax.plot(lx4,ly4,color=line,zorder=5)
        
        ly5 = [30.6,30.6,37.4,37.4]
        lx5 = [0,-0.2,-0.2,0]
        ax.plot(lx5,ly5,color=line,zorder=5)
        
        
           #6 yard boxes#
        ly6 = [25.5,25.5,42.5,42.5]
        lx6 = [105,99.75,99.75,105]
        ax.plot(lx6,ly6,color=line,zorder=5)
        
        ly7 = [25.5,25.5,42.5,42.5]
        lx7 = [0,5.25,5.25,0]
        ax.plot(lx7,ly7,color=line,zorder=5)
        
        #Halfway line, penalty spots, and kickoff spot
        ly8 = [0,68] 
        lx8 = [52.5,52.5]
        ax.plot(lx8,ly8,color=line,zorder=5)
        
        
        ax.scatter(94.5,34,color=line,zorder=5, s=12)
        ax.scatter(10.5,34,color=line,zorder=5, s=12)
        ax.scatter(52.5,34,color=line,zorder=5, s=12)
        
        arc1 =  Arc((95.25,34),height=18.3,width=18.3,angle=0,theta1=130,theta2=230,color=line,zorder=zo+1)
        arc2 = Arc((9.75,34),height=18.3,width=18.3,angle=0,theta1=310,theta2=50,color=line,zorder=zo+1)
        circle1 = plt.Circle((52.5, 34), 9.15,ls='solid',lw=1.5,color=line, fill=False, zorder=2,alpha=1)
        
        ## Rectangles in boxes
        rec1 = plt.Rectangle((89.25,20), 16,30,ls='-',color=pitch, zorder=1,alpha=1)
        rec2 = plt.Rectangle((0, 20), 16.5,30,ls='-',color=pitch, zorder=1,alpha=1)
        
        ## Pitch rectangle
        rec3 = plt.Rectangle((-5, -5), 115,78,ls='-',color=pitch, zorder=1,alpha=1)
        
        ## Add Direction of Play Arrow
        DoP = ax.arrow(1.5, 1.5, 18-2, 1-1, head_width=1.2,
            head_length=1.2,
            color=line,
            alpha=1,
            length_includes_head=True, zorder=12, width=.3)
        
        ax.add_artist(rec3)
        ax.add_artist(arc1)
        ax.add_artist(arc2)
        ax.add_artist(rec1)
        ax.add_artist(rec2)
        ax.add_artist(circle1)
        ax.add_artist(DoP)
        ax.axis('off')
    draw_pitch('#B2B2B2', 'black')
    plt.xlim(-.5,105.5)
    plt.ylim(-.5,68.5)
    
    #df = season_df
    df = zone_df[zone_df['ifSP'] != 1]
    df = df.groupby(["Zone", "DestZone"], as_index=False).agg({
        "ifPass": 'sum', 'ifComplete': 'sum', 'xP':'sum', 'MatchID':'nunique',
        "X":'mean', 'Y':'mean', 'DestX':'mean', 'DestY':'mean'}).sort_values(by='ifPass', ascending=False)

    xS = df["X"]
    yS = df["Y"]
    xE = df["DestX"]
    yE = df["DestY"]

    #opta/mckeever blue hex code #2f3653 & #82868f
    #plt.title(str(Season)+' - '+str(Player)+' - xA Map', color='white', size=30, weight='bold')
    
    norm = TwoSlopeNorm(vmin=df.ifPass.min(),vcenter=df.ifPass.mean(),vmax=df.ifPass.max())
    for i in range(len(df)):
        plt.annotate('',xy=(xS.iloc[i], yS.iloc[i]), xycoords='data', xytext=(xE.iloc[i], yE.iloc[i]),textcoords='data',
                   arrowprops=dict(arrowstyle='wedge', connectionstyle='arc3', color='#333333', lw=5))
        plt.scatter(xE.iloc[i], yE.iloc[i],zorder=zo+2,c=df.ifPass.iloc[i], 
                    cmap="RdYlBu_r", edgecolor='white', marker='o', linewidths=7.5, 
                    s=df.ifPass.iloc[i]*75, norm=norm)
        plt.scatter(xE.iloc[i],yE.iloc[i],marker='o',facecolors="none",
            s=df.ifPass.iloc[i]*75,edgecolors="black",zorder=zo+3, linewidth=1.5, norm=norm)

    
    cax = plt.axes([0.175, 0.065, 0.675, 0.025])
    sm = plt.cm.ScalarMappable(cmap='RdYlBu_r', norm=TwoSlopeNorm(vmin=df.ifPass.min(),vcenter=df.ifPass.mean(),vmax=df.ifPass.max()))
    sm.A = []
    cbar = fig.colorbar(sm, cax=cax, orientation='horizontal', fraction=0.046, pad=0.04)
    cbar.set_label('Number of Pases', fontproperties=TableHead)
    cbar.ax.tick_params(labelsize=20)

        
    st.pyplot()
    
    destzone = st.sidebar.selectbox('Select Destination Zone', natsorted(match_df.DestZone.unique()))  
    destzone_df = match_df[match_df['DestZone'] == destzone]


    fig,ax = plt.subplots(figsize=(32,18))
    plt.title(str(season)+' - '+str(player)+" Passing to Destination Zone "+str(destzone), fontproperties=headers, color="black")

    def numbers():
        ax.annotate(25 ,xy=(94.5, 64), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(24 ,xy=(94.5, 49), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(23 ,xy=(94.5, 34), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(22 ,xy=(94.5, 20), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(21 ,xy=(94.5, 4), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(20 ,xy=(73.5, 64), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(19 ,xy=(73.5, 49), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(18 ,xy=(73.5, 34), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(17 ,xy=(73.5, 20), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(16 ,xy=(73.5, 4), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(15 ,xy=(52.5, 64), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(14 ,xy=(52.5, 49), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(13 ,xy=(52.5, 34), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(12 ,xy=(52.5, 20), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(11 ,xy=(52.5, 4), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(10 ,xy=(31.5, 64), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(9 ,xy=(31.5, 49), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(8 ,xy=(31.5, 34), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(7 ,xy=(31.5, 20), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(6 ,xy=(31.5, 4), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(5 ,xy=(10.5, 64), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(4 ,xy=(10.5, 49), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(3 ,xy=(10.5, 34), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(2 ,xy=(10.5, 20), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)
        ax.annotate(1 ,xy=(10.5, 4), color="black", ha="center", zorder=20, fontproperties=PitchNumbers, alpha=.2)

    numbers()
    
    zo=12
    def draw_pitch(pitch, line): 
    # side and goal lines #
        ly1 = [0,0,68,68,0]
        lx1 = [0,105,105,0,0]
        
        ax.plot(lx1,ly1,color=line,zorder=5)
        
        
        # boxes, 6 yard box and goals
        
            #outer boxes#
        ly2 = [15.3,15.3,52.7,52.7] 
        lx2 = [105,89.25,89.25,105]
        ax.plot(lx2,ly2,color=line,zorder=5)
        
        ly3 = [15.3,15.3,52.7,52.7]  
        lx3 = [0,15.75,15.75,0]
        ax.plot(lx3,ly3,color=line,zorder=5)
        
            #goals#
        ly4 = [30.6,30.6,37.4,37.4]
        lx4 = [105,105.2,105.2,105]
        ax.plot(lx4,ly4,color=line,zorder=5)
        
        ly5 = [30.6,30.6,37.4,37.4]
        lx5 = [0,-0.2,-0.2,0]
        ax.plot(lx5,ly5,color=line,zorder=5)
        
        
           #6 yard boxes#
        ly6 = [25.5,25.5,42.5,42.5]
        lx6 = [105,99.75,99.75,105]
        ax.plot(lx6,ly6,color=line,zorder=5)
        
        ly7 = [25.5,25.5,42.5,42.5]
        lx7 = [0,5.25,5.25,0]
        ax.plot(lx7,ly7,color=line,zorder=5)
        
        #Halfway line, penalty spots, and kickoff spot
        ly8 = [0,68] 
        lx8 = [52.5,52.5]
        ax.plot(lx8,ly8,color=line,zorder=5)
        
        
        ax.scatter(94.5,34,color=line,zorder=5, s=12)
        ax.scatter(10.5,34,color=line,zorder=5, s=12)
        ax.scatter(52.5,34,color=line,zorder=5, s=12)
        
        arc1 =  Arc((95.25,34),height=18.3,width=18.3,angle=0,theta1=130,theta2=230,color=line,zorder=zo+1)
        arc2 = Arc((9.75,34),height=18.3,width=18.3,angle=0,theta1=310,theta2=50,color=line,zorder=zo+1)
        circle1 = plt.Circle((52.5, 34), 9.15,ls='solid',lw=1.5,color=line, fill=False, zorder=2,alpha=1)
        
        ## Rectangles in boxes
        rec1 = plt.Rectangle((89.25,20), 16,30,ls='-',color=pitch, zorder=1,alpha=1)
        rec2 = plt.Rectangle((0, 20), 16.5,30,ls='-',color=pitch, zorder=1,alpha=1)
        
        ## Pitch rectangle
        rec3 = plt.Rectangle((-5, -5), 115,78,ls='-',color=pitch, zorder=1,alpha=1)
        
        ## Add Direction of Play Arrow
        DoP = ax.arrow(1.5, 1.5, 18-2, 1-1, head_width=1.2,
            head_length=1.2,
            color=line,
            alpha=1,
            length_includes_head=True, zorder=12, width=.3)
        
        ax.add_artist(rec3)
        ax.add_artist(arc1)
        ax.add_artist(arc2)
        ax.add_artist(rec1)
        ax.add_artist(rec2)
        ax.add_artist(circle1)
        ax.add_artist(DoP)
        ax.axis('off')
    draw_pitch('#B2B2B2', 'black')
    plt.xlim(-.5,105.5)
    plt.ylim(-.5,68.5)
    
    #df = season_df
    df = destzone_df[destzone_df['ifSP'] != 1]
    df = df.groupby(["Zone", "DestZone"], as_index=False).agg({
        "ifPass": 'sum', 'ifComplete': 'sum', 'xP':'sum', 'MatchID':'nunique',
        "X":'mean', 'Y':'mean', 'DestX':'mean', 'DestY':'mean'}).sort_values(by='ifPass', ascending=False)

    xS = df["X"]
    yS = df["Y"]
    xE = df["DestX"]
    yE = df["DestY"]

    #opta/mckeever blue hex code #2f3653 & #82868f
    #plt.title(str(Season)+' - '+str(Player)+' - xA Map', color='white', size=30, weight='bold')
    
    norm = TwoSlopeNorm(vmin=df.ifPass.min(),vcenter=df.ifPass.mean(),vmax=df.ifPass.max())
    for i in range(len(df)):
        plt.annotate('',xy=(xS.iloc[i], yS.iloc[i]), xycoords='data', xytext=(xE.iloc[i], yE.iloc[i]),textcoords='data',
                   arrowprops=dict(arrowstyle='wedge', connectionstyle='arc3', color='#333333', lw=5))
        plt.scatter(xS.iloc[i], yS.iloc[i],zorder=zo+2,c=df.ifPass.iloc[i], 
                    cmap="RdYlBu_r", edgecolor='white', marker='o', linewidths=7.5, 
                    s=df.ifPass.iloc[i]*75, norm=norm)
        plt.scatter(xS.iloc[i],yS.iloc[i],marker='o',facecolors="none",
            s=df.ifPass.iloc[i]*75,edgecolors="black",zorder=zo+3, linewidth=1.5, norm=norm)

    
    cax = plt.axes([0.175, 0.065, 0.675, 0.025])
    sm = plt.cm.ScalarMappable(cmap='RdYlBu_r', norm=TwoSlopeNorm(vmin=df.ifPass.min(),vcenter=df.ifPass.mean(),vmax=df.ifPass.max()))
    sm.A = []
    cbar = fig.colorbar(sm, cax=cax, orientation='horizontal', fraction=0.046, pad=0.04)
    cbar.set_label('Number of Pases', fontproperties=TableHead)
    cbar.ax.tick_params(labelsize=20)

        
    st.pyplot()

def TeamMatchPN(state):
    sm_df = load_sm_data()
    
    team = st.sidebar.multiselect('Select Team(s)', natsorted(sm_df.Team.unique()))
    sm_df = sm_df[sm_df['Team'].isin(team)]
    
    season = st.sidebar.multiselect('Select Season(s)',natsorted(sm_df.Season.unique()))  
    sm_df = sm_df[sm_df['Season'].isin(season)]
    
    pass_df = load_pass_data(season, team, 'no')
    
    match = st.sidebar.selectbox("Select Match", natsorted(pass_df.MatchName.unique()))    
    match_df = pass_df[pass_df['MatchName'] == match]
    
    matchid = st.sidebar.selectbox("Select MatchID", natsorted(match_df.MatchID.unique()))    
    match_df = match_df[match_df['MatchID'] == matchid]

    minute = st.sidebar.slider("Select Range of Minutes", 0,120,90)
    minute_df = match_df[match_df['Minute'] <= minute]
    
    PoPs = ['Establish', 'Evolve', 'Innovate']

    PoP = st.sidebar.multiselect('Select Phase(s) of Play', ['Establish', 'Evolve', 'Innovate'], default=PoPs)
    PoP_df = minute_df[minute_df.PhaseofPlay.str.contains('|'.join(PoP))]



    def v_pass_network(data):
        Title = fm.FontProperties(fname=fontPathBold, size=32)
        Annotate = fm.FontProperties(fname=fontPathBold, size=30)
        Legend = fm.FontProperties(fname=fontPathBold, size=28)
        
        #Team1 = Team1
        players = table['Players'].tolist()
        x = table['X']
        y = table['Y']
        touches_raw = table['xPR'].tolist()
        #maxpass = table['MaxPV'].tolist()
        maxpass = 0.08 * (minute/90)
    
        touches = []
        for item in touches_raw:
            size = 20*item
            touches.append(size)
    
        passes = {}
        for row in table.iterrows():
            index, data = row
            temp = []
            player = data[0]
            for n in range (5, len(data)):
                temp.append(data[n])
            passes[player] = temp
    
        #draw_pitch("#333333","white","vertical","full")
        fig,ax = plt.subplots(figsize=(22,32))
        vertfull_pitch('#333333', 'white', ax)
        
        pass1 = round((maxpass) * .25,3) 
        pass2 = round((maxpass) * .26,3) 
        pass3 = round((maxpass) * .44,3) 
        pass4 = round((maxpass) * .45,3) 
        pass5 = round((maxpass) * .65,3) 
        pass6 = round((maxpass) * .66,3) 
        pass7 = round((maxpass) * .84,3)
        pass8 = round((maxpass) * .85,3)
        pass9 = round((maxpass) * .99,3) 
        pass10 = round((maxpass),3)           
                   
        
        plt.plot(-2,color="darkblue",label="< "+str(pass1)+ ' GPA',zorder=0)
        plt.plot(-2,color="lightblue",label="Between " +str(pass2)+' and '+str(pass3)+ ' GPA',zorder=0)
        plt.plot(-2,color="darkkhaki",label="Between " +str(pass4)+' and '+str(pass5)+ ' GPA',zorder=0)
        plt.plot(-2,color="darkgoldenrod",label="Between " +str(pass6)+' and '+str(pass7)+ ' GPA',zorder=0)
        plt.plot(-2,color="orangered",label="Between " +str(pass8)+' and '+str(pass9)+ ' GPA',zorder=0)
        plt.plot(-2,color="darkred",label=str(pass10)+'+ GPA',zorder=0)
        leg = plt.legend(loc=1,ncol=3,frameon=False)
        plt.setp(leg.get_texts(), color='white', fontproperties=Legend)
        plt.title(str(season)+' - '+str(team)+ ' Pass Network\n'+str(match)+'\nUp To Minute '+str(minute), fontproperties=Title, color="black")
        for i, player in enumerate(players):
            plt.annotate(player, xy=(68-y[i],x[i]), xytext=((68-y[i]), x[i]-3), fontproperties=Annotate, color="white", ha="center", weight="bold", zorder=zo+8)
            for n in range(len(players)):
                player_passes = passes[player][n]
                width = player_passes / .1
                if player_passes >0: 
                    x_start = x[i]
                    x_length = x[n] - x[i]
                    y_start = 68-y[i]
                    y_length = (68-y[n]) - (68-y[i])
                    if x_length > 0:
                        x_start = x[i] + 1
                        x_length = x[n] - x[i] - 1
                    else:
                        x_start = x[i] - 1
                        x_length = x[n] - x[i] + 1.5
                    if y_length > 0:
                        y_start = 68-y[i] + 1.5
                        y_length = (68-y[n]) - (68-y[i]) - 2
                    else:
                        y_start = 68-y[i] - 1.5
                        y_length = (68-y[n]) - (68-y[i]) + 2
    
                    if player_passes >= pass10: 
                        color = "darkred" 
                        alpha = .8
                        zorder=zo+5
                    elif player_passes >= pass8 and player_passes <= pass9: 
                        color = "orangered"
                        alpha=.55
                        zorder=zo+4
                    elif player_passes >= pass6 and player_passes <= pass7: 
                        color = "darkgoldenrod"
                        alpha=.45
                        zorder=zo+3
                    elif player_passes >= pass4 and player_passes <= pass5: 
                        color = "darkkhaki"
                        alpha=.35
                        zorder=zo+3
                    elif player_passes >= pass2 and player_passes <= pass3: 
                        color = "lightblue"
                        alpha=.2
                        zorder=zo+2                 
                    else:
                        color = "darkblue"
                        alpha=.15
                        zorder=zo+1    
                    
                    plt.scatter(68-y, x, s = table.ifPass*25/matchcount, c=table.xPR,cmap='RdYlBu_r', linewidths=2, edgecolors='white',zorder=zo+1)
                    plt.arrow(y_start,x_start,y_length,x_length, 
                    head_length=1, color=color, alpha=alpha, width=width, head_width=width*2, length_includes_head=True,zorder=zorder)

        cax = plt.axes([0.15, 0.085, 0.7, 0.025])
        sm = plt.cm.ScalarMappable(cmap='RdYlBu_r', norm=TwoSlopeNorm(vmin=.9,vcenter=1, vmax=1.1))
        sm.A = []
        cbar = plt.colorbar(sm, cax=cax, orientation='horizontal', fraction=0.02, pad=0.01, ticks=[.9, .95, 1, 1.05, 1.1])
        cbar.set_label('xPR - Dots', fontproperties=Annotate)
                    
    Passes = PoP_df
    Passes['Players'] = Passes['Player']
    
    #Season = Season
    #Match = MatchID
    #Team1 = Team1
    data = Passes[(Passes['ifComplete'] == 1) & (Passes['ifSP'] != 1)]#((Passes['Minute'] >= StartMinute) & (Passes['Minute'] <= EndMinute))] 
    data1 = Passes[(Passes['ifPass'] == 1) & (Passes['ifSP'] != 1)] # ((Passes['Minute'] >= StartMinute) & (Passes['Minute'] <= EndMinute))]

    matchcount = data.MatchID.nunique()
    table = pd.pivot_table(data,index=["Players"],columns=['Teammate'],values=["GPA"],aggfunc=np.sum, fill_value=0).reset_index(col_level=1)
    table.columns = table.columns.droplevel()
    table['MaxGPA'] = table.iloc[:,1:].max(axis=1)
    table1 = pd.pivot_table(data1,index=["Players"],aggfunc={"X":'mean', "Y":'mean'}, fill_value=0).reset_index()
    table2 = pd.pivot_table(data1, index=["Players"], aggfunc={"ifPass":'sum', 'xP':'sum', 'ifComplete':'sum'}, fill_value=0).reset_index()
    #print(table2)
    table2['xPR'] = table2['ifComplete'] / table2['xP']    
    test = pd.merge(table1, table2, on = "Players")
    table = pd.merge(test,table, on = "Players")
    #print(table.PassesAttempted.max()*.3)
    table = table.loc[table['ifPass'] >= table.ifPass.max()*.1]
    idxnames = table['Players'].tolist()
    idxnames.extend(['Players', 'MaxGPA', 'X', 'Y', 'xPR', 'ifPass'])
    table = table.loc[:,table.columns.str.contains('|'.join(idxnames))].reset_index(drop=True)
    table3 = pd.pivot_table(data1, index=["Teammate", "OppTeam"], aggfunc={'ifComplete':'sum'}, fill_value=0).reset_index()
    table3 = table3.rename(columns={'Teammate':'Players', 'ifComplete':'Received'})
    test5 = pd.merge(table,table3, on = "Players")
    test1 = test5.loc[test5['ifPass'] >= test5.ifPass.max()*.1]
    idxnames = test1['Players'].tolist()
    idxnames.extend(['Players', 'X', 'Y', 'ifPass', 'xPR', 'MaxGPA'])
    table = test1.loc[:,test1.columns.str.contains('|'.join(idxnames))].reset_index(drop=True)

    v_pass_network(PoP_df)
    
    st.pyplot()
    
    st.subheader("Passing Data")    
    st.text("")

    
    PNdf = PoP_df[PoP_df['ifSP'] != 1]
    PNdf = PNdf.groupby(["Player"], as_index=False).agg({'GPA':'sum','ifPass':'sum','xP':'sum','ifComplete':'sum',
                'ifAssist':'sum', 'ShotAssist':'sum', 'ifRetain':'sum','ProgPass':'sum',
                'DeepProg':'sum', 'in18':'sum', 'Cin18':'sum'}).sort_values(by='Cin18', ascending=False)
    PNdf = PNdf.rename(columns={'ifPass':'Passes','ifAssist':'Assists','ShotAssist':'Shot Assists', 
                                  'ifRetain':'Retained','ifComplete':'Completed','Cin18':'Completedin18'})
    PNdf['xPR'] = PNdf.Completed / PNdf.xP
    PNdf = PNdf.sort_values(by='GPA', ascending=False)
    st.dataframe(PNdf)
    
    st.subheader("Passing Data By Player Connections")    
    st.text("")

    
    PNdf1 = PoP_df[(PoP_df['ifSP'] != 1) & (PoP_df['OppTeam'].isin(team))]
    PNdf1 = PNdf1.groupby(["Player", "Teammate"], as_index=False).agg({'GPA':'sum','ifPass':'sum','xP':'sum','ifComplete':'sum',
                'ifAssist':'sum', 'ShotAssist':'sum', 'ifRetain':'sum','ProgPass':'sum',
                'DeepProg':'sum', 'in18':'sum', 'Cin18':'sum'}).sort_values(by='Cin18', ascending=False)
    PNdf1 = PNdf1.rename(columns={'ifPass':'Passes','ifAssist':'Assists','ShotAssist':'Shot Assists', 
                                  'ifRetain':'Retained','ifComplete':'Completed','Cin18':'Completedin18'})
    PNdf1['xPR'] = PNdf1.Completed / PNdf1.xP
    PNdf1 = PNdf1.sort_values(by='GPA', ascending=False)
    st.dataframe(PNdf1)


def PlayerMatchPN(state):
    sm_df = load_sm_data()
    
    team = st.sidebar.multiselect('Select Team(s)', natsorted(sm_df.Team.unique()))
    sm_df = sm_df[sm_df['Team'].isin(team)]
    
    season = st.sidebar.multiselect('Select Season(s)',natsorted(sm_df.Season.unique()))  
    sm_df = sm_df[sm_df['Season'].isin(season)]
    
    pass_df = load_pass_data(season, team, 'no')
    
    player1 = st.sidebar.selectbox('Select Player', natsorted(pass_df.Player.unique()))
    player_df = pass_df[pass_df['Player'] == (player1)]

    
    match = st.sidebar.selectbox("Select Match", natsorted(player_df.MatchName.unique()))    
    match_df = player_df[player_df['MatchName'] == match]
    
    matchid = st.sidebar.selectbox("Select MatchID", natsorted(match_df.MatchID.unique()))    
    match_df = match_df[match_df['MatchID'] == matchid]

    minute = st.sidebar.slider("Select Range of Minutes", 0,120,90)
    minute_df = match_df[match_df['Minute'] <= minute]
    
    PoPs = ['Establish', 'Evolve', 'Innovate']

    PoP = st.sidebar.multiselect('Select Phase(s) of Play', ['Establish', 'Evolve', 'Innovate'], default=PoPs)
    PoP_df = minute_df[minute_df.PhaseofPlay.str.contains('|'.join(PoP))]

    
    def v_pass_network(data):
        Title = fm.FontProperties(fname=fontPathBold, size=32)
        Annotate = fm.FontProperties(fname=fontPathBold, size=30)
        Legend = fm.FontProperties(fname=fontPathBold, size=28)

        #Player = Player
        players = table['Player'].tolist()
        x = table['X']
        y = table['Y']
        touches_raw = table['ifPass'].tolist()
        #maxpass = table['MaxPV'].tolist()
        maxpass = 0.08 * (minute/90)
    
        touches = []
        for item in touches_raw:
            size = 20*item
            touches.append(size)
    
        passes = {}
        for row in table.iterrows():
            index, data = row
            temp = []
            player = data[0]
            for n in range (4, len(data)):
                temp.append(data[n])
            passes[player] = temp
    
        fig,ax = plt.subplots(figsize=(22,32))
        vertfull_pitch('#333333', 'white', ax)
        
        pass1 = round((maxpass) * .25,3) 
        pass2 = round((maxpass) * .26,3) 
        pass3 = round((maxpass) * .44,3) 
        pass4 = round((maxpass) * .45,3) 
        pass5 = round((maxpass) * .65,3) 
        pass6 = round((maxpass) * .66,3) 
        pass7 = round((maxpass) * .84,3)
        pass8 = round((maxpass) * .85,3)
        pass9 = round((maxpass) * .99,3) 
        pass10 = round((maxpass),3)           
                   
        
        plt.plot(-2,color="darkblue",label="< "+str(pass1)+ ' GPA',zorder=0)
        plt.plot(-2,color="lightblue",label="Between " +str(pass2)+' and '+str(pass3)+ ' GPA',zorder=0)
        plt.plot(-2,color="darkkhaki",label="Between " +str(pass4)+' and '+str(pass5)+ ' GPA',zorder=0)
        plt.plot(-2,color="darkgoldenrod",label="Between " +str(pass6)+' and '+str(pass7)+ ' GPA',zorder=0)
        plt.plot(-2,color="orangered",label="Between " +str(pass8)+' and '+str(pass9)+ ' GPA',zorder=0)
        plt.plot(-2,color="darkred",label=str(pass10)+'+ GPA',zorder=0)
        leg = plt.legend(loc=1,ncol=3,frameon=False)
        plt.setp(leg.get_texts(), color='white', fontproperties=Legend)
        plt.title(str(season)+' - '+str(player1)+ ' Pass Network\n'+str(match), fontproperties=Title, color="black")
        for i, player in enumerate(players):
            plt.annotate(player, xy=(68-y[i],x[i]), xytext=((68-y[i]), x[i]-3), fontproperties=Annotate, color="white", ha="center", weight="bold", zorder=zo+5)
            for n in range(len(players)):
                player_passes = passes[player][n]
                width = player_passes / .1
                if player_passes >0: 
                    x_start = x[i]
                    x_length = x[n] - x[i]
                    y_start = 68-y[i]
                    y_length = (68-y[n]) - (68-y[i])
                    if x_length > 0:
                        x_start = x[i] + 1
                        x_length = x[n] - x[i] - 1
                    else:
                        x_start = x[i] - 1
                        x_length = x[n] - x[i] + 1.5
                    if y_length > 0:
                        y_start = 68-y[i] + 1.5
                        y_length = (68-y[n]) - (68-y[i]) - 2
                    else:
                        y_start = 68-y[i] - 1.5
                        y_length = (68-y[n]) - (68-y[i]) + 2
    
                    if player_passes >= pass10: 
                        color = "darkred" 
                        alpha = .8
                        zorder=zo+5
                    elif player_passes >= pass8 and player_passes <= pass9: 
                        color = "orangered"
                        alpha=.55
                        zorder=zo+4
                    elif player_passes >= pass6 and player_passes <= pass7: 
                        color = "darkgoldenrod"
                        alpha=.45
                        zorder=zo+3
                    elif player_passes >= pass4 and player_passes <= pass5: 
                        color = "darkkhaki"
                        alpha=.35
                        zorder=zo+3
                    elif player_passes >= pass2 and player_passes <= pass3: 
                        color = "lightblue"
                        alpha=.2
                        zorder=zo+2                 
                    else:
                        color = "darkblue"
                        alpha=.15
                        zorder=zo+1    
                        
                    norm=TwoSlopeNorm(vmin=0,vcenter=table.ifPass.mean()*.5, vmax=table.ifPass.mean()*.75)
                    plt.scatter(68-y, x, s = 350, c=table.ifPass,cmap='RdYlBu_r', norm=norm, linewidths=2, edgecolors='white',zorder=zo+1)
                    plt.arrow(y_start,x_start,y_length,x_length, 
                    head_length=1, color=color, alpha=alpha, width=width, head_width=width*2, length_includes_head=True,zorder=zorder)
        
    
        sm = plt.cm.ScalarMappable(cmap='RdYlBu_r', norm=TwoSlopeNorm(vmin=0,vcenter=round(table.ifPass.mean()*.5,0), vmax=round(table.ifPass.mean()*.95,0)))
        sm.A = []
        cbar = plt.colorbar(sm,orientation='horizontal', fraction=0.02, pad=0.01, ticks=[0, round(table.ifPass.mean()*.25,0), round(table.ifPass.mean()*.5,0), round(table.ifPass.mean()*.75,0)])
        cbar.set_label('Passes Attempted to Player', fontproperties=Annotate)

    Passes = PoP_df
    Passes['Players'] = Passes['Player']
    

    matchcount = Passes.MatchID.nunique()

    
    data = Passes.loc[(Passes['ifComplete'] == 1) & (Passes['ifSP'] != 1) ]
    data1 = Passes.loc[(Passes['ifPass'] == 1)  & (Passes['ifSP'] != 1) ]

    table = pd.pivot_table(data,index=["Player"],columns=['Teammate'],values=["GPA"],aggfunc=np.sum, fill_value=0).reset_index(col_level=1)
    table.columns = table.columns.droplevel()
    table['MaxGPA'] = table.iloc[:,1:].max(axis=1)
    table1 = pd.pivot_table(data1,index=["Player"],aggfunc={"X":'mean', "Y":'mean'}, fill_value=0).reset_index()    
    table2 = pd.pivot_table(data1, index=["Player"], aggfunc={"ifPass":'sum', 'xP':'sum', 'ifComplete':'sum'}, fill_value=0).reset_index()
    table2['xPR'] = table2['ifComplete'] / table2['xP']
    test = pd.merge(table1, table2, on = "Player")
    test = pd.merge(test,table, on = "Player")
    receive = Passes[(Passes['ifComplete'] == 1) & (Passes['ifSP'] != 1) ]
    receivep =  pd.pivot_table(receive,index=["Teammate"],aggfunc={"DestX":'mean', "DestY":'mean', 'ifPass':'sum'}, fill_value=0).reset_index()
    receivep = receivep.rename(columns={"Teammate":"Player","DestX": "X", "DestY":"Y"})
    frames = [test,receivep]
    data = pd.concat(frames)
    data = pd.DataFrame(data=data)
    test = data[data['ifPass'] >= 1]
    idxnames = test['Player'].tolist()
    idxnames.extend(['Player', 'X', 'Y', 'ifPass', 'MaxGPA'])
    table = test.loc[:,test.columns.str.contains('|'.join(idxnames))].reset_index(drop=True)
    table.insert(4, player1, 0) 
    table = table.fillna(0)
    #print(table)
    v_pass_network(PoP_df)
    
    st.pyplot()
    
    st.subheader("Passing Data By Player Connections")    
    st.text("")

    
    PNdf1 = PoP_df[(PoP_df['ifSP'] != 1) & (PoP_df['OppTeam'].isin(team))]
    PNdf1 = PNdf1.groupby(["Player", "Teammate"], as_index=False).agg({'GPA':'sum','ifPass':'sum','xP':'sum','ifComplete':'sum',
                'ifAssist':'sum', 'ShotAssist':'sum', 'ifRetain':'sum','ProgPass':'sum',
                'DeepProg':'sum', 'in18':'sum', 'Cin18':'sum'}).sort_values(by='Cin18', ascending=False)
    PNdf1 = PNdf1.rename(columns={'ifPass':'Passes','ifAssist':'Assists','ShotAssist':'Shot Assists', 
                                  'ifRetain':'Retained','ifComplete':'Completed','Cin18':'Completedin18'})
    PNdf1['xPR'] = PNdf1.Completed / PNdf1.xP
    PNdf1 = PNdf1.sort_values(by='GPA', ascending=False)
    st.dataframe(PNdf1)

    
def AttCorner(state):
    sm_df = load_sm_data()
    
    team = st.sidebar.multiselect('Select Team(s)', natsorted(sm_df.Team.unique()))
    sm_df = sm_df[sm_df['Team'].isin(team)]
    
    season = st.sidebar.multiselect('Select Season(s)',natsorted(sm_df.Season.unique()))  
    sm_df = sm_df[sm_df['Season'].isin(season)]
    
    pass_df = load_pass_data(season, team, 'no')
        
    pass_df = pass_df[pass_df['TypeofAttack'] == 'Corner']
    
    players = (pass_df.Player.unique()).tolist()
    
    player = st.sidebar.multiselect("Select Player(s)", natsorted(pass_df.Player.unique()), default=players)
    player_df = pass_df[pass_df['Player'].isin(player)]


    matches = (player_df.MatchName.unique()).tolist()
    
    match = st.sidebar.multiselect("Select Match(es)", natsorted(player_df.MatchName.unique()), default=matches)
    match_df = player_df[player_df['MatchName'].isin(match)]
    
    side = (match_df.CornerSide.unique()).tolist()

    cornerside = st.sidebar.multiselect("Select Side(s)", natsorted(match_df.CornerSide.unique()), default=side)
    cnrside_df = match_df[match_df['CornerSide'].isin(cornerside)]
    
    outcome = (cnrside_df.CornerOutcome.unique()).tolist()
    
    cnroutcome = st.sidebar.multiselect("Select Outcome(s)", natsorted(cnrside_df.CornerOutcome.unique()), default=outcome)
    match_df = cnrside_df[cnrside_df['CornerOutcome'].isin(cnroutcome)]

    st.header("Attacking Corner Service Map")  
    #st.subheader("Heat Map, GPA Map, & Coverage Map")    
    st.text("")

    
    df = match_df
    SA = df[(df['ShotAssist'] == 1)]
    A = df[(df['ifAssist'] == 1)]
    R = df[(df['ifRetain'] == 1)]
    C = df[(df['ifComplete'] == 1)]
    IC = df[(df['ifComplete'] != 1)]
    
    
    draw_pitch("white","black","vertical","half")
    plt.title(str(season)+' - '+str(team)+" Attacking Corner Touch Map",fontproperties=headers)

    

    #opta/mckeever blue hex code #2f3653 & #82868f
    #figsize1 = 32
    #figsize2 = 18
    #fig = plt.figure(figsize=(figsize1, figsize2),facecolor='#333333') 


    #plt.scatter(68-yS, xS, marker='o',s=125, facecolor="white", linewidths=2,
     #   zorder=zo+5, alpha=.5)
    
    for i in range(len(A)):
        plt.annotate('',xy=(68-A.Y.iloc[i], A.X.iloc[i]), xycoords='data', xytext=(68-A.DestY.iloc[i], A.DestX.iloc[i]),textcoords='data',
                    arrowprops=dict(arrowstyle='wedge', connectionstyle='arc3', color='#E6E6E6', lw=2))
        plt.scatter(68-A.DestY.iloc[i], A.DestX.iloc[i],zorder=zo+6,
            color="gold", edgecolor='black', marker='o', linewidths=2, s=250)
    for i in range(len(SA)):
        plt.annotate('',xy=(68-SA.Y.iloc[i], SA.X.iloc[i]), xycoords='data', xytext=(68-SA.DestY.iloc[i], SA.DestX.iloc[i]),textcoords='data',
                    arrowprops=dict(arrowstyle='wedge', connectionstyle='arc3', color='#E6E6E6', lw=2))
        plt.scatter(68-SA.DestY.iloc[i], SA.DestX.iloc[i],zorder=zo+5,
            color="midnightblue", edgecolor='black', marker='o', linewidths=2, s=250)
    for i in range(len(R)):
        plt.annotate('',xy=(68-R.Y.iloc[i], R.X.iloc[i]), xycoords='data', xytext=(68-R.DestY.iloc[i], R.DestX.iloc[i]),textcoords='data',
                    arrowprops=dict(arrowstyle='wedge', connectionstyle='arc3', color='#E6E6E6', lw=2))
        plt.scatter(68-R.DestY.iloc[i], R.DestX.iloc[i],zorder=zo+4,
            color="lime", edgecolor='black', marker='o', linewidths=2, s=250)
    for i in range(len(C)):
        plt.annotate('',xy=(68-C.Y.iloc[i], C.X.iloc[i]), xycoords='data', xytext=(68-C.DestY.iloc[i], C.DestX.iloc[i]),textcoords='data',
                    arrowprops=dict(arrowstyle='wedge', connectionstyle='arc3', color='#E6E6E6', lw=2))
        plt.scatter(68-C.DestY.iloc[i], C.DestX.iloc[i],zorder=zo+3,
            color="dodgerblue", edgecolor='black', marker='o', linewidths=2, s=250)
    for i in range(len(IC)):
        plt.annotate('',xy=(68-IC.Y.iloc[i], IC.X.iloc[i]), xycoords='data', xytext=(68-IC.DestY.iloc[i], IC.DestX.iloc[i]),textcoords='data',
                    arrowprops=dict(arrowstyle='wedge', connectionstyle='arc3', color='#E6E6E6', lw=2))
        plt.scatter(68-IC.DestY.iloc[i], IC.DestX.iloc[i],zorder=zo+2,
            color="red", edgecolor='black', marker='o', linewidths=2, s=250)
    
    plt.scatter(3,45,marker='o',c='gold', s=500,
           edgecolors="black",zorder=zo+2, linewidth=2)
    plt.scatter(18,45, marker='o', c='midnightblue', s=500, linewidths=2,
       edgecolors="black",zorder=zo)
    plt.scatter(33,45,marker='o', c="lime", s=500, linewidths=2,
       edgecolors="black",zorder=zo)
    plt.scatter(48,45,marker='o',c="dodgerblue", linewidths=2,
       s=500,edgecolors="black",zorder=zo+1)
    plt.scatter(63,45,marker='o',c='red',  s=500, linewidths=2,
       edgecolors="black",zorder=zo)
    plt.text(3,42.5,"Assist",fontsize=22, color='black', fontproperties=Annotate,
             horizontalalignment='center', verticalalignment='center', zorder=12)
    plt.text(18,42.5,"Shot Assist",fontsize=22, color='black', fontproperties=Annotate,
             horizontalalignment='center', verticalalignment='center', zorder=12)
    plt.text(33,42.5,"Retain",fontsize=22, color='black', fontproperties=Annotate,
             horizontalalignment='center', verticalalignment='center', zorder=12)
    plt.text(48,42.5,"1st Touch",fontsize=22, color='black', fontproperties=Annotate,
             horizontalalignment='center', verticalalignment='center', zorder=12)
    plt.text(63,42.5,"Incomplete",fontsize=22, color='black', fontproperties=Annotate,
             horizontalalignment='center', verticalalignment='center', zorder=12)

    st.pyplot()
    
    cnrdf = df.groupby(["Season", "Team", "Player"], as_index=False).agg({'ifPass':'sum',
                'ifAssist':'sum', 'ShotAssist':'sum', 'ifRetain':'sum', 
                'ifComplete':'sum'}).sort_values(by='ifPass', ascending=False)
    cnrdf = cnrdf.rename(columns={'ifPass':'Services','ifAssist':'Assists','ShotAssist':'Shot Assists', 'ifRetain':'Retained','ifComplete':'1st Touch'})
    st.dataframe(cnrdf)
    
def DefCorner(state):
    sm_df = load_sm_data()
    
    team = st.sidebar.multiselect('Select Team(s)', natsorted(sm_df.Team.unique()))
    sm_df = sm_df[sm_df['Team'].isin(team)]
    
    season = st.sidebar.multiselect('Select Season(s)',natsorted(sm_df.Season.unique()))  
    sm_df = sm_df[sm_df['Season'].isin(season)]
    
    pass_df = load_pass_data(season, team, 'yes')
        
    pass_df = pass_df[pass_df['TypeofAttack'] == 'Corner']
    
    players = (pass_df.Player.unique()).tolist()
    
    player = st.sidebar.multiselect("Select Player(s)", natsorted(pass_df.Player.unique()), default=players)
    player_df = pass_df[pass_df['Player'].isin(player)]


    matches = (player_df.MatchName.unique()).tolist()
    
    match = st.sidebar.multiselect("Select Match(es)", natsorted(player_df.MatchName.unique()), default=matches)
    match_df = player_df[player_df['MatchName'].isin(match)]
    
    side = (match_df.CornerSide.unique()).tolist()

    cornerside = st.sidebar.multiselect("Select Side(s)", natsorted(match_df.CornerSide.unique()), default=side)
    cnrside_df = match_df[match_df['CornerSide'].isin(cornerside)]
    
    outcome = (cnrside_df.CornerOutcome.unique()).tolist()
    
    cnroutcome = st.sidebar.multiselect("Select Outcome(s)", natsorted(cnrside_df.CornerOutcome.unique()), default=outcome)
    match_df = cnrside_df[cnrside_df['CornerOutcome'].isin(cnroutcome)]


    st.header("Defensive Corner Service Map")  
    #st.subheader("Heat Map, GPA Map, & Coverage Map")    
    st.text("")

    
    df = cnrside_df
    SA = df[(df['ShotAssist'] == 1)]
    A = df[(df['ifAssist'] == 1)]
    R = df[(df['ifRetain'] == 1)]
    C = df[(df['ifComplete'] == 1)]
    IC = df[(df['ifComplete'] != 1)]
    
    
    draw_pitch("white","black","vertical","half")
    plt.title(str(season)+' - '+str(team)+" Defensive Corner Touch Map",fontproperties=headers)

    

    #opta/mckeever blue hex code #2f3653 & #82868f
    #figsize1 = 32
    #figsize2 = 18
    #fig = plt.figure(figsize=(figsize1, figsize2),facecolor='#333333') 


    #plt.scatter(68-yS, xS, marker='o',s=125, facecolor="white", linewidths=2,
     #   zorder=zo+5, alpha=.5)
    
    for i in range(len(A)):
        plt.annotate('',xy=(68-A.Y.iloc[i], A.X.iloc[i]), xycoords='data', xytext=(68-A.DestY.iloc[i], A.DestX.iloc[i]),textcoords='data',
                    arrowprops=dict(arrowstyle='wedge', connectionstyle='arc3', color='#E6E6E6', lw=2))
        plt.scatter(68-A.DestY.iloc[i], A.DestX.iloc[i],zorder=zo+6,
            color="gold", edgecolor='black', marker='o', linewidths=2, s=250)
    for i in range(len(SA)):
        plt.annotate('',xy=(68-SA.Y.iloc[i], SA.X.iloc[i]), xycoords='data', xytext=(68-SA.DestY.iloc[i], SA.DestX.iloc[i]),textcoords='data',
                    arrowprops=dict(arrowstyle='wedge', connectionstyle='arc3', color='#E6E6E6', lw=2))
        plt.scatter(68-SA.DestY.iloc[i], SA.DestX.iloc[i],zorder=zo+5,
            color="midnightblue", edgecolor='black', marker='o', linewidths=2, s=250)
    for i in range(len(R)):
        plt.annotate('',xy=(68-R.Y.iloc[i], R.X.iloc[i]), xycoords='data', xytext=(68-R.DestY.iloc[i], R.DestX.iloc[i]),textcoords='data',
                    arrowprops=dict(arrowstyle='wedge', connectionstyle='arc3', color='#E6E6E6', lw=2))
        plt.scatter(68-R.DestY.iloc[i], R.DestX.iloc[i],zorder=zo+4,
            color="lime", edgecolor='black', marker='o', linewidths=2, s=250)
    for i in range(len(C)):
        plt.annotate('',xy=(68-C.Y.iloc[i], C.X.iloc[i]), xycoords='data', xytext=(68-C.DestY.iloc[i], C.DestX.iloc[i]),textcoords='data',
                    arrowprops=dict(arrowstyle='wedge', connectionstyle='arc3', color='#E6E6E6', lw=2))
        plt.scatter(68-C.DestY.iloc[i], C.DestX.iloc[i],zorder=zo+3,
            color="dodgerblue", edgecolor='black', marker='o', linewidths=2, s=250)
    for i in range(len(IC)):
        plt.annotate('',xy=(68-IC.Y.iloc[i], IC.X.iloc[i]), xycoords='data', xytext=(68-IC.DestY.iloc[i], IC.DestX.iloc[i]),textcoords='data',
                    arrowprops=dict(arrowstyle='wedge', connectionstyle='arc3', color='#E6E6E6', lw=2))
        plt.scatter(68-IC.DestY.iloc[i], IC.DestX.iloc[i],zorder=zo+2,
            color="red", edgecolor='black', marker='o', linewidths=2, s=250)
    
    plt.scatter(3,45,marker='o',c='gold', s=500,
           edgecolors="black",zorder=zo+2, linewidth=2)
    plt.scatter(18,45, marker='o', c='midnightblue', s=500, linewidths=2,
       edgecolors="black",zorder=zo)
    plt.scatter(33,45,marker='o', c="lime", s=500, linewidths=2,
       edgecolors="black",zorder=zo)
    plt.scatter(48,45,marker='o',c="dodgerblue", linewidths=2,
       s=500,edgecolors="black",zorder=zo+1)
    plt.scatter(63,45,marker='o',c='red',  s=500, linewidths=2,
       edgecolors="black",zorder=zo)
    plt.text(3,42.5,"Assist",fontsize=22, color='black', fontproperties=Annotate,
             horizontalalignment='center', verticalalignment='center', zorder=12)
    plt.text(18,42.5,"Shot Assist",fontsize=22, color='black', fontproperties=Annotate,
             horizontalalignment='center', verticalalignment='center', zorder=12)
    plt.text(33,42.5,"Retain",fontsize=22, color='black', fontproperties=Annotate,
             horizontalalignment='center', verticalalignment='center', zorder=12)
    plt.text(48,42.5,"1st Touch",fontsize=22, color='black', fontproperties=Annotate,
             horizontalalignment='center', verticalalignment='center', zorder=12)
    plt.text(63,42.5,"Incomplete",fontsize=22, color='black', fontproperties=Annotate,
             horizontalalignment='center', verticalalignment='center', zorder=12)

    st.pyplot()

    
def PassDash(state):
    sm_df = load_sm_data()
    
    team = st.sidebar.multiselect('Select Team(s)', natsorted(sm_df.Team.unique()))
    sm_df = sm_df[sm_df['Team'].isin(team)]
    
    season = st.sidebar.multiselect('Select Season(s)',natsorted(sm_df.Season.unique()))  
    sm_df = sm_df[sm_df['Season'].isin(season)]
    
    pass_df = load_pass_data(season, team, 'no')
        
    matches = (pass_df.MatchName.unique()).tolist()
    
    match = st.sidebar.multiselect("Select Match(es)", natsorted(pass_df.MatchName.unique()), default=matches)
    match_df = pass_df[pass_df['MatchName'].isin(match)]
    
    
    st.header("Attacking Third Passing Maps")  
    st.subheader("Heat Maps by Zones")    
    st.text("")


    Passes = match_df
    in18 = Passes[(Passes['in18'] == 1) & (Passes['ifOP'] == 1)]
    Z14 = Passes[(Passes['ifOP'] == 1) & (((Passes['DestX'] >= 70) & (Passes['DestX'] <= 89.25)) & ((Passes['DestY'] >= 15.3) & (Passes['DestY'] <= 52.7)))]
    HalfSpace = Passes[((Passes['Zone'] == 19)|(Passes['Zone'] == 17))]
    AssistZone = Passes[((Passes['Zone'] == 24)|(Passes['Zone'] == 22))]
    
    fig,ax = plt.subplots(figsize=(32,20))
    plt.suptitle(str(season)+' - '+str(team)+' Attacking Third Passing', fontproperties=headers)
    #In Pen Area
    ax1 = plt.subplot(221)
    horizfull_pitch('none', 'black', ax1)
    plt.title("Passes into the Penalty Area", fontproperties=Subtitle)
    sns.kdeplot(in18.X, in18.Y, cmap="RdYlBu_r",shade=True, shade_lowest=False, n_levels=25, alpha=.75, zorder=5)
    ly2 = [15.3,15.3,52.7,52.7] 
    lx2 = [105,89.25,89.25,105]
    ax1.plot(lx2,ly2,color='#333333',zorder=zo, lw=6)
    ax1.plot((105,105), (15.3,52.7), color='#333333', zorder=zo+5, lw=6)
    rec3 = plt.Rectangle((89.25, 15.3), 89.25, 37.5,ls='-',color='#B2B2B2', zorder=6, alpha=.85)
    ax1.add_artist(rec3)
    plt.xlim(-0.5,105.5)
    plt.ylim(-0.5,68.5)
    
    #Zone 14
    ax2 = plt.subplot(222)
    horizfull_pitch('none', 'black', ax2)
    plt.title("Passes into Zone 14", fontproperties=Subtitle)
    sns.kdeplot(Z14.X, Z14.Y, cmap="RdYlBu_r",shade=True, shade_lowest=False, n_levels=25, alpha=.75, zorder=5)
    ly2 = [15.3,15.3,52.7,52.7] 
    lx2 = [89.25,70,70,89.25]
    ax2.plot(lx2,ly2,color='#333333',zorder=zo+5, lw=6)
    ax2.plot((89.25,89.25), (15.3,52.7), color='#333333', zorder=zo+5, lw=6)
   
    rec3 = plt.Rectangle((70, 15.3), 19, 37.5,ls='-',color='#B2B2B2', zorder=zo+1, alpha=.85)
    ax2.add_artist(rec3)
    plt.xlim(-0.5,105.5)
    plt.ylim(-0.5,68.5)
    
    #Half Spaces
    ax3 = plt.subplot(223)
    horizfull_pitch('none', 'black', ax3)
    plt.title("Passes from the Half Space", fontproperties=Subtitle)
    sns.kdeplot(HalfSpace.DestX, HalfSpace.DestY, cmap="RdYlBu_r",shade=True, shade_lowest=False, n_levels=25, alpha=.75, zorder=5)
    #Left Half Space       
    ly2 = [40.8,40.8,52.7,52.7] 
    lx2 = [89.25,63,63,89.25]
    ax3.plot(lx2,ly2,color='#333333',zorder=zo+5, lw=6)
    ax3.plot((89.25,89.25), (40.8,52.7), color='#333333', zorder=zo+5, lw=6)
    rec3 = plt.Rectangle((63, 40.8), 26, 12.2,ls='-',color='#B2B2B2', zorder=zo+1, alpha=.85)
    ax3.add_artist(rec3)
    #Right Half Space       
    ly2 = [15.3, 15.3,27.2,27.2] 
    lx2 = [89.25,63,63,89.25]
    ax3.plot(lx2,ly2,color='#333333',zorder=zo+5, lw=6)
    ax3.plot((89.25,89.25), (15.3,27.2), color='#333333', zorder=zo+5, lw=6)
    rec3 = plt.Rectangle((63, 15.3), 26, 12.2,ls='-',color='#B2B2B2', zorder=zo+1, alpha=.85)
    ax3.add_artist(rec3)
    plt.xlim(-0.5,105.5)
    plt.ylim(-0.5,68.5)


    
    #Assist Zone
    ax4 = plt.subplot(224)
    horizfull_pitch('none', 'black', ax4)
    plt.title("Passes from the Assist Zone", fontproperties=Subtitle)
    sns.kdeplot(AssistZone.DestX, AssistZone.DestY, cmap="RdYlBu_r",shade=True, shade_lowest=False, n_levels=25, alpha=.75, zorder=5)
    #Left Assist Zone       
    ly2 = [40.8,40.8,52.7,52.7] 
    lx2 = [105,89.25,89.25,105]
    ax4.plot(lx2,ly2,color='#333333',zorder=zo+5, lw=6)
    ax4.plot((105,105), (40.8,52.7), color='#333333', zorder=zo+5, lw=6)
    rec3 = plt.Rectangle((89.25, 40.8), 15.6, 12.2,ls='-',color='#B2B2B2', zorder=zo+1, alpha=.85)
    ax4.add_artist(rec3)
    #Right Assist Zone       
    ly2 = [15.3, 15.3,27.2,27.2] 
    lx2 = [105,89.25,89.25,105]
    ax4.plot(lx2,ly2,color='#333333',zorder=zo+5, lw=6)
    ax4.plot((105,105), (15.3,27.2), color='#333333', zorder=zo+5, lw=6) 
    rec3 = plt.Rectangle((89.25, 15.3), 15.6, 12.2,ls='-',color='#B2B2B2', zorder=zo+1, alpha=.85)
    ax4.add_artist(rec3)
    plt.xlim(-0.5,105.5)
    plt.ylim(-0.5,68.5)

    st.pyplot()
    
    st.subheader("Open Play Attacking Third Passing Data")    
    st.text("")

    
    A3 = match_df[(match_df['X'] >= 63) & (match_df['ifSP'] != 1)]
    passes = A3.groupby(["Season", "Team", "Player"], as_index=False).agg({'ifPass':'sum',
                'ifAssist':'sum', 'ShotAssist':'sum', 'ifRetain':'sum','ifComplete':'sum',
                'ProgPass':'sum', 'DeepProg':'sum', 'in18':'sum', 'Cin18':'sum'}).sort_values(by='Cin18', ascending=False)
    passes = passes.rename(columns={'ifPass':'Passes','ifAssist':'Assists','ShotAssist':'Shot Assists', 
                                  'ifRetain':'Retained','ifComplete':'Completed','Cin18':'Completedin18'})
    st.dataframe(passes)

    
    


if __name__ == "__main__":
    main()

#st.set_option('server.enableCORS', True)
# to run : streamlit run "/Users/michael/Documents/Python/Codes/NCAA Soccer App.py"
