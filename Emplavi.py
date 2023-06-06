###BIBLIOTECAS UTILIZADAS:_________________________________________________________________
import streamlit as st
import pandas as pd 
import numpy as np 
import openpyxl, os 
import plotly.express as px 
import plotly.graph_objects as go 
from datetime import datetime
from streamlit_option_menu import option_menu
from PIL import Image
from plotly.subplots import make_subplots
import hydralit_components as hc


###PARA SUBIR BASE DE DADOS:________________________________________________________________
@st.cache_data #Irá salvar as bases de dados uma única vez no sistema interno - #para não carregar a base de dados a todo momento - diminui o custo de processamento
def DadosFerias(): #função criada para importar o arquivo
    base_ferias = pd.read_excel(r"férias jan-mar.xlsx") #Caminho da pasta
    return base_ferias #return = resultado da função

@st.cache_data
def DadosRescisao():
    base_rescisao = pd.read_excel(r"rescisões jan-mar.xlsx")
    
    
    return base_rescisao

@st.cache_data
def DadosAdmissao():
    base_admissao = pd.read_excel(r"Admissões jan-mar.xlsx")
    
    
    excluir = ["i_empregados", "situacao"] #PARA EXCLUIR DA APRESENTAÇÃO UMA DETERMINADA COLUNA
    for i in excluir:
        base_admissao.drop(columns = i, inplace= True)

    #base_admissao["salario"] = base_admissao["salario"].map("R${:,.2f}".format) #PARA ALTERAR O FORMATO DO VALOR, COLOCANDO R$
    #base_admissao.loc[:,base_admissao.columns.isin(["nome","salario"])]  #edição da tabela de admissao
    
    Ordemcorreta = ["Data", "nome", "Cargo","Contrato","Valor"] #PARA INSERIR A ORDEM DE COLUNAS DESEJADA 
    base_admissao = base_admissao[Ordemcorreta]

   # base_admissao.rename(columns={"nome_quebra": "Contrato/Serviço"}, inplace=True)
    #base_admissao.rename(columns={"nome": "Colaborador"}, inplace=True)
   # base_admissao.rename(columns={"nome_cargo": "Cargo"}, inplace=True)
    #base_admissao.rename(columns={"admissao": "Data de Contratação"}, inplace=True)
    #base_admissao.rename(columns={"salario": "Salário"}, inplace=True)
    return base_admissao

@st.cache_data
def DadosOnvio():
    base_chamados = pd.read_excel(r"Indicadores do dp jan-dez.xlsx")
    base_chamados['mes'] = base_chamados["Competencia"].dt.to_period("M").dt.strftime('%m/%Y') #PARA ALTERAR FORMATO DA DATA (MêS/Ano) 
    return base_chamados

@st.cache_data
def DadosAta():
    base_ata = pd.read_excel(r"ata mes 4.xlsx")
    base_ata["Data"] = pd.to_datetime(base_ata["Data"],format="%d/%m/%Y") #alterar o formato da data
    base_ata["Prazo para realização"]= base_ata["Data"].dt.to_period("d").dt.strftime("%d/%m/%Y")
    
    excluir = ["Data"] #PARA EXCLUIR DA APRESENTAÇÃO UMA DETERMINADA COLUNA
    for i in excluir:
        base_ata.drop(columns = i, inplace= True)

    base_ata["Solicitado em"] = pd.to_datetime(base_ata["Solicitado em"],format="%d/%m/%Y") #alterar o formato da data
    base_ata["Solicitado em:"]= base_ata["Solicitado em"].dt.to_period("d").dt.strftime("%d/%m/%Y")

    Ordemcorreta = ["Solicitado em:", "Atividade", "Responsável", "Departamento", "Prazo para realização", "Realizado?"] #PARA INSERIR A ORDEM DE COLUNAS DESEJADA 
    base_ata = base_ata[Ordemcorreta]

    return base_ata

@st.cache_data
def DadosRubricas():
    base_rubrica = pd.read_excel(r"Rubricas Utilizadas Jan-Mar.xlsx")
    base_rubrica.dropna() #para retirar as linhas em branco "ex.: null"

    #base_rubrica.loc[:,~base_rubrica.columns.isin(["Data","Tipo", "Rubricas Utilizadas","Valor"])]  #edição da tabela de admissao
    base_rubrica_remove = base_rubrica.loc[(base_rubrica["Valor"]<60000) #para excluir valores menores que 10.000
                                         ]
    base_rubrica = base_rubrica.drop(base_rubrica_remove.index) #para excluir valores menores que 10.000

    
    return base_rubrica

@st.cache_data
def DadosAtivos():
    base_ativos = pd .read_excel(r"Colab Ativos jan-mar.xlsx")
    base_ativos["Competencia"] = pd.to_datetime(base_ativos["Competencia"],format="%d/%m/%Y") #alterar o formato da data
    base_ativos["Competência"]= base_ativos["Competencia"].dt.to_period("d").dt.strftime("%d/%m/%Y")

    base_ativos["Líquido Geral"] = base_ativos["Líquido Geral"].map("R${:,.2f}".format) #PARA ALTERAR O FORMATO DO VALOR, COLOCANDO R$
    st.subheader("Colaboradores Ativos - Custo Total da Folha de Pagamento:")   
    base_ativos.loc[:,~base_ativos.columns.isin(["Competencia","Ativos"])]  #edição da tabela de admissao

    
    return base_ativos



class apresentacao():
###PARA SUBIR AS IMAGENS:_______________________________________________________________
    def __init__(self):
    
        #self.base_extratos = pd.read_excel(r"T:\CLIENTES\GRUPO H2F\CONTROLADORIA\Extratos Jan-Mar.xlsx")
        self.logoalldaxreduzida = Image.open(r"LOGO OFICIAL.png")
       # self.logoh2f = Image.open(r"LOGO OFICIAL.png")
        #self.logos = Image.open(r"LOGO OFICIAL.png")
        #self.resultadosicone = Image.open(r"resukt.png")

    

#####FUNÇÃO LEMBRETES:_____________________________________________________________________________
    def Lembretes(self):
        Prazo1 = {'bgcolor': '#EFF8F7','title_color': 'green','content_color': 'green','icon_color': 'green', 'icon': 'fa fa-check-circle'}
        Prazo2 = {'bgcolor': '#EFF8F7','title_color': 'green','content_color': 'green','icon_color': 'green', 'icon': 'fa fa-check-circle'}
        Prazo3 = {'bgcolor': '#EFF8F7','title_color': 'green','content_color': 'green','icon_color': 'green', 'icon': 'fa fa-check-circle'}
        Prazo4 = {'bgcolor': '#EFF8F7','title_color': 'green','content_color': 'green','icon_color': 'green', 'icon': 'fa fa-check-circle'}
        Prazo5 = {'bgcolor': '#EFF8F7','title_color': 'green','content_color': 'green','icon_color': 'green', 'icon': 'fa fa-check-circle'}
        #Prazo6 = {'bgcolor': '#EFF8F7','title_color': 'green','content_color': 'green','icon_color': 'green', 'icon': 'fa fa-check-circle'}


    def Atafiltros(self,departamento):
        cardatafiltro = DadosAta()
        
        if departamento == "Todos":
            pass 
        else:
            card = cardatafiltro([cardatafiltro["Departamento"]==departamento])
           
        return card

    def Ata(self,coluna,departamento):
        cardata = DadosAta()
        #print(cardata)
        #PARA INTEGRAR FILTRO DE DEPARTAMENTO A TABELA DE ATA. 
        if departamento == "Todos":
            pass 
        else:
            cardata = cardata[cardata["Departamento"]==departamento]

        Tabelaata = go.Figure(
                            data=[go.Table(
                                    header= dict(
                                                values= list(cardata.columns),
                                                font = dict( 
                                                            size = 14, color = "rgba(3,102,102,1)", family = "Arial Black, monospace"),
                                                #fill_color = "darkslatergray",
                                                line_color = "rgba(153,226,180,1)",
                                                align = ["center", "center"],
                                                height = 30
                                                ),
                                    cells = dict(
                                                values = [cardata[k].tolist() for k in cardata.columns],
                                                font = dict(size = 14, color = "black", family = "Arial, monospace"),
                                                align = ["left", "center"],
                                                #fill_color = "darkslatergray",
                                                line_color = "rgba(153,226,180,1)",
                                                #font_size = 14,
                                                #format = [".2$"],
                                                height = 30
                                                )
                            )] )
        Tabelaata.update_layout(
                                height = 800,
                                width = 1800)
        Tabelaata.update_layout(xaxis = dict(
                                            rangeslider = dict(
                                                            visible = True)))
        
        
        return coluna.plotly_chart(Tabelaata, use_container_width=True)
        
