# Imagem base oficial do PostgreSQL - escolha a versão desejada
FROM postgres:16

# Mantenedor (opcional)
# LABEL maintainer="Seu Nome <seu@email.com>"

# Variáveis de ambiente para configuração inicial do PostgreSQL
# Estas são algumas opções comuns, você pode ajustá-las conforme necessário
ENV POSTGRES_USER=meu_usuario
ENV POSTGRES_PASSWORD=minha_senha
ENV POSTGRES_DB=meu_banco

# Porta padrão do PostgreSQL (opcional, já é o default)
EXPOSE 5432

# Diretório de trabalho (opcional)
WORKDIR /app

# Copiar scripts de inicialização (se houver)
# Crie uma pasta 'init' com seus scripts .sql ou .sh
COPY ./init/ /docker-entrypoint-initdb.d/

# Volume para persistência de dados
VOLUME /var/lib/postgresql/data

# O comando padrão já é definido pela imagem base postgres
# CMD ["postgres"]