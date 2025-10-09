/*quais clientes são do piauí*/
SELECT
c.nome,
c.email,
c.cpf
FROM
clientes AS c
JOIN
enderecos AS e ON c.id_cliente = e.id_cliente
WHERE
e.estado = 'PI';

/*quanto foi vendido de cada produto por categoria*/
SELECT
ca.nome AS nome_categoria,
sum(ip.quantidade * ip.preco_unitario) AS valor_total_vendas
FROM
itens_pedido AS ip
JOIN
produtos AS p ON ip.id_produto = p.id_produto
JOIN
categorias AS ca ON p.id_categoria = ca.id_categoria
GROUP BY
ca.nome;

/*quais clientes usaram cupons*/
SELECT DISTINCT
c.nome
FROM
clientes AS c
JOIN
pedidos AS pe ON c.id_cliente = pe.id_cliente
JOIN
cupons AS cu ON pe.id_cupom = cu.id_cupom;

/*produtos com preço acima de R$ 100*/
SELECT * FROM produtos
WHERE
preco > 100 AND estoque < 100;

/*pedidos feitos no mês de dezembro*/
SELECT * FROM pedidos 
WHERE
data_pedido >= '2024-12-01' AND data_pedido <= '2024-12-31';