#####FUNÇÃO RÚBRICAS:_____________________________________________________________________________
    '''def cardrubricas1(self,filtrodata,filtromodelo):
        cardrubrica1 = DadosRescisao()


        if filtrodata == "Todos":
            card = cardrubrica1[cardrubrica1["Rubrica"]==filtromodelo]
            card = cardrubrica1["Valor"].sum()
            
        else: 
            card = cardrubrica1[(cardrubrica1["Rubrica"]==filtromodelo)&
                                (cardrubrica1["cp_competencia"]==filtrodata)]
            
            card = card["Valor"].sum()

            card_4 = f"R$ {card:,.0f}"
            card_4= card_4.replace(",",".")
            return card_4'''

    def cardrubrica(self,data,descrição):
        cardrubrica = DadosRubricas()

        if data == "Todos":
                card = cardrubrica[cardrubrica["Rubrica"]==descrição]
                card = card["Valor"].sum()
        else:
                card = cardrubrica[(cardrubrica["Rubrica"]==descrição)&
                                   (cardrubrica["Data"]==data)
                ]
                card = card["Valor"].sum()

        card_3 = f"R$ {card:,.0f}"
        card_3= card_3.replace(",",".")
        return card_3
    
    '''def Rubricasdafolha(self,  data, descrição,):
        cardrubricas = DadosRubricas()
        if data == "Todos":
            if descrição == "Todos":
                
                card = cardrubricas[cardrubricas["Rubrica"]==descrição]
                card = cardrubricas[cardrubricas["Data"]== data]
                card = cardrubricas["Valor"].sum()
            else:
                
                card = cardrubricas[cardrubricas["Rubrica"]==descrição]
                card = cardrubricas["Valor"].sum()
            print(card)
        else:
            
                card = cardrubricas[cardrubricas["Data"]== data]
                card = cardrubricas["Valor"].sum()
           
                cardrubricas = cardrubricas[
                                            (cardrubricas["Data"]==data)&
                                            (cardrubricas["Rubrica"]==descrição)]
                card = cardrubricas["Valor"].sum()'''

        
    ''' if filtromodelo == "Todos":
            if filtrodata == "Todos":
                card = cardrubricas.groupby(["Valor"]).sum().reset_index()
            else: 
                card = cardrubricas([cardrubricas["Data"]==filtrodata])
                card = cardrubricas.groupby(["Valor"]).sum().reset_index()
        else: 
            if filtrodata == "Todos":
                card = cardrubricas[(cardrubricas["Rubrica"] == filtromodelo)]
                card = card.groupby(["Valor"]).sum().reset_index()
            else: 
                card = cardrubricas[(cardrubricas["Rubrica"]== filtromodelo)&
                                    (cardrubricas["Data"]==filtrodata)]
                card = card.groupby(["Valor"]).sum().reset_index()
        if filtrorubrica == "Todos":
            pass
        else:
            if filtrorubrica == "Proventos":
                A = "P"
            else:
                A = "D"
            cardrubricas = cardrubricas[cardrubricas["cp2_prov_desc"]==A]'''
           
    def tabelarubrica (self, coluna,filtrorubrica,filtrodatarubrica):
        cardrubricas = DadosRubricas()

        cardrubricas["Valor"] = cardrubricas["Valor"].map("R${:,.2%}".format) #PARA ALTERAR O FORMATO DO VALOR, COLOCANDO R$
        
        
      
        '''cardrubricas.rename(columns={'cp_competencia': 'Data'}, inplace = True)
        cardrubricas.rename(columns={'cp2_prov_desc': 'Tipo'}, inplace = True)
        cardrubricas.rename(columns={'cp3_nome_evento': 'Rubricas Utilizadas'}, iNplace = True)
        cardrubricas.rename(columns={'cp3_valor_calc': 'Valor'}, inplace = True)'''
        
        tabelarubrica = go.Figure(
                                data = [go.Table(
                                                columnorder = [1,2],
                                                columnwidth = [80,400],
                                                header = dict(
                                                            vlaues = [['Valor']],
                                                line_color = "rgba(0,146,122,1)",
                                                fill_color = "rgba(0,146,122,1)",
                                                align =["left","center"],
                                                font = dict(
                                                            color = "black", size = 12),
                                                            height = 40 ),
                                                cells = dict(
                                                            values = 'Valor',
                                                            line_color='darkslategray',
                                                            fill=dict(color=['paleturquoise', 'white']),
                                                            align=['left', 'center'],
                                                            font_size=12,
                                                            height=30)
                                                )])
   
    def Graficonovo(self, coluna, colunadodataframe, orientação, titulodografico,filtrodata ):
        cardrubrica = DadosRubricas()
        card = cardrubrica

        if filtrodata == "Todos":
            card = cardrubrica.groupby([colunadodataframe]).sum("Valor").reset_index()
        else: 
            card = cardrubrica[cardrubrica["Data"]==filtrodata]
            card = card.groupby([colunadodataframe]).sum("Valor").reset_index()
            
        '''graficorubrica1 = go.Figure()
        graficorubrica1.add_trace(go.Bar(
                                        x = card["Valor"],
                                        y = card[colunadodataframe],
                                        marker = dict(
                                                    color = "rgba(0,146,122,1)",
                                                    line = dict(
                                                                color = "rgba(0,146,122,0)",
                                                                width = 1),),
                                        name = "graficorubrica1",
                                        text = (card["Valor"].map("R${:,.0f}".format)).str.replace(",","."),
                                        orientation = orientação))
        graficorubrica1.update_layout(
                                        autosize = False,
                                        width = 400,
                                        height = 700,
                                        barmode = "stack",
                                        yaxis = {"categoryorder":"total ascending"},
                                        title = {"text": titulodografico,
                                                 "y": 1,"x": 0.5,
                                                 "yanchor": "top",
                                                 "xanchor": "center"},
                                        font = dict(size = 12,
                                                    family = "Arial Black, monospace",
                                                    color = "rgba(0,0,0,1)"))
        
        graficorubrica1.update_traces(textposition = "auto")'''

        Graficonovo = go.Figure()
        Graficonovo.add_trace(go.Bar(
                                    x = card["Valor"],
                                    y = card[colunadodataframe],
                                    marker = dict(
                                                    color = "rgba(0,146,122,1)",
                                                    line = dict(
                                                                color = "rgba(0,146,122,0)",
                                                                width =1),),
                                    name = "graficoderubrica",
                                    text = (card["Valor"].map("R${:,.0f}".format)).str.replace(",","."),
                                    orientation = orientação
                                    ))
        Graficonovo.update_layout(
                                autosize = False,
                                width = 200,
                                height = 600,
                                barmode = "stack",
                                yaxis = {"categoryorder":"total ascending"},
                                title = {"text": titulodografico,
                                         "y":1, "x":0.5,
                                         'yanchor':"top",
                                         "xanchor": "center"},
                                font = dict(size = 15,
                                            family = "Arial Black, monospace",
                                            color = "rgba(0,0,0,1)"))
        Graficonovo.update_traces(textposition = "auto")
        
        return coluna.plotly_chart(Graficonovo,use_container_width = True)

#####FUNÇÃO FÉRIAS:_____________________________________________________________________________
    ###PARA CRIAÇÃO DE CARD VALOR TOTAL - FÉRIAS:_______________________________________________________________
    def Ferias(self,filtroserviço,filtrocentrodecusto): #todo parametro apos isto deve aparecer sempre que a função for chamada
        cardferias = DadosFerias() #cardferias é o nome dado ao dataframe do banco de dados férias(dadosferias)
    
        ###1° PARTE - CRIAÇÃO DE PARÂMETRO PARA FILTRO:_________________________________
        if filtrocentrodecusto == "Todos": #se o filtro de centro de custos estiver selecionado em "TODOS" 
            if filtroserviço == "Todos": # se o filtro de serviços estiver estiver selecionado em "TODOS"  
                card = cardferias["value"].sum() # ("card" dataframe para filtro) irá filtrar somente filtroserviços e somar toda a coluna "value" da base de dados de ferias

        ###2° PARTE - CRIAÇÃO DE PARÂMETRO PARA FILTRO:_________________________________
            else: #se for contrária a opção de filtro serviços acima ele irá executar a opção abaixo - se o filtro serviços não estiver com a opção "TODOS" selecionada
                card_v = cardferias[cardferias["sq_nome_servico"]==filtroserviço] #...ele irá filtrar a coluna de serviços de acordo com o filtro centro de custo (card_v é um novo data frame para o filtro) 
                card = card_v["value"].sum() #e somar somente a coluna "value" da base de dados de ferias

        ###3° PARTE - CRIAÇÃO DE PARÂMETRO PARA FILTRO:_________________________________       
        else: #se a opção de filtro centro de custo (linha 41) não estiver selecionado em "TODOS"...
            if filtroserviço == "Todos": 
                card_v = cardferias[cardferias["sq_nome_ccustos"]==filtrocentrodecusto] ##...ele irá filtrar a coluna de centro de custo de acordo com o filtro serviço (card_v é um novo data frame para o filtro) 
                card = card_v["value"].sum() #e somar somente a coluna "value" da base de dados de ferias

        ###4° PARTE - CRIAÇÃO DE PARÂMETRO PARA FILTRO:_________________________________   
            else: #se a opção de filtro centro de custo e filtro serviços estiverem divergentes de "Todos"...
                card_v = cardferias[ #ele irá filtrar as opções em um e em outro e...
                     (cardferias["sq_nome_ccustos"]==filtrocentrodecusto) &
                                        (cardferias["sq_nome_servico"]==filtroserviço)]
                card = card_v["value"].sum() #somar a coluna "value" da base de dados de férias
        
        card_1 = f"R$ {card:,.0f}" #criação da variavel "card_1" para trazer o 0 para as casas decimais, transformando em um string
        card_1 = card_1.replace(",",".") #trocar virgula por ponto
        return card_1 #resultado da função
        
    
    ###PARA CRIAÇÃO DE CARD DESCONTOS - FÉRIAS:_______________________________________________________________
    def Ferias2(self, tipo, filtro_mêsferias,): #novo nome para a função do card de descontos - foi definido o termo "tipo" para facilitar no preenchimento 
        cardferias = DadosFerias() #data frame anterior
        if filtro_mêsferias == "Todos": # se o (nome do filtro para o mês) estiver selecionado em "todos"
            card = cardferias[cardferias["variable"]==tipo] #ele irá executar este código, filtrando somente a coluna variável
          
        else: #se não for "todos"
            card= cardferias[(cardferias["variable"]==tipo)& #irá filtrar a coluna variável puxando o "tipo" que posteriormente será informada a informação desejada
                             (cardferias["sq_dataini"]==filtro_mêsferias) #... e filtrando a coluna "data" 
                            ]
        
        card = card["value"].sum()

        card_1 = f"R$ {card:,.0f}" #criação da variavel "card_1" para trazer o 0 para as casas decimais, transformando em um string
        card_1 = card_1.replace(",",".") #trocar virgula por ponto
        return card_1 #resultado da função
 
    ###PARA CRIAÇÃO DE CARD PROVENTOS - FÉRIAS:_______________________________________________________________
    def Ferias3(self, tipo1, filtro_mêsferias,):
        cardferias = DadosFerias()
        if filtro_mêsferias == "Todos":
            card = cardferias[cardferias["variable"]==tipo1]
          
        else: 
            card= cardferias[(cardferias["variable"]==tipo1)&
                             (cardferias["sq_dataini"]==filtro_mêsferias)
                            ]
        
        card = card["value"].sum()

        card_1 = f"R$ {card:,.0f}" #criação da variavel "card_1" para trazer o 0 para as casas decimais, transformando em um string
        card_1 = card_1.replace(",",".") #trocar virgula por ponto
        return card_1 #resultado da função
        

