from datetime import date
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

class Emailer:
    def __init__(self, **kwargs):
        self.to_emails = kwargs['to_emails']
        self.from_email = kwargs['from_email']
        self.from_email_password = kwargs['from_email_password']

    # TODO these functions are largely the same
    # TODO also arguably we dont want to make the to-emails fixed...? idk

    def send_html_email(self, subject, sent_from, message_html, images=[], **kwargs):
        """

        :param subject:
        :param sent_from:
        :param message_html:
        :param images: list of dicts like { path: '/path/to/file', id: 'name of file?' }
        :return:
        """

        verbose = kwargs.get('verbose') or False

        msg_related = MIMEMultipart('related')

        msg_related['Subject'] = subject
        msg_related['From'] = sent_from
        msg_related['To'] = ', '.join(self.to_emails)
        msg_related.preamble = 'This is a multi-part message in MIME format.'

        msg_alternative = MIMEMultipart('alternative')
        msg_related.attach(msg_alternative)

        html_part = MIMEText(message_html, 'html')

        msg_alternative.attach(html_part)

        for image in images:
            with open(image['path'], 'rb') as f:
                msg_image = MIMEImage(f.read())
                msg_image.add_header('Content-ID', '<{0}>'.format(image['id']))
                msg_related.attach(msg_image)

        server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server_ssl.ehlo()
        server_ssl.login(self.from_email, self.from_email_password)
        server_ssl.sendmail(sent_from, self.to_emails, msg_related.as_string())
        server_ssl.close()
        if verbose:
            print(f'{date.today()} Email sent')


    def send_email(self, body, subject, sent_from, **kwargs):
        """

        :param body: email body
        :param subject:  email subject
        :param sent_from: the "name" that will appear as who sent the email
        :return:
        """

        verbose = kwargs.get('verbose') or False

        email_text = f"""\
    From: {sent_from}
    To: {','.join(self.to_emails)}
    Subject: {subject}

    {body}
    """

        server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server_ssl.ehlo()
        server_ssl.login(self.from_email, self.from_email_password)
        server_ssl.sendmail(sent_from, self.to_emails, email_text)
        server_ssl.close()
        if verbose:
            print(f'{date.today()} Sent email')
