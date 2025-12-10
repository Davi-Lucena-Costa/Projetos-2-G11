# 📈 Otimizando o site do Jornal do Commercio e buscando a fidelidade dos clientes

## 🎯 Objetivo do Projeto
Este projeto tem como objetivo **conquistar a fidelidade dos clientes do Jornal do Commercio**, oferecendo uma experiência digital mais agradável por meio de **estratégias de otimização do site**.

## 📌 Resultados Esperados
- Aumento da taxa de **retenção de leitores**
- Crescimento no número de **assinantes**
- Melhoria da **imagem da marca** como um veículo moderno e acessível
- **Maior engajamento** com o conteúdo jornalístico

## 🔗 Links Importantes
- 🚀 **[Site no Ar (Deploy)](https://projetos-2-g11.onrender.com)**
- 📄 **[Histórias de usuário e cenários](https://docs.google.com/document/d/1dRo1rZinYxXtpklP78JwofUMNUwflzO9PsG-q0wJt4M/edit?tab=t.0)**
- 🌐 **[Site oficial do grupo](https://sites.google.com/cesar.school/g11/home)**
- 📖 **[Relatório de Pair Programming](https://github.com/Davi-Lucena-Costa/Projetos-2-G11/wiki/Relat%C3%B3rio-de-Pair-Programming)**

### 📊 Backlog do Projeto

![Backlog do Projeto](https://raw.githubusercontent.com/Davi-Lucena-Costa/Projetos-2-G11/main/imagens/jira.png)

---

## 🎥 Screencast

Confira o vídeo demonstrativo do nosso site em funcionamento:
[**📺 Assistir no YouTube**](https://youtu.be/LCIPnGnmC9A)

---



## 🛠️ Configuração do Ambiente de Desenvolvimento

Siga estes passos para rodar o projeto no seu computador localmente (Windows).

### 1. Pré-requisitos
Certifique-se de ter instalado:
- **Python 3.11+**: [Baixar Python](https://www.python.org/downloads/)
- **Git**: [Baixar Git](https://git-scm.com/downloads)
- **VS Code** (Recomendado)

### 2. Clonar o Repositório
Abra o seu terminal (Git Bash ou PowerShell) e rode:

```bash
git clone [https://github.com/Davi-Lucena-Costa/Projetos-2-G11.git](https://github.com/Davi-Lucena-Costa/Projetos-2-G11.git)
cd Projetos-2-G11

# Criar e Ativar o Ambiente Virtual (Venv)
No Windows (PowerShell):

# Cria a pasta 'venv'
python -m venv venv

# Ativa o ambiente (Obrigatório antes de rodar o projeto)
.\venv\Scripts\activate


# Instalar Dependências
Com o ambiente virtual ativo, instale todas as bibliotecas necessárias (Django e demais dependências):

pip install -r requirements.txt


# Configurar o Banco de Dados

Crie as tabelas necessárias no banco local (SQLite):

python manage.py migrate

 #Opcional: Crie um superusuário para acessar o painel administrativo (/admin):

python manage.py createsuperuser

# Rodar o Projeto 🚀

Agora basta iniciar o servidor local:

python manage.py runserver

