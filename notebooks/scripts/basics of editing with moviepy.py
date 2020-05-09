#!/usr/bin/env python
# coding: utf-8

# In[1]:


from matplotlib import pyplot as plt
import pandas as pd

import sys, os
sys.path.insert(0, os.path.abspath('../scripts/'))
import footyviz


# # Loading Data
# 
# 

# In[2]:


data = pd.read_csv('../datasets/positional_data/liverpool_2019.csv', index_col=('play', 'frame'))
data.tail()


# In[5]:


#list of goals included in the dataset
data.index.get_level_values('play').unique()


# In[6]:


play = 'Liverpool [4] - 0 Barcelona'
df = data.loc[play]
df.tail()


# # Basic Plotting
# 
# You may have noticed I picked an interesting goal. It was my favorite football moment from 2019: a simple corner taken quickly.

# In[20]:


fig, ax, dfFrame = footyviz.draw_frame(df, t=5.7)


# This was probably what was on Trent Alexander-Arnold's head:

# In[21]:


fig, ax, dfFrame = footyviz.draw_frame(df, t=4)
fig, ax, dfFrame = footyviz.add_voronoi_to_fig(fig, ax, dfFrame)


# In[22]:


#you can mix different frames for the player's positioning and for the voronoi (e.g. fixing the voronoi to the time of the pass)
fig, ax, dfFrame = footyviz.draw_frame(df, t=5)
dfFrame_for_voronoi = footyviz.get_frame(df, t=4)
fig, ax, dfFrame = footyviz.add_voronoi_to_fig(fig, ax, dfFrame_for_voronoi)


# # MoviePy
# 
# MoviePy is a Python module for video editing that works nicely with matplotlib and Jupyter and is built on top of FFmpeg. You may think you never used FFMpeg, but you have. From Wikipedia:
# 
# > FFmpeg is used by software such as VLC media player, xine, Cinelerra-GG video editor, Plex, Kodi, Blender, HandBrake, YouTube, and MPC-HC; it handles video and audio playback in Google Chrome, and Linux version of Firefox. 
# 
# You can find MoviePy's documentation at: https://zulko.github.io/moviepy/
# 
# Let's start with a basic animation:

# In[23]:


from moviepy import editor as mpy
from moviepy.video.io.bindings import mplfig_to_npimage

def draw_frame_x(df, t, fps, voronoi=False):
    fig,ax,dfFrame = footyviz.draw_frame(df, t=t, fps=fps)
    if voronoi:
        fig, ax, dfFrame = footyviz.add_voronoi_to_fig(fig, ax, dfFrame)
    image = mplfig_to_npimage(fig)
    plt.close()
    return image    

def make_animation(df, fps=20, voronoi=False):
    #calculated variables
    length=(df.index.max()+20)/fps
    clip = mpy.VideoClip(lambda x: draw_frame_x(df, t=x, fps=fps, voronoi=voronoi), duration=length-1).set_fps(fps)
    return clip

clip = make_animation(df)

clip.ipython_display()
clip.write_videofile("Goal.mp4")


# This isn't much different from what you can do with Matplotlib's native animate capabilities.
# 
# The advantage of having MoviePy in the mix is having easy accsess to editing, compositing and transformation functions. Let's try some examples:

# In[ ]:


clip.rotate(90).ipython_display()


# In[ ]:


#moviepy allows for method chaining several effects in one line of code:
clip.rotate(90).crop(y1=100, y2=500).ipython_display()


# Linear editing is easy with the ``subclip`` method (for trimming) and ``concatenate_videoclips`` function (to join clips):

# In[ ]:


full_clip = mpy.concatenate_videoclips([make_animation(data.loc[play]) for play in data.index.get_level_values('play').unique()])

print('normal speed:', full_clip.duration, 'seconds')
print('2x speed:', full_clip.speedx(2).duration, 'seconds')

full_clip.ipython_display(t=50)
full_clip.write_videofile("AllGoals.mp4")


# Non-linear editing uses the ``CompositeClip`` object:

# In[ ]:


clip_voronoi = make_animation(df, voronoi=True)
composite_clip = mpy.CompositeVideoClip([clip, clip_voronoi.resize(0.3).set_position((200,100))])
composite_clip.ipython_display(t=4)


# In[ ]:




