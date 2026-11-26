# ⚡ EnergiaHub AM

Plataforma acadêmica de indicadores energéticos públicos e simulação no Amazonas.

## Executar
Abra index.html em um servidor estático. O GitHub Pages pode servir a raiz da branch main.

## v1.4
Dashboard, cadastro local demonstrativo, filtros, exclusão, exportação JSON e consulta à API pública de municípios do IBGE. Dados locais ficam no navegador. Não há conexão com infraestrutura elétrica nem telemetria real.

Inclui painel DEC/FEC simulado, explorador municipal e mapa administrativo Leaflet/IBGE. Revisão estática de validação e armazenamento realizada; testes de navegador e chamadas externas pendentes.

## API
Backend independente em backend/. Execute pip install -r requirements.txt e uvicorn main:app a partir dessa pasta. A API é um exemplo local, não deve ser exposta sem autenticação.

## SPECTION
Veja docs/SPECTION.md. Integrações ANEEL/ONS/INMET ainda planejadas.

## Analytics v1.4
Contagens de registros locais, filtro municipal, gráfico por categoria e exportação CSV com proteção básica contra fórmulas. Não representa indicadores elétricos reais. Testes de execução pendentes.

## API central v1.9 (prévia)
Configure DATABASE_URL para um PostgreSQL de desenvolvimento e ENERGIA_ADMIN_TOKEN com um segredo aleatório de pelo menos 32 caracteres no ambiente do servidor. Em backend/, instale requirements.txt e execute uvicorn central:app --host 127.0.0.1. Swagger em /docs. Use o token Bearer apenas em cliente administrativo confiável; nunca no frontend público. Não há JWT, contas individuais, CORS ou sincronização com o frontend nesta versão. O backend demo main.py continua separado. Não exponha a API sem HTTPS e revisão de segurança. Testes e implantação pendentes.
