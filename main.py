from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


def main():
    print(get_foods())


def get_foods():
    food_data = []

    options = webdriver.ChromeOptions()
    # options.add_argument('--headless=new')

    driver = webdriver.Chrome(options=options)
    driver.get('https://www.mcdonalds.com.br/cardapio')
    wait = WebDriverWait(driver, 10)

    for menu_index in range(2, 15):

        link = wait.until(
            EC.presence_of_element_located((By.XPATH, f'//*[@id="categoriesMenu"]/div/div[{menu_index}]/a'))
            )
        
        # driver.find_element(
        #         By.XPATH, f'//*[@id="categoriesMenu"]/div/div[{menu_index}]/a'
        #     )

        link.click()
        sleep(2)
        item_links = []

        for item in driver.find_elements(By.CLASS_NAME, 'mcd-category-detail__item'):
            print(item.get_attribute('href'))
            item_links.append(item.get_attribute('href'))

        for item_link in item_links:

            driver.get(item_link)
            meal = {}
            details = wait.until(EC.presence_of_element_located(
               ( By.CLASS_NAME, 'mcd-product-detail__summary')))
            
            meal['name'] = details.find_element(By.TAG_NAME, 'h1').text
            meal['detail'] = details.find_element(
                By.CLASS_NAME, 'mcd-product-detail__description').text
            meal['calories'] = details.find_element(By.TAG_NAME, 'h5').text
            driver.find_element(
                By.XPATH, '//*[@id="mcd-content"]/div/article/div[2]/div/section[1]/a').click()
            sleep(1)
            meal['carbs'] = driver.find_element(
                By.XPATH, '//*[@id="mcd-content"]/div/article/div[2]/div/section[1]/div/div/div[2]/div[3]/div/div[2]/span').text
            meal['protein'] = driver.find_element(
                By.XPATH, '//*[@id="mcd-content"]/div/article/div[2]/div/section[1]/div/div/div[2]/div[6]/div/div[2]/span').text
            meal['fats'] = driver.find_element(
                By.XPATH, '//*[@id="mcd-content"]/div/article/div[2]/div/section[1]/div/div/div[2]/div[7]/div/div[2]/span').text
            food_data.append(meal)
            print(meal)
            driver.close()

        driver.get('https://www.mcdonalds.com.br/cardapio')

    return food_data


if __name__ == '__main__':
    main()
