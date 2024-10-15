# main.py

from bot.meet_joiner import join_google_meet
from config import MEETING_URL, VIDEO_URL
from bot.utils import print_welcome_message
from bot.models import MeetJoinerConfig


if __name__ == "__main__":
    # Load configuration
    config = MeetJoinerConfig(meeting_url=MEETING_URL, video_url=VIDEO_URL)

    # Print welcome message
    print_welcome_message()

    # Start the process of joining the Google Meet and recording audio
    join_google_meet(config)
