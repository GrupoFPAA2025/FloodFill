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

## 🔍 Funcionamento Detalhado do Algoritmo Flood Fill

### Visão Geral
O algoritmo Flood Fill é uma técnica de preenchimento que, a partir de um ponto inicial, "inunda" uma região conectada até encontrar bordas ou obstáculos. Em nosso projeto, ele é usado para identificar e colorir regiões navegáveis em um grid 2D.

### Processo de Execução
1. **Inicialização**:
   - Recebe uma célula inicial (x, y)
   - Verifica se a célula é válida e navegável (valor 0)
   - Prepara uma nova cor para preenchimento (valor ≥ 2)

2. **Exploração de Células**:
   - A partir da célula inicial, o algoritmo explora as células adjacentes nas quatro direções:
     ```
         ↑
     ← (x,y) →
         ↓
     ```
   - Para cada direção, verifica:
     * Se a célula está dentro dos limites do grid
     * Se a célula é navegável (valor 0)
     * Se a célula ainda não foi visitada

3. **Processo de Preenchimento**:
   - Quando uma célula válida é encontrada:
     * Preenche com a cor atual
     * Adiciona à fila de células para explorar
     * Marca como visitada
   - O processo continua recursivamente para todas as células conectadas
   - Para quando encontra:
     * Obstáculos (valor 1)
     * Células já coloridas (valor ≥ 2)
     * Limites do grid

4. **Busca de Novas Regiões**:
   - Após preencher uma região completa:
     * Busca a próxima célula navegável não colorida
     * Incrementa o valor da cor
     * Inicia novo preenchimento
   - Continua até que todas as células navegáveis estejam coloridas

### Exemplo de Execução
```
Grid Inicial:      Após (0,0):       Após (0,3):       Final:
0 0 1 0 0         2 2 1 0 0         2 2 1 3 3         2 2 1 3 3
0 1 1 0 0   →     2 1 1 0 0   →     2 1 1 3 3   →     2 1 1 3 3
0 0 1 1 1         2 2 1 1 1         2 2 1 1 1         2 2 1 1 1
1 1 0 0 0         1 1 0 0 0         1 1 0 0 0         1 1 4 4 4
```

### Estruturas de Dados
- **Grid Principal**: Matriz 2D para armazenar o estado atual
- **Fila/Pilha**: Para controlar células a serem exploradas
- **Conjunto de Visitados**: Para evitar loops infinitos

### Otimizações Implementadas
1. **Busca Eficiente**: Uso de estruturas de dados otimizadas
2. **Verificação Prévia**: Validação de células antes da recursão
3. **Controle de Memória**: Gerenciamento eficiente de recursos

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
