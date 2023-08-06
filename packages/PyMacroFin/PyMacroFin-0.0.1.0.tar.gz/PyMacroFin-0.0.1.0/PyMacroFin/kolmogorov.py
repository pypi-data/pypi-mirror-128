import numpy as np
import pandas as pd
from PyMacroFin.outerloop import hjb2d_map, hjb1d_map, hjb1d_map_stationary
import warnings
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
import scipy.spatial as spatial
import PyMacroFin.utilities as util
import os
import time
import scipy.stats as stats
from numbers import Number



def stationary_distribution(m,df,quiet=False,live_plot=True,reflecting=[],print_volume=False,dt='default',initialization='normal',sleep_time=0.0):
    """
    Run Fokker Planck / Kolmogorov forward equations to determine the movement through 
    time of a distribution given the law of motion and an initial distribution (in df) for state variables:
    $\frac{\partial p(x,t)}{\partial t} = -\sum_{i=1}^N \frac{\partial}{\partial x_i} \left[ \mu_i (x,t) p(x,t)\right] + \sum_{i=1}^N \sum_{j=1}^N \frac{\partial^2}{\partial x_i \partial x_j} \left[ S_{ij}(x,t)p(x,t)\right]$
    where $S_{ij} = \frac{1}{2} \sum_{k=1}^M \sigma_{ik}(x,t)\sigma_{jk}(x,t) = \frac{1}{2} \sigma \sigma^T$
    
    Parameters
    -----------
    m: model.macro_model 
        PyMacroFin macro_model object 
    df: pandas.core.frame.DataFrame
        DataFrame containing the model data required for the stationary distribution. 
    quiet: bool
        Whether or not to mute updates. Defaults to :code:`False`.
    live_plot: bool
        Whether or not to plot at each iteration to view the development of the distribution 
        through time. Defaults to :code:`True`.
    reflecting: list(str)
        Reflecting argument in the same format accepted by :code:`hjb2d_map` in the :code:`outerloop` module.
        If you want the minimum boundary for the first state variable to be a reflecting boundary, you should have 
        :code:`'b0min'` in the reflecting argument. Likewise, for the maximum boundary for the second state variable 
        you should have :code:`'b1max'` in the reflecting argument.
    print_volume: bool
        Whether or not to calculate and print the volume under the surface for each iteration. Primarily an option for 
        debugging purposes. Defaults to :code:`False`.
    dt: str or numeric
        Delta time to use for iterating the Kolmogorov forward equations through time. Defaults to the string :code:`'default'` which 
        uses the :code:`macro_model.options.dt` option in the :code:`m` argument to this function. You may also pass a numeric value.
    initialization: str 
        Method to use to initialize the distribution to start iteration from. Defaults to :code:`'normal'` which uses a normal or multivariate normal
        distribution centered at the center of the grid. The other current option is :code:`'uniform'` which initializes a uniform distribution across 
        the grid. A future release will include an option to use a custom initialization function.
    sleep_time: numeric
        Number of seconds to sleep between iterations. This can be helpful for plotting purposes (each iteration happens very quickly). Defaults to 
        :code:`0.0`.
    """
    
    # old arguments for the old hjb1d_map function 
    #method: str
    #    Finite difference method to use for iterating through the Kolmogorov forward equations. Defaults to :code:`'monotone'`.
    #    Other available options are :code:`'backward'`, :code:`'forward'`, and :code:`'central'`.
    #boundary_method: None or str
    #    Method for treating boundaries. The option :code:`'interior'` has volatility at boundary grid points only affect the interior rather than 
    #    pushing mass outside of the grid. The option :code:`'shadow'` uses shadow point to the exterior of the boundary grid point. The boundary 
    #    grid point loses mass to its exterior, but also receives mass from volatility and drift from its exterior. The drift and volatility at this 
    #    exterior shadow point is estimated from the variable values at the boundary grid point. Defaults to :code:`None`. 


    if len(m.boundaries)>0:
        df,m.options,m.grid = util.remove_boundary_conditions(df,m)
    if live_plot:
        util.start_dash(m,stationary_distribution=True)
    if m.state[-1] == 'o':
        one_dimension = True
    else:
        one_dimension = False
    if dt != 'default':
        assert isinstance(dt,Number), "dt must be 'default' or a number"
        m.options.dt = dt
    # initialize the error term 
    loop_error = 10
    volumestring = ''
    if one_dimension:
        if initialization=='normal':
            df['stationary'] = util.initial_stationary_1d(m,df[m.state[0]],4)
        elif initialization=='uniform':   
            df['stationary'] = 1/(m.options.end0-m.options.start0)
    else:
        if initialization=='normal':
            df['stationary'] = util.initial_stationary_2d(m).pdf(df[[m.state[0],m.state[1]]])
        elif initialization=='uniform':
            df['stationary'] = 1/(m.options.end0-m.options.start0)*(m.options.end1-m.options.start1) # start with something with volume one and uniform distribution 
    var = 'stationary'
    df['_u_{}'.format(var)] = 0.0
    df['_r_{}'.format(var)] = 0.0
    for i_loop in range(m.options.max_hjb):
        df['_{}_old'.format(var)] = df[var].copy()
        if one_dimension:
            # vol_multiplier hould start at 0.01, converge to a tolerance, then slowly increase toward one, waiting for convergence 
            # at each multiplier before increasing
            df[var] = hjb1d_map(m,df,0,var_type='stationary',reflecting=reflecting,stationary_distribution=True,method='proper-high-order-central',boundary_method=None) 
            #df[var] = hjb1d_map_stationary(m,df,method='central',vol_multiplier=1,accuracy=8)
        else:
            df[var] = hjb2d_map(m,df,0,var_type='stationary',reflecting=reflecting,stationary_distribution=True) 
        loop_error = (np.abs(df[var]-df['_{}_old'.format(var)])).max()  
        if print_volume:
            myinput = np.hstack([np.reshape(m.grid.x[0],[m.options.N,1],order='F'),np.reshape(m.grid.x[1],[m.options.N,1],order='F'),np.reshape(df[var].to_numpy(),[m.options.N,1],order='F')])
            volume = trapezoidal_volume(myinput)
            volumestring = ", volume = {0:.3g}".format(volume)
        if not quiet:
            print("Stationary distribution iteration {0} completed with error {1:.3g} and dt = {2}".format(i_loop+1,loop_error,m.options.dt)+volumestring)
        if live_plot:
            df[['stationary',m.state[0],m.state[1]]].to_csv('./tmp{}_stationary/dash_data.csv'.format(m.name),index=False)
            if sleep_time>0:
                time.sleep(sleep_time)
        if i_loop > m.options.min_hjb1 and loop_error < m.options.tol_hjb:
            break
        if i_loop == m.options.max_hjb-1:
            warnings.warn("Maximum iterations reached for calculating the stationary distribution. Convergence not achieved.")
    # plot when converged or reached maximum iterations
    if not live_plot:
        stationary_plot(m,df,one_dimension=one_dimension)
    # return the dataframe portion that contains the stationary distribution 
    return df[var]
	
