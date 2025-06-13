import pytest
import numpy as np
from src.grid import Grid

def test_grid_initialization():
    """Testa a inicialização básica do grid"""
    grid = Grid(3, 4)
    assert grid.rows == 3
    assert grid.cols == 4
    assert grid.grid.shape == (3, 4)
    assert np.all(grid.grid == 0)

def test_grid_from_list():
    """Testa a criação do grid a partir de uma lista"""
    data = [
        [0, 0, 1],
        [1, 0, 0]
    ]
    grid = Grid.from_list(data)
    assert grid.rows == 2
    assert grid.cols == 3
    assert np.array_equal(grid.grid, np.array(data))

def test_flood_fill_simple():
    """Testa o preenchimento de uma região simples"""
    data = [
        [0, 0, 1],
        [0, 0, 1]
    ]
    grid = Grid.from_list(data)
    grid.flood_fill(0, 0)
    
    expected = [
        [2, 2, 1],
        [2, 2, 1]
    ]
    assert np.array_equal(grid.grid, np.array(expected))

def test_flood_fill_multiple_regions():
    """Testa o preenchimento de múltiplas regiões"""
    data = [
        [0, 1, 0],
        [1, 1, 0]
    ]
    grid = Grid.from_list(data)
    grid.fill_all_regions()
    
    # Verifica se as regiões desconectadas têm cores diferentes
    assert grid.grid[0, 0] != grid.grid[0, 2]
    assert grid.grid[0, 2] == grid.grid[1, 2]
    assert np.all(grid.grid[0:2, 1] == 1)  # Obstáculos permanecem como 1

def test_invalid_position():
    """Testa o comportamento com posições inválidas"""
    grid = Grid(2, 2)
    assert not grid.is_valid_position(-1, 0)
    assert not grid.is_valid_position(0, -1)
    assert not grid.is_valid_position(2, 0)
    assert not grid.is_valid_position(0, 2)
    assert grid.is_valid_position(0, 0)
    assert grid.is_valid_position(1, 1)

def test_get_neighbors():
    """Testa a obtenção de vizinhos válidos"""
    grid = Grid(3, 3)
    neighbors = grid.get_neighbors(1, 1)
    expected_neighbors = [(1, 2), (2, 1), (1, 0), (0, 1)]
    assert sorted(neighbors) == sorted(expected_neighbors)
    
    # Testa vizinhos de um canto
    corner_neighbors = grid.get_neighbors(0, 0)
    expected_corner = [(0, 1), (1, 0)]
    assert sorted(corner_neighbors) == sorted(expected_corner) 