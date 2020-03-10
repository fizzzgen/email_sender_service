import unittest
import mock
import engine
import multiprocessing
import time
import sqlite3


class TestSchedulingTestCase(unittest.TestCase):

    def check_diff(self, file1, file2):
        with open(file1, 'r') as f1:
            with open(file2, 'r') as f2:
                assert f1.read() == f2.read()

    def test_scheduler(self):
        filename = 'ut/test.output'
        canonical = 'ut/test.canonical'
        with open(filename, 'w') as f:
            f.write('TEST\n')

        def log_output(*args, **kwargs):
            conn = sqlite3.connect('db.sqlite')
            cur = conn.cursor()
            cur.execute(
                'UPDATE queue SET status="SENT" where id=?',
                (kwargs['email_id'], )
            )
            conn.commit()
            conn.close()
            string = str((args, kwargs))
            with open(filename, 'a') as f:
                f.write(string + '\n')
            return

        def get_default_values_from_spreadsheet(spreadsheet_id):
            dict_values = []
            dict_values.append(
                {
                    'to_addr': 'fizzzgen@gmail.com',
                    'html_text': 'HELLO',
                    'subject': 'HELLO',
                    'unsubscribe_link': 'HELLO'
                }
            )
            return dict_values

        self.patch_0 = mock.patch(
            'reader.reader.get_default_values_from_spreadsheet',
            get_default_values_from_spreadsheet
        )
        self.patch_1 = mock.patch(
            'engine.email_processor.sender.send_email',
            log_output
        )
        with self.patch_1:
            with self.patch_0:
                self.poll = multiprocessing.Process(
                    target=engine.email_processor.poll
                )
                self.poll.start()
                engine.email_processor.schedule(
                    'KIRILL',
                    'new-year@simple-digital.ru',
                    'qazwsxedc123',
                    'smtp.yandex.ru:465',
                    '/d/1DN_cpfs9b1w5DTVcm2NZ_MHxUOfrUQ4LwGui8JzhTFY/edit',
                )
                time.sleep(5)
                engine.email_processor.schedule(
                    'KIRILL',
                    'new-year@simple-digital.ru',
                    'qazwsxedc123',
                    'smtp.yandex.ru:465',
                    '/d/1DN_cpfs9b1w5DTVcm2NZ_MHxUOfrUQ4LwGui8JzhTFY/edit',
                )
                time.sleep(5)
                self.poll.terminate()
        self.check_diff(filename, canonical)
