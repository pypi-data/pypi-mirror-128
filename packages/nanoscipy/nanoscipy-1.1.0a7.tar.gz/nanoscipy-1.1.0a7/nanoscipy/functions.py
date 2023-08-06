import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from statsmodels.graphics.gofplots import qqplot
from scipy.optimize import curve_fit

def plot_grid(nr=0,r=1,s=1,share=0,set_dpi=300):
    global figure_global_output
    global ax_global_output
    global figure_number_global_output
    global share_axis_bool_output
    global boundary_ax_global_fix
    
    boundary_ax_global_fix = r*s
    figure_number_global_output = nr
    share_axis_bool_output = share
    
    if r == 1 and s == 1:
        figure_global_output, _ax_global_output = plt.subplots(num=nr, dpi=set_dpi)
        ax_global_output = [_ax_global_output]
    if r > 1 or s > 1:
        if share == 'x' or share == 1:
            figure_global_output, ax_global_output = plt.subplots(r,s,num=nr,sharex=True, dpi=set_dpi)
        elif share == 'y' or share == 2:
            figure_global_output, ax_global_output = plt.subplots(r,s,num=nr,sharey=True, dpi=set_dpi)
        elif share == 'xy' or share == 'yx' or share == 'both' or share == 3:
            figure_global_output, ax_global_output = plt.subplots(r,s,num=nr,sharex=True,sharey=True, dpi=set_dpi)
        elif share == 'no' or share == 0:
            figure_global_output, ax_global_output = plt.subplots(r,s,num=nr,sharex=False,sharey=False, dpi=set_dpi)
        else: 
            print('Wrong <share> key, check _help() for more information')
            return
    elif r == 0 or s == 0: 
        print('Wrong <r> or <s> key, check _help() for more information')
        return

def plot_data(p=0,xs=[],ys=[],ttl=None,dlab=[],xlab=None,
                  ylab=None,ms=[],lw=[],ls=[],dcol=[],
                  plt_type=0,tight=True,mark=[],trsp=[] ,v_ax=None,
                  h_ax=None,no_ticks=False,share_ttl=False):
    if len(ax_global_output) != boundary_ax_global_fix:
        axs = ax_global_output.flatten()
    else:
        axs = ax_global_output
    
    # chek for correct list input, and try fix if data-list is not in list
    if not isinstance(xs,list):
        print('Error: Wrong <xs> key, check _help() for more information')
    else:
        if any(isinstance(i, list) for i in xs):
            xs_fix = [xs]
        else: 
            xs_fix = xs
    if plt_type != 2 or plt_type != 'qqplot':
        if not isinstance(ys,list):
            print('Error: Wrong <ys> key, check _help() for more information')
        else:
            if any(isinstance(i, list) for i in ys):
                ys_fix = [ys]
            else: 
                ys_fix = ys
            
    datas = len(xs_fix)
    non = np.repeat(None,datas)
    one = np.repeat(1,datas)
    if not dlab:
        dlab = non
    if not mark:
        mark = non
    if not ms: 
        ms = one
    if not lw: 
        lw = one
    if not mark.all():
        mark = ['.']*datas
    if not dcol: 
        dcol = ['black']*datas
    if not ls:
        ls = ['solid']*datas
    if not trsp: 
        trsp = one
    
    # set title according to share_ttl
    if share_ttl == False:
        axs[p].set_title(ttl) 
    elif share_ttl == True:
        figure_global_output.suptitle(ttl)
        
    ds = range(datas) 
    if plt_type == 0 or plt_type == 'plot': 
        [axs[p].plot(xs_fix[n],ys_fix[n],c=dcol[n],label=dlab[n],linewidth=lw[n],markersize=ms[n],
                     marker=mark[n],linestyle=ls[n],alpha=trsp[n]) for n in ds]  
    if plt_type == 1 or plt_type == 'scatter':
        [axs[p].scatter(xs_fix[n],ys_fix[n],c=dcol[n],label=dlab[n],s=ms[n],alpha=trsp[n]) for n in ds]  
    if plt_type == 2 or plt_type == 'qqplot':
        [qqplot(data=xs_fix[n],line='r',ax=axs[p],marker=mark[n],color=dcol[n],label=dlab[n],alpha=trsp[n]) for n in ds]
        axs[p+1].boxplot([xs_fix[n] for n in ds],labels=[dlab[n] for n in ds]) 
    
    # fix labels according to share_axis_bool_output
    if share_axis_bool_output == 'x' or share_axis_bool_output == 1:
        axs[-1].set_xlabel(xlab)
        axs[p].set_ylabel(ylab)
    elif share_axis_bool_output == 'y' or share_axis_bool_output == 2: 
        axs[p].set_xlabel(xlab)
        axs[0].set_ylabel(ylab)
    elif share_axis_bool_output == 'xy' or share_axis_bool_output == 'yx' or share_axis_bool_output == 'both' or share_axis_bool_output == 3:
        axs[-1].set_xlabel(xlab)
        axs[0].set_ylabel(ylab) 
    elif share_axis_bool_output == 'no' or share_axis_bool_output == 0:
        axs[p].set_xlabel(xlab)
        axs[p].set_ylabel(ylab) 
    
    # set fitted layout according to tight
    if tight == True:
        plt.tight_layout()
        
    # set axis tics according to no_ticks
    if no_ticks == True:
        axs[p].set_yticks([])
        axs[p].set_xticks([])
        
    # define preset axis, according to input
    if h_ax == None:
        h_ax == axs[p].axhline(visible=False)
    elif h_ax == 0:
        axs[p].axhline(y=0,xmin=0,xmax=1,color='black',linestyle='solid',linewidth=0.5,alpha=1)
    elif h_ax == 1:
        axs[p].axhline(y=0,xmin=0,xmax=1,color='black',linestyle='dashed',linewidth=1,alpha=0.5)
    elif h_ax == 2: 
        axs[p].axhline(y=0,xmin=0,xmax=1,color='black',linestyle='dotted',linewidth=1,alpha=1)
    if v_ax == None:
        v_ax = axs[p].axvline(visible=False)
    elif v_ax == 0:
        axs[p].axvline(x=0,ymin=0,ymax=1,color='black',linestyle='solid',linewidth=0.5,alpha=1)
    elif v_ax == 1:
        axs[p].axvline(x=0,ymin=0,ymax=1,color='black',linestyle='dashed',linewidth=1,alpha=0.5) 
    elif v_ax == 2:
        axs[p].axvline(x=0,ymin=0,ymax=1,color='black',linestyle='dotted',linewidth=1,alpha=1)
    
    # set legends
    axs[p].legend() 
        
