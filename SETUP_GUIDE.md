# 🚀 Guia Completo de Execução - PixelDex Pro

## 📋 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- **Node.js** 20+ ([Download](https://nodejs.org/))
- **Python** 3.11+ ([Download](https://www.python.org/))
- **PostgreSQL** 15+ ([Download](https://www.postgresql.org/))
- **Git** ([Download](https://git-scm.com/))

**OU**

- **Docker** + **Docker Compose** ([Download](https://www.docker.com/))

---

## 🐳 Opção 1: Executar com Docker (RECOMENDADO)

### Passo 1: Clone o repositório
```bash
git clone https://github.com/seu-usuario/PixelDexPro.git
cd PixelDexPro
```

### Passo 2: Configure as variáveis de ambiente
```bash
cp .env.example .env
```

O arquivo `.env` já vem com valores padrão que funcionam com Docker. Não precisa alterar nada para começar.

### Passo 3: Suba os containers
```bash
docker-compose up -d
```

Isso irá:
- ✅ Criar banco PostgreSQL na porta 5432
- ✅ Criar Redis na porta 6379
- ✅ Instalar dependências e iniciar backend na porta 8000
- ✅ Instalar dependências e iniciar frontend na porta 5173

### Passo 4: Execute as migrações do banco
```bash
docker-compose exec backend alembic upgrade head
```

### Passo 5: (Opcional) Importe dados da PokéAPI
```bash
# Importar os primeiros 151 Pokémon (Geração 1)
curl -X POST "http://localhost:8000/api/v1/sync/pokeapi/pokemon?limit=151&offset=0"

# Importar tipos
curl -X POST "http://localhost:8000/api/v1/sync/pokeapi/types"
```

**⚠️ Nota**: A importação de 151 Pokémon pode levar alguns minutos (a PokéAPI tem rate limit).

### Passo 6: Acesse a aplicação

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **Documentação da API**: http://localhost:8000/docs
- **Swagger UI Alternativo**: http://localhost:8000/redoc

### Comandos úteis do Docker

```bash
# Ver logs em tempo real
docker-compose logs -f

# Ver logs só do backend
docker-compose logs -f backend

# Ver logs só do frontend
docker-compose logs -f frontend

# Parar os containers
docker-compose stop

# Parar e remover os containers
docker-compose down

# Parar, remover containers E volumes (⚠️ deleta o banco!)
docker-compose down -v

# Reconstruir as imagens
docker-compose build

# Acessar o shell do container do backend
docker-compose exec backend bash

# Acessar o PostgreSQL
docker-compose exec db psql -U postgres -d pixeldex
```

---

## 💻 Opção 2: Executar Localmente (Sem Docker)

### Passo 1: Clone o repositório
```bash
git clone https://github.com/seu-usuario/PixelDexPro.git
cd PixelDexPro
```

### Passo 2: Configure o PostgreSQL

```bash
# Criar o banco de dados
createdb pixeldex

# Ou via psql
psql -U postgres -c "CREATE DATABASE pixeldex;"
```

### Passo 3: Configure o Backend

```bash
cd backend

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# No Linux/Mac:
source venv/bin/activate
# No Windows:
venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Copiar arquivo de configuração
cp ../.env.example .env

# Editar .env e configurar DATABASE_URL
# DATABASE_URL=postgresql://seu_usuario:sua_senha@localhost:5432/pixeldex

# Executar migrações
alembic upgrade head

# Iniciar o servidor
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

O backend estará rodando em: http://localhost:8000

### Passo 4: Configure o Frontend

**Em um NOVO terminal** (deixe o backend rodando):

```bash
cd frontend

# Instalar dependências
npm install

# Iniciar servidor de desenvolvimento
npm run dev
```

O frontend estará rodando em: http://localhost:5173

### Passo 5: (Opcional) Importe dados da PokéAPI

**Em um NOVO terminal**:

```bash
# Importar os primeiros 151 Pokémon (Geração 1)
curl -X POST "http://localhost:8000/api/v1/sync/pokeapi/pokemon?limit=151&offset=0"

# Importar tipos
curl -X POST "http://localhost:8000/api/v1/sync/pokeapi/types"

# Importar um Pokémon específico
curl -X POST "http://localhost:8000/api/v1/sync/pokeapi/pokemon/pikachu"
```

---

## 📊 Importar Dados do Cobblemon

### Via API (Swagger UI)

1. Acesse: http://localhost:8000/docs
2. Vá para a seção **sync**
3. Clique em `POST /api/v1/sync/cobblemon/spawns`
4. Clique em "Try it out"
5. Cole a URL da planilha do Cobblemon:
```json
{
  "sheet_url": "URL_DA_PLANILHA_COBBLEMON",
  "version": "1.5.0"
}
```
6. Clique em "Execute"

### Via cURL

```bash
curl -X POST "http://localhost:8000/api/v1/sync/cobblemon/spawns" \
  -H "Content-Type: application/json" \
  -d '{
    "sheet_url": "URL_DA_PLANILHA_COBBLEMON",
    "version": "1.5.0"
  }'
```

---

## 🧪 Testando a Aplicação

### Backend

```bash
cd backend

# Executar testes (quando implementados)
pytest

# Executar com coverage
pytest --cov=. --cov-report=html
```

### Frontend

```bash
cd frontend

# Executar testes (quando implementados)
npm test

# Executar com coverage
npm run test:coverage
```

---

## 🔍 Endpoints Disponíveis

### Pokémon
- `GET /api/v1/pokemon` - Listar todos os Pokémon
- `GET /api/v1/pokemon/{id}` - Obter Pokémon por ID
- `GET /api/v1/pokemon/{id}/details` - Obter detalhes completos
- `GET /api/v1/pokemon/search?q=pikachu` - Buscar por nome

### Types
- `GET /api/v1/types` - Listar todos os tipos
- `GET /api/v1/types/chart` - Tabela de efetividade

### Cobblemon
- `GET /api/v1/cobblemon/spawns` - Listar spawns
- `GET /api/v1/cobblemon/spawns/{pokemon_id}` - Spawns de um Pokémon
- `GET /api/v1/cobblemon/biomes` - Listar biomas

### Compare
- `GET /api/v1/compare?pokemon1=1&pokemon2=25` - Comparar dois Pokémon

### Teams
- `POST /api/v1/teams` - Criar time
- `GET /api/v1/teams/{id}` - Obter time
- `POST /api/v1/teams/{id}/pokemon` - Adicionar Pokémon ao time
- `GET /api/v1/teams/{id}/analysis` - Analisar time

### Favorites
- `GET /api/v1/favorites` - Listar favoritos
- `POST /api/v1/favorites/{pokemon_id}` - Adicionar favorito
- `DELETE /api/v1/favorites/{pokemon_id}` - Remover favorito

### Sync (Importação de Dados)
- `POST /api/v1/sync/pokeapi/pokemon` - Importar Pokémon
- `POST /api/v1/sync/pokeapi/types` - Importar tipos
- `POST /api/v1/sync/cobblemon/spawns` - Importar spawns do Cobblemon

---

## 🛠️ Comandos de Desenvolvimento

### Backend - Migrations

```bash
cd backend

# Criar nova migração
alembic revision --autogenerate -m "Descrição da mudança"

# Aplicar migrações
alembic upgrade head

# Reverter última migração
alembic downgrade -1

# Ver histórico
alembic history

# Ver migração atual
alembic current
```

### Frontend - Build

```bash
cd frontend

# Build de produção
npm run build

# Preview da build
npm run preview

# Linting
npm run lint

# Format com Prettier (quando configurado)
npm run format
```

---

## 🐛 Troubleshooting

### Problema: Backend não inicia

**Erro**: `ModuleNotFoundError: No module named 'fastapi'`

**Solução**:
```bash
cd backend
source venv/bin/activate  # ou venv\Scripts\activate no Windows
pip install -r requirements.txt
```

### Problema: Erro de conexão com o banco

**Erro**: `could not connect to server: Connection refused`

**Solução**:
1. Verifique se o PostgreSQL está rodando:
```bash
# Linux
sudo systemctl status postgresql

# macOS
brew services list

# Windows
net start postgresql-x64-15
```

2. Verifique as credenciais no `.env`:
```env
DATABASE_URL=postgresql://usuario:senha@localhost:5432/pixeldex
```

### Problema: Frontend não carrega dados

**Erro**: `Network Error` ou `Failed to fetch`

**Solução**:
1. Verifique se o backend está rodando em http://localhost:8000
2. Verifique o console do navegador (F12) para ver erros CORS
3. Confirme que `VITE_API_URL` está correto no `.env`

### Problema: Migrações falham

**Erro**: `alembic.util.exc.CommandError`

**Solução**:
```bash
cd backend

# Reverter todas as migrações
alembic downgrade base

# Recriar o banco
dropdb pixeldex
createdb pixeldex

# Aplicar novamente
alembic upgrade head
```

### Problema: Docker não inicia

**Erro**: `port is already allocated`

**Solução**:
```bash
# Ver processos usando a porta
lsof -i :8000  # Linux/Mac
netstat -ano | findstr :8000  # Windows

# Alterar as portas no docker-compose.yml
# ou matar o processo que está usando a porta
```

---

## 📚 Estrutura do Projeto

```
PixelDexPro/
├── backend/                 # Backend FastAPI
│   ├── alembic/            # Migrações do banco
│   ├── api/                # Rotas da API
│   ├── core/               # Configurações
│   ├── db/                 # Sessão do banco
│   ├── integrations/       # PokéAPI + Cobblemon
│   ├── models/             # Modelos SQLAlchemy
│   ├── repositories/       # Camada de dados
│   ├── schemas/            # Schemas Pydantic
│   ├── services/           # Lógica de negócio
│   ├── main.py            # Entrada da aplicação
│   └── requirements.txt   # Dependências Python
│
├── frontend/               # Frontend React
│   ├── src/
│   │   ├── components/    # Componentes React
│   │   ├── hooks/         # Custom hooks
│   │   ├── pages/         # Páginas
│   │   ├── services/      # API clients
│   │   ├── store/         # Zustand stores
│   │   ├── types/         # TypeScript types
│   │   └── utils/         # Utilitários
│   ├── index.html
│   ├── package.json
│   └── vite.config.ts
│
├── docker-compose.yml      # Orquestração Docker
├── .env.example            # Template de variáveis
└── README.md               # Documentação
```

---

## 🎯 Próximos Passos

Após executar o projeto:

1. ✅ **Importe dados**: Use os endpoints `/sync` para popular o banco
2. ✅ **Explore a interface**: Navegue pela Pokédex, crie times, compare Pokémon
3. ✅ **Teste as funcionalidades**: Adicione favoritos, monte times
4. ✅ **Consulte a API**: Veja http://localhost:8000/docs

---

## 💡 Dicas

- **Desenvolvimento rápido**: Use Docker para não se preocupar com dependências
- **Debug**: Use o Swagger UI em `/docs` para testar endpoints
- **Performance**: Importe poucos Pokémon inicialmente para testar
- **Dados de produção**: Para importar todas as gerações, execute múltiplos batches:
  ```bash
  # Geração 1 (1-151)
  curl -X POST "http://localhost:8000/api/v1/sync/pokeapi/pokemon?limit=151&offset=0"
  
  # Geração 2 (152-251)
  curl -X POST "http://localhost:8000/api/v1/sync/pokeapi/pokemon?limit=100&offset=151"
  
  # E assim por diante...
  ```

---

## 📞 Suporte

- **Documentação da API**: http://localhost:8000/docs
- **Issues**: Abra uma issue no GitHub
- **PokéAPI Docs**: https://pokeapi.co/docs/v2

---

**Desenvolvido com ❤️ para fãs de Pokémon e Cobblemon**
