import streamlit as st
import pandas as pd
import plotly.express as px

#Setando o layout para cobrir toda a página
st.set_page_config(layout="wide")

st.header("Dashboard")

uploadArquivo = st.file_uploader(label="Escolha um arquivo .csv", type='csv')

if (uploadArquivo != None):

    #Lendo o arquivo .csv da tabela principal com todos os dados a serem tratados
    tabelaGeral = pd.read_csv(uploadArquivo, sep=";" )

    #Tirando as colunas vazias para a tabela de download
    tabelaG_semVazios = tabelaGeral.dropna(axis='columns')

    #Lendo o arquivo .csv da tabela com os motivos do cancelamento
    motivosTabela = pd.read_csv("motivosCancelamento.csv", sep=";" )

    #Variáveis para armazenar a quantidade de notas fiscais que foram autorizadas e que foram canceladas 
    autorizados = 0
    cancelados = 0

    for situacaoNota in tabelaGeral['Situação']:
        if (situacaoNota == 'Cancelado'):
            cancelados += 1
        elif (situacaoNota == 'Autorizado'):
            autorizados += 1

    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Notas Fiscais", autorizados + cancelados)
    col2.metric("Notas Autorizadas", autorizados)
    col3.metric("Notas Canceladas", cancelados)

    #print(cancelados, autorizados)

    #Dicionário que armazena as notas que foram canceladas e os respectivos motivos
    notasCanceladas = {
        "Nota": [],
        "Motivo do Cancelamento": []
    }

    #Dicionário para armazenar o total de notas em cada motivo de cancelamento
    totalMotivos = {
        "Motivo": [],
        "Total": []
    }
    for motivo in motivosTabela.itertuples():
        totalMotivos["Motivo"].append(motivo._2)
        totalMotivos["Total"].append(0)

    for linha in tabelaGeral.itertuples():
        if (linha.Situação == 'Cancelado'):
            for motivo in motivosTabela.itertuples():
                if (linha._26 == motivo.Código):
                    notasCanceladas["Nota"].append(linha.Index) #armazena o indice da nota
                    notasCanceladas["Motivo do Cancelamento"].append(motivo._2) #armazena o motivo do cancelamento

                    #armazena no dicionário de totais para o gráfico de pizza
                    if (motivo.Código == 1): totalMotivos["Total"][0] += 1
                    if (motivo.Código == 2): totalMotivos["Total"][1] += 1
                    if (motivo.Código == 3): totalMotivos["Total"][2] += 1
                    if (motivo.Código == 4): totalMotivos["Total"][3] += 1
                    if (motivo.Código == 5): totalMotivos["Total"][4] += 1
                    if (motivo.Código == 6): totalMotivos["Total"][5] += 1


    #Tabela que relaciona os índeces das notas canceladas com os motivos
    dfCancel = pd.DataFrame(notasCanceladas)
    dfMotivos = pd.DataFrame(totalMotivos)

    #grafico = px.bar(dfCancel, x="Notas", y="Motivos")
    graficoPizza = px.pie(dfMotivos, values="Total", names="Motivo", title="Quantidade de notas canceladas por motivo", )

    col4, col5 = st.columns(2)

    with col4:

        st.write("")
        st.write("")
        st.subheader('Informações da NF-e Cancelada', )

        indiceNota = st.selectbox(label="Selecione uma NF-e", options=notasCanceladas["Nota"]) #Caixa de seleção para escolha da nota
        notaSelecionada = tabelaGeral.iloc[[indiceNota]] #A nota selecionada pelo usuário é selecionada da tabela geral

        #Exibindo as informações
        st.write(':blue-background[Dados da NF-e: ]', notaSelecionada.dropna(axis='columns'))
        st.write(':blue-background[Motivo do Cancelamento: ]', notasCanceladas["Motivo do Cancelamento"].__getitem__(notasCanceladas["Nota"].index(indiceNota)))



    col5.plotly_chart(graficoPizza)
