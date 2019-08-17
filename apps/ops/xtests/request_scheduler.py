from requests.api import request
import uuid


def test_add_job():
    resp = request(method="post",
                   url="http://localhost:3022/v1/cron/job/",
                   json=dict(cron="*/30 * * * * *", job_id="322", params={"task_name": "print5", "args": [1, 2, 3]}),
                   headers={'Content-Type': 'application/json'},
                   verify=False)

    print(resp.status_code)
    print(resp.content.decode('utf-8'))


def test_list_jobs():
    resp = request(method="get",
                   url="http://localhost:4033/v1/cron/job/",
                   headers={'Content-Type': 'application/json'},
                   verify=False)

    print(resp.status_code)
    print(resp.content.decode('utf-8'))


if __name__ == '__main__':
    test_add_job()

