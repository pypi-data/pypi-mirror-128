"""Main module."""
from copy import copy
from dataclasses import dataclass
from email.encoders import encode_base64
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from smtplib import SMTP
from typing import BinaryIO


@dataclass
class SMTPConf:
    """The SMTPConf stores configuration references for connecting to a SMTP server.

    :param host: The host address of the SMTP server. Expects a `str` like
                 `smtp.mailservice.com`.
    :param user: The `str` user credential required for a successful login.
    :param port: The `int` configured port of the SMTP server.
    :param password: The `str` password credential for a successful login.
    """

    host: str
    user: str
    port: int
    password: str


def draft_message(sender: str, receiver: str, subject: str, body: str) -> MIMEMultipart:
    """Return a `MIMEMultipart` object with the relevant headers and payload.

    :param sender: The `str` email address of the sender.
    :param receiver: The `str` email address of the receiver.
    :param subject: The `str` message subject matter.
    :param body: The `str` textual element of the message body.
    :returns: A `MIMEMultipart` object with headers and payload updated.
    """
    message: MIMEMultipart = MIMEMultipart()
    message["From"] = sender
    message["To"] = receiver
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    message.attach(MIMEText(body, "html"))
    return message


def add_attachment(message: MIMEMultipart, attachment: Path) -> MIMEMultipart:
    """Return a `MIMEMultipart` object with the asset at the path `attachment` attached
    to the payload. The header is also updated.

    :param message: A `MIMEMultipart` object with headers pre-set.
    :param attachment: A `Path` to an asset to be attached to the `message` payload.
    :returns: A `MIMEMultipart` object from the supplied `message` with the asset at
              `attachment` attached to the payload with the headers updated.
    """
    binio: BinaryIO
    with attachment.open(mode="rb") as binio:
        mime_base: MIMEBase = MIMEBase("application", "octet-stream")
        mime_base.set_payload(binio.read())
    encode_base64(mime_base)
    mime_base.add_header(
        "Content-Disposition", f"attachment; filename={attachment.name}"
    )
    _message = copy(message)
    _message.attach(mime_base)
    return _message


def send_message(message: MIMEMultipart, smtp_conf: SMTPConf) -> None:
    """Sends the `message` using SMTP configuration `smtp_conf`.

    All login and TLS handling is done internally.

    :param message: A `MIMEMultipart` object message.
    :param smtp_conf: A `SMTPConf` object referencing desired settings.
    """
    smtp: SMTP = SMTP(smtp_conf.host, smtp_conf.port)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(smtp_conf.user, smtp_conf.password)
    smtp.sendmail(message["From"], message["To"], message.as_string())
    smtp.quit()
