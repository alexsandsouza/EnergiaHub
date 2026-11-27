# EnergiaHub Live API

Protótipo FastAPI/PostgreSQL compatível com Supabase. Não é uma API oficial de fornecimento.

1. Crie um projeto Supabase e obtenha a conexão PostgreSQL para servidor (SSL obrigatório).
2. Configure DATABASE_URL e ENERGIA_REPORT_TOKEN (segredo aleatório de 32+ caracteres) no ambiente do backend, nunca no GitHub Pages.
3. Instale backend/requirements.txt e execute `uvicorn backend.live:app --host 0.0.0.0 --port 8000`.
4. Consulte `/docs`, `/health` e `/api/v1/summary`. POST `/api/v1/reports` exige Bearer de operador autorizado; não disponibilize o token no navegador.

Resumo público: contagem estadual diária de relatos não verificados, dias concluídos, mínimo cinco registros. Não representa interrupções confirmadas. Antes de aceitar contribuições públicas, implementar autenticação individual, validação de localidades, moderação, limites de requisições e política de retenção. Não coletar endereços, nomes ou contatos. Hospedagem e banco ainda não provisionados.
