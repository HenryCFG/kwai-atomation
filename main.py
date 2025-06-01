from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
import time
import os
from datetime import datetime, timedelta
import pandas as pd
from natsort import natsorted 
import sys

# Path to your videos folder
videos_folder = r"C:\Users\henrycfg\Desktop\Automacao\videos"
video_files = [os.path.join(videos_folder, f) for f in natsorted(os.listdir(videos_folder)) if f.endswith('.mp4')][:300]

# Load titles from spreadsheet
titles_df = pd.read_excel(r"C:\Users\henrycfg\Desktop\Automacao\names.xlsx") 
titles_list = titles_df["title"].tolist()

navegador = webdriver.Chrome()
navegador.get("https://www.cutmotions.com/pool")
navegador.maximize_window()
time.sleep(80)  

# Switch to the second tab (index 1)
if len(navegador.window_handles) > 1:
    navegador.switch_to.window(navegador.window_handles[1])
    time.sleep(2)

# Set base_datetime to tomorrow at 03:00:32
base_datetime = (datetime.now() + timedelta(days=1)).replace(hour=3, minute=0, second=32, microsecond=0)

total_videos = len(video_files)
success_count = 0
skipped_count = 0
error_count = 0
start_time = time.time()

def print_progress(current_idx):
    elapsed = time.time() - start_time
    percent = (current_idx + 1) / total_videos
    bar_len = 30
    filled_len = int(bar_len * percent)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    if current_idx > 0:
        avg_time = elapsed / (current_idx + 1)
        eta = avg_time * (total_videos - (current_idx + 1))
    else:
        eta = 0
    eta_str = time.strftime("%H:%M:%S", time.gmtime(eta))
    elapsed_str = time.strftime("%H:%M:%S", time.gmtime(elapsed))
    print(
        f"\r[{bar}] {percent*100:5.1f}% | Success: {success_count} | Skipped: {skipped_count} | Errors: {error_count} | Elapsed: {elapsed_str} | ETA: {eta_str}",
        end='', flush=True
    )

