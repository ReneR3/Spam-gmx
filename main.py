# ! Python 3 ! #

###############################################################################
# this is a little Program to delete and Blacklist all mails in the spam folder
###############################################################################
# 1. load the latest driver for the Browser from https://github.com/mozilla/geckodriver
# 2. start the Code and follow
# 3. that's it

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with
import pickle
from datetime import datetime
import time

#     !!!! Variables !!!!     # 3
cookie_path = "C:\\Users\\reneR\\Desktop\\code\\Spam gmx\\cookie.txt"
driver_path = "C:\Program Files\Mozilla Firefox\geckodriver.exe"


def save_cookie(browser, path):  # first time run the program check the cookie in the Browser
    print("Safe Cookie: ", end=" ")
    with open(path, 'wb') as filehandler:
        pickle.dump(browser.get_cookies(), filehandler)
    print("Done")


def load_cookie(browser, path):  # just load the cookies
    print("Load Cookie: ", end=" ")
    with open(path, 'rb') as cookiesfile:
        cookies = pickle.load(cookiesfile)
        for cookie in cookies:
            browser.add_cookie(cookie)
    print("Done")


def start_brows(browser, cookie_path):  # open the browser load the cookies in the Browser open new tap and close one
    print("Start Browser: ", end=" ")
    browser.get("https://www.gmx.at")
    print("Done")
    browser.minimize_window()
    load_cookie(browser, cookie_path)
    browser.execute_script("window.open('');")
    browser.get("https://www.gmx.at")
    browser.switch_to.window(browser.window_handles[1])
    browser.close()
    browser.switch_to.window(browser.window_handles[0])


def login_data():
    try:
        with open("LoginData", "r") as file:
            data = file.read().splitlines()
            user_mail = data[0]  # first row at LoginData file insert mail address
            user_password = data[1]  # second row at LoginData file insert password


    except IndexError:
        user_mail = input("GMX e-mail-address: ")
        user_password = input("GMX password: ")
        login_save = input("Safe your login Mail and password? press 'Y' for save or 'N' for not save ")
        if login_save.lower() == "y":
            with open("LoginData", "a") as file:
                file.write("%s\n%s" % (user_mail, user_password))
    return user_mail, user_password


def login(wait, mail, password):  # login to GMX
    print(f"Login with: {mail}")

    mail_login = wait.until(EC.element_to_be_clickable((By.NAME, "username")))
    mail_login.send_keys(mail)
    password_login = wait.until(EC.element_to_be_clickable((By.NAME, "password")))
    password_login.send_keys(password)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#freemailLoginForm > button:nth-child(8)"))).click()


def to_spam(browser, wait):  # change the site to spam folder
    print("Go to Spam: ", end=" ")
    wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/nav/nav-actions-menu/div[1]/div[1]/a[2]"))).click()
    time.sleep(1)
    browser.switch_to.frame("thirdPartyFrame_mail")
    time.sleep(4)
    try:
        browser.find_element(By.XPATH, "//*[@id='tfol1643b1b9f7e1cd51']").click()
    except:
        browser.find_element(By.XPATH, "// *[ @ id = 'idf']").click()

    print("Done")


def read_safe_spam(browser):  # read and safe the spam mails in a list
    print("Read and Safe Mail addresses: ", end=" ")
    next_mail = browser.find_element(locate_with(By.CLASS_NAME, "name"))
    mail_list = []
    while True:
        spam_mail = next_mail.get_attribute("title").split("<")
        mail_list.append(spam_mail[1][:-1])
        try:
            next_mail = browser.find_element(locate_with(By.CLASS_NAME, "name").below(next_mail))
        except IndexError:
            time.sleep(1)
            try:
                browser.find_element(By.NAME, "maillist:rowsCheckGroup:paging:container:align:form:next").click()
            except:
                break
            break
    print("Done")
    return mail_list


def delete_mail(browser):
    if input("\nWant clean spam? press ENTER to clean or 'N' to not delete the mails ") != "n":
        browser.find_element(By.ID, "checkbox-select-all").click()
        browser.find_element(By.ID, "toolbarButtonDelete").click()


def filter_mail(email):  # check if mail is already at Blacklist
    print("Filter Mails: ", end=" ")
    mail_to = []
    blacklist = [line for line in map(str.split, open("Blacklist.txt"))]
    for i in blacklist:
        for a in i:
            mail_to.append(a)
    not_unique = [i for i in email if any(x in i for x in mail_to)]
    for i in not_unique:
        email.remove(i)
    print("Done")


def user_check_mails(email):
    print("Check Mails!\n")
    for i in email:
        for a in i:
            print("--", end="")
    print("\n", email)
    for i in email:
        for a in i:
            print("--", end="")
    if input("\n\nWant to Blacklist Mails? press ENTER for further or 'N' for Cancel ").lower() == "n":
        return False
    return True


def blacklisted(browser, email):  # write the mails in the Blacklist
    print("\nGo to Blacklist: ")
    time.sleep(2)
    browser.find_element(By.ID, "navigationSettingsLink").click()
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                           "li.gui-toggle:nth-child(3) > div:nth-child(2) > ul:nth-child(1) > li:nth-child(5) > a:nth-child(1)"))).click()
    for i in email:
        browser.find_element(By.NAME, "addressField").send_keys(i)
        browser.find_element(By.CLASS_NAME, "button-primary").click()
        browser.find_element(By.NAME, "addressField").clear()
        print(i, "-------------------> are successful Blacklisted.")
    with open("Blacklist.txt", "a") as file:
        now = datetime.now()
        file.write("\n")
        file.write(now.strftime("%d.%m.%Y %H:%M:%S"))
        for i in email:
            file.write("\n")
            file.write(i)
        file.write("\n")
        file.write("_______________________________")


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! #
# !!!!!!!!!!!!!!!!!  Main Programm  !!!!!!!!!!!!!!!!! #
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! #


if __name__ == "__main__":
    browser = webdriver.Firefox(executable_path=driver_path)
    wait = WebDriverWait(browser, 10, poll_frequency=1)
    start_brows(browser, cookie_path)
    mail, password = login_data()
    login(wait, mail, password)
    to_spam(browser, wait)
    email = read_safe_spam(browser)
    filter_mail(email)
    email = list(dict.fromkeys(email))
    if len(email) != 0:
        print("\n----------", len(email), "Mails found for the Blacklist-----------\n")
        if user_check_mails(email):
            delete_mail(browser)
            blacklisted(browser, email)
            print("\n----------", len(email), " Mails are successful Blacklisted!----------\n")
        else:
            print("\n----------Quit without Mails to Blacklist!----------\n")
    else:
        print("\n----------No Mails in Spam or Mails are already on the blacklist----------\n")
    browser.close()
