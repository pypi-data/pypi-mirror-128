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

    @staticmethod
    def __normalize_content(content):
        if not isinstance(content, list):
            content = [content]
        return content

    @staticmethod
    def __log_response(response):
        if GOOGLE_LOG_RESPONSE:
            logger.info("google api response: %s", response)

    def send_single_message(self, content, _settings):
        logger.info("seding single message to google chat")
        content = self.__normalize_content(content)

        first_message = content.pop(0)
        data = {"text": first_message}

        response = post(
            GOOGLE_DEFAULT_CHAT_ROOM, data=json.dumps(data), headers=HEADERS
        ).json()
        self.__log_response(response)

        self.__send_to_thread(response["thread"], content)

    def init_thread(self, content, _settings):
        logger.info("creating a new thread in google chat")
        content = self.__normalize_content(content)

        first_message = content.pop(0)
        data = {"text": first_message}

        response = post(
            GOOGLE_DEFAULT_CHAT_ROOM, data=json.dumps(data), headers=HEADERS
        ).json()
        self.__log_response(response)

        thread_id = response["thread"]
        self.__send_to_thread(thread_id, content)

        return thread_id

    def update_thread(self, thread_id, content, _settings):
        logger.info("updating thread %s in google chat", thread_id)
        self.__send_to_thread(thread_id, content)

    def close_thread(self, thread_id, content, _settings):
        logger.info("closing thread %s in google chat", thread_id)
        self.__send_to_thread(thread_id, content)

    def __send_to_thread(self, thread_id, content):
        if not isinstance(content, list):
            content = [content]

        for entry in content:
            data = {"text": entry, "thread": thread_id}
            response = post(
                GOOGLE_DEFAULT_CHAT_ROOM, data=json.dumps(data), headers=HEADERS
            ).json()
            self.__log_response(response)
