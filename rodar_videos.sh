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
    
    if [ "$script" == "$PYTHON_SCRIPT_SEQUENCIAL" ]; then
        output=$(python3 "$script" "$video" "$frame")
        read -r value1 value2 value3 <<< "$output"
        echo "Sequencial - Video: $video, Frames: $frame - Tempo: ${value1}s ${value2}s ${value3}s" >> "$RELATORIO"
    else
        output=$(python3 "$script" "$video" "$frame" "$thread")
        read -r value1 value2 value3 <<< "$output"
        echo "Concorrente - Video: $video, Frames: $frame, Threads: $thread - Tempo: ${value1}s ${value2}s ${value3}s" >> "$RELATORIO"
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
