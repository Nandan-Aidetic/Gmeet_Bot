# main.py

from recorder.meet_joiner import join_google_meet
from config import MEETING_URL, RECORD_DURATION
from recorder.utils import print_welcome_message
from pydantic import BaseModel

class MainConfig(BaseModel):
    meeting_url: str = MEETING_URL
    record_duration: int = RECORD_DURATION

if __name__ == "__main__":
    # Load configuration
    config = MainConfig()

    # Print welcome message
    print_welcome_message()

    # Start the process of joining the Google Meet and recording audio
    join_google_meet(config)
