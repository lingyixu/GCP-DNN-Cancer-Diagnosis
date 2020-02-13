# functions needed for tiling

import time
import sys
import os
#import glob
#import pandas as pd
#import subprocess
#import pkg_resources
import numpy as np
#from openslide import deepzoom
import openslide as ops
from google.cloud import storage



class ProgressBar():
    def __init__(self,N,BarCounts = 40,newline_at_the_end=True, 
                    ProgressCharacter = "*", UnProgressCharacter = ' ', step = 1, dynamic_step = True):
        '''
        BarCounts : total number of bars in the progress bar
        newline_at_the_end : insert a newline when the loop ends
        ProgressCharacter : character to use for the progress bar (default is a full block)
        UnProgressCharacter : character to use for the remainder of progress bar (default is space)
        step : skip this many counts before updating the progress bar
        '''
        self.Time0 = time.time()
        self.BarCounts = BarCounts
        self.N = N
        self.i = 0
        self.newline_at_the_end = newline_at_the_end
        self.ProgressCharacter = ProgressCharacter
        self.UnProgressCharacter = UnProgressCharacter
        self.step = step    
        self.PrevWriteInputLength = 0
        self.dynamic_step = dynamic_step
        
    def Update(self,Text = '',no_variable_change = False, PrefixText=''):
        '''
        Text L: text to show during the update
        no_variable_change : do not update the internal counter if this is set to True
        '''        
        if not no_variable_change:
            self.i = self.i + 1
            
        if (self.i % self.step == 0) | (self.i==self.N):
            CurrentTime = (time.time()-self.Time0)/60.0
            CurrProgressBarCounts = int(self.i*self.BarCounts/self.N)
            self.WriteInput = u'\r%s|%s%s| %.1f%% - %.1f / %.1f minutes - %s'%(
                                                          PrefixText,
                                                          self.ProgressCharacter*CurrProgressBarCounts, 
                                                          self.UnProgressCharacter*(self.BarCounts-CurrProgressBarCounts), 
                                                          100.0*self.i/self.N, 
                                                          CurrentTime, 
                                                          CurrentTime*self.N/self.i,
                                                          Text)
            ExtraSpaces = ' '*(self.PrevWriteInputLength - len(self.WriteInput))    # Needed to clean remainder of previous text
            self.PrevWriteInputLength = len(self.WriteInput)                                        
            sys.stdout.write(self.WriteInput+ExtraSpaces)
            sys.stdout.flush()
            if (not no_variable_change) & self.newline_at_the_end & (self.i==self.N):
                print('\n')
    
    def NestedUpdate(self,Text = '',ProgressBarObj=None,no_variable_change = False, PrefixText=''): # nest this progressbar within another progressbar loop
        if ProgressBarObj!=None:
            ProgressBarObj.newline_at_the_end = False
            # assert not ProgressBarObj.newline_at_the_end, 'The object prints newline at the end. Please disable it.'
            self.newline_at_the_end = False
            no_variable_change = False
            PrefixText=ProgressBarObj.WriteInput
        self.Update(Text = Text,no_variable_change = no_variable_change, PrefixText=PrefixText)




def mkdir_if_not_exist(inputdir):
    if not os.path.exists(inputdir):
        os.makedirs(inputdir)
    return inputdir




def TileSVS(svsFile, outdir=None, outlocaldir = None, bucket_name=None, SaveToFile = True, tile_size=512, downsample = 1,
            bg_th = 220, max_bg_frac = 0.5, ProgressBarObj=None, **kwargs):    
    '''
    bg_th : intensities above this will be treated as background
    max_bg_frac : tiles with more background pixels than this fraction will not be saved to the disk. 
                  set this to 1 in order to save all tiles. This parameter only matters if SaveToFile=True
    '''
    L = downsample*tile_size
    Slide = ops.OpenSlide(svsFile)

    if SaveToFile:
        # set folder name
        tilesdir = os.path.join(outdir, os.path.basename(svsFile))  # I deleted a subfolder 'tiles'.
        mkdir_if_not_exist(tilesdir)
        tileslocaldir = os.path.join(outlocaldir, os.path.basename(svsFile))
        mkdir_if_not_exist(tileslocaldir)
        
        
    Xdims = np.floor((np.array(Slide.dimensions)-1)/L).astype(int)
    if SaveToFile:
        X = None
    else:
        X = np.zeros((Xdims[0], Xdims[1], tile_size, tile_size, 3), dtype='uint8')


    num_tiles = np.prod(Xdims)
    Pbar = ProgressBar(num_tiles, step=1)  # I deleted the script name 'util'
    
    
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    
    
    for m in range(Xdims[0]):
        for n in range(Xdims[1]):
            Pbar.NestedUpdate('(%d/%d,%d/%d)'%(m, Xdims[0], n, Xdims[1]), ProgressBarObj=ProgressBarObj)   

            try:
                tile = Slide.read_region((m*L, n*L), 0, (L, L))
            except ops.lowlevel.OpenSlideError:
                print('\n Skipping OpenSlideError, (m, n, L)=({:d}, {:d}, {:d}), {:s}'.format(m, n, L, svsFile))
                Slide = ops.OpenSlide(svsFile)
                tiles = ops.deepzoom.DeepZoomGenerator(Slide, tile_size=tile_size, overlap=0, limit_bounds=False)
                continue

            tile = tile.convert('RGB') # remove alpha channel
            tile = tile.resize((tile_size, tile_size))

            if SaveToFile:
                if (np.array(tile).min(axis=2)>=bg_th).mean() <= max_bg_frac: # only save tiles that are not background
                    outfile = os.path.join(tilesdir,'tile_%d_%d.jpg'%(m,n))
                    outlocalfile = os.path.join(tileslocaldir,'tile_%d_%d.jpg'%(m,n))
                    tile.save(outlocalfile, "JPEG", quality=100)
                    
                    blob = bucket.blob(outfile)
                    blob.upload_from_filename(outlocalfile)
                    
                    os.remove(outlocalfile)
            else:
                tile = np.array(tile)
                X[m,n,:tile.shape[0],:tile.shape[1],:] = tile

    Slide.close()
    return X

