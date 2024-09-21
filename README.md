# Ferramenta de Visualização 3D para Geometria Analítica

Este projeto é uma ferramenta de visualização 3D desenvolvida para o programa de monitoria de Geometria Analítica. Ela permite que os usuários explorem interativamente diferentes superfícies 3D com vários modelos de iluminação, demonstrando conceitos-chave de geometria analítica e computação gráfica.

## idealizadores
- João Renan S. Lopes (Monitor)
- Polyana Nascimento Fonseca (Professora)

## Visão Geral

A ferramenta utiliza Python com bibliotecas como NumPy, Matplotlib e Streamlit para criar uma aplicação web interativa. Os usuários podem visualizar diferentes superfícies 3D (esfera, cilindro, plano) e aplicar vários modelos de iluminação para entender como a luz interage com essas superfícies.

## Principais Recursos

- Geração interativa de superfícies 3D (esfera, cilindro, plano)
- Múltiplos modelos de iluminação (Difusa, Especular, Combinada)
- Posição e propriedades ajustáveis da fonte de luz
- Controle da posição da câmera
- Rotação da superfície
- Atualizações de visualização em tempo real

## Funções Principais

### `gerar_superficie(tipo='esfera', raio=1.0, altura=2.0, num_pontos=50)`
Gera coordenadas de superfície 3D com base no tipo especificado (esfera, cilindro ou plano).

### `calcular_normais(x, y, z)`
Calcula os vetores normais para os pontos da superfície fornecidos.

### `iluminacao_difusa(x, y, z, pos_luz, intensidade_luz, cor_luz)`
Calcula a iluminação difusa para a superfície com base na posição e propriedades da luz.

### `iluminacao_especular(x, y, z, pos_luz, intensidade_luz, cor_luz, pos_camera, shininess=32)`
Calcula a iluminação especular (modelo de Phong) para a superfície.

### `iluminacao_combinada(x, y, z, pos_luz, intensidade_luz, cor_luz, pos_camera, shininess=32)`
Combina os modelos de iluminação difusa e especular.

### `plotar_superficie_com_iluminacao(x, y, z, iluminacao, angulo_rotacao)`
Plota a superfície 3D com a iluminação aplicada usando Matplotlib.

## Como Funciona

1. O usuário seleciona um tipo de superfície, modelo de iluminação e ajusta vários parâmetros usando a barra lateral do Streamlit.
2. O programa gera a superfície 3D selecionada usando arrays NumPy.
3. Com base no modelo de iluminação escolhido, a ferramenta calcula a iluminação para cada ponto da superfície.
4. A superfície 3D é plotada usando Matplotlib, com cores representando a iluminação calculada.
5. O gráfico é exibido no aplicativo Streamlit, atualizando em tempo real conforme o usuário ajusta os parâmetros.

## Valor Educacional

Esta ferramenta ajuda os estudantes a visualizar e entender:
- Sistemas de coordenadas 3D e geração de superfícies
- Vetores normais e sua importância nos cálculos de iluminação
- Diferentes modelos de iluminação (difusa, especular) e suas representações matemáticas
- Como a luz interage com várias superfícies 3D
- O efeito da posição, cor e intensidade da fonte de luz na aparência do objeto

Ao fornecer uma representação visual e interativa desses conceitos, a ferramenta aprimora a experiência de aprendizagem dos alunos no curso de Geometria Analítica.
