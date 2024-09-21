import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

##HECHO POR DIEGO TUTIN

driver_path = 'C:\ChromeDriver\chromedriver-win64\chromedriver.exe'
download_path = os.path.join(os.getcwd(), "comprobantes")

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": download_path,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://srienlinea.sri.gob.ec/sri-en-linea")

boton_iniciar_sesion = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CLASS_NAME, "sri-iniciar-sesion"))
)
boton_iniciar_sesion.click()

formulario_login = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "kc-form-login"))
)
ruc_input = formulario_login.find_element(By.ID, "usuario")
ruc_input.send_keys("RUC-05555555555001")

clave_input = formulario_login.find_element(By.ID, "password")
clave_input.send_keys("CONTRASENA")

boton_ingresar = formulario_login.find_element(By.ID, "kc-login")
boton_ingresar.click()

boton_hamburguesa = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CLASS_NAME, "tamano-icono-hamburguesa"))
)
boton_hamburguesa.click()

enlace_facturacion_electronica = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CLASS_NAME, "sri-menu-icon-facturacion-electronica"))
)
enlace_facturacion_electronica.click()

texto_enlace = "Comprobantes electrónicos recibidos"
enlace_comprobantes_electronicos_recibidos = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.LINK_TEXT, texto_enlace))
)
enlace_comprobantes_electronicos_recibidos.click()

time.sleep(10)

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="frmPrincipal:tablaCompRecibidos"]'))
)

if not os.path.exists('comprobantes'):
    os.makedirs('comprobantes')

row_index = 0
while True:
    try:
        enlace_xpath = f'//*[@id="frmPrincipal:tablaCompRecibidos:{row_index}:lnkPdf"]'
        enlace = driver.find_element(By.XPATH, enlace_xpath)
        enlace.click()
        time.sleep(1)

        downloaded_files = os.listdir(download_path)
        for file in downloaded_files:
            if file.endswith(".pdf"):
                os.rename(os.path.join(download_path, file), os.path.join(download_path, f"comprobante_{row_index + 1}.pdf"))
                print(f"Comprobante {row_index + 1} descargado correctamente.")
                break

        row_index += 1
    except Exception as e:
        print(f"No se encontró más enlaces: {e}")
        break

driver.quit()
