import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import time
import os
from dotenv import load_dotenv

load_dotenv


def conectar_banco():
    try:
        conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
)
        print(" Conexão realizada com sucesso!\n")
        return conn
    except Exception as e:
        print(" Erro ao conectar:", e)
        return None


def carregar_dados(conn):
    query = """
    SELECT 
        c.nome AS cliente,
        p.nome AS produto,
        v.quantidade,
        p.preco,
        (v.quantidade * p.preco) AS total_venda,
        v.data_venda
    FROM vendas v
    JOIN clientes c ON v.clientes_id = c.id
    JOIN produtos p ON v.produto_id = p.id;
    """
    return pd.read_sql(query, conn)


def total_geral(df):
    total = df['total_venda'].sum()
    print(f"\n Total geral vendido: R$ {total:,.2f}\n")


def top_clientes(df):
    ranking = (
        df.groupby('cliente')['total_venda']
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )

    ranking.plot(kind='bar')
    plt.title('Top 5 Clientes')
    plt.ylabel('Total Comprado')
    plt.xlabel('Cliente')
    plt.tight_layout()
    plt.show()


def produto_mais_vendido(df):
    ranking = (
        df.groupby('produto')['quantidade']
        .sum()
        .sort_values(ascending=False)
    )

    print(" Produto mais vendido:")
    print(ranking.head(5))
    print()


def menu(df):
    while True:
        print("=== 📊 Análise de Vendas Informática ===")
        print("1) Venda total da loja")
        print("2) Top 5 Clientes")
        print("3) Produto mais vendido")
        print("4) Sair")

        try:
            opcao = int(input("O que deseja saber? "))

            if opcao == 1:
                total_geral(df)

            elif opcao == 2:
                top_clientes(df)

            elif opcao == 3:
                produto_mais_vendido(df)

            elif opcao == 4:
                print("Encerrando sistema...")
                break

            else:
                print("Opção inválida.\n")

        except ValueError:
            print("Digite um número válido.\n")

        time.sleep(1)


def main():
    conn = conectar_banco()

    if conn:
        df = carregar_dados(conn)
        menu(df)
        conn.close()


if __name__ == "__main__":
    main()