for idx, video_path in enumerate(video_files):
    try:
        # Refresh every 10 uploads (except the first one)
        if idx > 0 and idx % 10 == 0:
            navegador.refresh()
            time.sleep(20)  # Wait for the page to reload

            # 1. Click the "Timed publish" radio button
            try:
                timed_publish_radio = WebDriverWait(navegador, 30).until(
                    EC.element_to_be_clickable((By.XPATH, "//label[contains(@class, 'ks-radio') and .//span[contains(text(), 'Timed publish')]]"))
                )
                navegador.execute_script("arguments[0].scrollIntoView();", timed_publish_radio)
                timed_publish_radio.click()
                time.sleep(1)
            except Exception as e:
                print(f"Error clicking 'Timed publish' after refresh: {e}")
                navegador.save_screenshot(f"error_after_refresh_timed_publish_{idx}.png")
                navegador.quit()
                sys.exit("Could not click 'Timed publish' after refresh. Stopping automation.")

            # 2. Select "Brazil" in the country select box
            try:
                select_box = WebDriverWait(navegador, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Country']"))
                )
                select_box.click()
                time.sleep(1)
                brazil_option = WebDriverWait(navegador, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//li[contains(@class, 'ks-select-dropdown__item')]//span[normalize-space(text())='Brazil']"))
                )
                brazil_option.click()
                time.sleep(1)
            except Exception as e:
                print(f"Could not select 'Brazil': {e}")
                navegador.save_screenshot(f"error_select_brazil_{idx}.png")
                navegador.quit()
                sys.exit("Could not select 'Brazil'. Stopping automation.")

            # 3. Select the timezone "UTC−03:00"
            try:
                timezone_box = WebDriverWait(navegador, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Time zone']"))
                )
                timezone_box.click()
                time.sleep(1)
                timezone_option = WebDriverWait(navegador, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//li[contains(@class, 'ks-select-dropdown__item')]//span[normalize-space(text())='UTC−03:00']"))
                )
                timezone_option.click()
                time.sleep(1)
            except Exception as e:
                print(f"Could not select timezone: {e}")
                navegador.save_screenshot(f"error_select_timezone_{idx}.png")
                navegador.quit()
                sys.exit("Could not select timezone. Stopping automation.")

        # Upload video file 
        wait = WebDriverWait(navegador, 30)
        file_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
        file_input.send_keys(video_path)

        # Wait until the submit button is clickable (upload finished)
        try:
            wait = WebDriverWait(navegador, 400)  # 10 minutes max
            wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'ks-button--primary') and span[contains(., 'Submit')]]")))
        except Exception as e:
            print(f"Upload took too long for video {idx}: {e}")
            navegador.save_screenshot(f"error_upload_timeout_{idx}.png")
            navegador.refresh()
            time.sleep(20)  # Wait for the page to reload after refresh

            # Repeat the setup steps after refresh
            try:
                # 1. Click the "Timed publish" radio button
                timed_publish_radio = WebDriverWait(navegador, 30).until(
                    EC.element_to_be_clickable((By.XPATH, "//label[contains(@class, 'ks-radio') and .//span[contains(text(), 'Timed publish')]]"))
                )
                navegador.execute_script("arguments[0].scrollIntoView();", timed_publish_radio)
                timed_publish_radio.click()
                time.sleep(1)

                # 2. Select "Brazil" in the country select box
                select_box = WebDriverWait(navegador, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Country']"))
                )
                select_box.click()
                time.sleep(1)
                brazil_option = WebDriverWait(navegador, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//li[contains(@class, 'ks-select-dropdown__item')]//span[normalize-space(text())='Brazil']"))
                )
                brazil_option.click()
                time.sleep(1)

                # 3. Select the timezone "UTC−03:00"
                timezone_box = WebDriverWait(navegador, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Time zone']"))
                )
                timezone_box.click()
                time.sleep(1)
                timezone_option = WebDriverWait(navegador, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//li[contains(@class, 'ks-select-dropdown__item')]//span[normalize-space(text())='UTC−03:00']"))
                )
                timezone_option.click()
                time.sleep(1)
            except Exception as e2:
                print(f"Error redoing setup after refresh: {e2}")
                navegador.save_screenshot(f"error_after_refresh_setup_{idx}.png")
                navegador.quit()
                sys.exit("Could not redo setup after refresh. Stopping automation.")

            skipped_count += 1
            continue  # Skip to next video and title

        
        # Click edit button to add title
        wait = WebDriverWait(navegador, 20)
        for attempt in range(7):
            try:
                # Wait for the edit button to be visible and clickable
                edit_button = wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'ks-link') and .//span[text()='Edit']]"))
                )
                navegador.execute_script("arguments[0].scrollIntoView();", edit_button)
                time.sleep(1.5)  # Give time for any overlay/animation to finish

                try:
                    edit_button.click()
                except Exception:
                    # Fallback: click with JavaScript if normal click fails
                    navegador.execute_script("arguments[0].click();", edit_button)
                break  # Success
            except Exception as e:
                # Try to close popup if it appears
                try:
                    popup_close_btn = navegador.find_element(By.CSS_SELECTOR, ".ks-message-custom-box .ks-message-box__btns button")
                    if popup_close_btn.is_displayed():
                        popup_close_btn.click()
                        time.sleep(1)
                        print(f"Closed popup for video {idx}")
                except Exception:
                    pass  # No popup, continue
                if attempt == 6:
                    print(f"Failed to click edit button for video {idx}: {e}")
                    navegador.save_screenshot(f"error_edit_{idx}.png")
                    navegador.quit()
                    sys.exit("Edit button not found. Stopping automation.")
                time.sleep(2)  # Wait and retry

        else:
            navegador.quit()
            sys.exit("Edit button not found after retries. Stopping automation.")

        time.sleep(1)

        # Wait for the textarea to be present and visible, with retries
        for attempt in range(5):
            try:
                wait = WebDriverWait(navegador, 20)
                title_input = wait.until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "textarea.ks-textarea__inner"))
                )
                break  # Success
            except Exception as e:
                if attempt == 4:
                    navegador.save_screenshot(f"error_textarea_{idx}.png")
                    print(f"Could not find textarea for video {idx}: {e}")
                    continue  # Skip this video and go to the next
                time.sleep(2)  # Wait a bit longer and retry

        else:
            continue  # If not found after retries, skip to next video

        title_input.clear()
        # Use the title with the same index as the video
        if idx < len(titles_list):
            title_input.send_keys(titles_list[idx])
        else:
            title_input.send_keys("")
        time.sleep(1)

        # Confirm title 
        wait = WebDriverWait(navegador, 20)
        confirm_title_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'ks-link') and .//span[text()='Confirm']]"))
        )
        navegador.execute_script("arguments[0].scrollIntoView();", confirm_title_btn)
        actions = ActionChains(navegador)
        actions.move_to_element(confirm_title_btn).click().perform()
        time.sleep(1)

        # Set publish date and time 
        publish_datetime = (base_datetime + timedelta(minutes=idx*4)).strftime("%Y-%m-%d %H:%M:%S")
        datetime_input = navegador.find_element(By.CSS_SELECTOR, "input.ks-input__inner[placeholder='Select a date']")
        datetime_input.clear()
        datetime_input.send_keys(publish_datetime)
        datetime_input.send_keys(Keys.ENTER)
        time.sleep(1)

        # Submit
        submit_button = navegador.find_element(By.XPATH, "//button[contains(@class, 'ks-button--primary') and span[contains(., 'Submit')]]")
        submit_button.click()
        time.sleep(5)

        # Delete the video after upload
        try:
            os.remove(video_path)
            print(f"Deleted: {video_path}")
        except Exception as e:
            print(f"Error deleting {video_path}: {e}")

        success_count += 1
    except Exception as e:
        error_count += 1
        continue  # Skip to next video

    print_progress(idx)

print()
print(f"\nFinished! Success: {success_count}, Skipped: {skipped_count}, Errors: {error_count}")

navegador.quit()