### PARA FORMATAR O R$ NOS CARDS:____________________________________________________________
        card_1 = f"R$ {card:,.0f}" #criação da variavel "card_1" para trazer o 0 para as casas decimais, transformando em um string
        card_1 = card_1.replace(",",".") #trocar virgula por ponto
        return card_1 #resultado da função
        

    ###PARA O PRIMEIRO GRÁFICO DE FÉRIAS - EVOLUÇÃO MENSAL:_______________________________________________________________        
    def Graficoevolucaomensalferias(self,coluna,colunadodataframe,orientação, titulodografico,filtroservicoferias, filtrocentrodecustoferias):
        cardferias = DadosFerias()

        if filtroservicoferias == "Todos":
            if filtrocentrodecustoferias == "Todos":
                pass
            else: 
                cardferias = cardferias[cardferias["sq_nome_ccustos"]==filtrocentrodecustoferias]
        else:
            cardferias = cardferias[cardferias["sq_nome_servico"]==filtroservicoferias]

        cardferias = cardferias[["nome","sq_dataini","value"]]
        card= cardferias.drop_duplicates(subset=["nome","sq_dataini"], 
                                    inplace=True)
        card = cardferias.groupby([colunadodataframe]).count().reset_index()
 #       print(card2)
    

        graficoevolucaomensalferias = go.Figure()
        ###1° ETAPA: CRIAÇÃO DO GRÁFICO DE BARRAS - POR PARTES:
        graficoevolucaomensalferias.add_trace(go.Bar(  
                                        x = card[colunadodataframe],
                                        y = card["value"],
                                        marker = dict(
                                                    color = "rgba(0,146,122,1)",
                                                    line = dict(
                                                                color = "rgba(0,146,122,0)",
                                                                width = 1),),
                                        name = "Graficoferias2",
                                        text=card["nome"],#.map("R$ {:,.0f}".format)).str.replace(",","."),
                                        orientation= orientação  ))
        ###2° ETAPA: EDIÇÃO DO LAYOUT DO GRÁFICO DE BARRAS - POR PARTES:
        graficoevolucaomensalferias.update_layout(
                                                autosize= False,
                                                width = 100,
                                                height = 400,
                                                barmode = 'stack',
                                                yaxis = {'categoryorder':'total ascending'},
                                                title = {"text": titulodografico, 
                                                         'y':1, 'x':0.5,
                                                         'yanchor':'top',
                                                         'xanchor': 'center'}, 
                                                font = dict(size = 15,
                                                            family= 'Arial Black, monospace',
                                                            color = 'rgba(0,0,0,1)')
        )
        ###3° ETAPA: EDIÇÃO DA POSIÇÃO DO RÓTULO EM RELAÇÃO A BARRA:
        graficoevolucaomensalferias.update_traces(textposition='inside')
        ###ETAPA FINAL - CHAMADOR DA FUNÇÃO:
        return coluna.plotly_chart(graficoevolucaomensalferias, use_container_width = True)

    ###PARA O SEGUNDO GRÁFICO DE FÉRIAS - SERVIÇOS:_______________________________________________________________
    def Graficoserviço_ferias(self, coluna, colunadodataframe,orientação,titulodografico,filtro_mêsferias): #filtroserviço, filtrocentrodecusto(caso vá integrar dos filtros) - os nomes são colocados junto ao "self" para facilitar na hora de chamar a função
        cardferias = DadosFerias() #cardferias é o nome dado ao dataframe do banco de dados férias(dadosferias)
        
      
        if filtro_mêsferias=="Todos":
            card = cardferias.groupby([colunadodataframe]).sum("value").reset_index() #("card" dataframe para filtro), ".groupby" é o nome da função para unir coluna, "colunadodataframe" é o nome dado a coluna que será puxada pelo gráfico, ".sum" para somar a coluna de valor, ".reset_index()" retirada de uma coluna de referência para que ela possa ser utilizada como índice
        else: 
            card = cardferias[cardferias["sq_dataini"]==filtro_mêsferias]
            card = card.groupby([colunadodataframe]).sum("value").reset_index() #("card" dataframe para filtro), ".groupby" é o nome da função para unir coluna, "colunadodataframe" é o nome dado a coluna que será puxada pelo gráfico, ".sum" para somar a coluna de valor, ".reset_index()" retirada de uma coluna de referência para que ela possa ser utilizada como índice
            
    #PARA INTEGRAR O GRÁFICO AO FILTRO: (não utilizado nesta parte do código)
        """if filtrocentrodecusto == "Todos": #se o filtro de centro de custos estiver em TODOS
            if filtroserviço == "Todos": #e se o filtro de serviços também estiver em TODOS
                #card = 2
                card = cardferias.groupby(["sq_nome_ccustos" #colunas que serão mantidas 
                                           pd.Grouper(key="sq_dataini",freq="M",axis= 0)]  
                                          ] ).sum("value").reset_index()
                
            else: #se não for a opção de cima ele irá puxar a opção abaixo - se o filtro serviços for diferente de TODOS
                card = cardferias.groupby(["sq_nome_ccustos"
                                             ]).sum("value").reset_index() #card_v é uma outra opção, ou seja, um novo data frame - ele irá filtrar a coluna de serviços 
        else:
            if filtrocentrodecusto == "Todos":
                card = cardferias.groupby(["sq_nome_ccustos"
                                           ]).sum("value").reset_index()
                
            else: 
                card = cardferias.groupby(["sq_nome_ccustos"]) .sum("value").reset_index()"""

        graficoferias1 = go.Figure()  #inicar o gráfico
        ###1° ETAPA: CRIAÇÃO DO GRÁFICO DE BARRAS - POR PARTES:
        graficoferias1.add_trace(go.Bar(  #utilizar o tipo de gráfico "go.bar" da biblioteca plotly
                                        x= card["value"], #eixo x (reto/deitado)
                                        y= card[colunadodataframe], #eixo y (reto/em pé)
                                        marker=dict(
                                                    color = "rgba(0,146,122,1)",
                                                    line = dict(
                                                                color = "rgba(0,146,122,0)",
                                                                width =1),),
                                        name="graficoferias1",
                                        text=(card["value"].map("R$ {:,.0f}".format)).str.replace(",","."),
                                        orientation= orientação)) #essa orientação será colocada no chamador da função
        ###2° ETAPA: EDIÇÃO DO LAYOUT DO GRÁFICO DE BARRAS - POR PARTES:
        graficoferias1.update_layout( #Parte gráfica, título, tamanho do grafico, etc
                                   autosize = False,
                                    width = 200, #largura do gráfico
                                    height = 600, #altura do gráfico
                                    barmode = 'stack',
                                    yaxis = {"categoryorder":"total ascending"},
                                    title = {"text": titulodografico,                                       
                                             "y":1, "x":0.5,
                                             "yanchor":"top",
                                             "xanchor":"center"},
                                    font = dict(size = 15, #tamanho e fonte utilizada nos rótulos
                                            family= "Arial Black, monospace",
                                            color = "rgba(0,0,0,1)")
                                   #xaxis_tickformat = "1%"
                                    )
        ###3° ETAPA: EDIÇÃO DA POSIÇÃO DO RÓTULO EM RELAÇÃO A BARRA:
        graficoferias1.update_traces(textposition='auto') #posição do rótulo em relação a barra - podendo ser: "outside" fora da barra, "inside" dentro da barrada ou "auto" ajuste automático
        
        ###ETAPA FINAL - CHAMADOR DA FUNÇÃO:
        return coluna.plotly_chart(graficoferias1, use_container_width = True) #retorno da base
    
    ###PARA O TERCEIRO GRÁFICO DE FÉRIAS - CENTRO DE CUSTO:_______________________________________________________________
    def Graficocentrodecusto_ferias(self, coluna, colunadodataframe,orientação,titulodografico,filtro_mêsferias): #filtroserviço, filtrocentrodecusto(caso vá integrar dos filtros) - os nomes são colocados junto ao "self" para facilitar na hora de chamar a função
        cardferias = DadosFerias() #cardferias é o nome dado ao df do banco de dados de ferias
        if filtro_mêsferias == "Todos":
            card = cardferias.groupby([colunadodataframe]).sum("value").reset_index() #("card" dataframe para filtro), ".groupby" é o nome da função para unir coluna, "colunadodataframe" é o nome dado a coluna que será puxada pelo gráfico, ".sum" para somar a coluna de valor, ".reset_index()" retirada de uma coluna de referência para que ela possa ser utilizada como índice
            #print(card)
        else:
            card = cardferias[cardferias["sq_dataini"]==filtro_mêsferias]
            card = card.groupby([colunadodataframe]).sum("value").reset_index()

        graficoferias1 = go.Figure() #iniciar o gráfico
        ###1° ETAPA: CRIAÇÃO DO GRÁFICO DE BARRAS - POR PARTES: 
        #obs: para gráficos verticais o x e y devem sem invertidos sendo o dataframe primeiro
        graficoferias1.add_trace(go.Bar( #utilizar o tipo de gráfico "go.bar" da biblioteca plotly
                                        x= card[colunadodataframe], #eixo x (reto/deitado)
                                        y= card["value"], #eixo y (reto/em pé)
                                        marker=dict(
                                                    color = "rgba(0,146,122,1)",
                                                    line = dict(
                                                                color = "rgba(0,146,122,0)",
                                                                width =1),),
                                        name="graficoferias1",
                                        text= (card["value"].map("R$ {:,.0f}".format)).str.replace(",","."), #".map" - percorre todas as linhas que estão na coluna, formatou em moeda {resumiu em zero casas decimais} ".format" é formatação de reduzir e "str.replace" substitui ponto por virgula
                                        #"R$ " + (card["value"]).round(0).astype(str),
                                        orientation= orientação))#essa orientação será colocada no chamador da função
        ###2° ETAPA: EDIÇÃO DO LAYOUT DO GRÁFICO DE BARRAS - POR PARTES:
        graficoferias1.update_layout( #Parte gráfica, título, tamanho do grafico, etc
                                   autosize = False,
                                    width = 700, #largura do gráfico
                                    height = 700, #altura do gráfico
                                    barmode = 'stack',
                                    yaxis = {"categoryorder":"total ascending"},
                                    title = {"text": titulodografico,
                                             "y":1, 
                                             "x":0.5,
                                             "yanchor":"top",
                                             "xanchor":"center"},
                                    font = dict(size =15, #tamanho e fonte utilizada nos rótulos
                                            family= "Arial Black, monospace",
                                            color = "rgba(0,0,0,1)" ))
                                   #xaxis_tickformat = "1%")
        ###3° ETAPA: EDIÇÃO DA POSIÇÃO DO RÓTULO EM RELAÇÃO A BARRA:                
        graficoferias1.update_traces(textposition='outside')    #posição do rótulo em relação a barra - podendo ser: "outside" fora da barra, "inside" dentro da barrada ou "auto" ajuste automático                       

        ###ETAPA FINAL - CHAMADOR DA FUNÇÃO:                            
        return coluna.plotly_chart(graficoferias1, use_container_width = True) #retorno da base


