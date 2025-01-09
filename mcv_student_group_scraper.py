from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time, csv, os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Initialize the WebDriver
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

# เปิดเว็บไซต์
url = "<Target URL>"
driver.get(url)

# รอให้หน้าเว็บโหลดเสร็จ (เพิ่มเวลาตามความเหมาะสมหากเว็บโหลดช้า)
time.sleep(5)

star_element = driver.find_element(By.ID, "courseville-login-w-platform-cu-button")
star_element.click()
time.sleep(3)

username_element = driver.find_element(By.ID,"username")

username_element.send_keys(os.getenv('MCV_USERNAME'))
time.sleep(1)

password_element = driver.find_element(By.ID,"password")

password_element.send_keys(os.getenv('MCV_PASSWORD'))
time.sleep(1)

submit_element = driver.find_element(By.ID,"cv-login-cvecologinbutton")
submit_element.click()

# Navigate to the target website
driver.get(url)

# Optional: Wait for the page to load completely (adjust time as needed)
time.sleep(5)

# Find all elements with class 'cvgroupcard'
group_cards = driver.find_elements(By.CLASS_NAME, "cvgroupcard")

# Prepare a data structure to store the scraped data
scraped_data = []

for group_card in group_cards:
    # Extract the group name
    group_name_element = group_card.find_element(By.CLASS_NAME, "cvgroupcard-groupname")
    group_name = group_name_element.text

    # Extract the member list
    member_list_element = group_card.find_element(By.CLASS_NAME, "cvgroupcard-member-list")
    member_elements = member_list_element.find_elements(By.TAG_NAME, "li")
    members = [member.text for member in member_elements]

    # Append the data to the list
    scraped_data.append({
        "group_name": group_name,
        "members": members
    })

# Save the scraped data to a CSV file
csv_file = "scraped_data.csv"
with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Group Name", "Members"])
    for group in scraped_data:
        writer.writerow([group['group_name'], ", ".join(group['members'])])

print(f"Data saved to {csv_file}")

# Print the scraped data
for group in scraped_data:
    print(f"Group Name: {group['group_name']}")
    print("Members:")
    for member in group['members']:
        print(f"- {member}")
    print()

# Quit the browser
driver.quit()
