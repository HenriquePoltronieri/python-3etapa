python -m pip install pandas matplotlib seaborn xlrd

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

Nesta aula você junta as duas **Tabelas 5** (composição da desocupação por sexo em 2012 e 2026), compara ano a ano e cruza com a **Tabela 1.1.1** do IBGE (horas semanais de cuidados e afazeres domésticos, 2022). (AULA 2, UTILIZE ELA)

Abrir e juntar as duas Tabelas 5 e Tabela da Aula 2
Utilize o código da aula2 para tratar a tabela 1.1 (Você deve pegar apenas o estados dela)


exemplo

juntar tabelas comp = t2012.merge(t2026, on=["Sigla", "Código", "Estado"], how="inner")


FAZER O GRÁFICO UTILIZANDO O MERGE

ordem = nomedatabela.insira aqui o comando para ordernar("coluna de ordenacao")["Estado"]
longo = comp.QUAL FUNCAO DERRETE O DATAFRAME? INSIRA AQUI(
    id_vars=VARIAVEIS QUE NAO SERÃO DERRETIDAS
    value_vars=["mulheres_2012", "mulheres_2026"],
    var_name="Ano",
    value_name="Participacao_mulheres",
)
longo["Ano"] = longo["Ano"].map({"mulheres_2012": "2012 T1", "mulheres_2026": "2026 T1"})

COMANDO PARA INSTANCIAR A FIGURA, ax = plt.subplots(COMANDO PARA O TAMANHO=(10, 10))
sns.barplot(
    data=NOME DO DATAFRAME DERRETIDO,
    y="COLUNA EIXO Y",
    x="Participacao_mulheres",
    hue="COLUNA QUE TERÁ DUAS COMPARAÇÕES",
    order=ordem,
    ax=ax,
)
ax.axvline(50, color="gray", linestyle="--", linewidth=1) # MUDE A COR
ax.set_xlabel("Participação das mulheres entre as pessoas desocupadas (%)")
ax.set_ylabel("")
ax.set_title("Desocupação: participação feminina em 2012 T1 e 2026 T1")
ax.legend(title="COLOQUE UM TITULO")
fig.tight_layout()
COMANDO PARA MOSTRAR()