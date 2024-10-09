# recorder/meet_joiner.py

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from pydantic import BaseModel
from recorder.audio_recorder import record_audio
from typing import Union
from recorder.models import AudioRecorderConfig, MeetJoinerConfig





def get_participant_count(driver) -> int:
    """Fetches the number of participants in the meeting."""
    try:

        sample_div = driver.find_element(
            By.XPATH, '//div[contains(text(), "Contributors")]'
        )
        time.sleep(5)
        contributor_count_element = sample_div.find_element(
            By.XPATH, "following-sibling::*[1]"
        )
        contributor_count = contributor_count_element.text
        print(contributor_count, "9"*9)
        print(f"Contributor Count: {contributor_count}")
        return int(contributor_count)
    except Exception as e:
        print(f"Error while fetching participant count: {e}")
        return 0


def mute_audio_camera_before_join(driver) -> None:
    """Mute the microphone and camera before joining the meeting."""
    try:
        mute_mic_button = driver.find_element(
            By.XPATH, '//div[contains(@aria-label, "microphone")]'
        )
        mute_mic_button.click()
        print("Microphone muted in preview.")

        mute_camera_button = driver.find_element(
            By.XPATH, '//div[contains(@aria-label, "camera")]'
        )
        mute_camera_button.click()
        print("Camera muted in preview.")
    except Exception as e:
        print(f"Error muting microphone or camera: {e}")


def is_in_meeting(driver) -> bool:
    """Check if the bot has successfully joined the meeting."""
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, '//div[contains(text(), "Guest Bot")]')
            )
        )
        print("Bot has joined the meeting.")
        return True
    except Exception as e:
        print(f"Error detecting meeting: {e}")
        return False


def leave_meeting(driver) -> None:
    """Leave the Google Meet session."""
    try:
        leave_button = driver.find_element(
            By.XPATH, "//button[@aria-label='Leave call']"
        )
        leave_button.click()
        print("Clicked 'Leave call'. Leaving the meeting...")
    except Exception as e:
        print(f"Error while leaving the meeting: {e}")


def join_google_meet(config: MeetJoinerConfig) -> None:
    """Join a Google Meet session and start recording audio."""
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
            time.sleep(20)
        except Exception:
            try:
                join_button = driver.find_element(By.XPATH, '//span[text()="Join now"]')
                join_button.click()
                print("Clicked 'Join now'.")
            except Exception:
                print("Neither 'Ask to join' nor 'Join now' button found.")
                return

        # Click the 'People' button once at the start
        try:
            people_button = driver.find_element(By.XPATH, "//button[@aria-label='People']")
            people_button.click()
            print("Opened participants list.")
            time.sleep(5)
        except Exception as e:
            print(f"Error opening participants list: {e}")
            return

        # Check if the bot is in the meeting
        if is_in_meeting(driver):
            print("Joined the meeting. Starting audio recording...")

            # Start the audio recording
            recorder = record_audio(AudioRecorderConfig(output_file="meeting_recording.wav"))

            # Periodically check participants and stop recording if no participants
            while True:
                time.sleep(10)  # Wait before checking participant count again
                if get_participant_count(driver) <= 1:
                    print("Stopping the recording due to no participants.")
                    time.sleep(5)
                    recorder.stop_recording()
                    leave_meeting(driver)  # Leave the meeting if participant count is <= 1
                    break  # Exit the loop to end the recording session

    finally:
        # Ensure the driver quits after the meeting ends or if any error occurs
        print("Quitting the driver.")
        driver.quit()

