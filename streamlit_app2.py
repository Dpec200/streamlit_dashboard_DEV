# Importamos las librerias a utilizar
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.dates import DateFormatter, DayLocator


# Configuramos la página
st.set_page_config(
    page_title="Dashboard Desarrollos PEC",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
    )

try:
    businessnumber = st.experimental_get_query_params()
    businessnumber = int(businessnumber['token'][0])
except:
    st.stop()

# Función principal
def main():

    # Conexión a la base de datos
    db_username = st.secrets["DB_USERNAME"]
    db_password = st.secrets["DB_PASSWORD"]
    db_host = st.secrets["DB_HOST"]
    db_token = st.secrets["DB_TOKEN"]
    # Creamos la conexión
    conexion_string = f"mysql+pymysql://{db_username}:{db_password}@{db_host}/{db_token}"
    engine = create_engine(conexion_string,pool_pre_ping=True)
    # Query de consulta para la contraseña
    query = """
            SELECT DISTINCT businessPhoneNumber
            FROM clientes ;
    """
    df_password = pd.read_sql(query, engine)

    # Función para verificar la contraseña ingresada
    def verificar_contraseña(businessnumber):
        for elemento in df_password["businessPhoneNumber"]:
            if (businessnumber == int(elemento)):
                return True
            else:
                pass
        return False
    
    if not verificar_contraseña(businessnumber=businessnumber):
        st.stop()

    # SNACKYS
    def recompra_snackys():
        # Conexión a la base de datos
        db_username = st.secrets["DB_USERNAME"]
        db_password = st.secrets["DB_PASSWORD"]
        db_host = st.secrets["DB_HOST"]
        db_token = st.secrets["DB_TOKEN"]
        conexion_string = f"mysql+pymysql://{db_username}:{db_password}@{db_host}/{db_token}"
        engine = create_engine(conexion_string,pool_pre_ping=True)
        # Query de recompra
        query = f"""
                SELECT e.*, c.businessPhoneNumber, c.clientName, c.userPhoneNumber
                FROM experiencias e
                JOIN clientes c ON (e.idCliente = c.idCliente)
                WHERE e.journeyClassName IN ('GenerarRecompraGenteInactiva' ,'PreguntaSiClientePudoComprar', 'RecordatorioClienteQuiereRecomprar') AND c.businessPhoneNumber = {businessnumber} ;
                """
        df_recompra = pd.read_sql(query, engine)
        df_recompra.drop("hora",axis=1,inplace=True)
        # Aquí también ocultamos el DF
        #st.write("Dataframe")
        #st.dataframe(df_recompra)
        st.title("Dashboard Recompra")
        if (len(df_recompra) > 0 ):
            cliente_pec = df_recompra['clientName'].unique().tolist()
            st.subheader(f"Bienvenido {cliente_pec[0]}")
        st.write("---")

        # gráfico de torta
        torta = df_recompra[(df_recompra["journeyClassName"] == "GenerarRecompraGenteInactiva") & (df_recompra["journeyStep"] == "RespuestaMensajeInicial")]
        # Contamos la cantidad de + o - de recompra
        recompras = {"Positiva":     torta[torta["msgBody"].str.contains("\+")].shape[0] ,
                    "Negativa":    torta[torta["msgBody"].str.contains("\-")].shape[0]
                    }

        # Tarjetas
        # Cantidad de conversaciones
        cantidad_conversaciones = len(df_recompra.loc[(df_recompra["journeyClassName"] == "GenerarRecompraGenteInactiva") & (df_recompra["journeyStep"] == "RespuestaMensajeInicial")])
        # Conversaciones terminadas
        conversaciones_terminadas = len(df_recompra[df_recompra["msgBody"].str.contains("ff")])
        # Conversaciones incompletas
        conversaciones_incompletas = cantidad_conversaciones - conversaciones_terminadas
        # Intencion de recompra
        intencion_recompra = len(df_recompra.loc[(df_recompra["journeyStep"] == "RespuestaMensajeInicial") &  (df_recompra["msgBody"] == "Si, me encantaría (+)")]) 
        # Recompra exitosa
        recompra_exitosa = len(df_recompra.loc[(df_recompra["journeyClassName"] == "PreguntaSiClientePudoComprar")& (df_recompra["journeyStep"] == "RespuestaClienteQuiereComprarProducto") & (df_recompra["msgBody"].str.contains("\+"))]) + len(df_recompra.loc[(df_recompra["journeyClassName"] == "RecordatorioClienteQuiereRecomprar") & (df_recompra["msgBody"].str.contains("\+"))])
        # Tia Snackys
        tia_snackys =  len(df_recompra.loc[(df_recompra["msgBody"].str.contains("Tia Snackys"))])

        # Crear 5 tarjetas en la primera fila
        col1, col2, col3, col4 = st.columns(4)

        # Estilos CSS personalizados
        custom_css = """
        <style>
            .tarjeta {
                padding: 20px;
                border-radius: 5px;
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
                background-color: #f9f9f9;
                text-align: center;
            }
            .subheader {
                font-size: 20px;
                font-weight: bold;
                color: #333;
            }
        </style>
        """
        # Agregar el estilo CSS personalizado utilizando st.markdown
        st.markdown(custom_css, unsafe_allow_html=True)
    
        # Variable de ejemplo con estilos en línea
        tarjeta1 = f'<div class="tarjeta" style="font-size: 30px; color: #00008B;">{cantidad_conversaciones}</div>'
        tarjeta2 = f'<div class="tarjeta" style="font-size: 30px; color: #00008B;">{intencion_recompra}</div>'
        tarjeta3 = f'<div class="tarjeta" style="font-size: 30px; color: #00008B;">{recompra_exitosa}</div>'
        tarjeta4 = f'<div class="tarjeta" style="font-size: 30px; color: #00008B;">{tia_snackys}</div>'

        # Contenido de las tarjetas
        with col1:
            st.markdown('<div class="subheader">Cantidad de conversaciones</div>', unsafe_allow_html=True)
            st.markdown(tarjeta1, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            st.write(f"+ Conversaciones terminadas: **{conversaciones_terminadas}**")
            st.write(f"+ Conversaciones incompletas: **{conversaciones_incompletas}**")

        with col2:
            st.markdown('<div class="subheader">Intención de recompra</div>', unsafe_allow_html=True)
            st.markdown(tarjeta2, unsafe_allow_html=True)
            st.markdown('</div></div>', unsafe_allow_html=True)

        with col3:
            st.markdown('<div class="subheader">Recompra exitosa</div>', unsafe_allow_html=True)
            st.markdown(tarjeta3, unsafe_allow_html=True)
            st.markdown('</div></div>', unsafe_allow_html=True)

        with col4:
            st.markdown('<div class="subheader">Tia Snackys</div>', unsafe_allow_html=True)
            st.markdown(tarjeta4, unsafe_allow_html=True)
            st.markdown('</div></div>', unsafe_allow_html=True)
            ver_clientes = st.checkbox("Mostrar clientes")

        st.write("---")

    
        col5, col6 = st.columns(2)

        with col5 :
            # gráfico de cantidad de mensajes por fecha
            df_recompra['fecha'] = pd.to_datetime(df_recompra['fecha'])
            registros_por_dia = df_recompra['fecha'].value_counts().reset_index()
            registros_por_dia.columns = ['fecha', 'cantidad']
            fig, ax = plt.subplots()
            fig.set_size_inches(6, 3) 
            sns.set(style="whitegrid")
            ax = sns.lineplot(x="fecha", y="cantidad", marker='o', color='b',data=registros_por_dia,linewidth=4)
            plt.xlabel('')
            plt.ylabel('')
            date_form = DateFormatter("%d/%m")
            ax.xaxis.set_major_formatter(date_form)
            #plt.tight_layout() 
            gráfico_fecha = plt.gcf()
            st.write("#### **Total de mensajes**")
            st.pyplot(gráfico_fecha)

        with col6:
            if len(df_recompra) > 0 :
                # Extrae las etiquetas y los valores del diccionario
                etiquetas = list(recompras.keys())
                valores = list(recompras.values())
                total = sum(valores)
                # Colores para el gráfico
                colores = ['tab:green', 'tab:red']
                plt.figure(figsize=(6, 3))  
                sns.set(style="whitegrid")
                # Crea el gráfico de torta
                plt.pie(valores, labels=etiquetas, colors=colores, autopct=lambda p: '{:.0f} ({:.1f}%)'.format(p * total / 100, p), startangle=90)
                plt.axis('equal')  # Hace que el gráfico sea circular
                gráfico_torta = plt.gcf()
                st.write("#### **Intenciones de recompra**")
                st.pyplot(gráfico_torta)
            else:
                st.write("sin datos")

        
        st.write("---")

        if (len(df_recompra) > 0):
            # gráfico de barras horizontales de categorias 
            filtro = (df_recompra["msgBody"].str.contains("pp"))
            data_counts = df_recompra.loc[filtro, "msgBody"].value_counts().reset_index()
            data_counts.loc[(data_counts["msgBody"].str.contains("sazonador")),"msgBody" ] = "Sazonador"
            data_counts.loc[(data_counts["msgBody"].str.contains("snack hipoalergénico")),"msgBody" ] = "Snack Hipoalergénico"
            data_counts.loc[(data_counts["msgBody"].str.contains("masticable")),"msgBody" ] = "Masticable"
            data_counts.loc[(data_counts["msgBody"].str.contains("snacks liofinizados")),"msgBody" ] = "Snacks Liofinizados"
            data_counts.loc[(data_counts["msgBody"].str.contains("Busco algo para dar como premio")),"msgBody" ] = "Busco algo para dar como premio"
                        # Configura el estilo de Seaborn (opcional)
            sns.set(style="whitegrid")
            # Crea el gráfico de barras horizontales
            plt.figure(figsize=(10, 6))  # Ajusta el tamaño del gráfico si es necesario
            barplot = sns.barplot(x="count", y="msgBody",data=data_counts, orient="h")
            # Agrega etiquetas y título
            plt.xlabel("")
            plt.ylabel("")
            gráfico_productos = plt.gcf()
            st.write("#### **Productos más seleccionados**")
            st.pyplot(gráfico_productos)
        else: 
             st.write("sin datos")

        st.write("---")
        
        # para ver clientes de tia snackys
        if ver_clientes :
            st.markdown("## **Clientes que buscan contacto con Tia Snackys**:")
            df_tia = df_recompra.loc[(df_recompra["msgBody"].str.contains("Tia Snackys")),["fecha","userPhoneNumber"]]
            st.dataframe(df_tia)

        st.write("---")


    # SNACKYS
    def oferta_snackys():
        # Conexión a la base de datos
        db_username = st.secrets["DB_USERNAME"]
        db_password = st.secrets["DB_PASSWORD"]
        db_host = st.secrets["DB_HOST"]
        db_token = st.secrets["DB_TOKEN"]
        conexion_string = f"mysql+pymysql://{db_username}:{db_password}@{db_host}/{db_token}"
        engine = create_engine(conexion_string,pool_pre_ping=True)
        # Query de recompra
        query = f"""
                SELECT e.* , c.businessPhoneNumber, c.clientName, c.userPhoneNumber
                FROM experiencias e
                JOIN clientes c ON (e.idCliente = c.idCliente)
                WHERE e.journeyClassName = 'SnackyOfertas' AND c.businessPhoneNumber = {businessnumber} ;
                """
        df_oferta_snackys = pd.read_sql(query, engine)
        df_oferta_snackys.drop("hora",axis=1,inplace=True)
        # Aquí también ocultamos el DF
        #st.write("Dataframe")
        #st.dataframe(df_oferta_snackys)
        st.title("Dashboard ofertas")
        if (len(df_oferta_snackys) > 0 ):
            cliente_pec = df_oferta_snackys['clientName'].unique().tolist()
            st.subheader(f"Bienvenido {cliente_pec[0]}")
        st.write("---")

        # gráfico de torta
        torta = df_oferta_snackys[(df_oferta_snackys["journeyStep"] == "RespuestaMensajeInicial")]
        # Contamos la cantidad de suscriptos
        subs = {"Suscriptos":     torta[torta["msgBody"] == '1'].shape[0],
                "No suscriptos":    torta[torta["msgBody"] == '0'].shape[0]
                    }

        # Tarjetas
        # Cantidad de conversaciones
        cantidad_conversaciones = len(df_oferta_snackys.loc[(df_oferta_snackys["journeyStep"] == "RespuestaMensajeInicial")].reset_index())
        # motivos_clientes_no_interesados
        con_motivo_no_interesados1 = len(df_oferta_snackys.loc[(df_oferta_snackys["journeyStep"] == "RespuestaMotivoClienteParaNoSuscripcion")].reset_index()) 
        con_motivo_no_interesados = f"{con_motivo_no_interesados1} de {subs['No suscriptos']}" 
        # Intencion de no dejar motivos
        sin_motivo_no_interesado = len((df_oferta_snackys['msgBody'] == 0) & (df_oferta_snackys['journeyStep'] == 'RespuestaClienteQuiereDejarMotivo'))
        # Conversaciones terminadas
        # conversaciones_terminadas = len(df_oferta_snackys[df_oferta_snackys["msgBody"].str.contains("ff")]) + motivos_clientes_no_interesados1
        # Conversaciones_incompletas 
        # conversaciones_incompletas = cantidad_conversaciones - conversaciones_terminadas
        # clientes suscriptos
        clientes_suscriptos = subs["Suscriptos"]
        # Clientes prefieren 'dejar de recibir'
        clientes_dejar_de_recibir = len(df_oferta_snackys[df_oferta_snackys['msgBody'] == 'dejar de recibir'])
        # Crear 5 tarjetas en la primera fila
        col1, col2, col3, col4= st.columns(4)

        # Estilos CSS personalizados
        custom_css = """
        <style>
            .tarjeta {
                padding: 20px;
                border-radius: 5px;
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
                background-color: #f9f9f9;
                text-align: center;
            }
            .subheader {
                font-size: 20px;
                font-weight: bold;
                color: #333;
            }
        </style>
        """
        custom_css2 = """ 
        <style>
            .ag-format-container {
            width: 1142px;
            margin: 0 auto;
            }


            body {
            background-color: #000;
            }
            .ag-courses_box {
            display: -webkit-box;
            display: -ms-flexbox;
            display: flex;
            -webkit-box-align: start;
            -ms-flex-align: start;
            align-items: flex-start;
            -ms-flex-wrap: wrap;
            flex-wrap: wrap;

            padding: 50px 0;
            }
            .ag-courses_item {
            -ms-flex-preferred-size: calc(25% - 30px);
            flex-basis: calc(25% - 30px);

            margin: 0 15px 30px;

            overflow: hidden;

            border-radius: 28px;
            }
            .ag-courses-item_link {
            display: block;
            background-color: #000;

            overflow: hidden;

            position: relative;
            }
            .ag-courses-item_link:hover,
            .ag-courses-item_link:hover .ag-courses-item_date {
            text-decoration: none;
            color: #FFF;
            }
            .ag-courses-item_link:hover .ag-courses-item_bg {
            -webkit-transform: scale(10);
            -ms-transform: scale(10);
            transform: scale(10);
            }
            .ag-courses-item_title {
            margin: 0 0 25px;

            overflow: hidden;

            font-weight: bold;
            font-size: 23px;
            color: #FFFFFF;
            text-align: center;


            z-index: 2;
            position: relative;
            }
            .ag-courses-item_date-box {
            font-size: 18px;
            color: #C4C5AE;

            z-index: 2;
            position: relative;
            }
            .ag-courses-item_date {
            font-weight: bold;
            color: #FFC641;
            text-align: center;

            -webkit-transition: color .5s ease;
            -o-transition: color .5s ease;
            transition: color .5s ease
            }
            .ag-courses-item_bg {
            height: 128px;
            width: 128px;
            background-color: #E5A102;

            z-index: 1;
            position: absolute;
            top: -200px;
            right: -200px;

            border-radius: 50%;

            -webkit-transition: all .5s ease;
            -o-transition: all .5s ease;
            transition: all .5s ease;
            }

            .adjustable-text {
                font-size: 100%; /* Puedes ajustar el valor según sea necesario */
            }

            .ag-courses_item:nth-child(2n) .ag-courses-item_bg {
            background-color: #3ecd5e;
            }
            .ag-courses_item:nth-child(3n) .ag-courses-item_bg {
            background-color: #e44002;
            }
            .ag-courses_item:nth-child(4n) .ag-courses-item_bg {
            background-color: #952aff;
            }
            .ag-courses_item:nth-child(5n) .ag-courses-item_bg {
            background-color: #cd3e94;
            }
            .ag-courses_item:nth-child(6n) .ag-courses-item_bg {
            background-color: #4c49ea;
            }



            @media only screen and (max-width: 979px) {
            .ag-courses_item {
                -ms-flex-preferred-size: calc(50% - 30px);
                flex-basis: calc(50% - 30px);
            }
            .ag-courses-item_title {
                font-size: 24px;
            }
            }

            @media only screen and (max-width: 767px) {
            .ag-format-container {
                width: 96%;
            }

            }
            @media only screen and (max-width: 639px) {
            .ag-courses_item {
                -ms-flex-preferred-size: 100%;
                flex-basis: 100%;
            }
            .ag-courses-item_title {
                min-height: 72px;
                line-height: 1;

                font-size: 24px;
            }
            .ag-courses-item_link {
                padding: 22px 40px;
            }
            .ag-courses-item_date-box {
                font-size: 16px;
            }
            }
        </style>
        """

        # Agregar el estilo CSS personalizado utilizando st.markdown
        st.markdown(custom_css2, unsafe_allow_html=True)
    
        # Variable de ejemplo con estilos en línea
        tarjeta1 = f'<div class="ag-format-container"><div class="ag-courses_box"><div class="ag-courses_item"><div href="#" class="ag-courses-item_link"><div class="ag-courses-item_bg"></div><div class="ag-courses-item_title"><span class="adjustable-text"> Clientes Subscritos <br><br>{clientes_suscriptos}</span></div></div></div></div></div></div>'
        tarjeta2 = f'<div class="ag-format-container"><div class="ag-courses_box"><div class="ag-courses_item"><div href="#" class="ag-courses-item_link"><div class="ag-courses-item_bg"></div><div class="ag-courses-item_title"><span class="adjustable-text"> Clientes que se dieron de baja <br>{clientes_dejar_de_recibir}</span></div></div></div></div></div></div>'
        tarjeta3 = f'<div class="ag-format-container"><div class="ag-courses_box"><div class="ag-courses_item"><div href="#" class="ag-courses-item_link"><div class="ag-courses-item_bg"></div><div class="ag-courses-item_title"><span class="adjustable-text"> Clientes que dejaron motivos <br>{con_motivo_no_interesados}</span></div></div></div></div></div></div>'
        tarjeta4 = f'<div class="ag-format-container"><div class="ag-courses_box"><div class="ag-courses_item"><div href="#" class="ag-courses-item_link"><div class="ag-courses-item_bg"></div><div class="ag-courses-item_title"><span class="adjustable-text"> Clientes que no dejaron motivos <br>{sin_motivo_no_interesado}</span></div></div></div></div></div></div>'

        # Contenido de las tarjetas
        with col1:
            # st.markdown('<div class="ag-courses-item_title">Cantidad de clientes que dejaron motivos</div>', unsafe_allow_html=True)
            st.markdown(tarjeta1, unsafe_allow_html=True)
            # st.markdown('</div>', unsafe_allow_html=True)
            # st.write(f"+ Conversaciones terminadas: **{conversaciones_terminadas}**")
            # st.write(f"+ Conversaciones incompletas: **{conversaciones_incompletas}**")

        with col2:
            # st.markdown('<div class="ag-courses-item_title">Clientes suscriptos</div>', unsafe_allow_html=True)
            st.markdown(tarjeta2, unsafe_allow_html=True)
            # st.markdown('</div></div>', unsafe_allow_html=True)

        with col3:
            # st.markdown('<div class="ag-courses-item_title">Clientes que se dieron de baja</div>', unsafe_allow_html=True)
            st.markdown(tarjeta3, unsafe_allow_html=True)
            # st.markdown('</div></div>', unsafe_allow_html=True)

        with col4:
            # st.markdown('<div class="ag-courses-item_title">Clientes que no dejaron motivos</div>', unsafe_allow_html=True)
            st.markdown(tarjeta4, unsafe_allow_html=True)
            # st.markdown('</div></div>', unsafe_allow_html=True)
            # ver_motivos = st.checkbox("Mostrar motivos")
            
        st.write("---")

    
        col4, col5 = st.columns(2)

        with col4 :
            # gráfico de cantidad de mensajes por fecha
            df_oferta_snackys['fecha'] = pd.to_datetime(df_oferta_snackys['fecha'])
            registros_por_dia = df_oferta_snackys['fecha'].value_counts().reset_index()
            registros_por_dia.columns = ['fecha', 'cantidad']
            fig, ax = plt.subplots()
            fig.set_size_inches(6, 3) 
            sns.set(style="whitegrid")
            ax = sns.lineplot(x="fecha", y="cantidad", marker='o', color='b',data=registros_por_dia,linewidth=4)
            plt.xlabel('')
            plt.ylabel('')
            date_form = DateFormatter("%d/%m")
            ax.xaxis.set_major_formatter(date_form)
            #plt.tight_layout() 
            gráfico2 = plt.gcf()
            st.write("#### **Total de mensajes**")
            st.pyplot(gráfico2)

        with col5:
            if len(df_oferta_snackys) > 0 :
                # Extrae las etiquetas y los valores del diccionario
                etiquetas = list(subs.keys())
                valores = list(subs.values())
                total = sum(valores)
                # Colores para el gráfico
                colores = ['tab:green', 'tab:red']
                plt.figure(figsize=(6, 3))  
                sns.set(style="whitegrid")
                # Crea el gráfico de torta
                plt.pie(valores, labels=etiquetas, colors=colores, autopct=lambda p: '{:.0f} ({:.1f}%)'.format(p * total / 100, p), startangle=90)
                plt.axis('equal')  # Hace que el gráfico sea circular
                gráfico11 = plt.gcf()
                st.write("#### **Porcentaje de suscriptos**")
                st.pyplot(gráfico11)
            else:
                st.write("sin datos")


        st.write("---")
 
        # if ver_motivos:
        #     st.markdown("## **Comentarios**:")
        #     motivos_clientes = df_oferta_snackys.loc[(df_oferta_snackys["journeyStep"] == "RespuestaMotivoClienteParaNoSuscripcion") ,"userPhoneNumber"].reset_index()
        #     motivos_clientes = sorted(motivos_clientes["userPhoneNumber"].unique().tolist())
        #     motivos_clientes.insert(0, "Todos")
        #     seleccion_cliente = st.selectbox("Clientes", motivos_clientes)
        #     if (seleccion_cliente == "Todos"):
        #         msgbody_feedback1 = df_oferta_snackys.loc[(df_oferta_snackys["journeyStep"] == "RespuestaMotivoClienteParaNoSuscripcion") ,"msgBody"].str.capitalize()
        #         for elemento1 in msgbody_feedback1 :
        #             st.write(f"+ {elemento1}")
        #     else:
        #         msgbody_feedback = df_oferta_snackys.loc[(df_oferta_snackys["journeyStep"] == "RespuestaMotivoClienteParaNoSuscripcion") & (df_oferta_snackys["userPhoneNumber"] == seleccion_cliente), "msgBody"].str.capitalize()
        #         for elemento in msgbody_feedback :
        #             st.write(f"+ {elemento}")
                    
        st.write("---")

    # Snackys
    opciones_paginas_snackys = ["Ofertas", "Recompra"]
    # pagina_seleccionada = st.sidebar.selectbox("Selecciona una página:", opciones_paginas_snackys)
    pagina_seleccionada = st.selectbox("Selecciona una página:", opciones_paginas_snackys)
    # Mostrar páginas para Snackys
    # if pagina_seleccionada == "Inicio":
    #     pagina_inicio()
    if pagina_seleccionada == "Recompra":
        recompra_snackys()
    if pagina_seleccionada == "Ofertas" :
        oferta_snackys()
  

# Iniciar la aplicación
if __name__ == "__main__":
    main()