import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# Função para gerar uma superfície 3D
def gerar_superficie(tipo='esfera', raio=1.0, altura=2.0, num_pontos=50):
    if tipo == 'esfera':
        phi = np.linspace(0, np.pi, num_pontos)  # Coordenadas esféricas
        theta = np.linspace(0, 2 * np.pi, num_pontos)
        phi, theta = np.meshgrid(phi, theta)

        x = raio * np.sin(phi) * np.cos(theta)
        y = raio * np.sin(phi) * np.sin(theta)
        z = raio * np.cos(phi)
    elif tipo == 'cilindro':
        theta = np.linspace(0, 2 * np.pi, num_pontos)
        z = np.linspace(-altura / 2, altura / 2, num_pontos)
        theta, z = np.meshgrid(theta, z)

        x = raio * np.cos(theta)
        y = raio * np.sin(theta)
    elif tipo == 'plano':
        x = np.linspace(-raio, raio, num_pontos)
        y = np.linspace(-raio, raio, num_pontos)
        x, y = np.meshgrid(x, y)
        z = np.zeros_like(x)

    return x, y, z


# Função para calcular os vetores normais de uma superfície
def calcular_normais(x, y, z):
    normais_x = x / np.linalg.norm([x, y, z], axis=0)
    normais_y = y / np.linalg.norm([x, y, z], axis=0)
    normais_z = z / np.linalg.norm([x, y, z], axis=0)
    return normais_x, normais_y, normais_z


# Função para calcular a iluminação difusa
def iluminacao_difusa(x, y, z, pos_luz, intensidade_luz, cor_luz):
    normais_x, normais_y, normais_z = calcular_normais(x, y, z)

    # Vetor de iluminação
    pos_luz = np.array(pos_luz).reshape(3, 1, 1)
    vetor_luz = pos_luz - np.array([x, y, z])
    vetor_luz /= np.linalg.norm(vetor_luz, axis=0)

    # Produto escalar entre normais e vetor da luz para iluminação difusa
    produto_escalar = normais_x * vetor_luz[0] + normais_y * vetor_luz[1] + normais_z * vetor_luz[2]
    produto_escalar = np.clip(produto_escalar, 0, 1)  # Não pode ser negativo

    # Cálculo da cor final
    r = cor_luz[0] * intensidade_luz * produto_escalar
    g = cor_luz[1] * intensidade_luz * produto_escalar
    b = cor_luz[2] * intensidade_luz * produto_escalar

    return np.stack((r, g, b), axis=-1)


# Função para calcular a iluminação especular (Phong)
def iluminacao_especular(x, y, z, pos_luz, intensidade_luz, cor_luz, pos_camera, shininess=32):
    normais_x, normais_y, normais_z = calcular_normais(x, y, z)

    # Vetor de iluminação
    pos_luz = np.array(pos_luz).reshape(3, 1, 1)
    pos_camera = np.array(pos_camera).reshape(3, 1, 1)
    vetor_luz = pos_luz - np.array([x, y, z])
    vetor_luz /= np.linalg.norm(vetor_luz, axis=0)

    # Vetor para a câmera
    vetor_camera = pos_camera - np.array([x, y, z])
    vetor_camera /= np.linalg.norm(vetor_camera, axis=0)

    # Reflexão especular (modelo Phong)
    produto_escalar_difuso = normais_x * vetor_luz[0] + normais_y * vetor_luz[1] + normais_z * vetor_luz[2]
    refletido = 2 * (normais_x * produto_escalar_difuso) - vetor_luz
    produto_escalar_especular = np.clip(
        refletido[0] * vetor_camera[0] + refletido[1] * vetor_camera[1] + refletido[2] * vetor_camera[2], 0,
        1) ** shininess

    # Cálculo da cor final
    r = cor_luz[0] * intensidade_luz * produto_escalar_especular
    g = cor_luz[1] * intensidade_luz * produto_escalar_especular
    b = cor_luz[2] * intensidade_luz * produto_escalar_especular

    return np.stack((r, g, b), axis=-1)


# Função para calcular a iluminação combinada (difusa + especular)
def iluminacao_combinada(x, y, z, pos_luz, intensidade_luz, cor_luz, pos_camera, shininess=32):
    difusa = iluminacao_difusa(x, y, z, pos_luz, intensidade_luz, cor_luz)
    especular = iluminacao_especular(x, y, z, pos_luz, intensidade_luz, cor_luz, pos_camera, shininess)

    # Combina difusa e especular e clipa o resultado para [0, 1]
    iluminacao_total = np.clip(difusa + especular, 0, 1)
    return iluminacao_total


