#####################################################################################################################################################
#---------------------------------------------------------------------------------------------------------------------------------------------------#
#	- This file is a part of the VocalTractLab Python module PyVTL, see https://github.com/paul-krug/VocalTractLab
#---------------------------------------------------------------------------------------------------------------------------------------------------#
#
#	- Copyright (C) 2021, Paul Konstantin Krug, Dresden, Germany
#	- https://github.com/paul-krug/VocalTractLab
#	- Author: Paul Konstantin Krug, TU Dresden
#
#	- License info:
#
#		This program is free software: you can redistribute it and/or modify
#		it under the terms of the GNU General Public License as published by
#		the Free Software Foundation, either version 3 of the License, or
#		(at your option) any later version.
#		
#		This program is distributed in the hope that it will be useful,
#		but WITHOUT ANY WARRANTY; without even the implied warranty of
#		MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#		GNU General Public License for more details.
#		
#		You should have received a copy of the GNU General Public License
#		along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#---------------------------------------------------------------------------------------------------------------------------------------------------#
#####################################################################################################################################################
#---------------------------------------------------------------------------------------------------------------------------------------------------#

#---------------------------------------------------------------------------------------------------------------------------------------------------#
#####################################################################################################################################################
#---------------------------------------------------------------------------------------------------------------------------------------------------#
# Load essential packages:
import os
import warnings
import pandas as pd
import numpy as np
import VocalTractLab.VocalTractLabApi as vtl
import VocalTractLab.function_tools as FT
import matplotlib.pyplot as plt
from  itertools import chain
import math
import VocalTractLab.plotting_tools as PT
from VocalTractLab.plotting_tools import finalize_plot
from VocalTractLab.plotting_tools import get_plot
from VocalTractLab.plotting_tools import get_plot_limits
from VocalTractLab.plotting_tools import get_valid_tiers
#---------------------------------------------------------------------------------------------------------------------------------------------------#
#####################################################################################################################################################



#####################################################################################################################################################
#---------------------------------------------------------------------------------------------------------------------------------------------------#
class State_Sequence():
#---------------------------------------------------------------------------------------------------------------------------------------------------#
	def __str__( self, ):
		return str( self.states )
#---------------------------------------------------------------------------------------------------------------------------------------------------#
	def plot( self, plot_type = 'trajectory', time = 'seconds', **kwargs ):
		if plot_type in [ 'trajectory', 'trajectoris', 'time' ]:
			return self.plot_trajectories( time = time, **kwargs )
		elif plot_type in [ 'distribution', 'distributions', 'dist', 'dists' ]:
			return self.plot_distributions( **kwargs )
#---------------------------------------------------------------------------------------------------------------------------------------------------#
	def plot_distributions( self, parameters = None, axs = None, n_columns = 5, plot_kwargs = PT.state_hist_kwargs, **kwargs ):
		parameters = get_valid_tiers( parameters, self.states.columns )
		n_rows = math.ceil( len( parameters ) / n_columns )
		figure, axs = get_plot( n_rows = n_rows, n_columns = n_columns, axs = axs, sharex = False, sharey = True, gridspec_kw = {} )
		index_row = 0
		index_col = 0
		for index, parameter in enumerate( parameters ):
			if index_col == n_columns:
				index_row += 1
				index_col = 0
			y = self.states.loc[ :, parameter ]
			axs[ index_row, index_col ].hist( y, **plot_kwargs.get( parameter ) )
			axs[ index_row, index_col ].set( xlabel = parameter ) #, ylim = get_plot_limits( y ) )
			index_col += 1
		#for ax in axs:
		#	ax.label_outer()
		finalize_plot( figure, axs, hide_labels = False, **kwargs )
		return axs
