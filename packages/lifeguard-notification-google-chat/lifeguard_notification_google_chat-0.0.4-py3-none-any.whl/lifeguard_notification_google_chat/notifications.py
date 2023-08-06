"""
Base of notification system
"""
import json

from lifeguard.http_client import post
from lifeguard.logger import lifeguard_logger as logger
from lifeguard.notifications import NotificationBase

from lifeguard_notification_google_chat.settings import (
    GOOGLE_DEFAULT_CHAT_ROOM,
    GOOGLE_LOG_RESPONSE,
)

HEADERS = {"Content-Type": "application/json; charset=UTF-8"}


class GoogleNotificationBase(NotificationBase):
    """
    Base of notification
    """

    @property
    def name(self):
        return "google-chat"

    def send_single_message(self, content, _settings):
        logger.info("seding single message to google chat")
        data = {"text": content}
        response = post(
            GOOGLE_DEFAULT_CHAT_ROOM, data=json.dumps(data), headers=HEADERS
        )
        if GOOGLE_LOG_RESPONSE:
            logger.info("google api response: %s", response.json())

    def init_thread(self, content, _settings):
        logger.info("creating a new thread in google chat")
        data = {"text": content}
        content = post(
            GOOGLE_DEFAULT_CHAT_ROOM, data=json.dumps(data), headers=HEADERS
        ).json()

        if GOOGLE_LOG_RESPONSE:
            logger.info("google api response: %s", content.json())

        return content["thread"]

    def update_thread(self, thread_id, content, _settings):
        logger.info("updating thread %s in google chat", thread_id)
        self.__send_to_thread(thread_id, content)

    def close_thread(self, thread_id, content, _settings):
        logger.info("closing thread %s in google chat", thread_id)
        self.__send_to_thread(thread_id, content)

    def __send_to_thread(self, thread_id, content):
        data = {"text": content, "thread": thread_id}
        response = post(
            GOOGLE_DEFAULT_CHAT_ROOM, data=json.dumps(data), headers=HEADERS
        )
        if GOOGLE_LOG_RESPONSE:
            logger.info("google api response: %s", response.json())
