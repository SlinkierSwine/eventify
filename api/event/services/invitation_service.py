import logging
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from event.exceptions import EventException
from event.models import Event

logger = logging.getLogger(__name__)


class InvitationService:
    @classmethod
    def get_invitation_link(cls, event: Event) -> str:
        uid = urlsafe_base64_encode(force_bytes(event.pk))
        link = settings.EVENT_INVITATION_URL + "/" + uid
        return link

    @classmethod
    def decode_uid(cls, uid: str) -> str:
        try:
            return urlsafe_base64_decode(uid).decode()
        except Exception as e:
            logger.error(e)
            raise EventException("Invitation link is invalid")

    @classmethod
    def get_event_from_uid(cls, uid: str) -> Event:
        event_id = cls.decode_uid(uid)
        return get_object_or_404(Event, pk=event_id)