#---------------------------------------------------------------------------------------------------------------------------------------------------#
	def plot_trajectories( self, parameters = None, axs = None, time = 'seconds', plot_kwargs = PT.state_plot_kwargs, **kwargs ):
		parameters = PT.get_valid_tiers( parameters, self.states.columns )
		constants = vtl.get_constants()
		figure, axs = get_plot( n_rows = len( parameters ), axs = axs )
		for index, parameter in enumerate( parameters ):
			y = self.states.loc[ :, parameter ]
			x = np.array( range( 0, len( y ) ) )
			if time == 'seconds':
				x = x / constants[ 'samplerate_internal' ]
			axs[ index ].plot( x, y, **plot_kwargs.get( parameter ) )
			axs[ index ].set( ylabel = parameter, ylim = get_plot_limits( y ) )
		if time == 'seconds':
			plt.xlabel( 'Time [s]' )
		else:
			plt.xlabel( 'Tract state' )
		#for ax in axs:
		#	ax.label_outer()
		finalize_plot( figure, axs, **kwargs )
		return axs
#---------------------------------------------------------------------------------------------------------------------------------------------------#
#####################################################################################################################################################



#####################################################################################################################################################
class Sub_Glottal_Sequence( State_Sequence ):
	def __init__( self,
		          states: np.array,
		          name: str = 'sequence',
		          extension: str = '.sub_glottal',
		          ):
		self.constants = vtl.get_constants()
		if len( states.shape ) != 2:
			raise ValueError( "Shape of passed state is not two-dimensional. The shape should be (x: no. states, y: no. features)" )
		if states.shape[ 1 ] != self.constants[ 'n_glottis_params' ]:
			raise ValueError( "Dimension of features is {}, but should be {}.".format( states.shape[ 1 ], self.constants[ 'n_glottis_params' ] ) )
		self.param_info = vtl.get_param_info( 'glottis' )
		self.name = name
		self.extension = extension
		self.states = pd.DataFrame( states, columns = self.param_info.index )
		self.glottis = self.states
		self.length = len( self.glottis.index )
		return
#---------------------------------------------------------------------------------------------------------------------------------------------------#
	@classmethod
	def from_sub_glottal_sequences( cls, sub_glottal_sequence_list ):
		sub_glottal_sequence_list = FT.check_if_input_lists_are_valid( [ sub_glottal_sequence_list ], [ Sub_Glottal_Sequence ] )
		states = pd.concat( [ x.states for x in sub_glottal_sequence_list ] ).to_numpy()
		name = [ x.name for x in sub_glottal_sequence_list ] #TODO concat string in list comp
		return cls( states, name )
#---------------------------------------------------------------------------------------------------------------------------------------------------#
	@classmethod
	def from_tract_file( cls, tract_file_path ):
		df_GLP = pd.read_csv( tract_file_path, delim_whitespace = True, skiprows= lambda x: read_tract_seq_GLP(x) , header = None )
		return cls( df_GLP.to_numpy(), tract_file_path )
#---------------------------------------------------------------------------------------------------------------------------------------------------#
	def append( self, sub_glottal_sequence ):
		if not isinstance( sub_glottal_sequence, Sub_Glottal_Sequence ):
			raise ValueError( 'Trying to append an object of type {} to an object of type {}'.format( type( self ), type( sub_glottal_sequence ) ) )
		self.glottis = pd.concat( [self.glottis, sub_glottal_sequence.glottis ] )
		self.name = self.name + ',' + sub_glottal_sequence.name
		return
#####################################################################################################################################################



#####################################################################################################################################################
class Supra_Glottal_Sequence( State_Sequence ):
	def __init__( self,
		          states: np.array,
		          name: str = 'sequence',
		          extension: str = '.supra_glottal',
		          ):
		self.constants = vtl.get_constants()
		if len( states.shape ) != 2:
			raise ValueError( "Shape of passed state is not two-dimensional. The shape should be (x: no. states, y: no. features)" )
		if states.shape[ 1 ] != self.constants[ 'n_tract_params' ]:
			raise ValueError( "Dimension of features is {}, but should be {}.".format( states.shape[ 1 ], self.constants[ 'n_tract_params' ] ) )
		self.param_info = vtl.get_param_info( 'tract' )
		self.name = name
		self.extension = extension
		self.states = pd.DataFrame( states, columns = self.param_info.index )
		self.tract = self.states
		self.length = len( self.tract.index )
		return
