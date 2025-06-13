import tkinter as tk
from tkinter import ttk, messagebox, font
import numpy as np
from typing import List, Dict, Optional, Tuple
from .grid import Grid
from .grid_generator import GridGenerator

# Constantes
CELL_SIZE = 50
MIN_GRID_SIZE = 5
DEFAULT_GRID_SIZE = 10
DEFAULT_DENSITY = 0.3
DEFAULT_REGIONS = 4

# Configurações de cores
COLORS = {
    0: 'white',     # Célula navegável
    1: 'black',     # Obstáculo
    2: '#FF0000',   # Vermelho
    3: '#FFA500',   # Laranja
    4: '#FFFF00',   # Amarelo
    5: '#00FF00',   # Verde
    6: '#0000FF',   # Azul
    7: '#800080',   # Roxo
    8: '#FF1493',   # Rosa escuro
    9: '#00FFFF',   # Ciano
    10: '#FF4500',  # Laranja avermelhado
    11: '#32CD32',  # Verde limão
    12: '#4169E1',  # Azul royal
    13: '#8B008B',  # Magenta escuro
    14: '#FF69B4',  # Rosa claro
    15: '#20B2AA',  # Verde-azulado
    16: '#DAA520',  # Dourado
    17: '#9370DB',  # Roxo médio
    18: '#3CB371',  # Verde mar médio
    19: '#4682B4',  # Azul aço
    20: '#DC143C',  # Vermelho cremisi
    21: '#FF8C00',  # Laranja escuro
    22: '#6B8E23',  # Verde oliva
    23: '#483D8B',  # Azul ardósia escuro
    24: '#8B4513',  # Marrom sela
    25: '#556B2F',  # Verde oliva escuro
}

COLOR_NAMES = {
    0: 'Branco',
    1: 'Preto',
    2: 'Vermelho',
    3: 'Laranja',
    4: 'Amarelo',
    5: 'Verde',
    6: 'Azul',
    7: 'Roxo',
    8: 'Rosa Escuro',
    9: 'Ciano',
    10: 'Laranja Avermelhado',
    11: 'Verde Limão',
    12: 'Azul Royal',
    13: 'Magenta Escuro',
    14: 'Rosa Claro',
    15: 'Verde-azulado',
    16: 'Dourado',
    17: 'Roxo Médio',
    18: 'Verde Mar Médio',
    19: 'Azul Aço',
    20: 'Vermelho Cremisi',
    21: 'Laranja Escuro',
    22: 'Verde Oliva',
    23: 'Azul Ardósia Escuro',
    24: 'Marrom Sela',
    25: 'Verde Oliva Escuro'
}

# Texto de dicas
TIPS_TEXT = (
    "🖌️ Desenhe obstáculos clicando e arrastando\n"
    "🧹 Use 'Apagar' para remover obstáculos\n"
    "🎨 'Preencher Regiões' colore áreas conectadas\n"
    "🔄 Gere grids automáticos com diferentes padrões:\n"
    "   • Aleatório: Obstáculos distribuídos\n"
    "   • Regiões: Áreas separadas por obstáculos\n"
    "   • Labirinto: Padrão de caminhos conectados\n"
    "📊 Acompanhe as estatísticas em tempo real"
)

