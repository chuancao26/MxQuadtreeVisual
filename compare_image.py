from PIL import Image
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Definición de la clase del MX-Quadtree
class MXQuadtreeNode:
    def __init__(self, image_data, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.image_data = image_data

        if self.size == 1:
            # Nodo hoja, valor de píxel único
            self.value = self.image_data[y, x]
            self.children = []
        else:
            half_size = size // 2
            self.children = [
                MXQuadtreeNode(image_data, x, y, half_size),  # Top-left
                MXQuadtreeNode(image_data, x + half_size, y, half_size),  # Top-right
                MXQuadtreeNode(image_data, x, y + half_size, half_size),  # Bottom-left
                MXQuadtreeNode(image_data, x + half_size, y + half_size, half_size)  # Bottom-right
            ]
            self.value = np.mean([child.value for child in self.children])

def build_quadtree(image_data):
    size = image_data.shape[0]
    return MXQuadtreeNode(image_data, 0, 0, size)

def draw_quadtree_with_diff(node1, node2, ax, x, y, size, threshold=30):
    if not node1.children and not node2.children:
        diff = abs(node1.value - node2.value)
        if diff > threshold:
            ax.add_patch(patches.Rectangle((x, y), size, size, fill=True, edgecolor='blue', facecolor='red', alpha=0.5))
    elif node1.children and node2.children:
        half_size = size // 2
        draw_quadtree_with_diff(node1.children[0], node2.children[0], ax, x, y, half_size)
        draw_quadtree_with_diff(node1.children[1], node2.children[1], ax, x + half_size, y, half_size)
        draw_quadtree_with_diff(node1.children[2], node2.children[2], ax, x, y + half_size, half_size)
        draw_quadtree_with_diff(node1.children[3], node2.children[3], ax, x + half_size, y + half_size, half_size)

def calculate_similarity(image1_data, image2_data):
    tree1 = build_quadtree(image1_data)
    tree2 = build_quadtree(image2_data)
    difference = compare_quadtrees(tree1, tree2)
    max_diff = 255
    similarity = 1 - (difference / max_diff)
    return similarity, tree1, tree2

def compare_quadtrees(tree1, tree2):
    if not tree1.children and not tree2.children:
        return abs(tree1.value - tree2.value)
    elif tree1.children and tree2.children:
        diff = 0
        for child1, child2 in zip(tree1.children, tree2.children):
            diff += compare_quadtrees(child1, child2)
        return diff / 4
    else:
        return 255

def visualize_differences(tree1, tree2, reference_image_data, comparison_image_data, image_name):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.imshow(reference_image_data, cmap='gray')
    draw_quadtree_with_diff(tree1, tree2, ax, 0, 0, reference_image_data.shape[0], threshold=30)
    plt.title(f'Diferencias Quadtree con {image_name}')
    plt.axis('off')
    plt.show()

def find_most_similar(reference_image_path, comparison_image_paths):
    reference_image = Image.open(reference_image_path).convert('L')
    reference_image_data = np.array(reference_image)

    similarities = []
    best_similarity = -1
    best_image_path = None
    best_tree1, best_tree2 = None, None

    for image_path in comparison_image_paths:
        comparison_image = Image.open(image_path).convert('L')
        if comparison_image.size != reference_image.size:
            comparison_image = comparison_image.resize(reference_image.size)

        comparison_image_data = np.array(comparison_image)
        similarity, tree1, tree2 = calculate_similarity(reference_image_data, comparison_image_data)
        similarities.append((image_path, similarity))

        # Visualizamos las diferencias entre el Quadtree de referencia y el Quadtree de la imagen de comparación
        visualize_differences(tree1, tree2, reference_image_data, comparison_image_data, os.path.basename(image_path))

        if similarity > best_similarity:
            best_similarity = similarity
            best_image_path = image_path
            best_tree1, best_tree2 = tree1, tree2

    print(f'La imagen más similar es: {best_image_path} con una similitud de {best_similarity:.2f}')

    # Visualizamos las diferencias entre la imagen más similar y la de referencia
    visualize_differences(best_tree1, best_tree2, reference_image_data, comparison_image_data, 'Imagen más similar')

    return similarities

# Ejemplo de uso
reference_image_path = 'imagenes/imagen0.png'  # Ruta de la imagen de referencia
comparison_image_paths = ['imagenes/imagen1.png', 'imagenes/imagen2.png', 'imagenes/imagen3.png', 'imagenes/imagen4.png']  # Lista de imágenes a comparar

# Llamamos a la función para encontrar la imagen más similar
similarities = find_most_similar(reference_image_path, comparison_image_paths)

# Imprimimos las similitudes de cada imagen
for image_path, similarity in similarities:
    print(f'Imagen: {image_path}, Similitud: {similarity:.2f}')