def file_select(path=None,set_cols=[0,1],cut_first_row=True,separator=','): 
    if path == None: 
        print('Error: No path selected')
        return
    else:
        filename, file_extension = os.path.splitext(path)
    if file_extension == '.excel':
        data = pd.read_excel(path,usecols=set_cols).to_numpy()
    elif file_extension == '.csv':
        data = pd.read_csv(path,usecols=set_cols, sep=separator).to_numpy()
    else:
        print('Error: Selected file type is not valid (use help function to see allowed file types)')
        return
    if cut_first_row == True:
        data_fix = data[1:,:]
    elif cut_first_row == False: 
        data_fix = data
    elif isinstance(cut_first_row,int) == True:
        data_fix = data[cut_first_row:,:]
    return data_fix

def fit_data(function=None,x_list=[],y_list=[],g_list=[],rel_var=False,N=100,mxf=5000):
    popt, pcov = curve_fit(f=function,xdata=x_list,ydata=y_list,p0=g_list,absolute_sigma=rel_var,maxfev=mxf)
    pcov_fix = [pcov[i][i] for i in range(len(popt))]
    pstd = [np.sqrt(pcov_fix[i]) for i in range(len(popt))]
    xs_fit = np.linspace(np.min(x_list),np.max(x_list),N)
    if len(popt) == 1:
        ys_fit = function(xs_fit,popt[0])
    elif len(popt) == 2: 
        ys_fit = function(xs_fit,popt[0],popt[1])
    elif len(popt) == 3: 
        ys_fit = function(xs_fit,popt[0],popt[1],popt[2])
    elif len(popt) == 4: 
        ys_fit = function(xs_fit,popt[0],popt[1],popt[2],popt[3])
    elif len(popt) == 5: 
        ys_fit = function(xs_fit,popt[0],popt[1],popt[2],popt[3],popt[4])
    elif len(popt) == 6: 
        ys_fit = function(xs_fit,popt[0],popt[1],popt[2],popt[3],popt[4],popt[5])
    elif len(popt) == 7:
        ys_fit = function(xs_fit,popt[0],popt[1],popt[2],popt[3],popt[4],popt[5],popt[6])
    else: 
        print('Error: Too many constants to fit')
        return
    return popt, pcov_fix, pstd, xs_fit, ys_fit

def data_extrema(function,pos_index=False): 
    data = function
    max_id = np.where(max(data[:,1]) == data)[0][0] # index max val
    max_val = [data[max_id,0],data[max_id,1]] # find max val coord
    min_id = np.where(min(data[:,1]) == data)[0][0] # index min val
    min_val = [data[min_id,0],data[min_id,1]] # find min val coord
    if pos_index == False:
        return [min_val,max_val]
    elif pos_index == True:
        index_raw = [np.where(data[:,0] == min_val[0]),np.where(data[:,0] == max_val[0])] # index extremas
        index_list = [[index_raw[0][0][0]],[index_raw[1][0][0]]]
        return [min_val,max_val], index_list