class GridVisualizer:
    """Classe responsável pela interface gráfica do visualizador de grid."""
    
    def __init__(self, master: tk.Tk, grid: Grid):
        """
        Inicializa o visualizador do grid.
        
        Args:
            master (tk.Tk): Janela principal do Tkinter
            grid (Grid): Instância da classe Grid a ser visualizada
        """
        self.master = master
        self.grid = grid
        self.drawing = False
        self.current_tool = "obstacle"
        self.last_cell = None
        
        self._setup_window()
        self._create_main_frames()
        self._create_grid_canvas()
        self._create_tools()
        self._create_generator()
        self._create_tips()
        self._setup_bindings()
        
        # Inicialização final
        self.update_params_frame(None)
        self.draw_grid()
    
    def _setup_window(self):
        """Configura a janela principal."""
        self.master.title('FloodFill Visualizer')
    
    def _create_main_frames(self):
        """Cria os frames principais da interface."""
        # Frame principal
        self.main_frame = ttk.Frame(self.master)
        self.main_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        
        # Frame esquerdo
        self.left_frame = ttk.Frame(self.main_frame)
        self.left_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        
        # Frame direito (estatísticas)
        self._create_stats_frame()
    
    def _create_stats_frame(self):
        """Cria o frame de estatísticas."""
        self.stats_frame = ttk.LabelFrame(self.main_frame, text="Estatísticas das Regiões", padding="10")
        self.stats_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        
        # Área de texto com scroll
        self.stats_text = tk.Text(self.stats_frame, width=40, height=30, wrap=tk.WORD)
        self.stats_scroll = ttk.Scrollbar(self.stats_frame, orient="vertical", command=self.stats_text.yview)
        self.stats_text.configure(yscrollcommand=self.stats_scroll.set)
        
        self.stats_text.grid(row=0, column=0, sticky='nsew')
        self.stats_scroll.grid(row=0, column=1, sticky='ns')
        
        # Fonte personalizada
        self.stats_font = font.Font(family='Consolas', size=10)
        self.stats_text.configure(font=self.stats_font)
    
    def _create_grid_canvas(self):
        """Cria o canvas para desenho do grid."""
        self.grid_frame = ttk.Frame(self.left_frame, padding="10")
        self.grid_frame.grid(row=0, column=0, sticky='nsew')
        
        canvas_width = self.grid.cols * CELL_SIZE
        canvas_height = self.grid.rows * CELL_SIZE
        self.canvas = tk.Canvas(self.grid_frame, width=canvas_width, height=canvas_height)
        self.canvas.grid(row=0, column=0, padx=5, pady=5)
    
    def _create_tools(self):
        """Cria as ferramentas de desenho."""
        self.control_frame = ttk.Frame(self.left_frame, padding="10")
        self.control_frame.grid(row=1, column=0, sticky='ew')
        
        self.drawing_frame = ttk.LabelFrame(self.control_frame, text="Ferramentas", padding="5")
        self.drawing_frame.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        
        # Botões
        buttons = [
            ("Desenhar Obstáculo", lambda: self.set_tool("obstacle")),
            ("Apagar", lambda: self.set_tool("clear")),
            ("Limpar Tudo", self.clear_all),
            ("Preencher Regiões", self.fill_and_update)
        ]
        
        for i, (text, command) in enumerate(buttons):
            btn = ttk.Button(self.drawing_frame, text=text, command=command)
            btn.grid(row=0, column=i, padx=5, pady=5)
            if text == "Desenhar Obstáculo":
                self.obstacle_button = btn
            elif text == "Apagar":
                self.clear_button = btn
    
    def _create_generator(self):
        """Cria o gerador de grids."""
        # Frame inferior
        self.bottom_frame = ttk.Frame(self.left_frame)
        self.bottom_frame.grid(row=2, column=0, sticky='ew', pady=5)
        
        # Frame do gerador
        self.generator_frame = ttk.LabelFrame(self.bottom_frame, text="Gerador de Grids", padding="10")
        self.generator_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nw')
        
        self._create_dimensions_controls()
        self._create_generator_controls()
    
    def _create_dimensions_controls(self):
        """Cria os controles de dimensões do grid."""
        self.dimensions_frame = ttk.Frame(self.generator_frame)
        self.dimensions_frame.grid(row=0, column=0, columnspan=2, pady=5)
        
        ttk.Label(self.dimensions_frame, text="Dimensões:").grid(row=0, column=0, padx=5)
        
        self.rows_var = tk.StringVar(value=str(DEFAULT_GRID_SIZE))
        self.rows_entry = ttk.Entry(self.dimensions_frame, textvariable=self.rows_var, width=3)
        self.rows_entry.grid(row=0, column=1, padx=2)
        
        ttk.Label(self.dimensions_frame, text="x").grid(row=0, column=2, padx=2)
        
        self.cols_var = tk.StringVar(value=str(DEFAULT_GRID_SIZE))
        self.cols_entry = ttk.Entry(self.dimensions_frame, textvariable=self.cols_var, width=3)
        self.cols_entry.grid(row=0, column=3, padx=2)
    
    def _create_generator_controls(self):
        """Cria os controles do gerador de grids."""
        ttk.Label(self.generator_frame, text="Tipo:").grid(row=1, column=0, padx=5, pady=5)
        
        self.generator_type = ttk.Combobox(self.generator_frame, 
            values=["Aleatório", "Regiões Conectadas", "Labirinto"],
            state="readonly", width=15)
        self.generator_type.set("Aleatório")
        self.generator_type.grid(row=1, column=1, padx=5, pady=5)
        
        # Frame para parâmetros
        self.params_frame = ttk.Frame(self.generator_frame)
        self.params_frame.grid(row=2, column=0, columnspan=2, pady=5)
        
        # Parâmetros específicos
        self.density_var = tk.StringVar(value=str(DEFAULT_DENSITY))
        self.density_label = ttk.Label(self.params_frame, text="Densidade de Obstáculos:")
        self.density_entry = ttk.Entry(self.params_frame, textvariable=self.density_var, width=4)
        
        self.regions_var = tk.StringVar(value=str(DEFAULT_REGIONS))
        self.regions_label = ttk.Label(self.params_frame, text="Número de Regiões:")
        self.regions_entry = ttk.Entry(self.params_frame, textvariable=self.regions_var, width=4)
        
        # Botão gerar
        self.generate_button = ttk.Button(self.generator_frame, text="Gerar Grid", 
                                        command=self.generate_new_grid)
        self.generate_button.grid(row=3, column=0, columnspan=2, pady=5)
    
    def _create_tips(self):
        """Cria o frame de dicas."""
        self.tips_frame = ttk.LabelFrame(self.bottom_frame, text="Dicas de Uso", padding="10")
        self.tips_frame.grid(row=0, column=1, padx=5, pady=5, sticky='nw')
        
        self.tips_label = ttk.Label(self.tips_frame, text=TIPS_TEXT, justify='left')
        self.tips_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
    
    def _setup_bindings(self):
        """Configura os eventos do mouse."""
        self.canvas.bind('<Button-1>', self.start_drawing)
        self.canvas.bind('<B1-Motion>', self.draw)
        self.canvas.bind('<ButtonRelease-1>', self.stop_drawing)
        self.generator_type.bind('<<ComboboxSelected>>', self.update_params_frame)
    
    def get_color(self, value: int) -> str:
        """Retorna a cor correspondente ao valor da célula."""
        if value <= 1:
            return COLORS.get(value, 'gray')
        
        color_index = ((value - 2) % (len(COLORS) - 2)) + 2
        return COLORS.get(color_index, 'gray')
    
    def update_params_frame(self, event):
        """Atualiza os parâmetros mostrados baseado no tipo de geração selecionado."""
        for widget in self.params_frame.winfo_children():
            widget.grid_remove()
        
        generator_type = self.generator_type.get()
        
        if generator_type == "Aleatório":
            self.density_label.grid(row=0, column=0, padx=5)
            self.density_entry.grid(row=0, column=1, padx=5)
        elif generator_type == "Regiões Conectadas":
            self.regions_label.grid(row=0, column=0, padx=5)
            self.regions_entry.grid(row=0, column=1, padx=5)
    
    def generate_new_grid(self):
        """Gera um novo grid baseado nos parâmetros selecionados."""
        try:
            rows = int(self.rows_var.get())
            cols = int(self.cols_var.get())
            
            if rows < MIN_GRID_SIZE or cols < MIN_GRID_SIZE:
                messagebox.showerror("Erro", f"Dimensões mínimas: {MIN_GRID_SIZE}x{MIN_GRID_SIZE}")
                return
            
            generator_type = self.generator_type.get()
            
            if generator_type == "Aleatório":
                density = float(self.density_var.get())
                self.grid = GridGenerator.generate_random_grid(rows, cols, density)
            elif generator_type == "Regiões Conectadas":
                num_regions = int(self.regions_var.get())
                self.grid = GridGenerator.generate_connected_regions(rows, cols, num_regions)
            else:  # Labirinto
                self.grid = GridGenerator.generate_maze_like_grid(rows, cols)
            
            # Atualiza o canvas
            canvas_width = self.grid.cols * CELL_SIZE
            canvas_height = self.grid.rows * CELL_SIZE
            self.canvas.config(width=canvas_width, height=canvas_height)
            
            self.draw_grid()
            self.update_statistics()
            
        except ValueError as e:
            messagebox.showerror("Erro", str(e))
    
    def draw_grid(self):
        """Desenha o grid no canvas."""
        self.canvas.delete('all')
        
        for row in range(self.grid.rows):
            for col in range(self.grid.cols):
                x1 = col * CELL_SIZE
                y1 = row * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                
                value = self.grid.grid[row, col]
                color = self.get_color(value)
                
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='gray')
    
    def update_statistics(self):
        """Atualiza as estatísticas das regiões encontradas."""
        self.stats_text.configure(state='normal')
        self.stats_text.delete(1.0, tk.END)
        
        region_counts = {}
        total_cells = self.grid.rows * self.grid.cols
        obstacle_count = 0
        empty_count = 0
        
        # Contagem de células
        for row in range(self.grid.rows):
            for col in range(self.grid.cols):
                value = self.grid.grid[row, col]
                if value == 0:
                    empty_count += 1
                elif value == 1:
                    obstacle_count += 1
                else:
                    region_counts[value] = region_counts.get(value, 0) + 1
        
        # Cabeçalho
        self._add_stats_header(total_cells, empty_count, obstacle_count)
        
        # Detalhes das regiões
        if region_counts:
            self._add_region_details(region_counts, total_cells)
        else:
            self._add_empty_state_message()
        
        self.stats_text.configure(state='disabled')
    
    def _add_stats_header(self, total_cells: int, empty_count: int, obstacle_count: int):
        """Adiciona o cabeçalho das estatísticas."""
        self.stats_text.insert(tk.END, "🎨 ANÁLISE DO GRID\n\n")
        self.stats_text.insert(tk.END, f"📏 Dimensões: {self.grid.rows}x{self.grid.cols}\n")
        self.stats_text.insert(tk.END, f"📊 Total de células: {total_cells}\n\n")
        self.stats_text.insert(tk.END, "📍 VISÃO GERAL\n")
        self.stats_text.insert(tk.END, f"⬜ Células navegáveis: {empty_count}\n")
        self.stats_text.insert(tk.END, f"⬛ Obstáculos: {obstacle_count}\n")
    
    def _add_region_details(self, region_counts: Dict[int, int], total_cells: int):
        """Adiciona os detalhes das regiões."""
        self.stats_text.insert(tk.END, f"🎯 Regiões preenchidas: {len(region_counts)}\n\n")
        self.stats_text.insert(tk.END, "🔍 DETALHES DAS REGIÕES\n")
        
        for region_id in sorted(region_counts.keys()):
            count = region_counts[region_id]
            color_name = COLOR_NAMES.get(region_id, f"Cor {region_id}")
            percentage = (count / total_cells) * 100
            
            region_info = f"Região {region_id-1} ({color_name}):\n"
            region_info += f"  • Células: {count}\n"
            region_info += f"  • Porcentagem: {percentage:.1f}%\n\n"
            
            start = self.stats_text.index("end-1c")
            self.stats_text.insert(tk.END, region_info)
            end = self.stats_text.index("end-1c")
            
            self.stats_text.tag_add(f"color_{region_id}", start, end)
            self.stats_text.tag_config(f"color_{region_id}", foreground=COLORS[region_id])
    
    def _add_empty_state_message(self):
        """Adiciona mensagem de estado vazio."""
        self.stats_text.insert(tk.END, "🎯 Nenhuma região preenchida\n\n")
        self.stats_text.insert(tk.END, "Use o botão 'Preencher Regiões' para\n")
        self.stats_text.insert(tk.END, "colorir as áreas conectadas.\n")
    
    def fill_and_update(self):
        """Executa o algoritmo flood fill e atualiza a visualização."""
        self.grid.next_color = 2
        self.grid.fill_all_regions()
        self.draw_grid()
        self.update_statistics()
    
    def set_tool(self, tool: str):
        """Define a ferramenta atual de desenho."""
        self.current_tool = tool
        if tool == "obstacle":
            self.obstacle_button.state(['pressed'])
            self.clear_button.state(['!pressed'])
        else:
            self.obstacle_button.state(['!pressed'])
            self.clear_button.state(['pressed'])
    
    def get_cell_from_coords(self, event) -> Optional[Tuple[int, int]]:
        """Converte coordenadas do mouse para índices do grid."""
        col = event.x // CELL_SIZE
        row = event.y // CELL_SIZE
        
        if 0 <= row < self.grid.rows and 0 <= col < self.grid.cols:
            return (row, col)
        return None
    
    def start_drawing(self, event):
        """Inicia o desenho quando o botão do mouse é pressionado."""
        self.drawing = True
        self.draw(event)
    
    def draw(self, event):
        """Desenha ou apaga células enquanto o mouse é arrastado."""
        if not self.drawing:
            return
        
        cell = self.get_cell_from_coords(event)
        if cell is None or cell == self.last_cell:
            return
        
        row, col = cell
        new_value = 1 if self.current_tool == "obstacle" else 0
        
        if self.grid.grid[row, col] == new_value:
            return
        
        self.grid.grid[row, col] = new_value
        
        # Limpa cores existentes
        mask = self.grid.grid > 1
        self.grid.grid[mask] = 0
        
        # Atualiza célula
        x1 = col * CELL_SIZE
        y1 = row * CELL_SIZE
        x2 = x1 + CELL_SIZE
        y2 = y1 + CELL_SIZE
        
        self.canvas.create_rectangle(x1, y1, x2, y2, 
                                   fill=self.get_color(new_value), 
                                   outline='gray')
        
        self.last_cell = cell
        self.update_statistics()
    
    def stop_drawing(self, event):
        """Para o desenho quando o botão do mouse é solto."""
        self.drawing = False
        self.last_cell = None
    
    def clear_all(self):
        """Limpa todo o grid, removendo obstáculos e cores."""
        self.grid.grid.fill(0)
        self.draw_grid()
        self.update_statistics()

def create_visualizer(grid: Grid):
    """Cria e exibe a janela do visualizador."""
    root = tk.Tk()
    app = GridVisualizer(root, grid)
    root.mainloop() 