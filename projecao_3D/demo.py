import pygame
import numpy as np

# Funções para gerar as matrizes de transformação
def rotation_matrix_x(theta):
    return np.array([
        [1, 0, 0, 0],
        [0, np.cos(theta), -np.sin(theta), 0],
        [0, np.sin(theta), np.cos(theta), 0],
        [0, 0, 0, 1]
    ])

def rotation_matrix_y(theta):
    return np.array([
        [np.cos(theta), 0, np.sin(theta), 0],
        [0, 1, 0, 0],
        [-np.sin(theta), 0, np.cos(theta), 0],
        [0, 0, 0, 1]
    ])

def rotation_matrix_z(theta):
    return np.array([
        [np.cos(theta), -np.sin(theta), 0, 0],
        [np.sin(theta), np.cos(theta), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

def translation_matrix(tx, ty, tz):
    return np.array([
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1]
    ])

# Matriz de projeção pinhole
def projection_matrix(d):
    return np.array([
        [d, 0, 0, 0],
        [0, d, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 1/d, 0]
    ])

# Projeção perspectiva (câmera pinhole) usando multiplicação de matriz
def project_points(vertices, d):
    P = projection_matrix(d)
    
    # Multiplicação da matriz de projeção com os vértices
    projected_vertices_homogeneous = P @ vertices

    # Normaliza as coordenadas projetadas dividindo pelo fator homogêneo
    projected_vertices = projected_vertices_homogeneous[:3] / projected_vertices_homogeneous[3]

    return projected_vertices[:2].T  # Retorna as coordenadas x e y

# Função para desenhar as arestas do objeto na tela
def draw_shape(screen, vertices_2d, edges, color):
    for edge in edges:
        start, end = edge
        pygame.draw.line(screen, color,
                         (vertices_2d[start][0], vertices_2d[start][1]),
                         (vertices_2d[end][0], vertices_2d[end][1]), 1)

def run():
    pygame.init()
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Projeção 3D de Formas Geométricas")
    clock = pygame.time.Clock()
    FPS = 60
    background_color = (0, 0, 0)
    line_color = (255, 0, 0)

    # Definição dos vértices e arestas do cubo e da pirâmide
    cube_vertices = np.array([
        [-1, -1, -1, 1], [1, -1, -1, 1], [1, 1, -1, 1], [-1, 1, -1, 1],
        [-1, -1, 1, 1], [1, -1, 1, 1], [1, 1, 1, 1], [-1, 1, 1, 1]
    ]).T  # Transpor diretamente na definição para operar sem precisar de nova transposição depois

    cube_edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7)
    ]

    pyramid_vertices = np.array([
        [0, 0, 1, 1], [1, 1, -1, 1], [-1, 1, -1, 1], [-1, -1, -1, 1], [1, -1, -1, 1]
    ]).T  # Transpor diretamente na definição

    pyramid_edges = [
        (0, 1), (0, 2), (0, 3), (0, 4),
        (1, 2), (2, 3), (3, 4), (4, 1)
    ]

    # Variáveis de controle
    theta_x, theta_y, theta_z = 0, 0, 0
    x_offset, y_offset, z_offset = 0, 0, 5  # Controle inicial da translação
    shape_choice = 'cube'
    rodando = True

    # Distância focal da câmera (d)
    d = 2

    while rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            theta_y -= 0.05
        if keys[pygame.K_RIGHT]:
            theta_y += 0.05
        if keys[pygame.K_UP]:
            theta_x -= 0.05
        if keys[pygame.K_DOWN]:
            theta_x += 0.05
        if keys[pygame.K_q]:
            theta_z -= 0.05
        if keys[pygame.K_e]:
            theta_z += 0.05
        if keys[pygame.K_w]:
            z_offset -= 0.1  # Movimenta no eixo Z
        if keys[pygame.K_s]:
            z_offset += 0.1  # Movimenta no eixo Z
        if keys[pygame.K_a]:
            x_offset -= 0.1
        if keys[pygame.K_d]:
            x_offset += 0.1

        if keys[pygame.K_1]:
            shape_choice = 'cube'
        if keys[pygame.K_2]:
            shape_choice = 'pyramid'

        screen.fill(background_color)

        # Seleciona vértices e arestas de acordo com a escolha
        if shape_choice == 'cube':
            vertices = cube_vertices
            edges = cube_edges
        else:
            vertices = pyramid_vertices
            edges = pyramid_edges

        # Matriz de transformação completa (rotação + translação)
        rotation_x = rotation_matrix_x(theta_x)
        rotation_y = rotation_matrix_y(theta_y)
        rotation_z = rotation_matrix_z(theta_z)
        translation = translation_matrix(x_offset, y_offset, z_offset)

        # Aplica as transformações aos vértices
        transformation_matrix = translation @ rotation_z @ rotation_y @ rotation_x
        transformed_vertices = transformation_matrix @ vertices

        # Projeta os vértices 3D em 2D
        projected_vertices = project_points(transformed_vertices, d)

        # Converte para coordenadas da tela
        projected_vertices[:, 0] = screen_width / 2 + projected_vertices[:, 0] * 100
        projected_vertices[:, 1] = screen_height / 2 - projected_vertices[:, 1] * 100

        # Desenha o objeto na tela
        draw_shape(screen, projected_vertices, edges, line_color)

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()