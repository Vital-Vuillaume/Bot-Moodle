import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

email = input("Votre email: ")

pwd = input("Votre mode passe: ")

ui = input("Si vous voulez avoir l'interface ecrivez yes sinon mettez autres choses: ")

chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

if ui.lower() != "yes":
    chrome_options.add_argument("--headless")

chrome_service = Service(executable_path='/usr/bin/chromedriver')

driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

driver.get("https://learn.s2.rpn.ch/my/courses.php")

btnConnect = driver.find_element(By.CSS_SELECTOR, ".btn.login-identityprovider-btn.btn-block.btn-secondary")
btnConnect.click()

time.sleep(2)

inputEmail = driver.find_element(By.CSS_SELECTOR, ".form-control")
inputEmail.send_keys(email, Keys.ENTER)

time.sleep(2)

inputPwd = driver.find_element(By.CSS_SELECTOR, "input#i0118")
inputPwd.send_keys(pwd, Keys.ENTER)

time.sleep(3)

try:
    div_element = driver.find_element(By.ID, "idRichContext_DisplaySign")

    chiffre = div_element.text

    input(f"Mets le code {chiffre} sur l'application authentificator et ensuite cliquez enter: ")

    btnStayConnect = driver.find_element(By.CSS_SELECTOR, ".win-button")
    btnStayConnect.click()

except Exception as e:
    print(f"Erreur en traitant le lien: {e}") 

def process_courses():

    time.sleep(3)

    course_names = driver.find_elements(By.CSS_SELECTOR, ".multiline span[aria-hidden='true']")

    courseArray = []

    i = 0

    for course in course_names:
        if course.text.strip():
            courseArray.append(course.text.strip())
            print(f"{i} : {course.text.strip()}")
            i += 1

    choice = int(input("Entrez le numéro du cours que vous souhaitez sélectionner : "))

    try:
        if 0 <= choice < len(courseArray):
            selected_course_name = courseArray[choice]

            selected_course_link = driver.find_elements(By.XPATH, f"//span[contains(text(), '{selected_course_name}')]/ancestor::a")

            selected_course_link[0].click()

        else:
            print("Numéro de cours invalide.")
    except ValueError:
        print("Veuillez entrer un numéro valide.")

    time.sleep(2)



    links = driver.find_elements(By.CLASS_NAME, 'courseindex-link')

    for link in links:
        try:
            href = link.get_attribute('href')
            
            if href and href.startswith('https://learn.s2.rpn.ch/mod/resource/view.php?id='):
                driver.execute_script("window.open(arguments[0], '_blank');", href)
                driver.switch_to.window(driver.window_handles[0])
            else:
                action = ActionChains(driver)
                action.context_click(link).perform()

        except Exception as e:
           print(f"Erreur en traitant le lien: {e}") 

process_courses()



again = input("Si vous voulez choisir un nouveau cours ecrivez yes sinon mettez autres choses: ")

if again.lower() == "yes":
    main_window = driver.window_handles[0]

    for handle in driver.window_handles:
        if handle != main_window:
            driver.switch_to.window(handle)
            driver.close()

    driver.switch_to.window(main_window)
    driver.get("https://learn.s2.rpn.ch/my/courses.php")
    process_courses()
else:
    driver.quit()