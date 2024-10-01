import pygame
import numpy as np


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


def translation_matrix(x_offset, y_offset, z_offset):
    return np.array([
        [1, 0, 0, x_offset],
        [0, 1, 0, y_offset],
        [0, 0, 1, z_offset],
        [0, 0, 0, 1]
    ])


def scaling_matrix(sx, sy, sz):
    return np.array([
        [sx, 0, 0, 0],
        [0, sy, 0, 0],
        [0, 0, sz, 0],
        [0, 0, 0, 1]
    ])


# Função de projeção perspectiva com coordenadas homogêneas
def project_points(vertices, d=1):
    """
    Projeta pontos 3D no plano 2D usando a fórmula da projeção perspectiva.
    d é a distância focal, controlando o nível de perspectiva.
    """
    projected = vertices[:2] / (vertices[2] + d)  # Projeção em perspectiva simples
    return projected


# Função para desenhar as arestas do objeto na tela
def draw_shape(screen, vertices_2d, edges, color):
    """
    Desenha a forma na tela usando as coordenadas 2D projetadas.
    """
    for edge in edges:
        start, end = edge
        pygame.draw.line(screen, color,
                         (vertices_2d[0, start], vertices_2d[1, start]),
                         (vertices_2d[0, end], vertices_2d[1, end]), 1)


def run():
    pygame.init()
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Projeção 3D de Formas Geométricas")
    clock = pygame.time.Clock()
    FPS = 60
    background_color = (0, 0, 0)
    line_color = (255, 0, 0)

    # Definição dos vértices e arestas do cubo e pirâmide
    cube_vertices = np.array([
        [-1, -1, -1, 1], [1, -1, -1, 1], [1, 1, -1, 1], [-1, 1, -1, 1],
        [-1, -1, 1, 1], [1, -1, 1, 1], [1, 1, 1, 1], [-1, 1, 1, 1]
    ]).T # Vértices do cubo em coordenadas homogêneas (4x4)

    cube_edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7)
    ]

    pyramid_vertices = np.array([
        [0, 0, 1, 1], [1, 1, -1, 1], [-1, 1, -1, 1], [-1, -1, -1, 1], [1, -1, -1, 1]
    ]).T # Vértices da pirâmide em coordenadas homogêneas (4x4)

    pyramid_edges = [
        (0, 1), (0, 2), (0, 3), (0, 4),
        (1, 2), (2, 3), (3, 4), (4, 1)
    ]

    # Variáveis de controle
    theta_x, theta_y, theta_z = 0, 0, 0
    x_offset, y_offset, z_offset = 0, 0, 5
    shape_choice = 'cube'
    rodando = True

    # Definir fatores de escala para o cubo e pirâmide
    cube_scale = (3.5, 3.5, 3.5)
    pyramid_scale = (4.0, 4.0, 4.0)

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
            z_offset -= 0.1
        if keys[pygame.K_s]:
            z_offset += 0.1
        if keys[pygame.K_a]:
            x_offset -= 0.1
        if keys[pygame.K_d]:
            x_offset += 0.1

        if keys[pygame.K_1]:
            shape_choice = 'cube'
        if keys[pygame.K_2]:
            shape_choice = 'pyramid'

        if shape_choice == 'cube':
            vertices = cube_vertices
            edges = cube_edges
            scale_matrix = scaling_matrix(*cube_scale)
        else:
            vertices = pyramid_vertices
            edges = pyramid_edges
            scale_matrix = scaling_matrix(*pyramid_scale)

        screen.fill(background_color)

        rotation = rotation_matrix_x(theta_x) @ rotation_matrix_y(theta_y) @ rotation_matrix_z(theta_z)
        translation = translation_matrix(x_offset, y_offset, z_offset)

        transformation_matrix = translation @ rotation @ scale_matrix
        transformed_vertices = transformation_matrix @ vertices

        projected_vertices = project_points(transformed_vertices, 2)

        # Converte para coordenadas da tela
        projected_vertices[0, :] = screen_width / 2 + projected_vertices[0, :] * 100
        projected_vertices[1, :] = screen_height / 2 - projected_vertices[1, :] * 100

        # Desenha o objeto na tela
        draw_shape(screen, projected_vertices, edges, line_color)

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()