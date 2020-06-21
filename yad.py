import os
import posixpath
from typing import Optional

import yadisk


def get_yad_client(yad_id: str, yad_password: str, yad_token: Optional[str]) -> yadisk.YaDisk:
    if yad_token is None:
        yad_token = receive_token(yad_id, yad_password)
    client = yadisk.YaDisk(id=yad_id, secret=yad_password, token=yad_token)
    client.check_token()
    return client


def recursive_upload(yad_client: yadisk.YaDisk, source: str, dest: str):
    for root, dirs, files in os.walk(source):
        p = root.split(source)[1].strip(os.path.sep)
        dir_path = posixpath.join(dest, p)
        if yad_client.exists(dir_path):
            yad_client.remove(dir_path)
        yad_client.mkdir(dir_path)
        for file in files:
            file_path = posixpath.join(dir_path, file)
            p_sys = p.replace("/", os.path.sep)
            in_path = os.path.join(source, p_sys, file)
            print(f"Uploading {in_path} to {file_path}")
            yad_client.upload(in_path, file_path)
            print("Done")


def receive_token(yad_id: str, yad_password: str) -> str:
    y = yadisk.YaDisk(yad_id, yad_password)
    url = y.get_code_url()
    print("Go to the following url: %s" % url)
    code = input("Enter the confirmation code: ")
    response = y.get_token(code)
    y.token = response.access_token
    if y.check_token():
        print(f"Successfully received token: {y.token}")
    else:
        print("Something went wrong. Not sure how though...")
    return y.token
