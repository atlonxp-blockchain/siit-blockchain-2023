from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import matplotlib.pyplot as plt
from statistics import mean

driver = webdriver.Chrome()
# You must get the link from ngrok fist, or you can replace it with the localhost URL
driver.get("https://f7b6-58-9-132-37.ngrok-free.app")


iteration = 1000

# Please change into the product ID that is available in the system, you may add and copy the ID and put in the list.
# Then, navigate to landing page
track_list = ["qUbjmlaYCpNp", "TrZDAtzLpJ9R", "34bUnepEESNh", "nsmWAjbXVhl0"]
time_list = [[], [], [], []]
round_list = []
for round in range(iteration):
    for i in range(len(track_list)):
        while True:
            try:
                driver.find_elements(By.TAG_NAME, "input")[0].clear()
                driver.find_elements(By.TAG_NAME, "input")[0].send_keys(track_list[i])
                break
            except:
                continue

        driver.find_elements(By.TAG_NAME, "form")[0].submit()
        start = time.time()
        while True:
            try:
                driver.find_element(By.ID, "qrcode-popup")
                break
            except:
                continue
        end = time.time()
        driver.back()
        time_list[i].append(end - start)
        print(f"{i} track: {end-start} s")

    x = ["1 Record(s)", "2 Record(s)", "3 Record(s)", "4 Record(s)"]
    plt.bar(
        x,
        [
            mean(time_list[0]) * 1000,
            mean(time_list[1]) * 1000,
            mean(time_list[2]) * 1000,
            mean(time_list[3]) * 1000,
        ],
    )
    plt.xlabel("Number of Record")
    plt.ylabel("Time (ms)")
    plt.title("Track Record Retrival Time Consumption")
    plt.savefig("./test_run/get_track.png")
    plt.clf()

    with open("./test_run/average_time_get_record.txt", "w") as f:
        f.write("1 Record(s): " + str(mean(time_list[0]) * 1000) + " ms\n")
        f.write("2 Record(s): " + str(mean(time_list[1]) * 1000) + " ms\n")
        f.write("3 Record(s): " + str(mean(time_list[2]) * 1000) + " ms\n")
        f.write("4 Record(s): " + str(mean(time_list[3]) * 1000) + " ms\n")
