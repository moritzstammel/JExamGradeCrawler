from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

PASSWORD = "Your Password"
USERNAME = "Your Username"
CHROMEDRIVER_PATH = "Path to chromedriver"

J_EXAM_EXAM = "Prüfung"
J_EXAM_COMPLETED_MODULE = "Modulberechnung"
J_EXAM_PENDING_MODULE = "Modul wird noch berechnet"
J_EXAM_GRADE = "Note"
J_EXAM_PASSED = "Bestanden"
J_EXAM_POINTS = "Punkte"

EXAMS = "exams"
EXAM = "exam"
COMPLETED_MODULE = "completed module"
PENDING_MODULE = "pending module"
TYPE = "type"
NAME = "name"
GRADE = "grade"
POINTS = "points"
PASSED = "passed"
NAME_VALUE = 1
TYPE_VALUE = 0


def get_grades(username, password, chromedriver_path=""):
    endpoint = "https://jexam.inf.tu-dresden.de/de.jexam.web.v5"

    browser = webdriver.Chrome(chromedriver_path)
    browser.get(endpoint + "/spring/welcome")

    username_textfield = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='j_username']")))
    password_textfield = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='j_password']")))

    username_textfield.clear()
    password_textfield.clear()
    username_textfield.send_keys(username)
    password_textfield.send_keys(password)

    WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit']"))).click()
    try:
        WebDriverWait(browser, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="wrapper"]/div/div/div[2]/a[3]'))).click()
    except:
        # Login failed
        browser.close()
        return None
    WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="wrapper"]/div/div/div[2]/div/div/form/input'))).click()
    WebDriverWait(browser, 5).until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="wrapper"]/div/div/div[2]/section/div[1]/div/button[2]'))).click()

    elements_to_expand = browser.find_elements_by_class_name('arrow-down')

    for element in elements_to_expand:
        element.click()

    gradelist = browser.find_element_by_xpath('//*[@id="wrapper1"]/ul').text

    data = []
    lines = gradelist.splitlines()
    curr = [lines.pop(0)]
    for line in lines:
        if line == J_EXAM_EXAM:
            data.append(curr)
            curr = [J_EXAM_EXAM]
        elif line == J_EXAM_COMPLETED_MODULE:
            data.append(curr)
            curr = [J_EXAM_COMPLETED_MODULE]
        elif line == J_EXAM_PENDING_MODULE:
            data.append(curr)
            curr = [J_EXAM_PENDING_MODULE]
        else:
            curr.append(line)
    data.append(curr)

    output = []
    modules = []
    exams = []

    for elem in data:
        if elem[TYPE_VALUE] == J_EXAM_PENDING_MODULE:
            modules.append(elem)
        elif elem[TYPE_VALUE] == J_EXAM_EXAM:
            exams.append(elem)
        elif elem[TYPE_VALUE] == J_EXAM_COMPLETED_MODULE:
            modules.append(elem)

    # Calculating Modules

    for module in modules:

        if J_EXAM_GRADE in module:
            grade_index = module.index(J_EXAM_GRADE) + 1
            grade = module[grade_index]
        else:
            grade = None

        passed = J_EXAM_PASSED in module
        if module[TYPE_VALUE] == J_EXAM_PENDING_MODULE:
            module_type = PENDING_MODULE
            passed = None
        else:
            module_type = COMPLETED_MODULE
        module_output = {
            NAME: module[NAME_VALUE],
            TYPE: module_type,
            GRADE: grade,
            PASSED: passed,
            EXAMS: []
        }

        short_module_name = module[NAME_VALUE].split(" ")[0]
        exams_to_remove = []
        for exam in exams:
            if short_module_name in exam[NAME_VALUE]:

                if J_EXAM_POINTS in exam:
                    point_index = exam.index(J_EXAM_POINTS) + 1
                    points = exam[point_index]
                else:
                    points = None

                if J_EXAM_GRADE in exam:
                    grade_index = exam.index(J_EXAM_GRADE) + 1
                    grade = exam[grade_index]
                else:
                    grade = None

                passed = J_EXAM_PASSED in exam

                module_output[EXAMS].append({
                    NAME: exam[NAME_VALUE],
                    TYPE: EXAM,
                    GRADE: grade,
                    POINTS: points,
                    PASSED: passed
                })
                exams_to_remove.append(exam)
        output.append(module_output)

        for exam in exams_to_remove:
            exams.remove(exam)

    # CALCULATING SINGLE EXAMS

    for exam in exams:
        if J_EXAM_POINTS in exam:
            point_index = exam.index(J_EXAM_POINTS) + 1
            points = exam[point_index]
        else:
            points = None

        if J_EXAM_GRADE in exam:
            grade_index = exam.index(J_EXAM_GRADE) + 1
            grade = exam[grade_index]
        else:
            grade = None

        passed = J_EXAM_PASSED in exam

        output.append({
            NAME: exam[NAME_VALUE],
            TYPE: EXAM,
            GRADE: grade,
            POINTS: points,
            PASSED: passed
        })

    browser.get(endpoint + "/spring/logout")
    browser.close()
    return output


if __name__ == "__main__":
    print(get_grades(USERNAME, PASSWORD, CHROMEDRIVER_PATH))
