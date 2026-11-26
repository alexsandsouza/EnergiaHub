# Quality gate v1.9.1

## Automatizado
- Sintaxe de todos os JavaScript da raiz.
- Compilação Python e testes unitários de validação/autorização.
- Consultar GitHub Actions para confirmar execução; código submetido não significa aprovação.

## Aceite manual pendente
- GitHub Pages: confirmar publicação, navegação de todos os módulos, temas, menu e responsividade.
- IBGE: municípios e mapa; ANEEL: catálogo, CORS, indisponibilidade.
- CSV: modelo, importação válida, rejeição de duplicatas, persistência, exclusão e relatórios.
- PostgreSQL: ambiente de teste isolado, inicialização, CRUD, paginação e falhas de autenticação.
- Revisão de segurança antes de exposição; HTTPS, segredos, autenticação individual e política de acesso.
- Verificar proveniência e granularidade de séries oficiais. Não tratar dados declarados como autenticados.

## Decisão
Manter frontend 1.8 e API central 1.9 independentes até aprovação dos testes de integração. Não conectar token administrativo ao frontend público. Não iniciar Digital Twin como versão estável antes do aceite.
