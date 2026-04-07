# 🚀 GUIA RÁPIDO - Começando do Zero

Erro corrigido! Agora você pode executar o projeto.

## ✅ Passo a Passo Atualizado

### 1. Pare tudo e limpe (se estava rodando)
```bash
cd /home/arthur/Prog/PixelDexPro
docker-compose down -v
```

### 2. Configure o ambiente
```bash
cp .env.example .env
```

### 3. Suba os containers
```bash
docker-compose up -d
```

**Aguarde 2-3 minutos** para os containers iniciarem completamente.

### 4. Verifique se tudo está rodando
```bash
docker-compose ps
```

Você deve ver:
- ✅ pixeldex-db (healthy)
- ✅ pixeldex-redis (healthy)
- ✅ pixeldex-backend (running)
- ✅ pixeldex-frontend (running)

### 5. Execute as migrações do banco
```bash
docker-compose exec backend alembic upgrade head
```

### 6. Importe dados de teste
```bash
# Tipos (rápido - ~10 segundos)
curl -X POST "http://localhost:8000/api/v1/sync/pokeapi/types"

# Pokémon Geração 1 (lento - ~10 minutos)
curl -X POST "http://localhost:8000/api/v1/sync/pokeapi/pokemon?limit=151&offset=0"
```

**💡 Dica**: Enquanto importa, você já pode acessar o frontend!

### 7. Acesse a aplicação 🎉

- **Frontend**: http://localhost:5173
- **API Docs**: http://localhost:8000/docs
- **Backend**: http://localhost:8000

---

## 📝 O que foi corrigido?

1. ✅ Gerado `package-lock.json` no frontend
2. ✅ Dockerfile atualizado para usar `npm ci`
3. ✅ Projeto pronto para rodar

---

## 🔄 Se ainda der erro

### Ver logs em tempo real
```bash
docker-compose logs -f
```

### Reconstruir as imagens
```bash
docker-compose build --no-cache
docker-compose up -d
```

### Verificar logs específicos
```bash
# Frontend
docker-compose logs frontend

# Backend
docker-compose logs backend

# Banco
docker-compose logs db
```

---

## ⏱️ Importação de Dados - Quanto Tempo?

- **Tipos**: ~10 segundos ⚡
- **10 Pokémon**: ~1 minuto
- **151 Pokémon (Gen 1)**: ~10 minutos 🐌
- **898 Pokémon (Todos)**: ~1-2 horas 🕐

**Recomendação para teste**: Importe apenas 10-20 Pokémon primeiro:
```bash
curl -X POST "http://localhost:8000/api/v1/sync/pokeapi/pokemon?limit=20&offset=0"
```

---

## ✅ Checklist Final

- [ ] Docker Desktop rodando
- [ ] `docker-compose ps` mostra 4 containers
- [ ] http://localhost:5173 abre (pode estar vazio se não importou dados)
- [ ] http://localhost:8000/docs mostra Swagger
- [ ] Migrações executadas
- [ ] Tipos importados (mínimo)

---

## 🎯 Teste Rápido

1. Abra http://localhost:8000/docs
2. Clique em **GET /api/v1/types**
3. Clique em "Try it out" → "Execute"
4. Deve retornar lista de tipos (normal, fire, water, etc)

Se funcionar, está tudo OK! 🎉