pio.renderers.default = 'browser'
#pio.renderers.default = 'svg'

def stationary_plot(m,result,var='stationary',use_dash=True):
    """
    Plot the stationary distribution
    """
    if m.one_dimension:
        fig = make_subplots(rows=1,cols=1)
    else:
        fig = make_subplots(rows=1,cols=1,specs=[[{'type':'surface'}]])
    traces = []
    if m.one_dimension:
        myx = np.linspace(m.options.start0,m.options.end0,m.options.n0)
        myy = np.reshape(result[var].to_numpy(),[m.options.n1,m.options.n0],order='F')[0,:]
        t = go.Scatter(x=myx,y=myy,name=var,mode='lines')
    else:
        t = go.Surface(x=m.grid.x[0],y=m.grid.x[1],z=result[var].to_numpy().reshape([m.options.n1,m.options.n0],order='F'),colorscale='Viridis',name=var)
    traces.append(t)
    fig.add_trace(t,row=1,col=1)
    fig.update_xaxes(title_text=m.state[0], row=1, col=1)
    if not m.one_dimension:
        fig.update_yaxes(title_text=m.state_latex[1], row=1, col=1)
    else:
        fig.update_yaxes(title_text=var, row=1, col=1)
    fig.update_layout(height=1000*1, width=1000*1, title_text="Stationary Distribution",title_x=0.5,title_font_size=24)
    for i in fig['layout']['annotations']:
        i['font'] = dict(size=22)
    if not m.one_dimension:
        fig.update_traces(showscale=False)
    if use_dash:
        return fig
    else:
        fig.show()
    
def trapezoidal_volume(xyz):
    """Calculate volume under a surface defined by irregularly spaced points
    using delaunay triangulation. "x,y,z" is a <numpoints x 3> shaped ndarray."""
    d = spatial.Delaunay(xyz[:,:2])
    tri = xyz[d.vertices]

    a = tri[:,0,:2] - tri[:,1,:2]
    b = tri[:,0,:2] - tri[:,2,:2]
    vol = np.cross(a, b) @ tri[:,:,2]
    return vol.sum() / 6.0

