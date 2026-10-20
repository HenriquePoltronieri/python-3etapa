import streamlit as st
import pandas as pd

st.set_page_config(page_title="Concessionária - Vendas de Carros", page_icon="🚗", layout="wide")

# -----------------------------------------------------------------------------
# Catálogo de veículos
CATALOGO = {
    "Fiat Argo Drive 1.3": {"categoria": "Hatch", "ano": 2024, "preco": 89900.00, "estoque": 5},
    "Chevrolet Onix Plus LT 1.0": {"categoria": "Sedã", "ano": 2025, "preco": 112990.00, "estoque": 4},
    "Volkswagen Polo Comfortline 1.0": {"categoria": "Hatch", "ano": 2024, "preco": 105490.00, "estoque": 3},
    "Hyundai HB20 Comfort 1.0": {"categoria": "Hatch", "ano": 2025, "preco": 99990.00, "estoque": 6},
    "Toyota Corolla XEi 2.0": {"categoria": "Sedã", "ano": 2025, "preco": 169990.00, "estoque": 2},
    "Jeep Compass Sport 2.0": {"categoria": "SUV", "ano": 2024, "preco": 189990.00, "estoque": 2},
    "Honda HR-V EXL 1.5 Turbo": {"categoria": "SUV", "ano": 2025, "preco": 199900.00, "estoque": 3},
    "Ford Ranger XLS 3.2": {"categoria": "Picape", "ano": 2024, "preco": 239900.00, "estoque": 1},
    "Volkswagen T-Cross Comfortline 1.0": {"categoria": "SUV", "ano": 2025, "preco": 149990.00, "estoque": 4},
    "Renault Kwid Zen 1.0": {"categoria": "Hatch", "ano": 2024, "preco": 72990.00, "estoque": 7},
}

# Acessórios / serviços que podem ser incluídos na venda
ACESSORIOS = {
    "Nenhum": 0.00,
    "Kit de Pisos em Borracha": 450.00,
    "Película Solar Premium": 1200.00,
    "Central de Multimídia com GPS": 3500.00,
    "Bancos em Couro": 4200.00,
    "Protectora de Pintura (PPF)": 6900.00,
    "Seguro Total 1º Ano": 5400.00,
}

FORMAS_PAGAMENTO = ["À Vista (PIX/Transferência)", "Financiamento Banco", "Cartão de Crédito (até 12x)"]

# -----------------------------------------------------------------------------
# Estado persistente entre reruns
if "carrinho" not in st.session_state:
    st.session_state.carrinho = []

if "vendas" not in st.session_state:
    st.session_state.vendas = []

st.title("Dashboard de Vendas - Concessionária")
st.markdown("---")

col1, col2 = st.columns([1, 1], gap="large")


# -----------------------------------------------------------------------------
# Coluna 1: seleção de veículos e carrinho
with col1:
    st.subheader("Seleção de Veículos")

    with st.form("form_veiculo", clear_on_submit=False):
        veiculo_nome = st.selectbox("Escolha o Veículo", list(CATALOGO.keys()))
        veiculo = CATALOGO[veiculo_nome]

        c1, c2 = st.columns(2)
        with c1:
            st.caption(f"Categoria: **{veiculo['categoria']}**")
            st.caption(f"Ano: **{veiculo['ano']}**")
        with c2:
            st.caption(f"Preço Unit.: **R$ {veiculo['preco']:,.2f}**".replace(",", "X").replace(".", ",").replace("X", "."))
            st.caption(f"Estoque: **{veiculo['estoque']} un.**")

        col_qtd, col_desc = st.columns(2)
        with col_qtd:
            quantidade = st.number_input("Quantidade", min_value=1, max_value=veiculo["estoque"], value=1, step=1)
        with col_desc:
            desconto = st.number_input(
                "Desconto (%)",
                min_value=0.0, max_value=20.0, value=0.0, step=0.5,
                help="Desconto comercial concedido pela concessionária (máx. 20%)."
            )

        acessorio = st.selectbox("Acessório / Serviço", list(ACESSORIOS.keys()))

        forma_pagamento = st.selectbox("Forma de Pagamento", FORMAS_PAGAMENTO)

        btn_adicionar = st.form_submit_button("Adicionar ao Carrinho", use_container_width=True)

        if btn_adicionar:
            preco_final = veiculo["preco"] * (1 - desconto / 100)
            preco_acessorio = ACESSORIOS[acessorio]
            subtotal = (preco_final + preco_acessorio) * quantidade

            st.session_state.carrinho.append({
                "Veículo": veiculo_nome,
                "Categoria": veiculo["categoria"],
                "Ano": veiculo["ano"],
                "Qtd": quantidade,
                "Preço Unit. (R$)": round(preco_final, 2),
                "Acessório": acessorio,
                "Pagamento": forma_pagamento,
                "Subtotal (R$)": round(subtotal, 2),
            })
            st.success(f"**{veiculo_nome}** adicionado com sucesso ao carrinho!")

    # Carrinho atual
    st.subheader("Carrinho de Vendas")
    if st.session_state.carrinho:
        df_carrinho = pd.DataFrame(st.session_state.carrinho)

        st.dataframe(
            df_carrinho,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Preço Unit. (R$)": st.column_config.NumberColumn("Preço Unit.", format="R$ %.2f"),
                "Subtotal (R$)": st.column_config.NumberColumn("Subtotal", format="R$ %.2f"),
                "Qtd": st.column_config.NumberColumn("Qtd", format="%d"),
            },
        )

        c1, c2 = st.columns(2)
        with c1:
            if st.button("Limpar Carrinho", use_container_width=True):
                st.session_state.carrinho = []
                st.rerun()
        with c2:
            if st.button("Remover Último Item", use_container_width=True):
                st.session_state.carrinho.pop()
                st.warning("Último item removido do carrinho.")
                st.rerun()
    else:
        st.info("O carrinho está vazio. Selecione um veículo acima para iniciar a venda.")

    # Vendas já finalizadas
    if st.session_state.vendas:
        st.subheader("Histórico de Vendas do Dia")
        df_vendas = pd.DataFrame(st.session_state.vendas)
        st.dataframe(
            df_vendas,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Valor Total (R$)": st.column_config.NumberColumn("Valor Total", format="R$ %.2f"),
            },
        )
        st.metric(label="TOTAL FATURADO", value=f"R$ {df_vendas['Valor Total (R$)'].sum():.2f}")


