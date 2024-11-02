import skvideo.io
import numpy as np
import random
from numba import prange
from sklearn.cluster import KMeans
from tqdm import tqdm
import argparse
import warnings
warnings.filterwarnings("ignore")

def encontra_background(video, n_frames):
  background = video[0]
  background.shape
  frames_idx = []
  cols = video.shape[2]
  rows = video.shape[1]
  frames_idx = [random.randint(0, video.shape[0] - 1) for _ in range(n_frames)]
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

def main(filename, qtd_frames):
    video = skvideo.io.vread(filename)
    background=encontra_background(video, qtd_frames)
    video = video.astype("int16")
    background = background.astype("int16")
    foreground = video.copy()
    for i in range(0,foreground.shape[0]):
        foreground[i] = np.subtract(video[i], background)
        np.clip(foreground[i], 0, 255, out=foreground[i])
        foreground[i] = foreground[i].astype(np.uint8)

    foreground = foreground.astype(np.uint8)
    skvideo.io.vwrite(f"./foreground_videos/{filename.split('.')[0]}_{qtd_frames}.mp4", foreground)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("filename", type=str, help="Nome do arquivo de vídeo de entrada.")
    parser.add_argument("frames", type=int, help="Quantidade de frames a ser analisada.")

    args = parser.parse_args()
    main(args.filename, args.frames)

