class QuadtreeNode {
  constructor(x, y, size, value = null) {
    this.x = x; // Coordenada x de la región
    this.y = y; // Coordenada y de la región
    this.size = size; // Tamaño del nodo
    this.value = value; // Valor en la celda, si es homogénea
    this.children = []; // Subregiones (si es subdividido)
  }

  isLeaf() {
    return this.children.length === 0;
  }

  subdivide() {
    const halfSize = this.size / 2;
    this.children = [
      new QuadtreeNode(this.x, this.y, halfSize),
      new QuadtreeNode(this.x + halfSize, this.y, halfSize),
      new QuadtreeNode(this.x, this.y + halfSize, halfSize),
      new QuadtreeNode(this.x + halfSize, this.y + halfSize, halfSize),
    ];
  }

  consolidate() {
    // Comprobar si las subregiones tienen el mismo valor y podemos convertirlas en una hoja
    if (
      this.children.every(
        (child) => child.isLeaf() && child.value === this.children[0].value,
      )
    ) {
      this.value = this.children[0].value;
      this.children = [];
    }
  }
}

class MXQuadtree {
  constructor(size, minLevel = 0) {
    this.root = new QuadtreeNode(0, 0, size);
    this.minLevel = minLevel; // Nivel mínimo de subdivisión
  }

  insert(x, y, value, node = this.root, currentLevel = 0) {
    if (node.isLeaf() && node.value !== null && currentLevel < this.minLevel) {
      node.subdivide();
    }

    if (node.isLeaf() && currentLevel >= this.minLevel) {
      node.value = value;
      return;
    }

    if (node.isLeaf() && currentLevel < this.minLevel) {
      node.subdivide();
    }

    const halfSize = node.size / 2;
    if (x < node.x + halfSize && y < node.y + halfSize) {
      this.insert(x, y, value, node.children[0], currentLevel + 1);
    } else if (x >= node.x + halfSize && y < node.y + halfSize) {
      this.insert(x, y, value, node.children[1], currentLevel + 1);
    } else if (x < node.x + halfSize && y >= node.y + halfSize) {
      this.insert(x, y, value, node.children[2], currentLevel + 1);
    } else {
      this.insert(x, y, value, node.children[3], currentLevel + 1);
    }
  }

  search(x, y, node = this.root) {
    if (node.isLeaf()) {
      return node.value;
    }

    const halfSize = node.size / 2;
    if (x < node.x + halfSize && y < node.y + halfSize) {
      return this.search(x, y, node.children[0]);
    } else if (x >= node.x + halfSize && y < node.y + halfSize) {
      return this.search(x, y, node.children[1]);
    } else if (x < node.x + halfSize && y >= node.y + halfSize) {
      return this.search(x, y, node.children[2]);
    } else {
      return this.search(x, y, node.children[3]);
    }
  }

  delete(x, y, node = this.root) {
    if (node.isLeaf()) {
      node.value = null;
      return;
    }

    const halfSize = node.size / 2;
    if (x < node.x + halfSize && y < node.y + halfSize) {
      this.delete(x, y, node.children[0]);
    } else if (x >= node.x + halfSize && y < node.y + halfSize) {
      this.delete(x, y, node.children[1]);
    } else if (x < node.x + halfSize && y >= node.y + halfSize) {
      this.delete(x, y, node.children[2]);
    } else {
      this.delete(x, y, node.children[3]);
    }

    node.consolidate();
  }

  draw(ctx, node = this.root) {
    if (node.isLeaf()) {
      if (node.value !== null) {
        ctx.fillStyle = this.getColorForValue(node.value);
        ctx.fillRect(node.x, node.y, node.size, node.size);
      }
      ctx.strokeStyle = "black";
      ctx.strokeRect(node.x, node.y, node.size, node.size);
    } else {
      node.children.forEach((child) => this.draw(ctx, child));
    }
  }

  getColorForValue(value) {
    const colors = ["#FFD700", "#00FF00", "#FF4500", "#1E90FF"];
    return colors[value % colors.length];
  }

  clear() {
    this.root = new QuadtreeNode(0, 0, this.root.size);
  }

  // Búsqueda por rango
  rangeSearch(x1, y1, x2, y2, node = this.root, result = []) {
    if (node.isLeaf()) {
      if (
        node.value !== null &&
        this.isWithinRange(node.x, node.y, node.size, x1, y1, x2, y2)
      ) {
        result.push({
          x: node.x,
          y: node.y,
          size: node.size,
          value: node.value,
        });
      }
      return result;
    }

    // Verificar cada hijo si cae dentro del rango
    node.children.forEach((child) => {
      if (this.intersectsRange(child.x, child.y, child.size, x1, y1, x2, y2)) {
        this.rangeSearch(x1, y1, x2, y2, child, result);
      }
    });

    return result;
  }

  isWithinRange(x, y, size, x1, y1, x2, y2) {
    return x >= x1 && y >= y1 && x + size <= x2 && y + size <= y2;
  }

  intersectsRange(x, y, size, x1, y1, x2, y2) {
    return !(x + size < x1 || x > x2 || y + size < y1 || y > y2);
  }
}

// Configuración de canvas y quadtree
const canvas = document.getElementById("quadtreeCanvas");
const ctx = canvas.getContext("2d");
const quadtree = new MXQuadtree(400, 6);

const clearCanvas = document.getElementById("clearCanvas");
clearCanvas.addEventListener("click", () => {
  quadtree.clear();
  ctx.clearRect(0, 0, canvas.width, canvas.height);
});

canvas.addEventListener("click", (event) => {
  if (event.button === 0) {
    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    const value = Math.floor(Math.random() * 4);
    quadtree.insert(x, y, value);

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    quadtree.draw(ctx);
  }
});

canvas.addEventListener("contextmenu", (event) => {
  event.preventDefault();

  if (event.button === 2) {
    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    quadtree.delete(x, y);

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    quadtree.draw(ctx);
  }
});

// Búsqueda por rango (ejemplo)
const searchButton = document.getElementById("searchRange");
searchButton.addEventListener("click", () => {
  const x1 = parseInt(document.getElementById("x1").value);
  const y1 = parseInt(document.getElementById("y1").value);
  const x2 = parseInt(document.getElementById("x2").value);
  const y2 = parseInt(document.getElementById("y2").value);

  const result = quadtree.rangeSearch(x1, y1, x2, y2);
  console.log("Resultado de la búsqueda por rango:", result);

  // Opcionalmente, podrías resaltar o hacer algo con los resultados
});