# -----------------------------------------------------------------------------
# Coluna 2: pagamento e fechamento
with col2:
    st.subheader("Pagamento e Fechamento")

    total_compra = sum(item["Subtotal (R$)"] for item in st.session_state.carrinho)
    total_qtd = sum(item["Qtd"] for item in st.session_state.carrinho)

    mc1, mc2, mc3 = st.columns(3)
    with mc1:
        st.metric(label="TOTAL DA VENDA", value=f"R$ {total_compra:.2f}")
    with mc2:
        st.metric(label="VEÍCULOS", value=total_qtd)
    with mc3:
        st.metric(label="ITENS NO CARRINHO", value=len(st.session_state.carrinho))

    st.markdown("---")

    # Agrupa as formas de pagamento presentes no carrinho
    pagamentos_carrinho = sorted({item["Pagamento"] for item in st.session_state.carrinho})

    with st.form("form_pagamento"):
        st.caption(f"Forma(ões) de pagamento do carrinho: **{', '.join(pagamentos_carrinho) if pagamentos_carrinho else '-'}**")
        valor_recebido = st.number_input(
            "Valor Entregue pelo Cliente (R$)",
            min_value=0.0,
            value=0.0,
            step=1000.0,
            format="%.2f",
        )
        nome_cliente = st.text_input("Nome do Cliente", placeholder="Ex.: João da Silva")
        btn_pagar = st.form_submit_button("Registrar Pagamento", use_container_width=True)

    if total_compra == 0:
        st.warning("Adicione veículos ao carrinho antes de prosseguir com o pagamento.")
    elif valor_recebido == 0:
        st.info("Aguardando o recebimento do pagamento...")
    elif valor_recebido < total_compra:
        falta = total_compra - valor_recebido
        st.error(f"**Valor Insuficiente!** Faltam **R$ {falta:.2f}** para concluir a venda.")
    else:
        troco = valor_recebido - total_compra
        st.success(" **Pagamento Concluído!**")
        st.metric(label="TROCO / ACRÉSCIMO A DEVOLVER", value=f"R$ {troco:.2f}")

        with st.expander("Ver Comprovante da Venda"):
            st.write(f"**Cliente:** {nome_cliente if nome_cliente else 'Consumidor Não Identificado'}")
            st.write(f"**Veículos Comprados:** {total_qtd}")
            st.write(f"**Forma de Pagamento:** {', '.join(pagamentos_carrinho)}")
            st.write("**Itens:**")
            st.dataframe(pd.DataFrame(st.session_state.carrinho), use_container_width=True, hide_index=True)
            st.write(f"**Total:** R$ {total_compra:.2f}")
            st.write(f"**Pago:** R$ {valor_recebido:.2f}")
            st.write(f"**Troco:** R$ {troco:.2f}")

        if st.button("Finalizar Atendimento e Novo Cliente", type="primary", use_container_width=True):
            st.session_state.vendas.append({
                "Cliente": nome_cliente if nome_cliente else "Consumidor Não Identificado",
                "Veículos": total_qtd,
                "Pagamento": ", ".join(pagamentos_carrinho),
                "Valor Total (R$)": round(total_compra, 2),
            })
            st.session_state.carrinho = []
            st.success("Atendimento finalizado! Pronto para o próximo cliente.")
            st.rerun()
