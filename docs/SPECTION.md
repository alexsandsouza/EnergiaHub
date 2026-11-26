# SPECTION — EnergiaHub v1.0
## Product Brief
Organizar indicadores públicos agregados e registros acadêmicos simulados por município.
## PRD
RF01 consultar municípios IBGE; RF02 cadastrar, filtrar, excluir e exportar registros locais; RF03 mostrar contagens. RNF01 interface responsiva; RNF02 distinguir simulação de dado oficial; RNF03 não armazenar segredos ou dados operacionais sensíveis.
## HLD / LLD
Frontend estático, localStorage, adaptador IBGE; backend FastAPI independente com SQLite local. Frontend ainda não consome backend.
## ADR-001
GitHub Pages para frontend; backend separado para permitir futura autenticação e persistência centralizada.
## API
GET /health, GET /api/v1/records, POST /api/v1/records, DELETE /api/v1/records/{id}. Apenas registros demonstrativos.
## Test plan
Validar cadastro, filtro, exclusão, recarga, exportação, falha IBGE, viewport móvel e validação API. Testes de navegador e integração pendentes.
## Roadmap
Validar fontes energéticas públicas, autenticação, indicadores agregados, mapa municipal e simulação acadêmica.
