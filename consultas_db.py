import mysql.connector
import pandas as pd

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Bote sua senha', #--- Bote sua senha ---
    'database': 'db_ecommerce'
}

# --- Consultas SQL ---
consultas_originais = [
    (
        "Consulta 1: Clientes cadastrados em 2024",
        """
        SELECT
            nome,
            email,
            data_cadastro
        FROM
            Clientes
        WHERE
            data_cadastro BETWEEN '2024-01-01' AND '2024-12-31'
        ORDER BY
            data_cadastro DESC;
        """
    ),
    (
        "Consulta 2: Produtos fora das categorias (1, 5, 10) e preço <= 100.00",
        """
        SELECT
            nome,
            preco,
            estoque
        FROM
            Produtos
        WHERE
            id_categoria NOT IN (1, 5, 10)
            AND preco <= 100.00;
        """
    ),
    (
        "Consulta 3: Contagem de pedidos por cliente",
        """
        SELECT
            c.nome AS Nome_Cliente,
            COUNT(p.id_pedido) AS Total_Pedidos
        FROM
            Clientes c
        INNER JOIN
            Pedidos p ON c.id_cliente = p.id_cliente
        GROUP BY
            c.nome
        ORDER BY
            Total_Pedidos DESC;
        """
    ),
    (
        "Consulta 4: Preço máximo e mínimo por categoria",
        """
        SELECT
            ca.nome AS Nome_Categoria,
            MAX(pr.preco) AS Preco_Maximo,
            MIN(pr.preco) AS Preco_Minimo
        FROM
            Produtos pr
        INNER JOIN
            Categorias ca ON pr.id_categoria = ca.id_categoria
        GROUP BY
            ca.nome;
        """
    ),
    (
        "Consulta 5: Valor total de pedidos pagos por 'Cartao Credito' ou 'Pix'",
        """
        SELECT
            pe.id_pedido,
            pe.data_pedido,
            SUM(pa.valor) AS Valor_Pago
        FROM
            Pedidos pe
        INNER JOIN
            Pagamentos pa ON pe.id_pedido = pa.id_pedido
        WHERE
            pa.metodo_pagamento = 'Cartao Credito' OR pa.metodo_pagamento = 'Pix'
        GROUP BY
            pe.id_pedido, pe.data_pedido
        HAVING
            SUM(pa.valor) > 0;
        """
    ),
    (
        "Consulta 6: Top 5 clientes que mais gastaram",
        """
        SELECT
            c.nome AS Nome_Cliente,
            SUM(p.valor_total) AS Gasto_Total
        FROM
            Clientes c
        INNER JOIN
            Pedidos p ON c.id_cliente = p.id_cliente
        GROUP BY
            c.nome
        ORDER BY
            Gasto_Total DESC
        LIMIT 5;
        """
    ),
    (
        "Consulta 7: Uso de cupons (incluindo não utilizados)",
        """
        SELECT
            cu.codigo AS Codigo_Cupom,
            cu.data_validade,
            COUNT(pe.id_pedido) AS Pedidos_Utilizaram
        FROM
            Cupons cu
        LEFT JOIN
            Pedidos pe ON cu.id_cupom = pe.id_cupom
        GROUP BY
            cu.codigo, cu.data_validade
        ORDER BY
            Pedidos_Utilizaram DESC;
        """
    ),
    (
        "Consulta 8: Pedidos com valor total acima da média",
        """
        SELECT
            p.id_pedido,
            c.nome AS Nome_Cliente,
            p.valor_total
        FROM
            Pedidos p
        INNER JOIN
            Clientes c ON p.id_cliente = c.id_cliente
        WHERE
            p.valor_total > (SELECT AVG(valor_total) FROM Pedidos)
        ORDER BY
            p.valor_total DESC;
        """
    ),
    (
        "Consulta 9: Lista de nomes de Clientes e Categorias",
        """
        SELECT nome, 'Cliente' AS Tipo
        FROM Clientes
        UNION ALL
        SELECT nome, 'Categoria' AS Tipo
        FROM Categorias
        ORDER BY Tipo, nome;
        """
    ),
    (
        "Consulta 10: Detalhes do pedido com id_pedido = 10",
        """
        SELECT
            p.id_pedido,
            p.data_pedido,
            c.nome AS Nome_Cliente,
            pr.nome AS Nome_Produto,
            ip.quantidade,
            ip.preco_unitario,
            (ip.quantidade * ip.preco_unitario) AS Subtotal_Item
        FROM
            Pedidos p
        INNER JOIN
            Clientes c ON p.id_cliente = c.id_cliente
        INNER JOIN
            Itens_Pedido ip ON p.id_pedido = ip.id_pedido
        INNER JOIN
            Produtos pr ON ip.id_produto = pr.id_produto
        WHERE
            p.id_pedido = 10
        ORDER BY
            pr.nome;
        """
    )
]