# Função para plotar a superfície com iluminação
def plotar_superficie_com_iluminacao(x, y, z, iluminacao, angulo_rotacao):
    # Configuração do gráfico 3D com matplotlib
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    # Aplicar rotação
    ax.view_init(elev=30, azim=angulo_rotacao)

    # Plotar a superfície com as cores da iluminação
    ax.plot_surface(x, y, z, facecolors=iluminacao, rstride=1, cstride=1, antialiased=True, shade=False)

    # Configurar rótulos e título
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(f"Superfície 3D com Iluminação")

    st.pyplot(fig)


# Interface do Streamlit
st.sidebar.title("Configurações de Iluminação")

# Escolha do tipo de superfície
tipo_superficie = st.sidebar.selectbox("Tipo de Superfície", ["esfera", "cilindro", "plano"])

# Escolha do tipo de iluminação
tipo_iluminacao = st.sidebar.selectbox("Modelo de Iluminação",
                                       ["Difusa", "Especular (Phong)", "Combinada (Difusa + Especular)"])

# Explicação matemática baseada no tipo de iluminação
if tipo_iluminacao == "Difusa":
    st.sidebar.latex(r"""
    I_{\text{difusa}} = L \cdot N \cdot I_{\text{fonte}}
    """)
    st.sidebar.write("""
    Onde:
    - \(L\) é o vetor de direção da luz.
    - \(N\) é o vetor normal da superfície.
    - \(I_Fonte) é a intensidade da luz.
    """)
elif tipo_iluminacao == "Especular (Phong)":
    st.sidebar.latex(r"""
    I_{\text{especular}} = (R \cdot V)^n \cdot I_{\text{fonte}}
    """)
    st.sidebar.write("""
    Onde:
    - \(R\) é o vetor de reflexão da luz.
    - \(V\) é o vetor de direção da câmera.
    - \(n\) é o expoente de especularidade (brilho).
    """)
elif tipo_iluminacao == "Combinada (Difusa + Especular)":
    st.sidebar.latex(r"""
    I = I_{\text{difusa}} + I_{\text{especular}}
    """)
    st.sidebar.write("""
    A iluminação difusa e especular são combinadas para produzir o efeito final.
    """)

# Posição da luz
luz_x = st.sidebar.slider("Posição da Luz - X", -5.0, 5.0, 2.0)
luz_y = st.sidebar.slider("Posição da Luz - Y", -5.0, 5.0, 2.0)
luz_z = st.sidebar.slider("Posição da Luz - Z", -5.0, 5.0, 2.0)
pos_luz = [luz_x, luz_y, luz_z]

# Intensidade e cor da luz
intensidade_luz = st.sidebar.slider("Intensidade da Luz", 0.0, 1.0, 1.0)
cor_luz_r = st.sidebar.slider("Cor da Luz - Vermelho", 0.0, 1.0, 1.0)
cor_luz_g = st.sidebar.slider("Cor da Luz - Verde", 0.0, 1.0, 1.0)
cor_luz_b = st.sidebar.slider("Cor da Luz - Azul", 0.0, 1.0, 1.0)
cor_luz = [cor_luz_r, cor_luz_g, cor_luz_b]

# Posição da câmera
camera_x = st.sidebar.slider("Posição da Câmera - X", -10.0, 10.0, 5.0)
camera_y = st.sidebar.slider("Posição da Câmera - Y", -10.0, 10.0, 5.0)
camera_z = st.sidebar.slider("Posição da Câmera - Z", -10.0, 10.0, 5.0)
pos_camera = [camera_x, camera_y, camera_z]

# Slider para controlar a quantidade de pontos (suavidade da superfície)
num_pontos = st.sidebar.slider("Número de Pontos na Superfície", 10, 100, 50)

# Controle da rotação
angulo_rotacao = st.sidebar.slider("Ângulo de Rotação", 0, 360, 45)

# Gerar a superfície escolhida
x, y, z = gerar_superficie(tipo=tipo_superficie, num_pontos=num_pontos)

# Calcular a iluminação de acordo com o modelo escolhido
if tipo_iluminacao == "Difusa":
    iluminacao = iluminacao_difusa(x, y, z, pos_luz, intensidade_luz, cor_luz)
elif tipo_iluminacao == "Especular (Phong)":
    iluminacao = iluminacao_especular(x, y, z, pos_luz, intensidade_luz, cor_luz, pos_camera)
else:
    iluminacao = iluminacao_combinada(x, y, z, pos_luz, intensidade_luz, cor_luz, pos_camera)

# Plotar a superfície com a iluminação calculada
plotar_superficie_com_iluminacao(x, y, z, iluminacao, angulo_rotacao)
