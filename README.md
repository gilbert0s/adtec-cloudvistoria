# Portal ADTEC CloudVistoria 🏢☁️

### Centro Universitário UNIFEOB
**Curso:** Análise e Desenvolvimento de Sistemas (ADS)
**Módulo:** Computação em Nuvem e Qualidade de Software
**Período:** 2º Trimestre Letivo de 2026

---

## 👥 Integrantes do Grupo (Desenvolvedores)
* **Ana Jaqueline da Costa França** - RA: 24000520
* **Gilberto Belizário de Souza** - RA: 24000566
* **Leonardo Mendes de Freitas** - RA: 24000528

## 👨‍🏫 Corpo Docente / Orientação
* **Computação em Nuvem:** Prof. Rodrigo Marudi de Oliveira
* **Qualidade de Software:** Prof. Nivaldo de Andrade
* **Projeto Integrado:** Prof. Mariangela Martimbianco Santos

---

## 📝 Sobre o Projeto
O **ADTEC CloudVistoria** é uma aplicação web unificada desenvolvida como solução de impacto real para a imobiliária parceira **ADTEC**. O foco principal é modernizar o processo arcaico de armazenamento de vistorias residenciais, eliminando gargalos físicos de hardware local através da transição para uma infraestrutura 100% em nuvem.


### 🛠️ Diferenciais Técnicos Implementados:
* **Arquitetura Serverless:** Conexão síncrona direta entre o frontend do usuário e os endpoints da nuvem utilizando o AWS SDK em JavaScript, reduzindo custos com servidores intermediários ativos.
* **Mecanismo de Idempotência:** Banco de dados de chaves baseado em um documento centralizado (`index_vistorias.json`). A chave primária é composta de forma combinada por `[Endereço] + ([Ano da Vistoria])`, impedindo a duplicidade ou a sobrescrita acidental de dados históricos.
* **Faxina Preventiva (Cleanup):** Rotina assíncrona baseada em Promises estruturadas (`async/await`) que limpa mídias obsoletas na AWS antes de subir novas atualizações, garantindo a integridade estrita do espelhamento de pastas.
* **Resiliência de Extensões:** O motor aceita qualquer formato de arquivo enviado pelo dispositivo móvel (como imagens modernas `.avif`, relatórios em `.docx` ou `.pdf`) sem exigir renomeação manual do usuário.

---

## 🏗️ Arquitetura e Tecnologias
* **Frontend:** HTML5, CSS3, JavaScript Vanilla
* **Provedor de Nuvem (Cloud):** Amazon Web Services (AWS)
* **Serviços Utilizados:** Amazon S3 (Simple Storage Service) - Modelo IaaS
* **Controle de Versão:** Git e GitHub

---

## 🔒 Segurança da Informação
O projeto segue rígidos padrões contra vazamentos de credenciais (*Secret Leaks*). Todas as chaves e tokens de acesso da AWS foram estritamente isolados em um arquivo de configuração local (`config.js`), o qual encontra-se devidamente blindado e ignorado pelo repositório público através das regras do arquivo de governança `.gitignore`.