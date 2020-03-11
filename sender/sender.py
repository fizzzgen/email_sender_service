import logging
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication # noqa
from email.mime.image import MIMEImage

logger = logging.getLogger('root')

_IMG_HTML_NAME = '<image1>'

fail_log = '[send_email] Fail: message from {} to {} id {} not sent... Retrying: {}'
fail_log2 = '[send_email] Fail: message from {} to {} id {} not sent... End retrying'


def send_email(
        login,
        password,
        server,
        to_addr,
        html_text,
        subject,
        unsubscribe_link,
        retry_nums=2,
        retry_interval=5,
        image_path=None,
        testing=True,
        email_id=1,
):

    # Retrying to send message if not success
    for i in range(retry_nums):
        conn = sqlite3.connect('db.sqlite')
        cur = conn.cursor()
        try:
            server = smtplib.SMTP_SSL(server, 465)
            server.login(login, password)
            server.auth_plain()

            msg = MIMEMultipart('related')
            msg['Subject'] = subject
            msg['From'] = login
            msg['To'] = to_addr
            msg['List-Unsubscribe'] = unsubscribe_link

            part = MIMEText('')
            msg.attach(part)
            msga = MIMEMultipart('alternative')
            msgText = MIMEText(html_text, 'html')
            msga.attach(msgText)
            msg.attach(msga)

            if image_path:
                assert _IMG_HTML_NAME in html_text
                # This example assumes the image is in the current directory
                fp = open(image_path, 'rb')
                msgImage = MIMEImage(fp.read())
                fp.close()

                # Define the image's ID as referenced above
                msgImage.add_header('Content-ID', _IMG_HTML_NAME)
                msg.attach(msgImage)

            if not testing:
                server.sendmail(login, to_addr, msg.as_string())

            server.quit()
            logger.info(
                '[send_email] Success: message from {} to {} sent'.format(
                    login,
                    to_addr,
                    email_id,
                )
            )
            cur.execute(
                'UPDATE queue SET status="SENT" where id=?', (email_id,)
            )
            conn.commit()
            conn.close()
            return True

        except Exception as ex:
            logger.warning(fail_log.format(login, to_addr, ex, email_id))
            exception = "EXCEPTION"
            if 'password' in repr(ex) or 'Password' in repr(ex):
                exception = "WRONG LOGIN OR PASSWORD"
            elif 'spam' in repr(ex) or 'Spam' in repr(ex):
                exception = "SPAM"
            else:
                exception = "BAD SMTP SERVER"
            cur.execute(
                'UPDATE queue SET status=? where id=?',
                (exception, email_id,)
            )
    conn.commit()
    conn.close()
    logger.warning(fail_log2.format(login, to_addr, email_id))
    return False
