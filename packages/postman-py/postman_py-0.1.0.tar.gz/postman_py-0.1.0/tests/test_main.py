"""Tests for `postman_py` package."""

from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

import pytest
from pytest_mock import MockerFixture

from postman_py.main import SMTPConf, add_attachment, draft_message, send_message


@pytest.fixture
def sender() -> str:
    return "sender@mail.py"


@pytest.fixture
def receiver() -> str:
    return "receiver@mail.py"


@pytest.fixture
def subject() -> str:
    return "This is the test email subject"


@pytest.fixture
def body() -> str:
    return "<html><body><p>This is the test email body.</p></body></html>"


@pytest.fixture
def message(sender: str, receiver: str, subject: str, body: str) -> MIMEMultipart:
    message: MIMEMultipart = MIMEMultipart()
    message["From"] = sender
    message["To"] = receiver
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    message.attach(MIMEText(body, "html"))
    return message


@pytest.fixture
def asset(tmp_path: Path) -> Path:
    asset: Path = tmp_path.joinpath("asset.txt")
    with asset.open(mode="wb") as binio:
        binio.write(b"1")
    return asset


@pytest.fixture
def conf() -> SMTPConf:
    return SMTPConf("0.0.0.0", "alex", 25, "password")


def test_draft_message(sender: str, receiver: str, subject: str, body: str) -> None:
    message = draft_message(sender, receiver, subject, body)
    assert message["From"] == sender
    assert message["To"] == receiver
    assert message["Subject"] == subject
    assert isinstance(message.get_payload()[0], MIMEText)
    assert isinstance(message.get_payload()[1], MIMEText)


def test_add_attachment(message: MIMEMultipart, asset: Path) -> None:
    message_with_attachment: MIMEMultipart = add_attachment(message, asset)
    assert isinstance(message_with_attachment.get_payload()[2], MIMEBase)


def test_send_message(
    mocker: MockerFixture, message: MIMEMultipart, conf: SMTPConf
) -> None:
    patched_smtp = mocker.patch("postman_py.main.SMTP")
    send_message(message, conf)
    patched_smtp.assert_any_call(conf.host, conf.port)  # Test constructor
    patched_smtp_ret = patched_smtp.return_value
    patched_smtp_ret.ehlo.assert_any_call()  # Test ehlo
    patched_smtp_ret.login.assert_any_call(conf.user, conf.password)
    patched_smtp_ret.sendmail.assert_any_call(
        message["From"], message["To"], message.as_string()
    )
