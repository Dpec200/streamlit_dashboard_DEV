# Importamos las librerias a utilizar
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.dates import DateFormatter, DayLocator
import numpy as np
import matplotlib.patches as mpatches


# Configuramos la página
st.set_page_config(
    page_title="Dashboard Desarrollos PEC",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
    )

try:
    token = st.experimental_get_query_params()
    token = str(token['token'][0])
except:
    st.stop()

# Función principal
def main():

    # Conexión a la base de datos
    db_username = st.secrets["DB_USERNAME"]
    db_password = st.secrets["DB_PASSWORD"]
    db_host = st.secrets["DB_HOST"]
    db_token = st.secrets["DB_TOKEN"]
    db_port = st.secrets["DB_PORT"]
    # Creamos la conexión
    conexion_string = f"mysql+pymysql://{db_username}:{db_password}@{db_host}:{db_port}/{db_token}"
    engine = create_engine(conexion_string,pool_pre_ping=True)
    # Query de consulta para la contraseña
    query = """
            SELECT DISTINCT businessPhoneNumber, token
            FROM clientes ;
    """
    df_password = pd.read_sql(query, engine)
    # Función para verificar la contraseña ingresada
    def verificar_contraseña(token):
        for elemento in df_password["token"]:
            if (token == str(elemento)):
                businessnumber = int(df_password['businessPhoneNumber'][df_password['token'] == token])
                return [True, businessnumber]
            else:
                pass
        return [False]
    
    if not verificar_contraseña(token=token)[0]:
        st.stop()
    else:
        businessnumber = verificar_contraseña(token=token)[1]
    custom_css = """ 
        <style>
            .ag-format-container {
            width: 1142px;
            margin: 0 auto;
            }

            body {
            background-color: #FFF;
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
            -ms-flex-preferred-size: calc(33.3333% - 30px);
            flex-basis: calc(33.3333% - 30px);
            border: 2px solid #15364C;

            margin: 0 15px 30px;

            overflow: hidden;

            border-radius: 28px;
            }
            .ag-courses_item_core_1 {
            -ms-flex-preferred-size: calc(40% - 30px);
            flex-basis: calc(40% - 30px);
            border: 2px solid #15364C;
            height: 14vh;

            margin-bottom: 1px;

            overflow: hidden;

            border-radius: 28px;
            }

            .ag-courses_item_gris_title {
            -ms-flex-preferred-size: auto;
            flex-basis: auto;
            height: auto;
            weight: auto;

            overflow: hidden;

            border-radius: 15px;
            }

            .ag-courses_item_gris_subtitle {
            -ms-flex-preferred-size: auto;
            flex-basis: auto;
            height: auto;
            weight: auto;
            overflow: hidden;

            border-radius: 15px;
            }

            .ag-courses_item_core_2 {
            border: 2px solid #15364C;
            display: inline-block;
            width: auto;
            height: auto;
            margin: 0 15px;

            overflow: hidden;

            border-radius: 28px;
            }
            .ag-courses-item_link {
            display: block;
            background-color: #FFF;

            overflow: hidden;

            position: relative;
            }

            .ag-courses-item_link_gris {
            display: block;
            background-color: #D1D1D1;

            overflow: hidden;

            position: relative;
            }

            .ag-courses-item_link_core {
            display: block;
            background-color: #F5B7B1;
            height: 14vh;
            overflow: hidden;
            margin-bottom: 1px;

            position: relative;
            }
            .ag-courses-item_link_core_2 {
            display: block;
            background-color: #F5B7B1;
            height: 40vh;
            overflow: hidden;

            position: relative;
            }

            .ag-courses-item_link:hover,
            .ag-courses-item_link:hover .ag-courses-item_date {
            text-decoration: none;
            color: #15364C;
            }
            .ag-courses-item_link:hover .ag-courses-item_bg {
            -webkit-transform: scale(10);
            -ms-transform: scale(10);
            transform: scale(10);
            }
            .ag-courses-item_title {
            margin: 10px 0 5px;

            overflow: hidden;

            font-weight: bold;
            font-size: 23px;
            color: #15364C;
            text-align: center;


            z-index: 2;
            position: relative;
            }

            .ag-courses-item_title_core {
            margin: 0 0 5px;

            overflow: hidden;

            font-weight: bold;
            font-size: 30px;
            color: #15364C;
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
            background-color: #F5B7B1;

            z-index: 1;
            position: absolute;
            top: -150px;
            right: -150px;

            border-radius: 50%;

            -webkit-transition: all .5s ease;
            -o-transition: all .5s ease;
            transition: all .5s ease;
            }

            .adjustable-text {
                font-size: 100%; /* Puedes ajustar el valor según sea necesario */
                margin: 0 0 0;
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

    # SNACKYS
    def recompra_snackys():
        # Conexión a la base de datos
        db_username = st.secrets["DB_USERNAME"]
        db_password = st.secrets["DB_PASSWORD"]
        db_host = st.secrets["DB_HOST"]
        db_token = st.secrets["DB_TOKEN"]
        db_port = st.secrets["DB_PORT"]
        conexion_string = f"mysql+pymysql://{db_username}:{db_password}@{db_host}:{db_port}/{db_token}"
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
        db_port = st.secrets["DB_PORT"]
        conexion_string = f"mysql+pymysql://{db_username}:{db_password}@{db_host}:{db_port}/{db_token}"
        engine = create_engine(conexion_string,pool_pre_ping=True)
        # Query de recompra
        query = f"""
                SELECT e.* , c.businessPhoneNumber, c.clientName, c.userPhoneNumber
                FROM experiencias e
                JOIN clientes c ON (e.idCliente = c.idCliente)
                WHERE e.journeyClassName = 'SnackyOfertasSuscripcion' AND c.businessPhoneNumber = {businessnumber} ;
                """
        df_oferta_snackys = pd.read_sql(query, engine)
        df_oferta_snackys.drop("hora",axis=1,inplace=True)
        # Aquí también ocultamos el DF
        #st.write("Dataframe")
        #st.dataframe(df_oferta_snackys)
        if (len(df_oferta_snackys) > 0 ):
            cliente_pec = df_oferta_snackys['clientName'].unique().tolist()
            st.markdown(f'<div class="ag-format-container"><div class="ag-courses_box"><div class="ag-courses_item_gris_title"><div href="#" class="ag-courses-item_link_gris"><span class="adjustable-text" style="font-size: 70px;">Dashboard de Ofertas <br></span><span class="adjustable-text" style="font-size: 40px;">Bienvenido {cliente_pec[0]}</span></div></div></div></div></div></div>',unsafe_allow_html=True)
            # st.subheader(f"Bienvenido {cliente_pec[0]}", class_="centered-subheader")
            # st.markdown(f'<div class="ag-format-container"><div class="ag-courses_box"><div class="ag-courses_item_gris_subtitle"><div href="#" class="ag-courses-item_link_gris"><span class="adjustable-text" style="font-size: 40px;">Bienvenido {cliente_pec[0]}</span></div></div></div></div></div></div>',unsafe_allow_html=True,)
        st.write("---")

        # gráfico de torta
        torta = df_oferta_snackys[(df_oferta_snackys["journeyStep"] == "RespuestaMensajeInicial") & (df_oferta_snackys['journeyClassName'] == 'SnackyOfertasSuscripcion')]
        # Contamos la cantidad de suscriptos
        subs = {"Suscriptos":     torta[torta["msgBody"] == '1'].shape[0],
                "No suscriptos":    torta[torta["msgBody"] == '2'].shape[0]
                    }

        # Tarjetas
        # Cantidad de conversaciones
        cantidad_conversaciones = len(df_oferta_snackys.loc[(df_oferta_snackys["journeyStep"] == "RespuestaMensajeInicial")].reset_index())
        # motivos_clientes_no_interesados
        con_motivo_no_interesados1 = len(df_oferta_snackys.loc[(df_oferta_snackys["journeyStep"] == "RespuestaMotivoClienteParaNoSuscripcion") & (df_oferta_snackys['journeyClassName'] == 'SnackyOfertasSuscripcion')].reset_index()) 
        con_motivo_no_interesados = f"{con_motivo_no_interesados1} de {subs['No suscriptos']}" 
        # Intencion de no dejar motivos
        sin_motivo_no_interesado = len(df_oferta_snackys[(df_oferta_snackys['msgBody'] == 2) & (df_oferta_snackys['journeyStep'] == 'RespuestaClienteQuiereDejarMotivo') & (df_oferta_snackys['journeyClassName'] == 'SnackyOfertasSuscripcion')])
        # Conversaciones terminadas
        # conversaciones_terminadas = len(df_oferta_snackys[df_oferta_snackys["msgBody"].str.contains("ff")]) + motivos_clientes_no_interesados1
        # Conversaciones_incompletas 
        # conversaciones_incompletas = cantidad_conversaciones - conversaciones_terminadas
        # clientes suscriptos
        clientes_suscriptos = subs["Suscriptos"]
        # Clientes prefieren 'dejar de recibir'
        clientes_dejar_de_recibir = len(df_oferta_snackys[df_oferta_snackys['msgBody'] == 'dejar de recibir'])
        # Estilos CSS personalizados
        
        # Agregar el estilo CSS personalizado utilizando st.markdown
        st.markdown(custom_css, unsafe_allow_html=True)
        st.markdown(f'<div class="ag-format-container"><div class="ag-courses_box"><div class="ag-courses_item_gris_title"><div href="#" class="ag-courses-item_link_gris"><span class="adjustable-text" style="font-size: 40px;">Informacion General</span></div></div></div></div></div></div>',unsafe_allow_html=True)
        col_core_1, col_core_2 = st.columns(2)
        tarjeta_clientes_contactados_col1 = f'<div class="ag-format-container"><div class="ag-courses_box"><div class="ag-courses_item_core_1"><div href="#" class="ag-courses-item_link_core"><div class="ag-courses-item_title_core"> Clientes Totales Contactados <br> Numero</div></div></div></div></div>'
        tarjeta_clientes_con_respuesta_col1 = f'<div class="ag-format-container"><div class="ag-courses_box"><div class="ag-courses_item_core_1"><div href="#" class="ag-courses-item_link_core"><div class="ag-courses-item_title_core"> Clientes con respuesta <br> Numero</div></div></div></div></div>'
        from io import BytesIO
        import base64

        # Genera un gráfico de Matplotlib
        def generar_grafico():
            # Extrae las etiquetas y los valores del diccionario
            etiquetas = list(subs.keys())
            valores = list(subs.values())
            
            total = sum(valores)
            # Colores para el gráfico
            colores = ['#2D8DEC', '#DFE2E5']
            plt.figure(figsize=(5, 3.5), facecolor='none')  
            # Crea el gráfico de torta
            plt.pie(x=valores, labels=etiquetas, colors=colores, autopct='%1.1f%%', startangle=90)
            plt.subplots_adjust(left=0.1, right=0.89, top=1, bottom=0.1)
            # Convierte el gráfico en una imagen
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            imagen_codificada = base64.b64encode(buffer.read()).decode()
            return imagen_codificada

        # Tarjeta con el gráfico de Matplotlib
        tarjeta_subscritos_vs_nosubscritos = f'<div class="ag-format-container"><div class="ag-courses_box"><div class="ag-courses_item_core_2"><div class="ag-courses-item_link_core_2"><div class="ag-courses-item_title_core">Clientes Subscritos VS No Subscritos</div><img src="data:image/png;base64,{generar_grafico()}" alt="Gráfico de Pastel"></div></div></div></div>'

        # Muestra la tarjeta en Streamlit
        with col_core_1:
            st.markdown(tarjeta_clientes_contactados_col1,unsafe_allow_html=True)
            st.markdown(tarjeta_clientes_con_respuesta_col1, unsafe_allow_html=True)

        with col_core_2:
            st.markdown(tarjeta_subscritos_vs_nosubscritos, unsafe_allow_html=True)

        st.write('---')
        st.markdown(f'<div class="ag-format-container"><div class="ag-courses_box"><div class="ag-courses_item_gris_subtitle"><div href="#" class="ag-courses-item_link_gris"><span class="adjustable-text" style="font-size: 40px;">Comportamiendo del cliente</span></div></div></div></div></div></div>',unsafe_allow_html=True)
        # Crear 5 tarjetas en la primera fila
        col1, col2, col3= st.columns(3)

        
    
        # Variable de ejemplo con estilos en línea
        tarjeta1 = f'<div class="ag-format-container"><div class="ag-courses_box"><div class="ag-courses_item"><div href="#" class="ag-courses-item_link"><div class="ag-courses-item_bg"></div><div class="ag-courses-item_title"><span class="adjustable-text"> Subscritos <br>{clientes_suscriptos}</span></div></div></div></div></div></div>'
        # tarjeta2 = f'<div class="ag-format-container"><div class="ag-courses_box"><div class="ag-courses_item"><div href="#" class="ag-courses-item_link"><div class="ag-courses-item_bg"></div><div class="ag-courses-item_title"><span class="adjustable-text"> Dados de baja <br>{clientes_dejar_de_recibir}</span></div></div></div></div></div></div>'
        tarjeta3 = f'<div class="ag-format-container"><div class="ag-courses_box"><div class="ag-courses_item"><div href="#" class="ag-courses-item_link"><div class="ag-courses-item_bg"></div><div class="ag-courses-item_title"><span class="adjustable-text"> Dejaron motivos <br>{con_motivo_no_interesados}</span></div></div></div></div></div></div>'
        tarjeta4 = f'<div class="ag-format-container"><div class="ag-courses_box"><div class="ag-courses_item"><div href="#" class="ag-courses-item_link"><div class="ag-courses-item_bg"></div><div class="ag-courses-item_title"><span class="adjustable-text"> No dejaron motivos <br>{sin_motivo_no_interesado}</span></div></div></div></div></div></div>'
        
        # Contenido de las tarjetas
        with col1:
            # st.markdown('<div class="ag-courses-item_title">Cantidad de clientes que dejaron motivos</div>', unsafe_allow_html=True)
            st.markdown(tarjeta1, unsafe_allow_html=True)
            # st.markdown('</div>', unsafe_allow_html=True)
            # st.write(f"+ Conversaciones terminadas: **{conversaciones_terminadas}**")
            # st.write(f"+ Conversaciones incompletas: **{conversaciones_incompletas}**")

        # with col2:
        #     # st.markdown('<div class="ag-courses-item_title">Clientes suscriptos</div>', unsafe_allow_html=True)
        #     st.markdown(tarjeta2, unsafe_allow_html=True)
        #     # st.markdown('</div></div>', unsafe_allow_html=True)

        with col2:
            # st.markdown('<div class="ag-courses-item_title">Clientes que se dieron de baja</div>', unsafe_allow_html=True)
            st.markdown(tarjeta3, unsafe_allow_html=True)
            # st.markdown('</div></div>', unsafe_allow_html=True)

        with col3:
            # st.markdown('<div class="ag-courses-item_title">Clientes que no dejaron motivos</div>', unsafe_allow_html=True)
            st.markdown(tarjeta4, unsafe_allow_html=True)
            # st.markdown('</div></div>', unsafe_allow_html=True)
            # ver_motivos = st.checkbox("Mostrar motivos")
            
        st.write("---")

        query2 = f"""
                SELECT e.* , c.businessPhoneNumber, c.clientName, c.userPhoneNumber
                FROM experiencias e
                JOIN clientes c ON (e.idCliente = c.idCliente)
                WHERE e.journeyClassName = 'SnackyOferta1' AND c.businessPhoneNumber = {businessnumber} ;
                """
        
        df_oferta_snackys2 = pd.read_sql(query2, engine)
        df_oferta_snackys2.drop("hora",axis=1,inplace=True)
        grafico_barras_data = df_oferta_snackys2[['msgBody','fecha']][(df_oferta_snackys2['msgBody'].isin(['1', '2'])) & (df_oferta_snackys2['journeyClassName'] == 'SnackyOferta1') & (df_oferta_snackys2['journeyStep'] == "RespuestaMensajeInicial")]
        # df_count = grafico_barras_data.groupby(['fecha', 'msgBody']).size().unstack(fill_value=0).reset_index()
        grafico_barras_data['fecha'] = pd.to_datetime(grafico_barras_data['fecha'])
        # st.write(df_count)
        # st.write(str(df_count['fecha'].dtype))
        
        # col7 = st.columns(1)

        # with col4 :
        #     # gráfico de cantidad de mensajes por fecha
        #     df_oferta_snackys['fecha'] = pd.to_datetime(df_oferta_snackys['fecha'])
        #     registros_por_dia = df_oferta_snackys['fecha'].value_counts().reset_index()
        #     registros_por_dia.columns = ['fecha', 'cantidad']
        #     fig, ax = plt.subplots()
        #     fig.set_size_inches(6, 3) 
        #     sns.set(style="whitegrid")
        #     ax = sns.lineplot(x="fecha", y="cantidad", marker='o', color='b',data=registros_por_dia,linewidth=4)
        #     plt.xlabel('')
        #     plt.ylabel('')
        #     date_form = DateFormatter("%d/%m")
        #     ax.xaxis.set_major_formatter(date_form)
        #     #plt.tight_layout() 
        #     gráfico2 = plt.gcf()
        #     st.write("#### **Total de mensajes**")
        #     st.pyplot(gráfico2)

        # with col5:
        #     if len(df_oferta_snackys) > 0 :
        #         # Extrae las etiquetas y los valores del diccionario
        #         etiquetas = list(subs.keys())
        #         valores = list(subs.values())
        #         total = sum(valores)
        #         # Colores para el gráfico
        #         colores = ['tab:green', 'tab:red']
        #         plt.figure(figsize=(6, 3))  
        #         sns.set(style="whitegrid")
        #         # Crea el gráfico de torta
        #         plt.pie(valores, labels=etiquetas, colors=colores, autopct=lambda p: '{:.0f} ({:.1f}%)'.format(p * total / 100, p), startangle=90)
        #         plt.axis('equal')  # Hace que el gráfico sea circular
        #         gráfico11 = plt.gcf()
        #         st.write("#### **Porcentaje de suscriptos**")
        #         st.pyplot(gráfico11)
        #     else:
        #         st.write("sin datos")

        # with col7:

        # Datos de ejemplo (reemplázalos con tus propios datos)
        # categorias = ['Si', 'No']
        # valores_1 = [10, 15]
        # valores_2 = [5, 10]

        # Crear un DataFrame de pandas (opcional, pero útil para Seaborn)
        # df = pd.DataFrame({'Categorías': categorias, 'Valor 1': valores_1, 'Valor 2': valores_2})
        
        # Crear el gráfico de barras apiladas vertical
        # sns.set(style="whitegrid")
        # plt.figure(figsize=(8, 6))
        # sns.barplot(x='fecha', y='1', data=df_count, color='#2D8DEC', label='Interesado')
        # sns.barplot(x='fecha', y='2', data=df_count, color='#DFE2E5', label='No Interesado')
        # plt.xlabel('Categorías')
        # plt.ylabel('Valores')
        # plt.xticks(rotation=45)
        # plt.title('Gráfico de Barras Apiladas Vertical')
        # plt.legend()
        # gráfico12 = plt.gcf()
        # st.pyplot(gráfico12)

        # Crear columnas de mes y semana
        grafico_barras_data['mes'] = grafico_barras_data['fecha'].dt.month
        grafico_barras_data['semana'] = grafico_barras_data['fecha'].dt.day // 7 + 1
        grafico_barras_data['mes'] = grafico_barras_data['mes'].astype(str)
        grafico_barras_data['semana'] = grafico_barras_data['semana'].astype(str)

        # Agrupar por mes y semana, contando las ocurrencias de cada categoría
        grouped = grafico_barras_data.groupby(['mes', 'semana', 'msgBody']).size().unstack(fill_value=0).reset_index()
        # grouped1 = grouped[grouped['msgBody'] == '1']
        # grouped2 = grouped[grouped['msgBody'] == '2']
        st.write(grouped)
        # st.write(grouped2)
        # # Crear el gráfico de barras apiladas
        # plt.figure(figsize=(10, 4))
        # sns.barplot(x='mes', y='count', hue='semana', data=grouped, palette=['red'])
        # # sns.barplot(x='mes', y='count', hue='semana', data=grouped2, palette=['blue'])
        # plt.xlabel('Mes')
        # plt.ylabel('Valores')
        # plt.title('Gráfico de Barras Apiladas por Mes y Semana')
        # plt.legend(title='Semana', labels=['1','2'], labelcolor=['red', 'blue']).get_lines()[0].set_color('red')
        # plt.ylim(0, 30)
        # st.pyplot(plt)
        # data = {
        #     'mes': ['Enero', 'Enero', 'Febrero', 'Febrero', 'Marzo', 'Marzo'],
        #     'semana': [1, 2, 1, 2, 1, 2],
        #     'msgBody': ['1', '2', '1', '2', '1', '2'],
        #     'count': [10, 3, 12, 8, 15, 9]
        # }

        # df = pd.DataFrame(data)

        # # Crear un DataFrame pivote
        # pivot_df = df.pivot_table(index=['mes', 'semana'], columns='msgBody', values='count', aggfunc='sum', fill_value=0)
        # st.write(pivot_df)
        # # Crear el gráfico de barras apiladas
        # ax = pivot_df.plot(kind='bar', stacked=True, figsize=(10, 4), colormap='Set1')

        # plt.xlabel('Mes y Semana')
        # plt.ylabel('Valores')
        # plt.title('Gráfico de Barras Apiladas por Mes y Semana')
        # plt.xticks(rotation=45)
        # plt.legend(title='Categoría')
        # plt.tight_layout()
        # st.pyplot(plt)
        # fig, ax = plt.subplots(figsize=(10, 6))

        # # Define los colores para '1' y '2'
        # colores = ['blue', 'green']
        data = {
            'mes': ['enero', 'enero', 'enero', 'enero', 'feb', 'feb', 'feb', 'feb'],
            'semana': [1, 2, 3, 4, 1, 2, 3, 4],
                 '1': [5, 6, 9, 2, 3, 4, 1, 3],
                 '2': [1, 2, 3, 5, 5, 7, 1, 1]
        }

        grouped = pd.DataFrame(data)
        st.write(grouped)
        # # Itera a través de los meses y crea las barras apiladas
        # for i, month in enumerate(grouped['mes'].unique()):
        #     data = grouped[grouped['mes'] == month]
            
        #     # Barras para '1'
        #     ax.bar(data['semana'], data['2'], label=f'Mes {month} - 2', color=colores[1], alpha=0.7)
            
        #     # Barras para '2' (apiladas encima de '1')            
        #     ax.bar(data['semana'], data['1'], bottom=data['2'], label=f'Mes {month} - 1', color=colores[0], alpha=0.7)
        
        # # Etiqueta los ejes y agrega una leyenda
        # ax.set_xlabel('Semana')
        # ax.set_ylabel('Cantidad')
        # ax.set_title('Cantidad de 1 y 2 por Semana y Mes (Barras Apiladas)')
        # ax.legend()

        # fig, ax = plt.subplots(figsize=(10, 6))

        # # Define los colores para '1' y '2'
        # colores = ['blue', 'green']

        # # Definir la cantidad de semanas y el ancho de las barras
        # num_semanas = grouped['semana'].max()
        # ancho_barra = 0.35

        # # Crear un arreglo de índices para las barras de cada semana
        # indices = list(range(1, num_semanas + 1))

        # # Itera a través de los meses y crea las barras separadas por mes
        # for i, month in enumerate(grouped['mes'].unique()):
        #     data = grouped[grouped['mes'] == month]
            
        #     # Barras para '1'
        #     ax.bar([x + i * ancho_barra for x in indices], data['1'], width=ancho_barra, label=f'Mes {month} - 1', color=colores[0], alpha=0.7)
            
        #     # Barras para '2'
        #     ax.bar([x + i * ancho_barra for x in indices], data['2'], width=ancho_barra, label=f'Mes {month} - 2', color=colores[1], alpha=0.7, bottom=data['1'])

        # # Etiqueta los ejes y agrega una leyenda
        # ax.set_xlabel('Semana')
        # ax.set_ylabel('Cantidad')
        # ax.set_title('Cantidad de 1 y 2 por Semana y Mes (Barras Separadas)')
        # ax.legend()
        fig, ax = plt.subplots(figsize=(10, 6))
        n = len(grouped.index)
        width = 0.40
        for i ,mes in enumerate(list(grouped['mes'].unique())):
            grouped1 = grouped[(grouped['semana'] == 1) & (grouped['mes'] == mes)]

            grouped3 = grouped[(grouped['semana'] == 2) & (grouped['mes'] == mes)]

            grouped5 = grouped[(grouped['semana'] == 3) & (grouped['mes'] == mes)]

            grouped7 = grouped[(grouped['semana'] == 4) & (grouped['mes'] == mes)]
            
            ax.bar(i*6*width + width, grouped1['2'], width=width, label='semana 1', color='#DFE2E5', edgecolor='black')
            ax.bar(i*6*width + width, grouped1['1'], bottom=grouped1['2'], width=width, label='semana 1', color='#2D8DEC', edgecolor='black')
            ax.text(x=(i*6*width + width), s='1era', y=-0.40, ha='center')

            ax.bar(i*6*width + 2*width, grouped3['2'], width=width, label='semana 2', color='#DFE2E5', edgecolor='black')
            ax.bar(i*6*width + 2*width, grouped3['1'], bottom=grouped3['2'], width=width, label='semana 2', color='#2D8DEC', edgecolor='black')
            ax.text(x=(i*6*width + 2*width), s='2da', y=-0.40, ha='center')

            ax.text(x=(i*6*width + ((4*width)/2)), s=str.capitalize(mes), y=-0.8, ha='left')

            ax.bar(i*6*width + 3*width, grouped5['2'], width=width, label='semana 3', color='#DFE2E5', edgecolor='black')
            ax.bar(i*6*width + 3*width, grouped5['1'], bottom=grouped5['2'], width=width, label='semana 3', color='#2D8DEC', edgecolor='black')
            ax.text(x=(i*6*width + 3*width), y=-0.40, s='3era', ha='center')

            ax.bar(i*6*width + 4*width, grouped7['2'], width=width, label='semana 4', color='#DFE2E5', edgecolor='black')
            ax.bar(i*6*width + 4*width, grouped7['1'], bottom=grouped7['2'], width=width, label='semana 4', color='#2D8DEC', edgecolor='black')
            ax.text(s='4ta', x=(i*6*width + 4*width), y=-0.40, ha='center')
            

        patch_1 = mpatches.Patch(color='#2D8DEC', label='Interesado')
        patch_2 = mpatches.Patch(color='#DFE2E5', label='No Interesado')
        plt.xticks([])
        # Crear la leyenda con las barras de color personalizadas
        plt.legend(handles=[patch_1, patch_2], loc='upper right')
        st.pyplot(plt)

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