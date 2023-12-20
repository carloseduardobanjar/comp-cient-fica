import skvideo.io
import numpy as np
import random
from numba import prange
from sklearn.cluster import KMeans
from tqdm import tqdm

def encontra_background(video):
  background = video[0]
  background.shape
  n_frames = 20
  frames_idx = []
  cols = video.shape[2]
  rows = video.shape[1]
  for i in range(0, n_frames):
    frames_idx.append(random.randint(0, video.shape[0]))
  for x in tqdm(prange(0, cols)):
    for y in prange(0, rows):
      colors=[]
      for z in frames_idx:
        colors.append(video[z][y][x])
      ca = KMeans(n_clusters = 2)
      ca = ca.fit(colors)
      labels, counts = np.unique(ca.labels_, return_counts=True)
      clusters = dict(zip(labels, counts))
      most_common = max(clusters, key=clusters.get)
      if most_common == 1:
        colors = [colors[i] for i in np.where(np.array(ca.labels_))[0]]
      else:
        colors = [colors[i] for i in np.where(np.logical_not(np.array(ca.labels_)))[0]]
      colors_a = np.array(colors)
      background_pixel = []
      background_pixel.append(np.median(colors_a[:,0]))
      background_pixel.append(np.median(colors_a[:,1]))
      background_pixel.append(np.median(colors_a[:,2]))
      background[y][x] = background_pixel
  return background

def main():
    video = skvideo.io.vread("video.mp4")
    background=encontra_background(video)
    video = video.astype("int16")
    background = background.astype("int16")
    foreground = video.copy()
    for i in range(0,foreground.shape[0]):
        foreground[i] = np.subtract(video[i], background)
        np.clip(foreground[i], 0, 255, out=foreground[i])
        foreground[i] = foreground[i].astype(np.uint8)

    foreground = foreground.astype(np.uint8)
    skvideo.io.vwrite("foreground.mp4", foreground)

if __name__ == "__main__":
    main()