#######FUNÇÃO PARA ADMISSÕES:____________________________________________________________
    def Admissoes(self,filtroserviçoadmissao, filtrocargoadmissao):#todo parametro apos isto deve aparecer sempre que a função for chamada
        cardadmissao = DadosAdmissao()

        #cardadmissao=cardadmissao.groupby(["i_empregados","nome","salario", "nome_quebra","nome_cargo","situacao",
                                        #  pd.Grouper(key="admissao", freq= "M", axis = 0)]).sum("salario").reset_index()
                     
        if filtrocargoadmissao == "Todos":
            if filtroserviçoadmissao == "Todos":
                card = cardadmissao["Valor"].sum()

            else: 
                card_v = cardadmissao[cardadmissao["Contrato"]==filtroserviçoadmissao]
                card = card_v["Valor"].sum()

        else: 
            if filtroserviçoadmissao == "Todos":
                card_v = cardadmissao[cardadmissao["Cargo"]==filtrocargoadmissao]
                card = card_v["Valor"].sum()

            else:
                card_v = cardadmissao[(
                                    cardadmissao["Cargo"]==filtrocargoadmissao)&
                                    (cardadmissao["Contrato"]==filtroserviçoadmissao)]
                card = card_v["Valor"].sum()


        card_5 = f"R$ {card:,.0f}"
        card_5 = card_5.replace(",",".")
        return card_5


    ###PARA O PRIMEIRO GRÁFICO DE QTD MENSAL - ADMISSÃO:_______________________________________________________________        
    def Graficoevolucaomensaladmissao(self, coluna, colunadataframe, orientação, titulodografico, filtroadmissaoservico,filtroadmissaocargo):
        cardadmissao = DadosAdmissao()
        if filtroadmissaoservico == "Todos":
            if filtroadmissaocargo == "Todos":
                pass
            else: 
                cardadmissao = cardadmissao[cardadmissao["Cargo"]==filtroadmissaocargo]
        else:
            cardadmissao = cardadmissao[cardadmissao["Contrato"]==filtroadmissaoservico]

        cardadmissao = cardadmissao[["nome","Data","Valor"]] #selecionar somente essas três colunas que serão usadas
        cardadmissao["Data"] = pd.to_datetime(cardadmissao["Data"],format="%d/%m/%Y") #alterar o formato da data
        #card = cardadmissao.drop_duplicates(subset=["nome","admissao"],
        #                                    inplace=True)
       
        card = cardadmissao.groupby([pd.Grouper(key= "Data", freq= "M", axis=0)]).count().reset_index()

        graficoevolucaomensaladmissao = go.Figure()

        graficoevolucaomensaladmissao.add_trace(go.Bar(
                                                        x = card[colunadataframe],
                                                        y = card["Valor"],
                                                        marker= dict(
                                                                    color = "rgba(0,146,122,1)",
                                                                    line = dict(
                                                                                color = "rgba(0,146,122,0)",
                                                                                width = 1),),
                                                        name = "Graficoadmissao_1",
                                                        text = card["nome"],
                                                        orientation= orientação ))

        graficoevolucaomensaladmissao.update_layout(
                                                    autosize = False,
                                                    width = 100,
                                                    height = 400,
                                                    barmode = "stack",
                                                    yaxis = {"categoryorder":"total ascending"},
                                                    xaxis = dict(
                                                                tickmode = "linear", 
                                                                dtick = "M1"),
                                                    title = {"text": titulodografico,
                                                             "y":1, "x":0.5,
                                                             "yanchor": "top",
                                                             "xanchor": "center"},
                                                    font = dict(size = 15,
                                                                family = "Arial Black, monospace",
                                                                color = "rgba(0,0,0,1)") 
                                                
        )

        graficoevolucaomensaladmissao.update_traces(textposition = "inside")

        return coluna.plotly_chart(graficoevolucaomensaladmissao, use_container_width = True)
    
    ###PARA O SEGUNDO GRÁFICO DE COLABORADORES ATIVOS - ADMISSAO:_______________________________________________________________
    
    def Graficoadmissaoativos(self,coluna,colunadataframe,orientação,titulodografico):
            cardadmissao = DadosAtivos()
        #print(cardadmissao.dtypes)
            '''if filtroadmissaosituacao8 == "Todos":
                pass 
       
            else:
                if filtroadmissaosituacao8 == "Ativo":
                    A = 8 
                else: 
                    A = 1 
            cardadmissao = cardadmissao[cardadmissao["situacao"]==A]'''
            #print(cardadmissao)
            #print(f"deu certo {filtroadmissaosituacao8}")
            #print(filtroadmissaosituacao8=="1")

            card = cardadmissao[["Empresa","Ativos","Competencia"]]
            #cardadmissao["Competencia"] = pd.to_datetime(cardadmissao["Competencia"],format="%d/%m/%Y")
        
            #card = cardadmissao.groupby([pd.Grouper(key="Competencia",freq= "M", axis=0)]).count().reset_index()

            Graficoadmissaoativos = go.Figure()
            Graficoadmissaoativos.add_trace(go.Bar(
                                                x = card[colunadataframe],
                                                y = card["Ativos"],
                                                marker= dict(
                                                            color = "rgba(0,146,122,1)",
                                                            line = dict(
                                                                        color = "rgba(0,146,122,0)",
                                                                        width = 1),),
                                                name = "Graficoadmissao_2",
                                                text = card["Ativos"],
                                                orientation= orientação))
            Graficoadmissaoativos.update_layout(
                                            autosize = False, 
                                            width = 100,
                                            height = 400,
                                            barmode = "stack",
                                            yaxis = {"categoryorder":"total ascending"},
                                            title = {"text": titulodografico,
                                                     "y":1, "x":0.5,
                                                     "yanchor": "top",
                                                     "xanchor": "center"},
                                            font = dict(size = 15,
                                                        family = "Arial Black, monospace",
                                                        color = "rgba(0,0,0,1)")
        )

            Graficoadmissaoativos.update_traces(textposition = "inside")

            return coluna.plotly_chart(Graficoadmissaoativos, use_container_width= True)



    ###PARA O TERCEIRO GRÁFICO DE CARGOS - ADMISSAO:_______________________________________________________________
    '''def Graficocargoadmissao(self,coluna, colunadataframe,orientação,titulodografico,filtromêsadmissao):
        cardadmissao = DadosAdmissao()
        #print(cardadmissao.dtypes)
        if filtromêsadmissao == "Todos":
            card = cardadmissao.groupby([colunadataframe]).sum("salario").reset_index()
        else: 
            card = cardadmissao[cardadmissao["salario"]==filtromêsadmissao]
            card = card.groupby([colunadataframe]).sum("salario").reset_index()

        tabelaadmissao2 = go.Figure(
                                    data = [go.Table(
                                                    header = dict(
                                                                values = list(cardadmissao.columns),
                                                                font = dict(
                                                                            size = 14, color = "rgba(3,102,102,1)", family = "Arial Black, monospace"),
                                                                line_color = "rgba(153,226,180,1)",
                                                                height = 30),
                                                    cells = dict(
                                                                values = [cardadmissao[k].tolist() for k in cardadmissao.columns],
                                                                font = dict( size = 14, color = "Black", family = "Arial, monospace"),
                                                                align = ["left", "center"],
                                                                line_color = "rgba(153,226,180,1)",
                                                                height = 30)
                                                                )])
        tabelaadmissao2.update_layout(
                                    height= 800, 
                                    width = 1800,
                                    xaxis = dict(
                                                rangeslider = dict(
                                                                    visible = True)))
            
        cardadmissao["salario"] = cardadmissao["salario"].map("R${:,.0f}".format)
        cardadmissao["salario"] = cardadmissao["salario"].str.replace(",",".")
        
        
        return coluna.plotly_chart(tabelaadmissao2, use_container_width = True)'''
        #return coluna.plotly_chart(graficoadmissao1, use_container_width = True)
    ###PARA TESTE DO QUARTA TABELA DE TOTAL DA FOLHA - ADMISSAO:_____________________________________________________________
    def testeterceiroadmissao(self, coluna, filtromêsadmissao ):
        cardadmissao = DadosAtivos()

        '''if filtromêsadmissao == "Todos":
            card = cardadmissao.groupby(["Ativos"]).sum("Líquido Geral").reset_index()
        else: 
            card = cardadmissao[cardadmissao["Líquido Geral"]==filtromêsadmissao]
            card = card.groupby(["Ativos"]).sum("Líquido Geral").reset_index()'''

        #cardadmissao["Líquido Geral"] = cardadmissao["Líquido Geral"].map("R${:,.2f}".format) #PARA ALTERAR O FORMATO DO VALOR, COLOCANDO R$

        cardadmissao.rename(columns={"nome_quebra": "Contrato/Serviço"}, inplace=True)
        cardadmissao.rename(columns={"nome": "Colaborador"}, inplace=True)
        cardadmissao.rename(columns={"nome_cargo": "Cargo"}, inplace=True)
        cardadmissao.rename(columns={"admissao": "Data de Contratação"}, inplace=True)
        cardadmissao.rename(columns={"salario": "Salário"}, inplace=True)

        tabelaadmissao = go.Figure(
                                   data = [go.Table(
                                                    header=dict(
                                                                values = list(cardadmissao.columns),
                                                                font = dict(
                                                                            size = 14, 
                                                                            color = "rgba(3,102,102,1)",
                                                                            family = "Arial Black, monospace"),
                                                                line_color = "rgba(153,226,180,1)",
                                                                align = ["center","center"],
                                                                height = 30),
                                                    cells = dict(
                                                                values = [cardadmissao[k].tolist() for k in cardadmissao.columns],
                                                                font = dict(size = 14,
                                                                            color = "black",
                                                                            family = "Arial, monospace"),
                                                                align = ["left", "center"],
                                                                line_color = "rgba(153,226,180,1)",
                                                                height = 30))])
        tabelaadmissao.update_layout(
                                    height = 800,
                                    width = 1800)
        tabelaadmissao.update_layout(xaxis = dict(
                                                    rangeslider = dict(
                                                                        visible = True)))
        
        return coluna.plotly_chart(tabelaadmissao, use_container_width = True)
        
    def tentativagraficobarra(self,coluna, titulodografico):
        card_a = DadosAdmissao()
        card_r = DadosRescisao()                       

