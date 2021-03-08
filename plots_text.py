import inline as inline
import plotly
import pandas as pd
import numpy as np
import seaborn as sns
import plotly.express as px
from matplotlib import pyplot as plt
import matplotlib.colors as mcolors



#---------------majority model stab time experiment slashdot--------
y_slashdot_ER_AV_ROUNDS_LT = [2.0, 4.0, 4.25, 5.0, 5.75, 14.5, 5.75, 5.0, 4.0, 4.0, 2.0]
y_slashdot_BA_AV_ROUNDS_LT = [2.0, 3.5, 4.0, 4.0, 5.0, 9.125, 5.0, 4.0, 4.0, 3.625, 2.0]
y_slashdot_HYP_AV_ROUNDS_LT = [2.0, 6.0, 7.875, 10.0, 16.25, 30.5, 16.125, 9.75, 8.0, 6.5, 3.0]
y_slashdot_REG_AV_ROUNDS_LT = [2.0, 5.75, 6.75, 7.375, 9.25, 12.875, 8.875, 7.625, 6.25, 5.5, 2.0]
y_slashdot_DREG_AV_ROUNDS_LT = [2.0, 4.0, 4.0, 4.875, 5.0, 20.75, 5.0, 4.875, 4.0, 3.75, 2.0]
y_slashdot_CM_AV_ROUNDS_LT = [2.0, 3.875, 4.0, 4.0, 5.0, 9.625, 5.0, 4.0, 4.0, 4.0, 2.0]

y_twitter_BA_0807_AVROUNDS = [2.0,3.5, 4.0, 4.0, 4.0, 5.0, 6.0, 21.625, 5.5, 4.0, 3.0, 3.75, 4.5, 7.75, 7.875, 5.0, 4.125, 4.0,2.0]
y_twitter_HYP_0807_AVROUNDS = [2.0,4.375, 4.875, 5.875, 6.375, 7.75, 10.5, 17.375, 70.125, 22.625, 15.75, 9.625, 16.75, 40.875, 17.25, 9.625, 7.375, 6.0,2.0]
y_twitter_REG_0807_AVROUNDS = [2.0,5.25, 6.625, 7.375, 8.75, 10.75, 14.875, 28.375, 37.5, 13.625, 13.875, 9.875, 13.25, 34.75, 18.5, 12.5, 9.0, 6.5,2.0]
y_twitter_DREG_0807_AVROUNDS = [2.0,4.0, 4.0, 4.0, 5.0, 5.0, 6.875, 12.75, 8.625, 4.5, 3.5, 4.125, 6.5, 19.25, 8.0, 6.0, 5.0, 4.0,2.0]

#insert the approperiate data in the form of a list
def plot1():
    x = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
    plt.plot(x, y_slashdot_ER_AV_ROUNDS_LT, linewidth=3, c='c')
    plt.plot(x, y_slashdot_BA_AV_ROUNDS_LT, linewidth=2, c='b')
    plt.plot(x, y_slashdot_HYP_AV_ROUNDS_LT, linewidth=2, c='#ff7f0e')
    plt.plot(x, y_slashdot_REG_AV_ROUNDS_LT, linewidth=2, c="g")
    plt.plot(x, y_slashdot_DREG_AV_ROUNDS_LT, linewidth=2,c='#d62728' )
    plt.plot(x, y_slashdot_CM_AV_ROUNDS_LT, linewidth=2, c='m')
    plt.legend(['ER', 'PA', 'HRG', 'SN', 'RRG', r'$CM_{1}$'], loc=2, fontsize=15)
    plt.ylabel("stabilization time")
    plt.xlabel(r'$p_b$')
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)

def plot2():
    x = [0.0,0.1,0.15, 0.2,0.25, 0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,1.0]
    plt.plot(x, y_twitter_BA_0807_AVROUNDS, linewidth=2, c='b')
    plt.plot(x, y_twitter_HYP_0807_AVROUNDS, linewidth=2, c='#ff7f0e')
    plt.plot(x, y_twitter_REG_0807_AVROUNDS, linewidth=2, c='g')
    plt.plot(x, y_twitter_DREG_0807_AVROUNDS, linewidth=2, c='#d62728')
    plt.legend(['PA', 'HRG', 'SN', "RRG"], loc=2, fontsize=15)
    plt.ylabel("stabilization time")
    plt.xlabel(r'$p_b$')
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)


f = plt.figure(figsize=(12, 6))
plt.rcParams["axes.labelsize"] = 20
gs = f.add_gridspec(1, 2)



with sns.axes_style("ticks"):
    ax = f.add_subplot(gs[0, 0])
    plot1()

with sns.axes_style("ticks"):
    ax = f.add_subplot(gs[0, 1])
    plot2()

f.tight_layout()
sns.despine()
#plt.show()
plt.savefig('plot_stab12_text_2.png', dpi=300)

