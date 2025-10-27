/*
 * Consultas SQL baseadas nas tabelas:
 * Clientes, Produtos, Categorias, Pedidos, Itens_Pedido, Pagamentos, Enderecos, Cupons
 */

/*
 * Consulta 1: Selecionar clientes cadastrados em um período específico
 * Uso: BETWEEN e ORDER BY
 */
SELECT
    nome,
    email,
    data_cadastro
FROM
    Clientes
WHERE
    data_cadastro BETWEEN '2024-01-01' AND '2024-12-31' -- Filtra clientes cadastrados dentro do ano de 2024
ORDER BY
    data_cadastro DESC; -- Ordena os resultados pela data de cadastro mais recente primeiro


/*
 * Consulta 2: Lista produtos que não pertencem a certas categorias e têm um preço máximo
 * Uso: NOT IN e operador de comparação (<=) com AND
 */
SELECT
    nome,
    preco,
    estoque
FROM
    Produtos
WHERE
    id_categoria NOT IN (1, 5, 10) -- Exclui produtos cujos IDs de categoria sejam 1, 5 ou 10
    AND preco <= 100.00; -- Filtra apenas produtos com preço menor ou igual a R$ 100,00


/*
 * Consulta 3: Contar o número total de Pedidos feitos por cada Cliente
 * Uso: COUNT, GROUP BY e INNER JOIN
 */
SELECT
    c.nome AS Nome_Cliente,
    COUNT(p.id_pedido) AS Total_Pedidos -- Conta o número de pedidos por grupo (cliente)
FROM
    Clientes c
INNER JOIN
    Pedidos p ON c.id_cliente = p.id_cliente -- Junta Clientes e Pedidos onde há correspondência
GROUP BY
    c.nome -- Agrupa o resultado pelo nome do cliente
ORDER BY
    Total_Pedidos DESC; -- Ordena pelo cliente com mais pedidos


/*
 * Consulta 4: Encontrar o Produto mais caro e o mais barato de cada Categoria
 * Uso: MAX, MIN, GROUP BY e INNER JOIN
 */
SELECT
    ca.nome AS Nome_Categoria,
    MAX(pr.preco) AS Preco_Maximo, -- Encontra o preço máximo do produto para o grupo (categoria)
    MIN(pr.preco) AS Preco_Minimo -- Encontra o preço mínimo do produto para o grupo (categoria)
FROM
    Produtos pr
INNER JOIN
    Categorias ca ON pr.id_categoria = ca.id_categoria -- Junta Produtos e Categorias
GROUP BY
    ca.nome; -- Agrupa o resultado por nome da categoria


/*
 * Consulta 5: Calcular o valor total de pedidos pagos via 'Cartao Credito' ou 'Pix'
 * Uso: SUM, GROUP BY, INNER JOIN e OR com HAVING
 */
SELECT
    pe.id_pedido,
    pe.data_pedido,
    SUM(pa.valor) AS Valor_Pago -- Soma o valor dos pagamentos para cada pedido
FROM
    Pedidos pe
INNER JOIN
    Pagamentos pa ON pe.id_pedido = pa.id_pedido -- Junta Pedidos e Pagamentos
WHERE
    pa.metodo_pagamento = 'Cartao Credito' OR pa.metodo_pagamento = 'Pix' -- Filtra por método de pagamento
GROUP BY
    pe.id_pedido, pe.data_pedido -- Agrupa pelo ID do pedido e data
HAVING
    SUM(pa.valor) > 0; -- Filtra os grupos (pedidos) onde a soma dos pagamentos é maior que zero


/*
 * Consulta 6: Mostrar os 5 Clientes que mais gastaram no total
 * Uso: SUM, GROUP BY, INNER JOIN, ORDER BY e LIMIT
 */
SELECT
    c.nome AS Nome_Cliente,
    SUM(p.valor_total) AS Gasto_Total -- Calcula o gasto total do cliente
FROM
    Clientes c
INNER JOIN
    Pedidos p ON c.id_cliente = p.id_cliente -- Junta Clientes e Pedidos
GROUP BY
    c.nome -- Agrupa pelo nome do cliente
ORDER BY
    Gasto_Total DESC -- Ordena do maior gasto para o menor
LIMIT 5; -- Limita o resultado às 5 primeiras linhas (top 5)


/*
 * Consulta 7: Listar todos os Cupons e a quantidade de Pedidos que o utilizaram (incluindo cupons não utilizados)
 * Uso: LEFT JOIN, COUNT e GROUP BY
 */
SELECT
    cu.codigo AS Codigo_Cupom,
    cu.data_validade,
    COUNT(pe.id_pedido) AS Pedidos_Utilizaram -- Conta quantos pedidos usaram o cupom
FROM
    Cupons cu
LEFT JOIN
    Pedidos pe ON cu.id_cupom = pe.id_cupom -- Junta Cupons com Pedidos. O LEFT JOIN garante que todos os cupons (mesmo sem pedidos) sejam listados.
GROUP BY
    cu.codigo, cu.data_validade -- Agrupa pelo cupom
ORDER BY
    Pedidos_Utilizaram DESC;


/*
 * Consulta 8: Selecionar Endereços no estado de 'SP' ou 'RJ' que são do tipo 'Entrega'
 * Uso: AND e OR com INNER JOIN
 */
SELECT
    c.nome AS Nome_Cliente,
    e.rua,
    e.cidade,
    e.estado
FROM
    Enderecos e
INNER JOIN
    Clientes c ON e.id_cliente = c.id_cliente -- Junta Enderecos com Clientes
WHERE
    e.tipo_endereco = 'Entrega' -- Filtra pelo tipo de endereço
    AND (e.estado = 'SP' OR e.estado = 'RJ'); -- Filtra por estados SP ou RJ


/*
 * Consulta 9: Obter uma lista de todos os nomes de Clientes e todos os nomes de Categorias
 * Uso: UNION ALL
 */
SELECT nome, 'Cliente' AS Tipo -- Seleciona nomes de clientes e atribui o tipo 'Cliente'
FROM Clientes
UNION ALL -- Combina o resultado com a próxima consulta, mantendo duplicatas se existirem
SELECT nome, 'Categoria' AS Tipo -- Seleciona nomes de categorias e atribui o tipo 'Categoria'
FROM Categorias
ORDER BY Tipo, nome; -- Ordena primeiro pelo tipo (Cliente/Categoria) e depois pelo nome


/*
 * Consulta 10: Detalhar os itens de um pedido específico
 * Uso: Múltiplas INNER JOIN
 */
SELECT
    p.id_pedido,
    p.data_pedido,
    c.nome AS Nome_Cliente,
    pr.nome AS Nome_Produto,
    ip.quantidade,
    ip.preco_unitario,
    (ip.quantidade * ip.preco_unitario) AS Subtotal_Item -- Calcula o subtotal do item
FROM
    Pedidos p
INNER JOIN
    Clientes c ON p.id_cliente = c.id_cliente -- Junta Pedidos e Clientes
INNER JOIN
    Itens_Pedido ip ON p.id_pedido = ip.id_pedido -- Junta Pedidos e Itens_Pedido
INNER JOIN
    Produtos pr ON ip.id_produto = pr.id_produto -- Junta Itens_Pedido e Produtos
WHERE
    p.id_pedido = 10 -- Filtra por um ID de pedido específico
ORDER BY
    pr.nome;