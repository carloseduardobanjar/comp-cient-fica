import skvideo.io
import numpy as np
import random
from sklearn.cluster import KMeans
from tqdm import tqdm
import time
from concurrent.futures import ProcessPoolExecutor
import argparse
import warnings
warnings.filterwarnings("ignore")

def process_columns(video, frames_idx, cols_range, rows):
    columns_background = {}
    for x in cols_range:
        column_background = np.zeros((rows, 3), dtype=np.uint8)
        for y in range(rows):
            colors = [video[z][y][x] for z in frames_idx]
            kmeans = KMeans(n_clusters=2)
            kmeans.fit(colors)

            labels, counts = np.unique(kmeans.labels_, return_counts=True)
            clusters = dict(zip(labels, counts))
            common_label = max(clusters, key=clusters.get)

            selected_colors = [colors[i] for i, label in enumerate(kmeans.labels_) if label == common_label]
            selected_colors = np.array(selected_colors)

            median_color = np.median(selected_colors, axis=0)
            column_background[y] = median_color

        columns_background[x] = column_background
    return columns_background

def encontra_background(video, threads, n_frames):
    n_frames = 20
    frames_idx = [random.randint(0, video.shape[0] - 1) for _ in range(n_frames)]
    # frames_idx = list(range(video.shape[0]))
    cols = video.shape[2]
    rows = video.shape[1]
    background = np.zeros((rows, cols, 3), dtype=np.uint8)

    cols_per_process = cols // threads
    col_ranges = [(i * cols_per_process, (i + 1) * cols_per_process) for i in range(threads)]
    col_ranges[-1] = (col_ranges[-1][0], cols)

    with ProcessPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(process_columns, video, frames_idx, range(start, end), rows) for start, end in col_ranges]

        for future in tqdm(futures, desc="Processing columns in fixed processes"):
            columns_background = future.result()
            for x, column_background in columns_background.items():
                background[:, x] = column_background

    return background

def main(filename, frames, threads):
    start_time = time.time()
    video = skvideo.io.vread(filename)
    end_time = time.time()
    execution_time_entrada = end_time - start_time

    start_time = time.time()
    background = encontra_background(video, threads, frames)
    video = video.astype("int16")
    background = background.astype("int16")
    foreground = video.copy()

    for i in range(foreground.shape[0]):
        foreground[i] = np.subtract(video[i], background)
        np.clip(foreground[i], 0, 255, out=foreground[i])
        foreground[i] = foreground[i].astype(np.uint8)
    end_time = time.time()
    execution_time_processamento = end_time - start_time
    
    start_time = time.time()
    skvideo.io.vwrite(f"foreground_videos/{filename.split('.')[0]}_{frames}_{threads}.mp4", foreground)
    end_time = time.time()
    execution_time_saida = end_time - start_time
    print(execution_time_entrada, execution_time_processamento, execution_time_saida)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("filename", type=str, help="Nome do arquivo de vídeo de entrada.")
    parser.add_argument("frames", type=int, help="Quantidade de frames a ser analisada.")
    parser.add_argument("threads", type=int, help="Quantidade de threads para executar.")
    
    args = parser.parse_args()
    main(args.filename, args.frames, args.threads)
    