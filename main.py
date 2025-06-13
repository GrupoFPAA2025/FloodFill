from src.grid import Grid
from src.gui import create_visualizer
from src.grid_generator import GridGenerator

def main():
    # Exemplo do enunciado
    grid_data = [
        [0, 0, 1, 0, 0],
        [0, 1, 1, 0, 0],
        [0, 0, 1, 1, 1],
        [1, 1, 0, 0, 0]
    ]
    
    # Cria o grid a partir dos dados do exemplo
    grid = Grid.from_list(grid_data)
    
    # Inicia o visualizador
    # O usuário pode gerar novos grids usando a interface
    create_visualizer(grid)

if __name__ == "__main__":
    main() 