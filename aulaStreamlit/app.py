import streamlit as st
import pandas as pd

st.title("Compre brownie")

st.subheader("Brownies da melhor qualidade")

st.write("R$5,00 cada")

brownie = st.text_input("Você quer comprar quantos brownies")

st.write("Confirme", brownie, "brownies")

df = pd.DataFrame({'disciplina': ["Python", "Matemática", "Português"], 'nota': [10, 5, 0]})

df

st.write("Compre brownie e melhore suas notas")