#---------------------------------------------------------------------------------------------------------------------------------------------------#
	@classmethod
	def from_supra_glottal_sequences( cls, supra_glottal_sequence_list ):
		supra_glottal_sequence_list = FT.check_if_input_lists_are_valid( [ supra_glottal_sequence_list ], [ Sub_Glottal_Sequence ] )
		states = pd.concat( [ x.states for x in supra_glottal_sequence_list ] ).to_numpy()
		name = [ x.name for x in supra_glottal_sequence_list ] #TODO concat string in list comp
		return cls( states, name )
#---------------------------------------------------------------------------------------------------------------------------------------------------#
	@classmethod
	def from_tract_file( cls, tract_file_path ):
		df_VTP = pd.read_csv( tract_file_path, delim_whitespace = True, skiprows= lambda x: read_tract_seq_VTP(x) , header = None )
		return cls( df_VTP.to_numpy(), tract_file_path )
#---------------------------------------------------------------------------------------------------------------------------------------------------#
	def append( self, supra_glottal_sequence ):
		if not isinstance( supra_glottal_sequence, Supra_Glottal_Sequence ):
			raise ValueError( 'Trying to append a {} type object to a {} type object.'.format( type( self ), type( supra_glottal_sequence ) ) )
		self.tract = pd.concat( [ self.tract, supra_glottal_sequence.tract ] )
		self.name = self.name + ',' + supra_glottal_sequence.name
		return
#---------------------------------------------------------------------------------------------------------------------------------------------------#
	def apply_biomechanical_constraints():
		self.tract = vtl.tract_sequence_to_limited_tract_sequence( self.tract ).tract
#####################################################################################################################################################



#####################################################################################################################################################
class Tract_Sequence( State_Sequence ):
	def __init__( self,
		          tract_states: Supra_Glottal_Sequence,
		          glottis_states: Sub_Glottal_Sequence,
		          name: str = 'sequence',
		          extension: str = '.tract',
		          ):
		if not isinstance( tract_states, Supra_Glottal_Sequence ):
			raise TypeError( '{} type object was passed, but {} was expected.'.format( tract_states, Supra_Glottal_Sequence ) )
		if not isinstance( glottis_states, Sub_Glottal_Sequence ):
			raise TypeError( '{} type object was passed, but {} was expected.'.format( glottis_states, Sub_Glottal_Sequence ) )
		for key in tract_states.constants:
			if tract_states.constants[ key ] != glottis_states.constants[ key ]:
				raise ValueError( 'API constant {} is different for supra and sub glottal state sequence.'.format( key ) )
		self.param_info = dict( tract = tract_states.param_info, glottis = glottis_states.param_info )
		self.name = name
		self.extension = extension
		self.states = pd.concat( [ tract_states.tract, glottis_states.glottis ], axis = 1 )
		self.tract = self.states[ self.param_info[ 'tract' ].index ]
		self.glottis = self.states[ self.param_info[ 'glottis' ].index ]
		#self.supra_glottal_sequence = tract_states
		#self.sub_glottal_sequence = glottis_states
		lengths_difference = np.abs( tract_states.length - glottis_states.length )
		if tract_states.length > glottis_states.length:
			warnings.warn( 'lengths of supra glottal sequence is longer than sub glottal sequence. Will pad the sub glottal sequence now.' )
			self.glottis = pd.concat( [ self.glottis, 
				                        pd.DataFrame( [ self.glottis.iloc[ -1, : ] for _ in range(0, lengths_difference ) ] )
				                        ], ignore_index = True,
				                        )
		elif tract_states.length < glottis_states.length:
			warnings.warn( 'lengths of supra glottal sequence is shorter than sub glottal sequence. Will pad the supra glottal sequence now.' )
			self.tract = pd.concat( [ self.tract, 
				                      pd.DataFrame( [ self.tract.iloc[ -1, : ] for _ in range(0, lengths_difference ) ] )
				                      ], ignore_index = True,
				                      )
		if len( self.tract.index ) != len( self.glottis.index ):
			raise ValueError( 'Lengths of supra- and sub-glottal parts do not match in tract_sequence: {}'.format( self.name + self.extension ) )
		self.length = len( self.tract.index )
		return
