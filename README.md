# Remoção do plano de fundo de vídeos usando k-means

### Autor: Carlos Eduardo de Schuller Banjar

## Utilização

### Linux

```
git clone https://github.com/carloseduardobanjar/comp-cientifica.git
```

Coloque um vídeo intitulado "video.mp4" dentro da pasta do repositório clonado e rode o comando

```
python3 main.py
```

## Tecnologias

- Python
- scikit-video
- numpy
- random
- numba
- scikit-learn
- tqdm

## Metodologia

### 1. Coleta de amostras

Para iniciar o processo de reconhecimento do plano de fundo em vídeos, coletamos 20 frames aleatórios do vídeo em questão.

Iremos demonstrar a metodologia aplicada a dois pixels, circulados em amarelo e vermelho.

![Frame](assets/imagem_com_circulos.png)

### 2. Análise de cores por pixel

Para cada pixel em cada frame selecionado, registramos as cores que ele assume nos 20 frames. Isso resulta em um conjunto de dados que representa a variação das cores ao longo dos frames.

Cores assumidas pelo pixel em vermelho:

![Cores](assets/cores_pixel_vermelho.png)
![Cores no gŕafico](assets/cores_vermelho_grafico.png)

Cores assumidas pelo pixel em amarelo:

![Cores](assets/cores_pixel_amarelo.png)
![Cores no gŕafico](assets/cores_amarelo_grafico.png)

### 3. Clusterização usando K-Means

Utilizamos o algoritmo K-Means para agrupar as cores registradas em dois clusters distintos. Este passo tem como objetivo separar as cores associadas ao plano de fundo das relacionadas ao objeto em movimento.

![Cluster](assets/cores_vermelho_cluster.png)
![Cluster](assets/cores_amarelo_cluster.png)

### 4. Identificação do cluster de fundo

Determinamos qual cluster contém mais elementos, considerando-o como o cluster associado ao plano de fundo. O outro cluster é associado ao objeto em movimento.

### 5. Estimativa da cor de fundo

No cluster identificado como plano de fundo, calculamos a mediana das cores para os canais R (vermelho), G (verde) e B (azul). Essa mediana representa a cor característica do plano de fundo.

![Cor do fundo](assets/cor_pixel_vermelho.png)
![Cor do fundo](assets/cor_pixel_amarelo.png)

### 6. Criação do frame de fundo

Criamos um novo frame com todos os pixels associados ao plano de fundo, estimados na etapa anterior.

### 7. Subtração do fundo

Subtraímos o frame de fundo de cada frame original para obter o objeto em movimento. O resultado é um novo conjunto de frames em que apenas o objeto em movimento é preservado.

## Resultado

### Plano de fundo:

![Plano de fundo](fundo.png)

### Vídeo original:

[Vídeo original](video.mp4)

### Vídeo com o plano de fundo removido:

[Vídeo com o plano de fundo removido](foreground.mp4)
