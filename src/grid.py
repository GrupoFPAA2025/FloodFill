import numpy as np
from typing import List, Tuple, Optional

class Grid:
    def __init__(self, rows: int, cols: int):
        """
        Inicializa um grid vazio com as dimensões especificadas.
        
        Args:
            rows (int): Número de linhas do grid
            cols (int): Número de colunas do grid
        """
        self.rows = rows
        self.cols = cols
        self.grid = np.zeros((rows, cols), dtype=int)
        self.next_color = 2  # Começa em 2 pois 0 é navegável e 1 é obstáculo
        
    @classmethod
    def from_list(cls, grid_data: List[List[int]]) -> 'Grid':
        """
        Cria um grid a partir de uma lista de listas.
        
        Args:
            grid_data (List[List[int]]): Lista de listas representando o grid
            
        Returns:
            Grid: Nova instância de Grid
        """
        rows = len(grid_data)
        cols = len(grid_data[0]) if rows > 0 else 0
        grid = cls(rows, cols)
        grid.grid = np.array(grid_data)
        return grid
    
    def is_valid_position(self, row: int, col: int) -> bool:
        """
        Verifica se uma posição está dentro dos limites do grid.
        
        Args:
            row (int): Linha a ser verificada
            col (int): Coluna a ser verificada
            
        Returns:
            bool: True se a posição é válida, False caso contrário
        """
        return 0 <= row < self.rows and 0 <= col < self.cols
    
    def get_neighbors(self, row: int, col: int) -> List[Tuple[int, int]]:
        """
        Retorna as posições vizinhas válidas de uma célula.
        
        Args:
            row (int): Linha da célula
            col (int): Coluna da célula
            
        Returns:
            List[Tuple[int, int]]: Lista de posições vizinhas válidas
        """
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # direita, baixo, esquerda, cima
        neighbors = []
        
        for dx, dy in directions:
            new_row, new_col = row + dx, col + dy
            if self.is_valid_position(new_row, new_col):
                neighbors.append((new_row, new_col))
                
        return neighbors
    
    def flood_fill(self, start_row: int, start_col: int) -> bool:
        """
        Aplica o algoritmo flood fill a partir de uma posição inicial.
        
        Args:
            start_row (int): Linha inicial
            start_col (int): Coluna inicial
            
        Returns:
            bool: True se alguma célula foi preenchida, False caso contrário
        """
        if not self.is_valid_position(start_row, start_col):
            return False
            
        # Se não é uma célula navegável, não faz nada
        if self.grid[start_row, start_col] != 0:
            return False
            
        color = self.next_color
        self.next_color += 1
        stack = [(start_row, start_col)]
        filled = False
        
        while stack:
            current_row, current_col = stack.pop()
            
            if self.grid[current_row, current_col] != 0:
                continue
                
            self.grid[current_row, current_col] = color
            filled = True
            
            for next_row, next_col in self.get_neighbors(current_row, current_col):
                if self.grid[next_row, next_col] == 0:
                    stack.append((next_row, next_col))
                    
        return filled
    
    def find_next_unfilled(self) -> Optional[Tuple[int, int]]:
        """
        Encontra a próxima célula não preenchida no grid.
        
        Returns:
            Optional[Tuple[int, int]]: Coordenadas da próxima célula não preenchida,
                                     ou None se não houver células não preenchidas
        """
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row, col] == 0:
                    return (row, col)
        return None
    
    def fill_all_regions(self):
        """
        Preenche todas as regiões não preenchidas do grid com cores diferentes.
        """
        while True:
            next_pos = self.find_next_unfilled()
            if next_pos is None:
                break
            self.flood_fill(*next_pos)
    
    def __str__(self) -> str:
        """
        Retorna uma representação em string do grid.
        
        Returns:
            str: Representação do grid
        """
        return str(self.grid) 