#---------------------------------------------------------------------------------------------------------------------------------------------------#
	@classmethod
	def from_tract_file( cls, tract_file_path ):
		df_GLP = pd.read_csv( tract_file_path, delim_whitespace = True, skiprows= lambda x: read_tract_seq_GLP(x) , header = None )
		df_VTP = pd.read_csv( tract_file_path, delim_whitespace = True, skiprows= lambda x: read_tract_seq_VTP(x) , header = None )
		return cls( Supra_Glottal_Sequence( df_VTP.to_numpy() ), Sub_Glottal_Sequence( df_GLP.to_numpy() ), tract_file_path )
#---------------------------------------------------------------------------------------------------------------------------------------------------#
	def append( self, tract_sequence ):
		if not isinstance( tract_sequence, Tract_Sequence ):
			raise ValueError( 'Trying to append a {} type object to a {} type object.'.format( type( self ), type( tract_sequence ) ) )
		self.states = pd.concat( [ self.states, tract_sequence.states ] )
		self.tract = pd.concat( [self.tract, tract_sequence.tract ] )
		self.name = self.name + ',' + supra_glottal_sequence.name
		return
#---------------------------------------------------------------------------------------------------------------------------------------------------#
	def apply_biomechanical_constraints( self, ):
		self.tract = vtl.tract_sequence_to_limited_tract_sequence( self.tract ).tract
#---------------------------------------------------------------------------------------------------------------------------------------------------#
	def insert( self, parameter, trajectory, trajectory_sr = None, start = 0, time_axis = 'samples', padding = None, smooth = True ):
		if parameter in self.tract.columns:
			feature = self.tract
		elif parameter in self.glottis.columns:
			feature = self.glottis
		else:
			#if parameter not in chain( *[ self.tract.columns, self.glottis.columns ] ):
			raise ValueError( 'The specified parameter: {} is neither a supra glottal nor a sub glottal parameter!'.format( parameter ) )
		if time_axis not in [ 'seconds', 'samples' ]:
			raise ValueError( 'Argument "time_axis" must be "seconds" or "samples", not "{}"!'.format( time_axis ) )
		trajectory = FT.check_if_list_is_valid( trajectory, (int, float) )
		state_sr = 44100/110
		if trajectory_sr != None:
			trajectory = resample_trajectory( trajectory, trajectory_sr, state_sr )
		if time_axis == 'seconds':
			start = round( state_sr * start )
		if padding == 'same':
			trajectory = [ trajectory[0] 
			               for _ in range(0, start) ] + trajectory + [ trajectory[-1] 
			               for _ in range( start + len( trajectory ), len(feature[parameter]) ) 
			               ] 
			#plt.plot(trajectory)
			#plt.show()
			feature[ parameter ] = trajectory
		else:	
			feature.loc[ start : start + len( trajectory ) - 1, parameter ] = trajectory
		#values_a = feature.loc[ : start, parameter ].to_list()
		#values_b = feature.loc[ : start, parameter ].to_list()
		#smooth_values_1 = transition( values_a, resampled_values, 40, fade='in' )
		#smooth_values_2 = transition( smooth_values_1, values_b, 40, fade='out' )
		#print(len(smooth_values_2))
		#feature.loc[ 0 : len( smooth_values_2 )-1, parameter ] = smooth_values_2
		return
#---------------------------------------------------------------------------------------------------------------------------------------------------#
	def to_sub_glottal_sequence( self ):
		return Sub_Glottal_Sequence( self.glottis.to_numpy(), name = '' ) #TODO name
#---------------------------------------------------------------------------------------------------------------------------------------------------#
	def to_supra_glottal_sequence( self ):
		return Supra_Glottal_Sequence( self.tract.to_numpy(), name = '' ) #TODO name
