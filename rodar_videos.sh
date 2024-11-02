#!/bin/bash

PYTHON_SCRIPT_SEQUENCIAL="backgroundSequencial.py"
PYTHON_SCRIPT_CONCORRENTE="backgroundConcorrente.py"

VIDEOS=("video1.mp4" "video2.mp4")

FRAMES=(20 50 100)
THREADS=(1 2 4 8)

RELATORIO="relatorio_execucao.txt"

echo "Relatório de Execução - $(date)" > "$RELATORIO"
echo "---------------------------------------" >> "$RELATORIO"

executar_e_marcar_tempo() {
    local script=$1
    local video=$2
    local frame=$3
    local thread=$4
    
    start_time=$(date +%s)
    
    if [ "$script" == "$PYTHON_SCRIPT_SEQUENCIAL" ]; then
        python3 "$script" "$video" "$frame"
    else
        python3 "$script" "$video" "$frame" "$thread"
    fi

    end_time=$(date +%s)
    duration=$((end_time - start_time))
    
    if [ "$script" == "$PYTHON_SCRIPT_SEQUENCIAL" ]; then
        echo "Sequencial - Video: $video, Frames: $frame - Tempo: ${duration}s" >> "$RELATORIO"
    else
        echo "Concorrente - Video: $video, Frames: $frame, Threads: $thread - Tempo: ${duration}s" >> "$RELATORIO"
    fi
}

echo "Executando versão sequencial:"
for video in "${VIDEOS[@]}"; do
    for frame in "${FRAMES[@]}"; do
        echo "Processando $video com $frame frames..."
        executar_e_marcar_tempo "$PYTHON_SCRIPT_SEQUENCIAL" "$video" "$frame"
    done
done

echo "Executando versão concorrente:"
for video in "${VIDEOS[@]}"; do
    for frame in "${FRAMES[@]}"; do
        for thread in "${THREADS[@]}"; do
            echo "Processando $video com $frame frames e $thread threads..."
            executar_e_marcar_tempo "$PYTHON_SCRIPT_CONCORRENTE" "$video" "$frame" "$thread"
        done
    done
done

# Exibe o relatório final
echo "---------------------------------------" >> "$RELATORIO"
echo "Relatório de Execução Completo:" >> "$RELATORIO"
echo "---------------------------------------" >> "$RELATORIO"
cat "$RELATORIO"
