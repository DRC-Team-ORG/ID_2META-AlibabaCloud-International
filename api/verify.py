from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import os
from alibabacloud_cloudauth_intl20220809.client import Client as CloudauthIntl20220809Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_cloudauth_intl20220809 import models as cloudauth_models
from alibabacloud_tea_util import models as util_models

app = FastAPI()

def create_client():
    access_key_id = os.getenv('ALIBABA_CLOUD_ACCESS_KEY_ID')
    access_key_secret = os.getenv('ALIBABA_CLOUD_ACCESS_KEY_SECRET')
    if not access_key_id or not access_key_secret:
        return None, 'Missing AK/SK envs'
    config = open_api_models.Config(access_key_id=access_key_id, access_key_secret=access_key_secret)
    config.endpoint = 'cloudauth-intl.cn-hongkong.aliyuncs.com'
    return CloudauthIntl20220809Client(config), None

def to_status(biz):
    b = str(biz) if biz is not None else ""
    if b == "1": return "match"
    if b == "2": return "mismatch"
    if b == "3": return "not_found"
    return "unknown"

@app.post("/api/verify")
async def verify(request: Request):
    data = await request.json()
    name = data.get('name')
    id_number = data.get('idNumber')
    if not name or not id_number:
        return JSONResponse(content={"error": "name and idNumber are required"}, status_code=400)

    # 可选：Bearer Token 保护
    api_token = os.getenv("API_TOKEN")
    auth = request.headers.get("authorization", "").replace("Bearer ", "")
    if api_token and auth != api_token:
        return JSONResponse(content={"error": "Unauthorized"}, status_code=401)

    client, err = create_client()
    if err:
        return JSONResponse(content={"error": err}, status_code=500)

    try:
        req = cloudauth_models.Id2MetaVerifyIntlRequest(
            product_code="ID_2META",
            param_type="normal",
            user_name=name,
            identify_num=id_number
        )
        resp = client.id_2meta_verify_intl_with_options(req, util_models.RuntimeOptions())
        biz = getattr(resp.body.result, "biz_code", None)
        return JSONResponse(content={
            "requestId": resp.body.request_id,
            "code": resp.body.code,
            "message": resp.body.message,
            "bizCode": str(biz) if biz is not None else None,
            "status": to_status(biz)  # 前端只看这个来决定显示
        })
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
