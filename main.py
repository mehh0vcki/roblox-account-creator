import time, random, os, traceback

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

size_window = input("[ window size ] >> Please, enter your window size, that you want to use. Default format for it is: (123, 456), but you can leave only (123), or blank.\n>  ")
if size_window.startswith("(") and size_window.endswith(")"):
    if "," in size_window:
        size_window = size_window[1:-1].split(",")
        window_size = (int(size_window[0]), int(size_window[1]))
    else:
        window_size = (int(size_window[1:-1]), int(size_window[1:-1]))
else:
    window_size = (1000, 1000)

print(f"[ window size ] >> Selected as {window_size}")

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_argument(f"--window-size={window_size[0]},{window_size[1]}")

def get_username(base: str) -> str:
    global base_number
    username_to_return: str = base + f"{base_number:02}"

    base_number += 1
    return username_to_return

def save_account(driver: webdriver, username: str, password: str):
    cookie_option: dict = driver.get_cookie(".ROBLOSECURITY")

    with open("accounts.txt", "a") as file:
        if cookie_option is not {}:
            file.write(f"{username}:{password}:{cookie_option['value']}")
        else:
            file.write(f"{username}:{password}")
    
        file.write("\n")
    file.close()

def create_accounts(itterations: int, base: str, password: str) -> None:
    def birthday_options(driver: webdriver):
        birthday: dict = {
            "day": random.randint(1, 28),
            "month": ["Jan", "Feb", "Mar", "Apr", "Jun", "Aug", "Sep", "Oct", "Nov", "Dec"],
            "year": ["1980", "1981", "1982", "1983", "1984", "1985", "1986", "1987", "1988", "1989", "1990", "1991", "1992", "1993", "1994", "1995", "1996", "1997", "1998", "1999", "2000"]
        }

        day: str = str(birthday["day"])
        month: str = random.choice(birthday["month"])
        year: str = random.choice(birthday["year"])

        dropdown = driver.find_element(By.CLASS_NAME, 'rbx-select')
        if dropdown:
            dropdown.click()
            time.sleep(random.uniform(0.5, 1.5))

            driver.find_element(By.XPATH, "//option[text()='" + day + "']").click()
            driver.find_element(By.CLASS_NAME, 'rbx-select').click()

            driver.find_element(By.XPATH, "//option[@value='" + month + "']").click()
            driver.find_element(By.CLASS_NAME, 'rbx-select').click()

            driver.find_element(By.XPATH, "//option[@value='" + year + "']").click()

            print(f"[ account ] >> Choosed birthday: {day}/{month}/{year} (dd/mm//yyyy).")
            return True
        else:
            return False
    
    def select_gender(driver: webdriver, x_path: str):
        driver.find_element(By.XPATH, x_path).click()

    def fill_singup(driver: webdriver, username: str, password: str):
        username_field = driver.find_element(By.XPATH, "//*[@id='signup-username']")
        if username_field:
            username_field.send_keys(username)
            time.sleep(1)

            password_field = driver.find_element(By.XPATH, "//*[@id='signup-password']")
            if password_field:
                password_field.send_keys(password)
                time.sleep(1)

                selected_function = random.choice([lambda: select_gender(driver, "//*[@id='MaleButton']"), lambda: select_gender(driver, "//*[@id='FemaleButton']")])
                selected_function()

    def check_for_captcha(driver: webdriver):
        while True:
            try:
                driver.find_element(By.XPATH, "/html/body/div[9]/div[2]/div/div/div/div")
                print(f"[ captcha ] >> Womp womp, you have captcha. Solve it. Please!")
                time.sleep(1)
            except NoSuchElementException:
                print(f"[ captcha ] >> You have no captcha. Good job!")
                return False
            time.sleep(2.5)

    for _ in range(itterations):
        username: str = get_username(base)
        print(f"[ account ] >> Trying to create {username}. ({itterations - _} left to create)")

        driver: webdriver = webdriver.Chrome(options=options)
        driver.get("https://www.roblox.com/")

        wait = WebDriverWait(driver, 30)
        try:
            accept_cookies = driver.find_element(By.XPATH, "//button[@class='btn-secondary-lg cookie-btn btn-primary-md btn-min-width']") 
            accept_cookies.click()
        except:
            pass

        fill_singup(driver, username, password)
        birthday_options(driver)

        try:
            driver.find_element(By.XPATH, "//*[@id='signup-button']").click()
        except:
            print(f"[ account ] >> Failed to create {username}.")
            driver.close()

        time.sleep(5)
        check_for_captcha(driver)
        time.sleep(5)

        try: # it is created
            element = driver.find_element(By.XPATH, "//*[@id='header-menu-icon']/button[2]")
            if element:
                element.click()
            print(f"[ account ] >> Created {username} successfully.")
            save_account(driver, username, password)
        except: # its NOT created
            global base_number
            itterations += 1
            base_number -= 1
            print(f"[ account ] >> Failed to create {username}.")

        print(f"[ account ] >> Sleeping for 1 second, then trying again...")
        time.sleep(1)
        driver.close()
    
    print(f"[ account ] >> Finished creating {itterations} accounts.")

os.system("cls")
while True:
    try:
        base_username: input = input("[ start ] >> Enter your username, that you are going to start with. \n>  ")
        base_number: int = int(input("[ start ] >> Enter number, that your autoclaiming accounts will start with. [0 > 000, 10 > 010]\n>  "))
        password: input = input("[ start ] >> Enter your password. \n>  ")
        itterations: int = int(input("[ start ] >> Enter the number of iterations (How many accounts). \n>  "))

        if base_number < 0 or base_number > 999:
            raise WindowsError
        elif base_username == "" or password == "":
            raise Warning
        elif itterations < 0:
            raise ValueError

        print(f"\n\nYou sure you want to create {itterations} accounts, with {base_username}{base_number:03}:{password} as start?")
        choice: input = input("[y/n] >  ")

        if choice.lower() == "y":
            create_accounts(itterations, base_username + str(base_number), password)
        
        print("Trying again...")
        print("\n\n")
    except ValueError: print(f"[ error ] >> You accidentally failed to enter a number. Trying again...")
    except WindowsError: print(f"[ error ] >> You entered a number less than 0, or greater than 999. Trying again...")
    except Warning: print(f"[ error ] >> You entered an empty string as username, or password. Trying again...")
    except ValueError: print(f"[ error ] >> You entered a number less than 0. Trying again...")
    except Exception as e: print("unknown error >>", traceback.format_exc())
    
    input("\n[ press enter to continue ] >> (this action clears console) ")
    os.system("cls")
