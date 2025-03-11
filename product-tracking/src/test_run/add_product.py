from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import matplotlib.pyplot as plt

# Please register and login first!, and navigate to landing page

driver = webdriver.Chrome()
# You must get the link from ngrok fist, or you can replace it with the localhost URL
driver.get("https://f7b6-58-9-132-37.ngrok-free.app")
while True:
    try:
        driver.find_elements(By.TAG_NAME, "button")[1].click()
        break
    except:
        continue
driver.find_elements(By.TAG_NAME, "input")[1].send_keys("Aekanut")
driver.find_elements(By.TAG_NAME, "input")[2].send_keys("steve1212")
driver.find_elements(By.TAG_NAME, "input")[3].click()

while True:
    try:
        driver.find_element(By.ID, "add-product").click()
        print("Click add product button")
        break
    except:
        continue


time_list = []
round_list = []
iteration = 100
x_axis = [i for i in range(iteration)]
for i in x_axis:
    print("filling add product form")
    while True:
        try:
            driver.find_elements(By.CLASS_NAME, "TextInput")[0].send_keys("test")
            break
        except:
            continue

    driver.find_elements(By.CLASS_NAME, "TextInput")[2].send_keys("test")
    driver.find_elements(By.CLASS_NAME, "TextInput")[3].send_keys("test")
    driver.find_elements(By.CLASS_NAME, "TextInput")[4].send_keys("steve1212")

    # Start timer
    start = time.time()
    driver.find_elements(By.CLASS_NAME, "FlexAddProduct")[0].submit()
    while True:
        try:
            driver.find_element(By.ID, "add-product").click()
            print("Click add product button")
            break
        except:
            continue

    # Stop timer
    end = time.time()
    time_list.append(end - start)
    round_list.append(i + 7)
    plt.plot(round_list, time_list)
    plt.xlabel("Block Number")
    plt.ylabel("Time (s)")
    plt.title(
        "Relation between number of block and time consuming\n in add product function"
    )

    plt.xlim(0, 105)

    plt.savefig("./test_run/add_product.png")
    plt.clf()

    average_time = sum(time_list) / len(time_list)

    print("Average time: ", average_time)
    with open("./test_run/average time add product.txt", "w") as f:
        f.write(str(average_time))

print("Finish testing")