#####FUNÇÃO PARA ONVIO/CHAMADOS:____________________________________________________________
    def Onvio_chamados(self,filtrotratativaonvio,filtrosituaçãoonvio):#todo parametro apos isto deve aparecer sempre que a função for chamada
        cardonvio = DadosOnvio()


        if filtrosituaçãoonvio == "Todos":
            if filtrotratativaonvio == "Todos":
                card = cardonvio["TRATATIVA"].count()

            else: 
                card = cardonvio[cardonvio["TRATATIVA"]== filtrotratativaonvio]
                card = card ["TRATATIVA"].count()

        else: 
            pass

    ###PARA CRIAÇÃO DE CARD total de chamados - ONVIO/CHAMADOS:_______________________________________________________________

    def Onvio_chamadoscard(self, filtrotratativaonvio,SITUAÇÃO):
        cardonvio = DadosOnvio()
        if filtrotratativaonvio == "Todos":
            card = cardonvio[#(cardonvio["TRATATIVA"]==filtrotratativaonvio)&
                             (cardonvio["SITUAÇÃO"]==SITUAÇÃO)]
            card = card["TRATATIVA"].count()
        else:
            card = cardonvio[(cardonvio["TRATATIVA"]==filtrotratativaonvio)&
                             (cardonvio["SITUAÇÃO"]==SITUAÇÃO)]
            card = card["TRATATIVA"].count()

        return card 
        

    ###PARA O PRIMEIRO GRÁFICO DE % - ONVIO/CHAMADO_______________________________________________________________        

    def Onvio_chamadografico1(self,coluna,titulodografico,filtrotratativaonvio,data):
        cardonvio = DadosOnvio()
        
        
        #PARA VINCULAR FILTRO TRATATIVA AO GRÁFICO
        if filtrotratativaonvio == "Todos":
            if data == "Todos":
                card = cardonvio.groupby(["SITUAÇÃO"]).count().reset_index()
            else:
                card=cardonvio[(cardonvio["mes"]==data)]
                card = card.groupby(["SITUAÇÃO"]).count().reset_index()
        else:
            if data == "Todos":
                card = cardonvio[(cardonvio["TRATATIVA"]==filtrotratativaonvio)]
                card = card.groupby(["SITUAÇÃO"]).count().reset_index()
            else:
                card = cardonvio[(cardonvio["TRATATIVA"]==filtrotratativaonvio)&
                                 (cardonvio["mes"]==data)]
                card = card.groupby(["SITUAÇÃO"]).count().reset_index()


        #OPÇÃO 1 DE GRÁFICO:
        #Graficopercentual1= px.pie(card, values="TRATATIVA", names="SITUAÇÃO",color_discrete_map={'Concluído':'lightcyan',
                #                                                                                     'Prescrita':'cyan',
                #                                                                                    'Respondido':'royalblue',
                 #    
                 #                                                                                'Aguardando o cliente':'darkblue'})
        ### PARA GERAR O GRÁFICO DE PIZZA 
        Graficopercentual1 = go.Figure(data=[
                                go.Pie(labels= card["SITUAÇÃO"], values= card["TRATATIVA"], pull=[0.01,0.01,0.01,0.01,0.01])])
        
        Graficopercentual1.update_traces(marker= dict( #CORES DE CADA RODELA DO GRÁFICO
                                                    colors= ["rgba(0,124,119,1)","rgba(0,67,70,1)","rgba(0,189,157,1)","rgba(76,224,210,1)","rgba(34,170,161,1)"],
                                                    line = dict(
                                                                color = "rgba(0,0,0,0)",
                                                                width = 1
                                                    )))
        Graficopercentual1.update_layout(
                                        autosize = True,
                                        width =400,
                                        height = 500,
                                        barmode = "stack",
                                        yaxis = {"categoryorder":"total ascending"},
                                        title = {"text":titulodografico,
                                                 "y":1, "x":0.5,
                                                 "yanchor": "top",
                                                 "xanchor": "center"},
                                        legend_font = dict( #PARA DEFINIR A LEGENDA
                                                            color = "rgba(0,0,0,1)",
                                                            family = "Arial , monospace",
                                                            size = 13 ),
                                        hoverlabel_font = dict( #PARA DEFINIR A DICA DE FERRAMENTA DO GRÁFICO
                                                                family = "Arial, monospace",   
                                                                size = 13                                                      
                                        ) ,
                                        hoverlabel_grouptitlefont = dict( #PARA DEFINIR O TÍTULO DO GRÁFICO
                                                                        family = "Arial Black, monospace",
                                                                        size = 15 ),
                                        font = dict( #PARA DEFINIR O RÓTULO DO GRAFICO - PARTE DE DENTRO
                                                    size = 15,
                                                    family = "Arial Black, monospace"), )

        return coluna.plotly_chart(Graficopercentual1, use_container_width = True)
        
    ###PARA O SEGUNDO GRÁFICO DE % - ONVIO/CHAMADO_______________________________________________________________        
    def Onvio_chamadografico2(self,coluna, titulodografico,orientação,colunadataframe,filtrotratativaonvio,data): #filtrotratativaonvio):
        cardonvio = DadosOnvio()
        if filtrotratativaonvio == "Todos":
            if data == "Todos":
                card = cardonvio.groupby(["TRATATIVA"]).count().reset_index()
            else: 
                card=cardonvio[(cardonvio["mes"]==data)]
                card = card.groupby(["TRATATIVA"]).count().reset_index()
        else:
            if data == "Todos":
                card = cardonvio[(cardonvio["TRATATIVA"]==filtrotratativaonvio)]
                card = card.groupby(["SITUAÇÃO"]).count().reset_index()
            else: 
                card = cardonvio[(cardonvio["TRATATIVA"]==filtrotratativaonvio)&
                                 (cardonvio["mes"]==data)]
                card = card.groupby(["SITUAÇÃO"]).count().reset_index()


        Graficoonvio2 = go.Figure()
        Graficoonvio2.add_trace(go.Bar(
                                        x = card["SITUAÇÃO"],
                                        y = card[colunadataframe],
                                        marker= dict(
                                                    color = "rgba(0,146,122,1)",
                                                    line = dict(
                                                                color = "rgba(0,146,122,0)",
                                                                width = 1),),
                                        name = "graficoonvio2",
                                        text=card["SITUAÇÃO"],
                                        orientation= orientação))

        Graficoonvio2.update_layout(
                                    autosize = False,
                                    width = 200,
                                    height = 600,
                                    barmode = "stack",
                                    yaxis = {"categoryorder":"total ascending"},
                                    title = {"text": titulodografico,
                                             "y":1, "x":0.5,
                                             "yanchor":"top",
                                             "xanchor": "center"},
                                    font = dict( size = 15,
                                                family = "Arial Black, monospace",
                                                color = "rgba(0,0,0,1)"))
        
        Graficoonvio2.update_traces(textposition = "outside")

        return coluna.plotly_chart(Graficoonvio2, use_container_width = True)
        

#####FUNÇÃO PARA RESCISÕES:____________________________________________________________
    def Rescisoes(self, filtroservicorescisao,filtrocentrodecustorescisao):#todo parametro apos isto deve aparecer sempre que a função for chamada
        cardrescisao = DadosRescisao()
        #print(filtroservicorescisao)
        if filtrocentrodecustorescisao == "Todos":
            if filtroservicorescisao == "Todos":
                card = cardrescisao["Valor"].sum()
                #print(card)

            else:
                card_v = cardrescisao[cardrescisao["Contrato"]==filtroservicorescisao]
                card = card_v["Valor"].sum()
        else: 
            if filtroservicorescisao == "Todos":
                card_v = cardrescisao[cardrescisao["Centro de Custo"]==filtrocentrodecustorescisao]
                card = card_v['Valor'].sum()

            else: 
                card_v = cardrescisao[
                    (cardrescisao["Centro de Custo"]==filtrocentrodecustorescisao) &
                                    (cardrescisao["Contrato"]==filtroservicorescisao)]
                card = card_v["Valor"].sum()

        card_2 = f"R$ {card:,.0f}" #criação da variavel "card_1" para trazer o 0 para as casas decimais, transformando em um string
        card_2 = card_2.replace(",",".") #trocar virgula por ponto
        
        return card_2

    ###PARA CRIAÇÃO DE CARD DESCONTOS - RESCISÕES:_______________________________________________________________
    def Rescisoes2(self,tipo,filtrorescisao_mês,):
        cardrescisao = DadosRescisao()
        if filtrorescisao_mês == "Todos":
            card = cardrescisao[cardrescisao['Tipo']==tipo]

        else: 
            card = cardrescisao[(cardrescisao["Tipo"]==tipo)&
                                (cardrescisao["Data"]==filtrorescisao_mês)]

        card = card["Valor"].sum()

        card_2 = f"R$ {card:,.0f}"
        card_2 = card_2.replace(",",".")
        return card_2

    ###PARA CRIAÇÃO DE CARD PROVENTOS - RESCISÕES:_______________________________________________________________
    def Rescisoes3(self,tipo2,filtrorescisao_mês,):
        cardrescisao = DadosRescisao()
        if filtrorescisao_mês == "Todos":
            card = cardrescisao[cardrescisao["Tipo"]==tipo2]

        else:
            card = cardrescisao[(cardrescisao["Tipo"]==tipo2)&
                                (cardrescisao["Data"]==filtrorescisao_mês)]
        
        card = card["Valor"].sum()

        card_2 = f"R$ {card:,.0f}"
        card_2 = card_2.replace(",",".")
        return card_2
    
    ###PARA O PRIMEIRO GRÁFICO DE EVOLUÇÃO MENSAL - RESCISAO:_______________________________________________________________        

    def Graficoevolucaomensalrescisao(self,coluna,colunadataframe,orientação,titulodografico, filtroserviçorescisao, filtrocentrodecustorescisao):
        cardrescisao = DadosRescisao()
        #PARA INTEGRAR O FILTRO AO GRAFICO
        if filtroserviçorescisao == 'Todos':
            if filtrocentrodecustorescisao == "Todos":
                pass 
            else: 
                cardrescisao = cardrescisao[cardrescisao["Centro de Custo"]==filtrocentrodecustorescisao]
        else:
            cardrescisao = cardrescisao[cardrescisao["Contrato"]==filtroserviçorescisao]


        #PARA COMEÇAR O GRÁFICO LIMPANDO AS LINHAS DUPLICADAS
        #cardrescisao = cardrescisao[["nome", "Data", "Valor"]]
        
        card = cardrescisao.drop_duplicates(subset=["nome"],
                                            inplace=True)
        card = cardrescisao.groupby("Data").count().reset_index()    
        

        graficoevolucaomensalrescisao = go.Figure()
        ###1° ETAPA: CRIAÇÃO DO GRÁFICO DE BARRAS - POR PARTES:
        graficoevolucaomensalrescisao.add_trace(go.Bar(
                                                    x = card[colunadataframe],
                                                    y = card["Valor"],
                                                    marker= dict(
                                                                color = "rgba(0,146,122,1)",
                                                                line = dict(
                                                                            color = "rgba(0,146,122,0)",
                                                                            width = 1),),
                                                    name = "Graficorescisao1",
                                                    text = card["nome"],
                                                    orientation= orientação  ))
        ###2° ETAPA: EDIÇÃO DO LAYOUT DO GRÁFICO DE BARRAS - POR PARTES:
        graficoevolucaomensalrescisao.update_layout(
                                                autosize = False,
                                                width = 900,
                                                height = 500,
                                                barmode = 'stack',
                                                yaxis = {"categoryorder":"total ascending"},
                                                title = {"text": titulodografico,
                                                        "y":1, "x":0.5,
                                                        "yanchor": "top",
                                                        "xanchor": "center"},
                                                font = dict(size = 15,
                                                            family = "Arial Black, monospace",
                                                            color = "rgba(0,0,0,1)"))
        
        ###3° ETAPA: EDIÇÃO DA POSIÇÃO DO RÓTULO EM RELAÇÃO A BARRA:
        graficoevolucaomensalrescisao.update_traces(textposition="inside")
        ###ETAPA FINAL - CHAMADOR DA FUNÇÃO:
        return coluna.plotly_chart(graficoevolucaomensalrescisao, use_container_width = True)

    ###PARA O SEGUNDO GRÁFICO DE RESCISÃO - SERVIÇOS:_______________________________________________________________
    def Graficoserviço_rescisao(self,coluna, colunadataframe, orientação,filtro_mêsrescisao, titulodografico):
        cardrescisao = DadosRescisao()
        if filtro_mêsrescisao == "Todos":
            card = cardrescisao.groupby([colunadataframe]).sum("Valor").reset_index()
        else: 
            card = cardrescisao[cardrescisao["Data"]==filtro_mêsrescisao]
            card = card.groupby([colunadataframe]).sum("Valor").reset_index()


        graficoserviçorescisao = go.Figure()
        graficoserviçorescisao.add_trace(go.Bar(
                                                x = card["Valor"],
                                                y = card[colunadataframe],
                                                marker = dict(
                                                                color = "rgba(0,146,122,1)",
                                                                line = dict(
                                                                            color = "rgba(0,146,122,0)",
                                                                            width = 1),),
                                                name = "graficorescisao1",
                                                text = (card["Valor"].map("R$ {:,.0f}".format)).str.replace(",","."),
                                                orientation = orientação))
        graficoserviçorescisao.update_layout(
                                            autosize = False,
                                            width = 200,
                                            height = 600,
                                            barmode = "stack",
                                            yaxis = {"categoryorder":"total ascending"},
                                            title = {"text":titulodografico,
                                                     "y":1, "x":0.5,
                                                     "yanchor": "top",
                                                     "xanchor": "center"},
                                            font = dict(size = 15,
                                                        family = "Arial Black, monospace",
                                                        color = "rgba(0,0,0,1)"))
        
        graficoserviçorescisao.update_traces(textposition = "auto")

        return coluna.plotly_chart(graficoserviçorescisao, use_container_width = True)
    
    ###PARA O TERCEIRO GRÁFICO DE RESCISÃO - CENTRO DE CUSTO:_______________________________________________________________
    def Graficocentrodecusto_rescisao(self, coluna, colunadataframe, orientação, titulodografico,filtro_mêsrescisao):
        cardrescisao = DadosRescisao()
        if filtro_mêsrescisao == "Todos":
            card = cardrescisao.groupby([colunadataframe]).sum("Valor").reset_index()

        else: 
            card = cardrescisao[cardrescisao["Data"]==filtro_mêsrescisao]
            card = card.groupby([colunadataframe]).sum("Valor").reset_index()

        graficorescisao3 = go.Figure()
        ###1° ETAPA: CRIAÇÃO DO GRÁFICO DE BARRAS - POR PARTES: 
        #obs: para gráficos verticais o x e y devem sem invertidos sendo o dataframe primeiro
        graficorescisao3.add_trace(go.Bar(
                                        x = card["Valor"],
                                        y = card[colunadataframe],
                                        marker=dict(
                                                    color = "rgba(0,146,122,1)",
                                                    line = dict(
                                                                color = "rgba(0,146,122,0)",
                                                                width =1),),
                                        name = "garficorescisao3",
                                        text= (card["Valor"].map("R$ {:,.0f}".format)).str.replace(",","."),
                                        orientation= orientação))
        ###2° ETAPA: EDIÇÃO DO LAYOUT DO GRÁFICO DE BARRAS - POR PARTES:
        graficorescisao3.update_layout(
                                    autosize = False,
                                    width = 100,
                                    height = 500,
                                    barmode = "stack",
                                    yaxis = {"categoryorder":"total ascending"},
                                    title = {"text": titulodografico,
                                             "y":1,
                                             "x":0.5,
                                             "yanchor":"top",
                                             "xanchor": "center"},
                                    font = dict(size = 13,
                                                family = "Arial Black, monospace",
                                                color = "rgba(0,0,0,1)"))
        
        
        ###3° ETAPA: EDIÇÃO DA POSIÇÃO DO RÓTULO EM RELAÇÃO A BARRA:    
        graficorescisao3.update_traces(textposition = "auto")
        ###ETAPA FINAL - CHAMADOR DA FUNÇÃO:                            
        return coluna.plotly_chart(graficorescisao3, use_container_width=True)


