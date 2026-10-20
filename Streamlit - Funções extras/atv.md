O código abaixo fornece um dashboard de vendas.
Além das funções que vocês já conhecem, aqui temos a:
session_state (Dicionário nativo do Streamlit para manter dados persistentes entre interações e recarregamentos de página 
(re-runs). No código, st.session_state.carrinho é usado para armazenar a lista de produtos sem perder os dados quando o usuário clica em botões ou altera campos.) 

o rerun (Força o Streamlit a recarregar o script inteiro imediatamente. Usado no código para atualizar a interface logo após limpar o carrinho ou finalizar uma venda.),  

as notificações:
 st.success(...): Exibe uma caixa de mensagem verde para indicar sucesso (ex.: produto adicionado, pagamento concluído).st.info(...): Exibe uma caixa azul de informação/instrução (ex.: "carrinho vazio", "aguardando pagamento").
st.warning(...): Exibe uma caixa amarela de alerta/aviso (ex.: carrinho vazio no momento do pagamento).
st.error(...): Exibe uma caixa vermelha de erro (ex.: valor entregue é insuficiente).

Os forms:
st.form(...) / with st.form(...)
Cria um formulário que agrupa campos de entrada. Impede que o script recarregue a cada alteração individual de valor nos inputs — a execução do script só ocorre ao clicar no botão de submissão do formulário.
st.form_submit_button(...)
Cria o botão específico de envio do formulário (st.form). Retorna True quando é clicado.
use_container_width=True: Faz o botão se estender para preencher toda a largura da coluna/container.

Em anexo, mais detalhes

O que você vai fazer?

Criar um dashboard de vendas de carro.


Se inspire no código abaixo
-------------------------------------------------------------



import streamlit as st
import pandas as pd

st.set_page_config(page_title="Caixa de Supermercado", page_icon="---", layout="wide")


CATALOGO = {
    "Arroz 5kg": {"categoria": "Mercearia", "preco": 26.90},
    "Feijão Carioca 1kg": {"categoria": "Mercearia", "preco": 7.50},
    "Leite Integral 1L": {"categoria": "Laticínios", "preco": 4.80},
    "Café Moído 500g": {"categoria": "Mercearia", "preco": 18.90},
    "Óleo de Soja 900ml": {"categoria": "Mercearia", "preco": 6.20},
    "Maçã Fuji (kg)": {"categoria": "Hortifrúti", "preco": 8.90},
    "Pão de Forma": {"categoria": "Padaria", "preco": 7.20},
    "Detergente Líquido": {"categoria": "Limpeza", "preco": 2.50},
}
if "carrinho" not in st.session_state:
    st.session_state.carrinho = []

# -----------------------------------------------------------------------------

st.title(" Dashboard de Supermercado - Ponto de Venda")
st.markdown("---")

col1, col2 = st.columns([1, 1], gap="large")


with col1:
    st.subheader("Seleção de Produtos")
   
    # Form de adição de item
    with st.form("form_item", clear_on_submit=False):
        produto_nome = st.selectbox("Escolha o Produto", list(CATALOGO.keys()))
        preco_unit = CATALOGO[produto_nome]["preco"]
        st.caption(f"Preço Unitário: **R$ {preco_unit:.2f}**")
       
        quantidade = st.number_input("Quantidade", min_value=1, value=1, step=1)
       
        btn_adicionar = st.form_submit_button("Adicionar ao Carrinho", use_container_width=True)
       
        if btn_adicionar:
            subtotal = preco_unit * quantidade
            st.session_state.carrinho.append({
                "Produto": produto_nome,
                "Preço Unit. (R$)": preco_unit,
                "Qtd": quantidade,
                "Subtotal (R$)": subtotal
            })
            st.success(f"**{produto_nome}** adicionado com sucesso!")

    # Exibe o carrinho atual
    st.subheader("Carrinho de Compras")
    if st.session_state.carrinho:
        df_carrinho = pd.DataFrame(st.session_state.carrinho)
       
        st.dataframe(
            df_carrinho,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Preço Unit. (R$)": st.column_config.NumberColumn(
                    "Preço Unit.",
                    format="R$ %.2f"
                ),
                "Subtotal (R$)": st.column_config.NumberColumn(
                    "Subtotal",
                    format="R$ %.2f"
                )
            }
        )
       
        if st.button("Limpar Carrinho", use_container_width=True):
            st.session_state.carrinho = []
            st.rerun()
    else:
        st.info("O carrinho está vazio. Adicione itens acima.")


with col2:
    st.subheader(" Pagamento e Fechamento")
   
    # Cálculo do total acumulado
    total_compra = sum(item["Subtotal (R$)"] for item in st.session_state.carrinho)
   
    # Cartão com o Total da Compra
    st.metric(label="TOTAL DA COMPRA", value=f"R$ {total_compra:.2f}")
   
    st.markdown("---")
   
    # Entrada de dinheiro
    valor_recebido = st.number_input(
        "Dinheiro Entregue pelo Cliente (R$)",
        min_value=0.0,
        value=0.0,
        step=5.0,
        format="%.2f"
    )
   
    # Validação e Cálculo de Troco
    if total_compra == 0:
        st.warning("Adicione produtos ao carrinho antes de prosseguir com o pagamento.")
    else:
        troco = valor_recebido - total_compra
       
        if valor_recebido == 0:
            st.info("Aguardando o recebimento do dinheiro...")
        elif valor_recebido < total_compra:
            falta = total_compra - valor_recebido
            st.error(f"**Dinheiro Insuficiente!** Faltam **R$ {falta:.2f}** para concluir a venda.")
        else:
            st.success(f" **Pagamento Concluído!**")
            st.metric(label="TROCO A DEVOLVER", value=f"R$ {troco:.2f}")
           
            # Resumo da Venda
            with st.expander("Ver Comprovante da Venda"):
                st.write(f"**Itens Comprados:** {len(st.session_state.carrinho)}")
                st.write(f"**Total:** R$ {total_compra:.2f}")
                st.write(f"**Pago em Dinheiro:** R$ {valor_recebido:.2f}")
                st.write(f"**Troco:** R$ {troco:.2f}")
           
            if st.button("Finalizar Atendimento e Novo Cliente", type="primary", use_container_width=True):
                st.session_state.carrinho = []
                st.rerun()