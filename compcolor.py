"""
Class implementing a multi-channel image renderer
"""

# Author: Guillaume Witz, Science IT Support, Bern University, 2020
# License: BSD3

import numpy as np
import ipywidgets as ipw
import skimage
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter
from IPython.display import HTML, display, Video
import matplotlib.animation as animation
import imageio

from matplotlib.colors import ListedColormap

class Combcol:
    
    def __init__(self, image,
                colors = ['Red','Green','Blue']):

        """Standard __init__ method.
        
        Parameters
        ----------
        image : numpy array
            image array
        colors : list of str
            list of colors to use a colormap for each channel
        
        Attributes
        ----------
            
        colormaps = dict
            dictionary of matplotlib ListedColormap
        
        """
        
        self.image = image
        self.colors = colors
        
        self.selected_contrast = [(0.0, 255.0) for i in range(3)]
        self.selected_colors = ['Red', 'Green', 'Blue']
        
        self.def_colormaps()
        
        self.hist_button = ipw.Button(description = 'Create movie')
        self.hist_button.on_click(self.button_callback)
        self.out_movie = ipw.Output()
        
       
    def def_colormaps(self):
        '''Generate color maps'''
        
        self.colormaps = {}
        custom_map = None
        
        custom_map = ListedColormap(np.c_[np.linspace(0,1,256),np.zeros(256),np.zeros(256)])
        self.colormaps['Red'] = custom_map
        
        custom_map = ListedColormap(np.c_[np.zeros(256),np.linspace(0,1,256),np.zeros(256)])
        self.colormaps['Green'] = custom_map
        
        custom_map = ListedColormap(np.c_[np.zeros(256),np.zeros(256),np.linspace(0,1,256)])
        self.colormaps['Blue'] = custom_map
        
        custom_map = ListedColormap(np.c_[np.zeros(256),np.linspace(0,1,256),np.linspace(0,1,256)])
        self.colormaps['Cyan'] = custom_map
        
        
    def combine(self, images, colors = None, contrast = None):
        '''Combine up to three images in a maximum projection RGB image'''
        
        if colors is None:
            colors = self.selected_colors
        if contrast is None:
            contrast = self.selected_contrast
            
        images = skimage.exposure.rescale_intensity(images, out_range = np.uint8).astype(np.uint8)
        rescaled_images = [skimage.exposure.rescale_intensity(images[i,:,:], in_range = contrast[i], out_range = np.uint8) for i in range(images.shape[0])]
                                   
        colored_images = [self.colormaps[colors[ind]](im) for ind, im in enumerate(rescaled_images)]
        
        im_combined = np.max(np.stack(colored_images,axis = 3),axis = 3)
        
        return im_combined
    
    
    def interactive_colors(self):
        '''Create an interactive GUI to set colors and contrast'''
        
        contrast = [ipw.FloatRangeSlider(min=0,max = 255, step=1, value = (0,255),layout={'width': '300px'}) for i in range(3)]
        time_slider = ipw.IntSlider(min=0, max = self.image.shape[0], value = 0, description = 'Time')
        possible_colors = ['Red','Green','Blue','Cyan']
        color_select = [ipw.Select(options = possible_colors, value = possible_colors[i],layout={'width': '300px'}) for i in range(3)]
        
        def f(c0, c1, c2, t, col0, col1, col2, im):
            
            self.selected_colors = [col0, col1, col2]
            self.selected_contrast = [c0,c1,c2]

            im_time = im[t,:,:,:].copy()            
            im_combined = self.combine(im_time, colors = self.selected_colors, contrast = self.selected_contrast)

            plt.figure(figsize=(4,4))
            plt.imshow(im_combined)

        ui_contrast = {'c'+str(ind): x for ind, x in enumerate(contrast)}
        ui_time = {'t':time_slider}
        ui_im ={'im' : ipw.fixed(self.image)}
        ui_col = {'col'+str(ind): x for ind, x in enumerate(color_select)}
        ui_widgets = {**ui_contrast, **ui_time, **ui_col, **ui_im}

        children = [ipw.VBox([ipw.HTML('Channel '+str(ind)), contrast[ind], color_select[ind]]) for ind in range(3)]
        tab = ipw.Tab()
        tab.children = children
        for i in range(len(children)):
            tab.set_title(i, 'Channel '+str(i))
        
        ui = ipw.VBox([time_slider, tab])

        out = ipw.interactive_output(f, ui_widgets)

        display(ipw.HBox([out, ui]))
    
    
    def movie_histogram(self):
        '''Create animated figure of image and histogram'''
        
        fig, axes = plt.subplots(1,2,figsize = (7,3))
        ims=[]
        for t in range(10):#range(im_proj.shape[0]):

            #create multi-channel iamge
            newim = self.combine(self.image[t,::])
            #show image and histogram
            a1 = axes[0].imshow(newim)
            ims.append([a1])
            for c in range(2):
                _,_,a2 = axes[1].hist(np.ravel(self.image[t,c,:,:]),color = self.selected_colors[c],alpha = 0.5,
                        bins = np.arange(0,8000,100))
                ims[-1]+=a2
            axes[0].set_axis_off()
            
        ani = animation.ArtistAnimation(fig, ims, interval=200, blit=True,
                                repeat_delay=1000)
        return ani
    
    
    def movie_histogram_writer(self, movie_name = 'movie.mp4'):
        '''Create and save a combined movie with image and histogram'''
        
        moviewriter = FFMpegWriter(fps=15)
        fig, axes = plt.subplots(1,2,figsize = (7,3))
        with moviewriter.saving(fig, movie_name, dpi=100):
            for t in range(10):#range(im_proj.shape[0]):
                
                axes[1].cla()
                #create multi-channel iamge
                newim = self.combine(self.image[t,::])
                #show image and histogram
                axes[0].imshow(newim)
                for c in range(2):
                    axes[1].hist(np.ravel(self.image[t,c,:,:]),color = self.selected_colors[c],alpha = 0.5,
                            bins = np.arange(0,8000,100))
                axes[0].set_axis_off()
            
                #update_figure(i)
                moviewriter.grab_frame()
        fig.clf()
                
    def button_callback(self, b):
        '''Call-back for movie creation button'''
        
        ani = self.movie_histogram()

        '''
        #using imageio
        filename = 'movie.mp4'
        vid = imageio.get_reader(filename,  'ffmpeg')

        ims=[]
        fig = plt.figure(figsize=(10,5))
        for x in list(vid.iter_data()):
            im = plt.imshow(x,animated=True)
            ims.append([im])
            
        ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True,
                                repeat_delay=1000)'''
        
        self.out_movie.clear_output()
        with self.out_movie:
            display(HTML(ani.to_html5_video()))
            #display(Video('./movie.mp4'))
            #display(HTML('<div align="middle"><video width="80%" controls><source src="./movie.mp4" type="video/mp4"></video></div>'))
            