#####FUNÇÃO PARA APRESENTAÇÕES:____________________________________________________________
    def Apresentacao(self): #todo parametro apos isto deve aparecer sempre que a função for chamada
        st.set_page_config(layout='wide') #"st" referente ao pacote do streamlit . "set_page_config" - configuração da página, opção de layout "wide"
        with st.sidebar: #barra lateral/menu

#####MENU:____________________________________________________________        
            st.sidebar.image(self.logos, use_column_width=True) #Imagem que virá no menu, "use_column..." para centralizar a imagem
            choose = option_menu("H2F",  #nome no topo do menu, título do menu
                                  ["Lembretes","Onvio/Chamados", "Rubricas", "Admissão", "Rescisão","Férias"], #abas/páginas
                                  icons = ['alarm','gear','pencil-square','cash-coin','cash', 'paperclip'], #ícones para cada opção de página
                                  menu_icon='list', #ícone do título do menu
                                  default_index= 0,
                                  styles={ "container": {"padding": "5!important", "background-color": "rgba(0,0,0,1"},
                                        "icon": {"color": "gold", "font-size": "20px"},
                                        "nav-link": {"font-size": "18px", "text-align": "left", "margin":"0px", "--hover-color": "#78C6A3"},
                                        "nav-link-selected": {"background-color": "#78C6A3"}}) #para identificar qual índice iniciará
            
#####FORMATAÇÃO DE TODAS AS PÁGINAS:____________________________________________________________              
        espaco_tela1,espaco_tela2,espaco_tela3,espaco_tela4, espaco_tela5= st.columns([0.05,15,2,1,2]) #Definição de colunas nas páginas do streamlit
        with espaco_tela2: #definição de coluna para a informação abaixo:
            espaco_tela2.title("Apresentação de Resultados :bar_chart:") #o título ao lado será inserido na "2° coluna" de todas as páginas do projeto, entre o : : é colocado o icone através do site https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/
         
         #Obs1 - Os dois itens abaixo (que estão comentados) foram inativados pois foi possível colocar as duas imagens no menu. 
        #with espaco_tela5: #para inserir imagem no topo de todas as páginas do projeto - ao lado do título - a imagem ficará na "5° coluna"
            #st.image(self.logoalldax, width= 70)  #A imagem será carregada do item "para subir as imagens", "width" para definir o tamanho da imagem

        #with espaco_tela3: #para inserir imagem no topo de todas as páginas do projeto - ao lado do título - a imagem ficará na "3° coluna"
           #st.image(self.logoh2f, width=170) #A imagem será carregada do item "para subir as imagens", "width" para definir o tamanho da imagem

        #with espaco_tela3:   #para inserir imagem no topo de todas as páginas do projeto - ao lado do título - a imagem ficará na "3° coluna"
           #st.image(self.resultadosicone, width=60) #A imagem será carregada do item "para subir as imagens", "width" para definir o tamanho da imagem


#####FORMATAÇÃO DA PRIMEIRA PÁGINA - LEMBRETES:____________________________________________________________              
        if choose == "Lembretes":
            with open('style.css') as f:
               st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

            st.title('Para não esquecer :heavy_exclamation_mark:')



            #filtroscolunafeedback1,filtroscolunafeedback2 = st.columns([1.5,0.01])

        ###DEFINIÇÃO DE FILTROS - LEMBRETES:____________________________________________________________
        #LEMBRETES = AO COLOCAR NO SENTIMENTO - "bad", "good", "neutral" - a cor e o ícone utilizado mudam
            cc = st.columns(3)
            with cc[0]:
                hc.info_card(title='Admissão', content='O envio do pedido de admissão deve ocorrer com até 24 horas de antecedência!', sentiment='good', title_text_size = "1.7rem",content_text_size="1.3rem",)
            with cc[1]:
                 hc.info_card(title='Folha', content='O envio dos apontamentos da sua folha de pagamento devem ser enviados todo dia 01 do mês! ', sentiment='good', title_text_size = "1.5rem",content_text_size="1.3rem",)
            with cc[2]:
                hc.info_card(title='Férias', content='As férias devem ser comunicadas com no mínimo 35 dias de antecedência! ', sentiment='good', title_text_size = "1.5rem",content_text_size="1.3rem",)
            cc = st.columns(3)
            with cc[0]:
                hc.info_card(title='Rescisão', content='O pagamento da rescisão deve ser feito 10 dias após a demissão! ', sentiment='good', title_text_size = "1.5rem",content_text_size="1.3rem",)
               
            with cc[1]:
                hc.info_card(title='Chamados/Onvio', content='O nosso tempo de análise e retorno dos chamados no Onvio é de 72 horas!', sentiment='good', title_text_size = "1.5rem",content_text_size="1.3rem",)
            #with cc[2]:
                #hc.info_card(title='Prazo Mensagens', content='01 de cada mês!', sentiment='neutral', title_text_size = "1.5rem",content_text_size="1.3rem",)
            
            

            #colunaata1, colunaata2,colunaata3 = st.columns([1,1,1])

           #self.Atafiltros(colunaata2,
               #             departamento= filtrodepartamento)


            colunatitulo1, colunatitulo2,colunatitulo3 = st.columns((0.2,1,0.01))
            with colunatitulo2:
                colunatitulo2.title("Atas de Reunião - DEMANDAS")
                
            filtroscolunasata0,filtroscolunasata1,filtroscolunasata2= st.columns([0.01,1,0.01])
            
            ATA = DadosAta()
            filtro_departamento = ATA["Departamento"].unique()
            filtro_departamento = np.append(["Todos"], filtro_departamento)

            with filtroscolunasata1:
                    filtrodepartamento = st.selectbox(
                        "Escolha o Departamento",
                        filtro_departamento,
                        help = "A incluir",
                        key = "Departamento",
                        index = 0
                )

            colunatabelaata1, colunatabelaata2 = st.columns((1,0.01))
            self.Ata(colunatabelaata1,
                     departamento=filtrodepartamento)


#####FORMATAÇÃO DA SEGUNDA PÁGINA - ONVIO/CHAMADO:____________________________________________________________              
        if choose == "Onvio/Chamados":  #Bloco de código Geral - tudo será dentro dele
            with open('style.css') as f:
               st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
            st.title('Solicitações de chamados no Onvio')  #Definição do título da página
            
            filtroscolunasonvio1,filtroscolunasonvio2 = st.columns([1,1]) #definição de colunas para as próximas informações nesta página e tamanho (em pixel)

        ###DEFINIÇÃO DE FILTROS - ONVIO/CHAMADO:____________________________________________________________
            ONVIO = DadosOnvio() #Criação de Dataframe. nomeado neste projeto como "GERAL" por ser o nome da página e assim facilitar na compreensão
            filtro_situação = ONVIO["SITUAÇÃO"].unique()  #Criação do filtro mês que será puxado na planilha nomeada como "sq_dataini", "unique()" irá remover toda a duplicata
            filtro_situação = np.append(["Todos"], filtro_situação) #"np.append" para adicionar algum item a ser filtrado devendo ser adicionado dentro de ["","",""]
            filtro_tratativa = ONVIO["TRATATIVA"].unique()  #Criação do filtro mês que será puxado na planilha nomeada como "sq_nome_servico", "unique()" irá remover toda a duplicata
            filtro_tratativa = np.append(['Todos'], filtro_tratativa) #"np.append" para adicionar algum item a ser filtrado devendo ser adicionado dentro de ["","",""]
            filtro_data = ONVIO["mes"].unique()
            filtro_data = np.append(["Todos"],filtro_data)


            with filtroscolunasonvio2: #posição do filtro de acordo com as colunas definidas anteriormente
                filtro_dataonvio = st.selectbox( #novo dataframe para o pacote de filtro
                    "Escolha a data", #nome/frase que identificará o filtro 
                    filtro_data, #objeto/variável
                    help="A incluir", #mensagem de suporte
                    key= "filtrodataonvio", #nome do filtro
                    index = 0) #ele irá selecionar o item n° x da lista
            
            with filtroscolunasonvio1: #posição do filtro de acordo com as colunas definidas anteriormente
                filtro_tratativaonvio = st.selectbox( #novo dataframe para o pacote de filtro
                    "Escolha a Tratativa", #nome/frase que identificará o filtro
                    filtro_tratativa, #objeto/variável
                    help= "A incluir",  #mensagem de suporte
                    index= 0, #ele irá selecionar o item n° x da lista
                    key= "filtrotratativaonvio",) #nome do filtro
                

    ###CHAMADOR DE FUNÇÕES - ONVIO/CHAMADOS:____________________________________________________________
            ColunageralA, ColunageralB, ColunageralC,ColunageralD,ColunageralE = st.columns((1,1,1,1,1))
            
        ###CHAMADOR DE FUNÇÕES - CARD ONVIO/CHAMADOS:____________________________________________________________
            ColunageralA.metric(label="Aguardando o Cliente", value=self.Onvio_chamadoscard(filtrotratativaonvio=filtro_tratativaonvio,
                                                                                SITUAÇÃO="Aguardando o cliente"))
            ColunageralB.metric(label="Aguardando Resposta", value=self.Onvio_chamadoscard(filtrotratativaonvio=filtro_tratativaonvio,
                                                                                SITUAÇÃO="Aguardando resposta"))
            ColunageralC.metric(label="Prescrita", value=self.Onvio_chamadoscard(filtrotratativaonvio=filtro_tratativaonvio,
                                                                                SITUAÇÃO="Prescrita"))
            ColunageralD.metric(label="Respondido", value=self.Onvio_chamadoscard(filtrotratativaonvio=filtro_tratativaonvio,
                                                                                SITUAÇÃO="Respondido")) 
            ColunageralE.metric(label="Concluído", value=self.Onvio_chamadoscard(filtrotratativaonvio=filtro_tratativaonvio,
                                                                                SITUAÇÃO="Concluído"))

    ###CHAMADOR DE FUNÇÕES - GRÁFICO 1,2 e 3 ONVIO/CHAMADOS:____________________________________________________________

            GraficoonviogeralA,GraficoonviogeralB = st.columns((1,0.01))
            self.Onvio_chamadografico1(GraficoonviogeralA, titulodografico= "Percentual de Chamados",
                                       filtrotratativaonvio=filtro_tratativaonvio,
                                       data=filtro_dataonvio) 
            
            GraficoonviogeralC, GraficoonviogeralD = st.columns((1,0.01))
            self.Onvio_chamadografico2(GraficoonviogeralC, 
                                       colunadataframe= "TRATATIVA",
                                       orientação= "h",
                                       titulodografico= "Quantidade de tratativas",
                                        filtrotratativaonvio=filtro_tratativaonvio,
                                        data=filtro_dataonvio)