# --- Consultas de Álgebra Relacional ---
consultas_algebra_5 = [
    (
        "Consulta 1 (Álgebra 1): Pagamentos 'Pix' > 50",
        """
        SELECT
            id_pedido,
            valor,
            data_pagamento
        FROM
            Pagamentos
        WHERE
            metodo_pagamento = 'Pix' AND valor > 50;
        """
    ),
    (
        "Consulta 2 (Álgebra 2): Produtos da categoria 'Eletrônicos'",
        """
        SELECT
            pr.nome AS Nome_Produto
        FROM
            Produtos pr
        INNER JOIN
            Categorias ca ON pr.id_categoria = ca.id_categoria
        WHERE
            ca.nome = 'Eletrônicos';
        """
    ),
    (
        "Consulta 3 (Álgebra 3): Clientes que compraram TODOS produtos 'Eletrônicos'",
        """
        SELECT
            c.nome AS Cliente_Comprou_Tudo
        FROM
            Clientes c
        WHERE NOT EXISTS (
            SELECT 
                pr.id_produto
            FROM 
                Produtos pr
            INNER JOIN 
                Categorias ca ON pr.id_categoria = ca.id_categoria
            WHERE 
                ca.nome = 'Eletrônicos'
                
            AND NOT EXISTS (
                SELECT 
                    ip.id_produto
                FROM 
                    Pedidos p
                INNER JOIN 
                    Itens_Pedido ip ON p.id_pedido = ip.id_pedido
                WHERE 
                    p.id_cliente = c.id_cliente 
                    AND ip.id_produto = pr.id_produto
            )
        );
        """
    ),
    (
        "Consulta 4 (Álgebra 4): Nomes de Clientes e Categorias (União)",
        """
        SELECT nome, 'Cliente' AS Tipo FROM Clientes
        UNION
        SELECT nome, 'Categoria' AS Tipo FROM Categorias
        ORDER BY Tipo, nome;
        """
    ),
    (
        "Consulta 5 (Álgebra 5): Detalhes do Pedido 10 (Álgebra)",
        """
        SELECT
            c.nome AS Nome_Cliente,
            pr.nome AS Nome_Produto,
            ip.quantidade
        FROM
            Pedidos p
        INNER JOIN
            Clientes c ON p.id_cliente = c.id_cliente
        INNER JOIN
            Itens_Pedido ip ON p.id_pedido = ip.id_pedido
        INNER JOIN
            Produtos pr ON ip.id_produto = pr.id_produto
        WHERE
            p.id_pedido = 10;
        """
    )
]

todas_as_consultas = consultas_originais + consultas_algebra_5

try:
    print("Conectando ao banco de dados...")
    conn = mysql.connector.connect(**db_config)
    print("Conexão bem-sucedida!")

    cursor = conn.cursor()

    for titulo, query in todas_as_consultas:
        print(f"\n========================================================")
        print(f"Executando: {titulo}")
        print("========================================================")
        
        try:
            cursor.execute(query)
            resultados = cursor.fetchall()
            nomes_colunas = [i[0] for i in cursor.description]
            
            if resultados:
                df = pd.DataFrame(resultados, columns=nomes_colunas)
                print(df)
            else:
                print("A consulta não retornou resultados.")
        
        except mysql.connector.Error as err:
            print(f"Erro ao executar a consulta '{titulo}': {err}")

except mysql.connector.Error as err:
    print(f"\nErro ao conectar ao banco de dados: {err}")
    print("Por favor, verifique suas credenciais (host, user, password) e o nome do banco (database) em 'db_config'.")

finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
        print("\n========================================================")
        print("Conexão com o banco de dados fechada.")