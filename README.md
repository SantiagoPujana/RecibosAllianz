<h1 align="center">Recibos Allianz</h1>

<div align="center">  
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=Selenium&logoColor=white" />
</div>

<h3><b>Acerca del proyecto</b></h3>

Este proyecto es un bot escrito en Python 3 junto con la librería Selenium, ya que realiza una descarga automática de recibos de seguros Allianz, estos son archivos PDF alojados en la plataforma <a href="https://www.allia2net.com.co/ngx-epac/public/home"><b>Allia2Net</b></a> así mismo usa un dataset en un archivo Excel para parametrizar los datos de los activos y tomar como referencia el recibo a descargar.

El propósito de programar este proyecto es el de automatizar y ahorrar tiempo al momento de descargar una gran magnitud de recibos o archivos alojados en internet, por lo tanto, este software puede ser utilizado principalmente por consultores o asesores de seguros específicamente para la empresa <a href="https://www.serconti.com"><b>SERCONTI</b></a> por lo que este software solo se utiliza para la descarga de recibos de seguros automovilísticos

<h3><b>Características</b></h3>

- El software automaticamente descarga el chrome webdriver, dependiendo de la versión que tenga Google Chrome.

- Antes de iniciar el proceso de descarga se le solicita al usuario las credenciales para ingresar a la plataforma, también la ruta del archivo Excel, un rango de fechas de facturación, en que carpeta desea que se descarguen los documentos, si desea generar un archivo de texto donde se guarden los procesos hechos por el software y si desea ver el procedimiento con el navegador desplegado.

- Durante el proceso muestra los pasos que realiza mientras accede al archivo mediante la plataforma para descargarlo, ya que puede generar algunos errores porque no se encontró un elemento necesario en el DOM de la plataforma para continuar.

<h3><b>Ayuda e instrucciones</b></h3>

Puede ver el archivo Excel de ejemplo <a href="https://github.com/ProzTock/RecibosAllianz/raw/main/Ejemplo.xlsx"><b>aquí</b></a> o accediendo al siguiente link (https://github.com/ProzTock/RecibosAllianz/raw/main/Ejemplo.xlsx) para saber cómo debe estar estructurado, a continuación, se presentan algunas instrucciones para usar el software:
- Los datos de en el archivo Excel deben ir en el siguiente orden:
              
    - Aplicativo
    - Placa
    - Tipo de Vehículo
    - Referencia de pago
    - Período facturado
    - Valor
    - Fecha límite
                                                                       
- La columna A y la I deben estar libres, la tabla debe iniciar desde la columna B y terminar hasta la columna H.                                                               
- Los datos en el archivo Excel deben iniciar desde la fila 1.
- Los datos en las filas del archivo Excel no deben tener color de relleno. 
- Antes de iniciar el procedimiento solo es necesario que la columna de Aplicativo, Placa y Tipo de Vehículo tengan datos, esta información debe ser propia de la empresa.
- Insertar fechas en el siguiente formato: dd/mm/aaaa
- Se recomienda usar una copia del archivo de Excel a utilizar por seguridad.
- El espacio entre tablas del archivo Excel debe ser máximo de 5 celdas.           
- No se recomienda cambiar el tamaño de la ventana del navegador, ni cambiar entre pestañas si seleccionó ver el proceso de descarga.                                                  - Tener habilitadas las notificaciones en Windows para que el software le indique cuando inició y terminó el proceso.                                                               
- Para salir del software oprima "Control + C" y espere un momento.

<h3><b>Descarga e Instalación</b></h3>
  
Para clonar este repositorio y descargar las dependencias, pueden ejecutar los siguientes comandos:

    git clone https://github.com/ProzTock/RecibosAllianz.git
    pip install -r requirements.txt
    python AllianzReceipt.py

Para descargar el instalador para Windows 10 acceda <a href="https://github.com/ProzTock/RecibosAllianz/raw/main/Instalador-Installer/Recibos_Allianz_Installer.exe"><b>aquí</b></a>, o use el siguiente link:

https://github.com/ProzTock/RecibosAllianz/raw/main/Instalador-Installer/Recibos_Allianz_Installer.exe

<h3><b>Recomendaciones</b></h3>

Se debe tener instalado y actualizado el navegador Google Chrome para un optimo desempeño del software, puede actualizarlo copiando el siguiente link: 

***chrome://settings/help***

<a href="https://github.com/ProzTock/RecibosAllianz/blob/main/LICENSE"><b>Licensia MIT</b></a>
