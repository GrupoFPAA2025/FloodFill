# 🎨 FloodFill - Colorindo Regiões de um Terreno com Obstáculos

## 👥 Equipe
- **Guilherme Augusto Jardim de Souza** 
- **João Pedro Mairinque de Azevedo** 
- **Mauricio Fernandes Leite** 
- **Sara Lourenço Iglesias** 
- **Vinicius Levi** 

## 📝 Introdução ao Problema

Este projeto implementa uma solução para o problema de identificação e coloração de regiões conectadas em um terreno com obstáculos, utilizando o algoritmo Flood Fill. O sistema foi desenvolvido para auxiliar robôs autônomos na navegação e mapeamento de terrenos desconhecidos.

### Contexto
O sistema recebe como entrada um grid bidimensional que representa um terreno, onde:
- **0**: Representa células navegáveis (branco)
- **1**: Representa obstáculos (preto)
- **2+**: Representa regiões já coloridas (vermelho, laranja, amarelo, etc.)

O objetivo é identificar e colorir automaticamente todas as regiões conectadas do terreno, respeitando os obstáculos e atribuindo cores diferentes para cada região isolada.

## 🔍 Algoritmo Flood Fill

### Funcionamento
O algoritmo implementado segue os seguintes passos:

1. **Inicialização**:
   - Recebe o grid bidimensional n × m
   - Identifica a célula inicial (x, y)
   - Prepara as estruturas de dados necessárias

2. **Processo de Preenchimento**:
   - A partir da célula inicial, explora células adjacentes ortogonalmente (cima, baixo, esquerda, direita)
   - Identifica células navegáveis (valor 0) conectadas
   - Preenche a região com uma cor específica (valores 2+)
   - Respeita obstáculos (valor 1) como limites
   - Busca automaticamente a próxima região não colorida

3. **Regras de Coloração**:
   - Cada região recebe uma cor única
   - Cores são atribuídas sequencialmente (2: vermelho, 3: laranja, etc.)
   - Regiões já coloridas são preservadas
   - O processo continua até que todas as células navegáveis estejam coloridas

## 🚀 Configuração e Execução

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/GrupoFPAA2025/FloodFill.git
cd FloodFill
```

2. (Recomendado) Crie um ambiente virtual:
```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

### Execução
```bash
python main.py
```

## 📊 Exemplos de Uso

### Exemplo 1
**Entrada:**
```
Grid inicial:
0 0 1 0 0
0 1 1 0 0
0 0 1 1 1
1 1 0 0 0

Coordenadas iniciais: (0, 0)
```

**Saída:**
```
Grid preenchido:
2 2 1 3 3
2 1 1 3 3
2 2 1 1 1
1 1 4 4 4
```

### Exemplo 2
**Entrada:**
```
Grid inicial:
0 1 0 0 1
0 1 0 0 1
0 1 1 1 1
0 0 0 1 0

Coordenadas iniciais: (0, 2)
```

**Saída:**
```
Grid preenchido:
3 1 2 2 1
3 1 2 2 1
3 1 1 1 1
3 3 3 1 4
```

### Legenda de Cores
- **0**: Branco (Terreno navegável)
- **1**: Preto (Obstáculo)
- **2**: Vermelho (Primeira região)
- **3**: Laranja (Segunda região)
- **4**: Amarelo (Terceira região)
- **5**: Verde (Quarta região)
- **6**: Azul (Quinta região)

## 🌟 Funcionalidades Extras

1. **Interface Gráfica**:
   - Visualização dinâmica do processo de preenchimento
   - Cores distintas para melhor identificação das regiões
   - Interação intuitiva para definição de obstáculos

2. **Gerador de Grids**:
   - Criação automática de grids com diferentes dimensões
   - Configuração da proporção de obstáculos
   - Validação automática da navegabilidade

## 📊 Análise de Complexidade

- **Tempo**: O(n×m), onde n e m são as dimensões do grid
- **Espaço**: O(n×m) para armazenamento do grid e estruturas auxiliares

## 🧪 Testes

Execute os testes automatizados:
```bash
python -m pytest tests/
```

## 📄 Licença

Este projeto está sob a licença MIT. 
