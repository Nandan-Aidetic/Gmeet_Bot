# recorder/meet_joiner.py

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from pydantic import BaseModel
from typing import Union
from recorder.audio_recorder import AudioRecorderConfig

class MeetJoinerConfig(BaseModel):
    meeting_url: str
    record_duration: int

def mute_audio_camera_before_join(driver) -> None:
    """
    Mute the microphone and camera before joining the meeting.
    
    :param driver: The Selenium WebDriver instance controlling the browser.
    """
    try:
        mute_mic_button = driver.find_element(By.XPATH, '//div[contains(@aria-label, "microphone")]')
        mute_mic_button.click()
        print("Microphone muted in preview.")

        mute_camera_button = driver.find_element(By.XPATH, '//div[contains(@aria-label, "camera")]')
        mute_camera_button.click()
        print("Camera muted in preview.")
    except Exception as e:
        print(f"Error muting microphone or camera: {e}")

def is_in_meeting(driver) -> bool:
    """
    Check if the bot has successfully joined the meeting.
    
    :param driver: The Selenium WebDriver instance controlling the browser.
    :return: True if the bot has joined, otherwise False.
    """
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Guest Bot")]')))
        print("Bot has joined the meeting.")
        return True
    except Exception as e:
        print(f"Error detecting meeting: {e}")
        return False

def join_google_meet(config: MeetJoinerConfig) -> None:
    """
    Join a Google Meet session and start recording audio.
    
    :param config: Configuration object containing the meeting URL and record duration.
    """
    chrome_options = Options()
    chrome_options.add_argument("--use-fake-ui-for-media-stream")  # Automatically allow microphone and camera access

    driver = uc.Chrome(options=chrome_options)

    try:
        driver.get(config.meeting_url)
        time.sleep(5)

        # Check if you need to enter a name as a guest
        try:
            name_input = driver.find_element(By.XPATH, '//input[@aria-label="Your name"]')
            name_input.send_keys("Guest Bot")
            time.sleep(2)
        except Exception:
            print("No guest name required.")

        mute_audio_camera_before_join(driver)

        # Handle the "Ask to join" or "Join now" button
        try:
            ask_to_join_button = driver.find_element(By.XPATH, '//span[text()="Ask to join"]')
            ask_to_join_button.click()
            print("Clicked 'Ask to join'. Waiting for host approval...")
        except Exception:
            try:
                join_button = driver.find_element(By.XPATH, '//span[text()="Join now"]')
                join_button.click()
                print("Clicked 'Join now'.")
            except Exception:
                print("Neither 'Ask to join' nor 'Join now' button found.")
                return

        for _ in range(10):  # Retry for up to ~30 seconds
            if is_in_meeting(driver):
                print("Joined the meeting. Starting audio recording...")
                from recorder.audio_recorder import record_audio
                record_audio(AudioRecorderConfig(duration=config.record_duration))
                break
            time.sleep(3)

        # Stay in the meeting for the duration
        time.sleep(config.record_duration)

    finally:
        driver.quit()