###FORMATAÇÃO DA TERCEIRA PÁGINA - RUBRICAS:____________________________________________________________ 
        if choose == "Rubricas":
            with open('style.css') as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html= True)
            st.title("Resumo de Rubricas:")
            
            filtrorubricacoluna1,filtrorubricacoluna2 = st.columns([1,0.1])

        ###DEFINIÇÃO DE FILTROS - RUBRICAS:____________________________________________________________
            RUBRICA = DadosRubricas()
            filtro_datar= RUBRICA["Data"].unique()
            filtro_datar = np.append(["Todos"],filtro_datar)
            #filtro_modelo = RUBRICA["Rubrica"].unique()
            #filtro_modelo = np.append(["Todos"],filtro_modelo)
            #filtro_rubrica =  ["Todos","Proventos","Desconto"]
            #fvalor = RUBRICA["cp3_valor_calc"].unique()
            #fvalor = np.append(["Todos"],fvalor)
            
            with filtrorubricacoluna1:
                filtrodatarubrica = st.selectbox(
                "Escolha a data",
                filtro_datar,
                help = "A Incluir",
                key = "Filtro de data",
                index= 0)
                
            
            '''with filtrorubricacoluna2:
                filtrorubricarubrica = st.selectbox(
                    "Escolha a situação",
                    filtro_rubrica,
                    help= "A Incluir",
                    key = "filtro rubrica",
                    index=0)
            
            with filtrorubricacoluna3:
                filtromodelorubrica = st.selectbox(
                  "Escolha a situação",
                    filtro_modelo,
                   help= "A Incluir",
                    key = "Filtro de modelo",
                   index=0)'''

###CHAMADOR DE FUNÇÕES - rubricas:____________________________________________________________
        ###CHAMADOR DE FUNÇÕES - CARD Rubricas:____________________________________________________________
            colunacardrubricaA,colunacardrubricaB,colunacardrubricaC = st.columns((1,1,1))
            colunacardrubricaA.metric(label= "SALÁRIO FIXO", value = self.cardrubrica( descrição="SALÁRIO FIXO",
                                                                                 data = filtrodatarubrica,
                                                                                 ))
            colunacardrubricaB.metric(label= "VALE ALIMENTAÇÃO", value = self.cardrubrica( descrição="VALE ALIMENTAÇÃO",
                                                                                 data = filtrodatarubrica,
                                                                                 ))
            colunacardrubricaC.metric(label= "VALE TRANSPORTE", value = self.cardrubrica( descrição="VALE TRANSPORTE",
                                                                                            data = filtrodatarubrica,
                                                                                            ))

            #colunacardrubricaA.metric(label= "SALÁRIO FIXO", value = self.cardrubricas(,
                                                                                       #filtrovalor= "SALÁRIO FIXO"))
            
###CHAMADOR DE FUNÇÕES - GRÁFICO 1,2 e 3 rubricas:____________________________________________________________
#obs.: gáfico horizontal - total
            graficocoluna1,graficocoluna2,graficocoluna3 = st.columns((1,0.01,0.01))
            self.Graficonovo(graficocoluna1,
                                 colunadodataframe="Rubrica",
                                 orientação= "h",
                                 titulodografico= "rubricas",
                                 filtrodata=filtrodatarubrica,
                                 #filtromodelo= filtromodelorubrica
                                )
            #graficocoluna0,graficocoluna2,graficocoluna3 = st.columns((0.2,1,0.01))

#obs.: tabela - total
            '''with graficocoluna2:
                graficocoluna2.title("Rubricas da Folha de Pagamento")
            
            graficocoluna1,graficocoluna12 = st.columns((1,0.01))

            self.tabelarubrica(graficocoluna1, 
                               filtrorubrica = filtrorubricarubrica,
                                filtrodatarubrica = filtrodatarubrica)'''

        

#####FORMATAÇÃO DA PRIMEIRA SEGUNDA - ADMISSÃO:____________________________________________________________   
        elif choose == "Admissão":
                with open('style.css') as f:
                    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
                st.title("Resumo de Admissões")
                filtrosadmissaocoluna1,filtrosadmissaocoluna2, = st.columns([1.5,1.5])
        
        ###DEFINIÇÃO DE FILTROS - ADMISSÃO:____________________________________________________________
        ###CHAMADOR DE FUNÇÕES - CARD valor total ADMISSAO:____________________________________________________________

                ADMISSAO = DadosAdmissao()
                #filtroadmissao_mês = ADMISSAO["Data"].unique()
                #filtroadmissao_mês = np.append(["Todos"], filtroadmissao_mês)
                filtroadmissao_serviço = ADMISSAO["Contrato"].unique()
                filtroadmissao_serviço = np.append(["Todos"], filtroadmissao_serviço)
                filtroadmissao_cargo = ADMISSAO["Cargo"].unique()
                filtroadmissao_cargo = np.append(["Todos"], filtroadmissao_cargo)
                filtroadmissao_ativos = ["Todos", "Demitido", "Ativo"]

                #with filtrosadmissaocoluna3:
                  #  filtroadmissao_mês1 = st.selectbox(
                   #                                "Escolha o mês",
                   #                                filtroadmissao_mês,
                   #                               help="A incluir",
                   #                               key= "Admissão_1",
                  #                                index= 0)

                with filtrosadmissaocoluna1:
                    filtroadmissao_serviço1 = st.selectbox(
                                                   "Esolha o Serviço",
                                                    filtroadmissao_serviço,
                                                    help = "A incluir",
                                                   key= "Admissão_2",
                                                    index=0)              

                with filtrosadmissaocoluna2:
                    filtroadmissao_cargo1 = st.selectbox(
                                                        "Escolha o cargo",
                                                        filtroadmissao_cargo,
                                                        help=" A incluir",
                                                        key = "Admissão_3",
                                                        index=0)
                    
                ''' with filtrosadmissaocoluna3:
                    filtroadmissao_ativos8 = st.selectbox(
                                                        "Escolha a situacao",
                                                        filtroadmissao_ativos,
                                                        help=" A incluir",
                                                        key = "Admissão_4",
                                                        index=0)'''


###CHAMADOR DE FUNÇÕES - ADMISSÃO:____________________________________________________________
        ###CHAMADOR DE FUNÇÕES - CARD valor total FÉRIAS:____________________________________________________________
                colunaadmissaoA,colunaadmissaoB,colunaadmissaoC = st.columns((1,1,1))
                colunaadmissaoA.metric(label="Salário Total", value=self.Admissoes(#filtroserviçoadmissao=filtroadmissao_serviço1,
                                                                         filtrocargoadmissao=filtroadmissao_cargo1,
                                                                         filtroserviçoadmissao =  filtroadmissao_serviço1))



###CHAMADOR DE FUNÇÕES - GRÁFICO 1,2 e 3 ADMISSÃO:____________________________________________________________
#obs.: gáfico vertical - evolução mensal

                GraficoevolucaomensaladmissaoA,GraficoevolucaomensaladmissaoB = st.columns((1,0.01)) 
                self.Graficoevolucaomensaladmissao(GraficoevolucaomensaladmissaoA,
                                            colunadataframe= "Data",
                                           orientação= "v",
                                           titulodografico= "Quantidade Mensal de Admissões",
                                            filtroadmissaoservico =  filtroadmissao_serviço1,
                                            filtroadmissaocargo = filtroadmissao_cargo1,)
                                            #filtroadmissaomês=  filtroadmissao_mês1 )

#obs.: gáfico vertical - ativos
                GraficoativosadmissaoA,GraficoativosadmissaoB = st.columns((0.01,1))
                self.Graficoadmissaoativos(GraficoativosadmissaoB,
                                           colunadataframe="Competencia",
                                           orientação= "v",
                                           titulodografico= "Colaboradores Ativos - H2F",)
                                           #filtroadmissaosituacao8=filtroadmissao_ativos8,)
                                           #filtroadmissaomês=filtroadmissao_mês1)
               # GraficoativosadmissaoC,GraficoativosadmissaoD = st.columns((0.01,1))
                #self.testeterceiroadmissao(GraficoativosadmissaoD,
                                           
                            #               filtromêsadmissao = filtroadmissao_mês1)
                                           #filtroadmissaosituacao8=filtroadmissao_ativos8,)
                                           #filtroadmissaomês=filtroadmissao_mês1)                          

#obs.: gáfico horizontal - Cargo
                
                '''colunatitulo1, colunatitulo2,colunatitulo3 = st.columns((0.2,1,0.01))
                with colunatitulo2:
                    colunatitulo2.title("Custo de Admissões por Cargo")

                
                GraficocargoadmissaoA,GraficocargoadmissaoB = st.columns((1,0.01))
                self.Graficocargoadmissao(GraficocargoadmissaoA,
                                          colunadataframe= "nome_cargo",
                                          orientação= "h",
                                          titulodografico="Custo de Admissões por Cargo",
                                          filtromêsadmissao=  filtroadmissao_mês1)'''
                
        #obs.: gáfico horizontal - Serviços
                #GraficoserviçoadmissaoA,GraficoserviçoadmissaoB = st.columns((1,0.01))
                #self.Graficoserviçoadmissao1(GraficoserviçoadmissaoB,
                                            #colunadataframe="nome_quebra",
                                            #orientação= "h",
                                            #titulografico= "Serviços que mais admitiram",
                                            #filtromêsadmissao= filtroadmissao_mês1)