#---------------------------------------------------------------------------------------------------------------------------------------------------#
	# def plot( self, parameters = ['LP','JA','LD','HX','HY'], n_params = 19 ):
	# 	figure, axs = plt.subplots( len(parameters), figsize = (8, 4/3 *len(parameters) ), sharex = True, gridspec_kw = {'hspace': 0} )
	# 	#figure.suptitle( 'Sharing both axes' )
	# 	#parameters = self.tract.columns
	# 	for index, parameter in enumerate( parameters ):
	# 		axs[ index ].plot( self.tract.loc[ :, parameter ] )
	# 		axs[ index ].set( ylabel = parameter )
	# 	plt.xlabel( 'Tract state' )
	# 	for ax in axs:
	# 	    ax.label_outer()
	# 	figure.align_ylabels( axs[:] )
	# 	plt.show()
	# 	return
#####################################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------------------------#
def resample_trajectory( trajectory, trajectory_sr, target_sr ):
	resample_rate = trajectory_sr / target_sr
	resampled_x = np.arange( 0, len(trajectory)-1, resample_rate )
	#resampled_y = interpolate( resampled_x, trajectory )
	return interpolate( resampled_x, trajectory )
#---------------------------------------------------------------------------------------------------------------------------------------------------#
def s( x, a, b ):
	return 0.5 + 0.5 * np.tanh( ( x - a ) / b )
#---------------------------------------------------------------------------------------------------------------------------------------------------#
def h( x, g, f, a = 0, b = 2 ):
	p = s( x, a, b )
	return (p * g) + (( 1 - p ) * f)
#---------------------------------------------------------------------------------------------------------------------------------------------------#
def transition( values_a, values_b, window_size, fade ):
	#print( 'len val a: ', len(values_a) )
	#print( 'len val b: ', len(values_b) )
	start = np.clip( len( values_a ) - int(window_size*0.5), a_min = 0, a_max = None, dtype = int )
	values_window_a = values_a[ start : ]
	values_window_b = values_b[ : window_size - len( values_window_a ) ]
	#print( 'len val w a: ', len(values_window_a) )
	#print( 'len val w b: ', len(values_window_b) )
	values_window_a = values_window_a + [ values_window_a[-1] for _ in range( 0, window_size - len(values_window_a) ) ]
	values_window_b = [ values_window_b[0] for _ in range( 0, window_size - len(values_window_b) ) ] + values_window_b
	#print( 'len val w a: ', values_window_a )
	#print( 'len val w b: ', values_window_b )
	#if fade == 'in':
	g = values_window_a
	f = values_window_b
	#elif fade == 'out':
	#	g = values_window_a
	#	f = values_window_b
	#else:
	#	raise ValueError( 'Argument "fade" must be "in" or "out", not "{}"!'.format( fade ) )
	values_window = [ h( x, f[x], g[x], window_size/2 ) for x in range( 0, len(values_window_a) ) ]
	#plt.plot( values_a[ : start ] + values_window + values_b[ window_size : ] )
	#plt.show()
	#stop
	#print( 'len val w: ', len(values_window) )
	return values_a[ : start ] + values_window + values_b[ window_size : ]
#---------------------------------------------------------------------------------------------------------------------------------------------------#
def pad( values: list, front: int = 0, back: int = 0, type: str = 'same', smooth = True ):
	insert_front = [ value[0] for _ in range( 0, front ) ]
	insert_back = [ value[-1] for _ in range( 0, back ) ]
	return insert_front + values + insert_back
#---------------------------------------------------------------------------------------------------------------------------------------------------#
def interpolate( values_x, values_y, type = 'linear' ):
	interpolated_values = []
	for x in values_x:
		x_0 = int( x )
		x_1 = int( x ) + 1
		y_0 = values_y[ x_0 ]
		y_1 = values_y[ x_1 ]
		interpolated_values.append( ( (y_0 * (x_1-x)) + (y_1 * (x-x_0)) ) / (x_1 - x_0) )
	return interpolated_values
#---------------------------------------------------------------------------------------------------------------------------------------------------#
def read_tract_seq_GLP( index ):
	if (index > 7) and (index % 2 == 0):
		return False
	else:
		return True
#---------------------------------------------------------------------------------------------------------------------------------------------------#
def read_tract_seq_VTP( index ):
	if (index > 7) and ((index-1) % 2 == 0):
		return False
	else:
		return True
#---------------------------------------------------------------------------------------------------------------------------------------------------#
#####################################################################################################################################################