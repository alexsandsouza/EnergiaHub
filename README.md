# ⚡ EnergiaHub AM

Plataforma acadêmica de indicadores energéticos públicos e simulação no Amazonas.

## Executar
Abra index.html em um servidor estático. O GitHub Pages pode servir a raiz da branch main.

## v1.0
Dashboard, cadastro local demonstrativo, filtros, exclusão, exportação JSON e consulta à API pública de municípios do IBGE. Dados locais ficam no navegador. Não há conexão com infraestrutura elétrica nem telemetria real.

## API
Backend independente em backend/. Execute pip install -r requirements.txt e uvicorn main:app a partir dessa pasta. A API é um exemplo local, não deve ser exposta sem autenticação.

## SPECTION
Veja docs/SPECTION.md. Integrações ANEEL/ONS/INMET ainda planejadas.