#####FORMATAÇÃO DA TERCEIRA PÁGINA - RESCISÕES:____________________________________________________________   
        elif choose == "Rescisão":
            with open('style.css') as f:
               st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
            st.title('Resumo de Rescisões') 
            filtrosrescisaocolunas1,filtrosrescisaocolunas2,filtrosrescisaocolunas3 = st.columns([1.5,1.5,1.5])


        ###DEFINIÇÃO DE FILTROS - RESCISÕES:____________________________________________________________

            RESCISAO = DadosRescisao()
            filtrorescisao_mês = RESCISAO["Data"].unique()
            filtrorescisao_mês = np.append(["Todos"], filtrorescisao_mês)
            filtrorescisao_serviço = RESCISAO["Contrato"]. unique()
            filtrorescisao_serviço = np.append(["Todos"], filtrorescisao_serviço)
            filtrorescisao_centrodecusto = RESCISAO["Centro de Custo"].unique()
            filtrorescisao_centrodecusto = np.append(["Todos"], filtrorescisao_centrodecusto)

            with filtrosrescisaocolunas1:
                filtrorescisao_mês1 = st.selectbox(
                    "Escolha o mês",
                    filtrorescisao_mês,
                    help = "A incluir",
                    key= "Rescisão_1",
                    index= 0)
                    
            with filtrosrescisaocolunas2:
                filtrorescisao_serviço1 = st.selectbox(
                    "Escolha a empresa",
                    filtrorescisao_serviço,
                    help = "A incluir",
                    key= "Rescisão_2",
                    index= 0)
                
            with filtrosrescisaocolunas3:
                filtrorescisao_centrodecusto1 = st.selectbox(
                    "Escolha o Centro de Custo",
                    filtrorescisao_centrodecusto,
                    help = "A incluir",
                    key= "Rescisão_3",
                    index= 0) 

#####CHAMADOR DE FUNÇÕES - RESCISAO:____________________________________________________________
            colunarescisaoA,colunarescisaoB,colunarescisaoC = st.columns((1,1,1)) 

        ###CHAMADOR DE FUNÇÕES - CARD valor total RESCISÕES:____________________________________________________________
            colunarescisaoA.metric(label="Valor Total de Rescisão", value= self.Rescisoes(filtroservicorescisao=filtrorescisao_serviço1, 
                                                                                          filtrocentrodecustorescisao=filtrorescisao_centrodecusto1))
        
        ###CHAMADOR DE FUNÇÕES - CARD valor de despesas RESCISÕES:____________________________________________________________
            colunarescisaoB.metric(label="Valor das despesas", value=self.Rescisoes2(tipo="descontos",
                                                                                  filtrorescisao_mês=filtrorescisao_mês1))
        
        ###CHAMADOR DE FUNÇÕES - CARD valor de proventos RESCISÕES:____________________________________________________________
            colunarescisaoC.metric(label="Valor dos Proventos", value=self.Rescisoes3(tipo2="proventos",
                                                                                      filtrorescisao_mês=filtrorescisao_mês1))

#####CHAMADOR DE FUNÇÕES - GRÁFICO 1,2 e 3 RESCISÕES:____________________________________________________________
        ##obs: Gráfico vertical = Evolução mensal
            colgraficorescisao1,colgraficorescisao0 = st.columns((1,0.01)) 
            self.Graficoevolucaomensalrescisao(colgraficorescisao1,
                                           colunadataframe='Data',
                                           orientação= "v",
                                           titulodografico="Quantidade Mensal de Rescisões",
                                           filtroserviçorescisao=filtrorescisao_serviço1,
                                           filtrocentrodecustorescisao=filtrorescisao_centrodecusto1)
            
        ##obs: Gráfico Horinzontal = Serviço
            colgraficorescisao2, colgraficorescisao00 = st.columns((1,0.01))
            self.Graficoserviço_rescisao(colgraficorescisao2,
                                     colunadataframe= "Contrato",
                                     orientação= "h",
                                     titulodografico= "Custo de Rescisões por Centro de Serviço",
                                     filtro_mêsrescisao = filtrorescisao_mês1
                                     )
            
        ##obs: Gráfico Horinzontal = Serviço
            colgraficorescisao3,colgraficorescisao000 = st.columns((1,0.01))
            self.Graficocentrodecusto_rescisao(colgraficorescisao3,
                                           colunadataframe="Centro de Custo",
                                           orientação="h",
                                           titulodografico="Custo de Rescisões por Centro de Custo",
                                           filtro_mêsrescisao=filtrorescisao_mês1)

#####FORMATAÇÃO DA QUARTA PÁGINA - FÉRIAS:____________________________________________________________   
        
        elif choose == "Férias": #Bloco de código Férias - tudo será dentro dele
            with open('style.css') as f:
               st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
            st.title('Resumo de Férias') #Definição do título da página

            filtrosferiascolunas1,filtrosferiascolunas2,filtrosferiascolunas3 = st.columns([1.5,1.5,1.5]) #definição de colunas para as próximas informações nesta página e tamanho (em pixel)


        ###DEFINIÇÃO DE FILTROS - FÉRIAS:____________________________________________________________
            FERIAS = DadosFerias() #Criação de Dataframe. nomeado neste projeto como "FÉRIAS" por ser o nome da página e assim facilitar na compreensão
            filtro_mês = FERIAS["sq_dataini"].unique() #Criação do filtro mês que será puxado na planilha nomeada como "sq_dataini", "unique()" irá remover toda a duplicata
            filtro_mês = np.append(["Todos"], filtro_mês) #"np.append" para adicionar algum item a ser filtrado devendo ser adicionado dentro de ["","",""]
            filtro_empresa = FERIAS["sq_nome_servico"].unique() #Criação do filtro mês que será puxado na planilha nomeada como "sq_nome_servico", "unique()" irá remover toda a duplicata
            filtro_empresa = np.append(['Todos'], filtro_empresa) #"np.append" para adicionar algum item a ser filtrado devendo ser adicionado dentro de ["","",""]
            filtro_centrodecusto = FERIAS["sq_nome_ccustos"].unique() #Criação do filtro mês que será puxado na planilha nomeada como "sq_nome_servico", "unique()" irá remover toda a duplicata
            filtro_centrodecusto = np.append(["Todos"], filtro_centrodecusto) #"np.append" para adicionar algum item a ser filtrado devendo ser adicionado dentro de ["","",""]
    

            with filtrosferiascolunas1: #posição do filtro de acordo com as colunas definidas anteriormente
                filtro_mêsferias = st.selectbox( #novo dataframe para o pacote de filtro
                    "Escolha o mês", #nome/frase que identificará o filtro
                    filtro_mês, #objeto/variáve
                    help="A incluir", #mensagem de suporte
                    key= "Férias_1", #nome do filtro
                    index = 0) #ele irá selecionar o item n° x da lista
            
            with filtrosferiascolunas2: #posição do filtro de acordo com as colunas definidas anteriormente
                filtro_serviçoferias = st.selectbox(  #novo dataframe para o pacote de filtro
                    "Escolha o Serviço",  #nome/frase que identificará o filtro
                    filtro_empresa, #objeto/variáve
                    help= "A incluir", #mensagem de suporte
                    index= 0, #ele irá selecionar o item n° x da lista
                    key= "Férias_2",) #nome do filtro

            with filtrosferiascolunas3: #posição do filtro de acordo com as colunas definidas anteriormente
                filtro_centrodecustoferias = st.selectbox( #novo dataframe para o pacote de filtro
                    "Escolha o Centro de Custo",
                    filtro_centrodecusto, #objeto/variáve
                    help= "A incluir", #mensagem de suporte
                    index= 0,  #ele irá selecionar o item n° x da lista
                    key= "Férias_3",) #nome do filtro
                

###CHAMADOR DE FUNÇÕES - FÉRIAS:____________________________________________________________

        ###CHAMADOR DE FUNÇÕES - CARD valor total FÉRIAS:____________________________________________________________
            colunaferiasA, colunaferiasB,colunaferiasC = st.columns((1,1,1)) #Para a inserção do card foi necessário a criação de novas definições das colunas da página
            colunaferiasA.metric(label= "Valor Total de Férias", value= self.Ferias(filtro_serviçoferias,filtro_centrodecustoferias)) #... para gerar um card com a somatória do serviço e centro de custo. sendo, "label = "valor total" - o nome do card e o "value = self.ferias" a base de dados
        ###CHAMADOR DE FUNÇÕES - CARD descontos FÉRIAS:____________________________________________________________

            #colunaferiasA, colunaferiasB,colunaferiasC = st.columns((1,1,1)) #Para a inserção do card foi necessário a criação de novas definições das colunas da página
            colunaferiasB.metric(label= "Descontos", value= self.Ferias2(tipo="descontos", 
                                                                         filtro_mêsferias=filtro_mêsferias
                                                                         )) #... para gerar um card com a somatória do serviço e centro de custo. sendo, "label = "valor total" - o nome do card e o "value = self.ferias" a base de dados
       
        ###CHAMADOR DE FUNÇÕES - CARD proventos FÉRIAS:____________________________________________________________
            colunaferiasC.metric(label= "Proventos", value= self.Ferias3(tipo1="proventos", 
                                                                         filtro_mêsferias=filtro_mêsferias
                                                                         ))

 ###CHAMADOR DE FUNÇÕES - GRÁFICO 1,2 e 3 FÉRIAS:____________________________________________________________
        ##obs: Gráfico vertical - Evolução mensal
            Graficoevolucaomensalferias5,Graficoevolucaomensalferias6 = st.columns((1,0.01)) #Definição de colunas e seus tamanhos 
            self.Graficoevolucaomensalferias(Graficoevolucaomensalferias5, #chamador da coluna criada
                                      colunadodataframe="sq_dataini",
                                      orientação="v",
                                      titulodografico="Quantidade Mensal de Férias",
                                      filtroservicoferias=filtro_serviçoferias,
                                      filtrocentrodecustoferias=filtro_centrodecustoferias)
        ##obs: Gráfico horizontal - Serviços
            Colunaparagraficoferias1,Colunaparagraficoferias2 = st.columns((1,0.01)) #Definição de colunas e seus tamanhos 
            self.Graficoserviço_ferias(Colunaparagraficoferias1, #chamador da coluna criada
                                       colunadodataframe="sq_nome_servico", #atalho presente no código do gráfico e nome da coluna que será selecionada
                                       orientação="h", #orientação do gráfico - horizontal
                                       titulodografico="Custo de Férias por Centro de Serviço",
                                       filtro_mêsferias=filtro_mêsferias) #, inserir filtro_serviçoferias, filtro_centrodecustoferias - caso va puxar dos filtros
            
        ##obs: Gráfico vertical - Centro de custo
            Colunaparagraficoferias3,Colunaparagraficoferias4 = st.columns((1,0.01)) #Definição de colunas e seus tamanhos 
            self.Graficocentrodecusto_ferias(Colunaparagraficoferias3, #chamador da coluna criada
                                       colunadodataframe="sq_nome_ccustos", #atalho presente no código do gráfico e nome da coluna que será selecionada
                                       orientação="v" , #orientação do gráfico - vertical
                                       titulodografico="Custo de Férias por Centro de Custo",
                                       filtro_mêsferias=filtro_mêsferias) #, inserir filtro_serviçoferias, filtro_centrodecustoferias - caso va puxar dos filtros

 
objeto=apresentacao()
objeto.Apresentacao()
