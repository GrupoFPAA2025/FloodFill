import numpy as np
from typing import Tuple
from .grid import Grid

class GridGenerator:
    @staticmethod
    def generate_random_grid(rows: int, cols: int, obstacle_density: float) -> Grid:
        """
        Gera um grid aleatório com uma determinada densidade de obstáculos.
        
        Args:
            rows (int): Número de linhas do grid
            cols (int): Número de colunas do grid
            obstacle_density (float): Proporção de obstáculos (entre 0 e 1)
            
        Returns:
            Grid: Nova instância de Grid com obstáculos aleatórios
        """
        if not 0 <= obstacle_density <= 1:
            raise ValueError("A densidade de obstáculos deve estar entre 0 e 1")
            
        # Gera um array aleatório de 0s e 1s
        random_grid = np.random.choice(
            [0, 1],
            size=(rows, cols),
            p=[1 - obstacle_density, obstacle_density]
        )
        
        return Grid.from_list(random_grid.tolist())
    
    @staticmethod
    def generate_connected_regions(rows: int, cols: int, num_regions: int) -> Grid:
        """
        Gera um grid com regiões conectadas separadas por obstáculos.
        
        Args:
            rows (int): Número de linhas do grid
            cols (int): Número de colunas do grid
            num_regions (int): Número desejado de regiões separadas
            
        Returns:
            Grid: Nova instância de Grid com regiões separadas
        """
        if num_regions > (rows * cols) // 4:
            raise ValueError("Número de regiões muito alto para o tamanho do grid")
            
        # Inicializa o grid com obstáculos
        grid_data = np.ones((rows, cols), dtype=int)
        
        # Lista para armazenar os pontos centrais das regiões
        region_centers = []
        
        # Gera regiões aleatórias
        for _ in range(num_regions):
            while True:
                # Escolhe um ponto central aleatório
                center_row = np.random.randint(1, rows-1)
                center_col = np.random.randint(1, cols-1)
                
                # Verifica se está longe o suficiente de outras regiões
                if all(abs(r - center_row) + abs(c - center_col) > 3 
                      for r, c in region_centers):
                    region_centers.append((center_row, center_col))
                    break
            
            # Cria uma região navegável ao redor do centro
            size = np.random.randint(2, 4)
            for i in range(-size, size+1):
                for j in range(-size, size+1):
                    if (0 <= center_row + i < rows and 
                        0 <= center_col + j < cols and
                        abs(i) + abs(j) <= size):
                        grid_data[center_row + i, center_col + j] = 0
        
        return Grid.from_list(grid_data.tolist())
    
    @staticmethod
    def generate_maze_like_grid(rows: int, cols: int) -> Grid:
        """
        Gera um grid no estilo labirinto com caminhos garantidos.
        
        Args:
            rows (int): Número de linhas do grid
            cols (int): Número de colunas do grid
            
        Returns:
            Grid: Nova instância de Grid com padrão de labirinto
        """
        # Inicializa o grid com obstáculos
        grid_data = np.ones((rows, cols), dtype=int)
        
        # Garante que linhas e colunas são ímpares
        for i in range(1, rows-1, 2):
            for j in range(1, cols-1, 2):
                grid_data[i, j] = 0
                
                # Conecta algumas células
                if np.random.random() < 0.7:  # 70% de chance de conectar
                    if j < cols-2:  # Conecta horizontalmente
                        grid_data[i, j+1] = 0
                if np.random.random() < 0.7:  # 70% de chance de conectar
                    if i < rows-2:  # Conecta verticalmente
                        grid_data[i+1, j] = 0
        
        return Grid.from_list(grid_data.tolist()) 