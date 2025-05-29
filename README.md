# 🤖 Automação de Coleta de Relatórios - DigiSac | MDI

Este projeto foi desenvolvido na empresa **MDI** com o objetivo de automatizar a extração de relatórios da plataforma **DigiSac**, otimizando tarefas manuais e recorrentes como filtragem de dados, download de arquivos e organização local. O sistema também prevê uma futura integração com o **SharePoint**, permitindo o envio automático dos relatórios para uma pasta compartilhada.

## 🎯 Funcionalidades

- 🔐 Login automatizado na plataforma **DigiSac**
- 📁 Acesso às seções:
  - Histórico de Chamados
  - Estatísticas de Avaliação
- 🧾 Aplicação de filtros conforme as necessidades da equipe
- 📥 Download automático dos relatórios
- 📝 Renomeação dinâmica dos arquivos com base em data e tipo
- 🗂️ Organização dos arquivos em pastas por categoria
- ☁️ (Em desenvolvimento) Upload automático para o **SharePoint**

## 🧰 Bibliotecas Utilizadas

- 🧪 `dotenv` — Carregamento de variáveis de ambiente sensíveis
- 📁 `os` — Manipulação de arquivos e diretórios
- 📂 `pathlib.Path` — Caminhos multiplataforma de forma robusta
- 🌐 `selenium` — Automação da navegação e interação com o DOM
  - `webdriver`, `By`, `WebDriverWait`, `expected_conditions`, `Keys`
- ⏱️ `time` — Temporização e delays
- 📅 `datetime`, `timedelta` — Manipulação de datas
- 🖱️ `pyautogui` — Automação de mouse e teclado para ações na interface

## 🛡️ Segurança

As credenciais e informações sensíveis são armazenadas em um arquivo `.env`, nunca versionado.  
Elas são carregadas usando `load_dotenv()` para manter o código seguro.

Exemplo de `.env`:
```env
DIGISAC_USER=seu_usuario
DIGISAC_PASS=sua_senha
🚀 Como Executar
### Instale os pacotes necessários:

```pip install selenium pyautogui python-dotenv```

### Crie um arquivo .env com suas credenciais.

### Execute o script principal:

```python main.py```

##📌 Próximos Passos
- Integração com SharePoint via API ou biblioteca externa

- Implementar notificações (email ou Teams) após a execução

- Melhorar tratamento de exceções e logs detalhados

- Agendar execução diária com Task Scheduler (Windows) ou cron (Linux)

## 👤 Autor
Desenvolvido por mim, Ramon Jorge, colaborador da MDI, com foco em análise de dados, automação de processos e melhoria contínua.

## ⚠️ Observações
Este projeto foi desenvolvido para atender às necessidades específicas da empresa MDI. Para uso externo, será necessário adaptar os parâmetros, URLs e credenciais de autenticação.