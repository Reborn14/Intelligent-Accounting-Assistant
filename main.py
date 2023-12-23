from fastapi import FastAPI, HTTPException, Request, Depends, Security, Body
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel, Field
from loguru import logger
import httpx
import os
from datetime import datetime
import pytz
from typing import List, Dict

app = FastAPI()

# 从环境变量中获取配置
app_id = os.getenv("APP_ID")
app_secret = os.getenv("APP_SECRET")
app_token = os.getenv("APP_TOKEN")
table_id = os.getenv("TABLE_ID")
api_key = os.getenv("API_KEY")  # API 密钥

# API 密钥鉴权
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == api_key:
        return api_key_header
    else:
        raise HTTPException(status_code=403, detail="Invalid API Key")


@app.get("/get-access-token")
async def get_access_token(api_key: str = Depends(get_api_key)):
    # 从环境变量读取飞书应用凭证
    auth_data = {"app_id": app_id, "app_secret": app_secret}
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=auth_data)
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail="Failed to get access token")
        return resp.json()["tenant_access_token"]


@app.get("/get-fields")
async def get_fields(api_key: str = Depends(get_api_key)):
    # 使用之前获取的tenant_access_token
    tenant_access_token = await get_access_token()
    headers = {"Authorization": f"Bearer {tenant_access_token}"}
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/fields"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail="Failed to get fields")
        return resp.json()

def convert_unix_timestamp_to_datetime(unix_timestamp):
    timestamp_in_seconds = unix_timestamp / 1000
    date_time = datetime.fromtimestamp(timestamp_in_seconds, tz=pytz.utc)
    date_time = date_time.astimezone(pytz.timezone('Asia/Shanghai'))  # 转换到中国标准时间（UTC+8）
    return date_time.strftime("%Y-%m-%d %H:%M:%S")


@app.get("/list-records")
async def list_records(filter: str = None, api_key: str = Depends(get_api_key)):
    # 获取访问令牌
    tenant_access_token = await get_access_token()

    # 构造请求URL和头部
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records"
    headers = {"Authorization": f"Bearer {tenant_access_token}"}
    params = {"filter": filter} if filter else {}

    # 发送请求
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers, params=params)
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail="Failed to list records")

    # 将时间戳转换为可读的日期时间
    records = resp.json()["data"]["items"]
    summary = {
        "收入": {"总收入": 0},
        "支出": {"总支出": 0}
    }

    for record in records:
        if "创建日期" in record["fields"]:
            unix_timestamp = record["fields"]["创建日期"]
            readable_date = convert_unix_timestamp_to_datetime(unix_timestamp)
            record["fields"]["创建日期"] = readable_date
        
        # 累加计算
        category = record["fields"]["收支类别"]
        bill_type = record["fields"]["账单类别"]
        amount = float(record["fields"]["账单金额"])

        if category not in summary:
            summary[category] = {}

        if bill_type not in summary[category]:
            summary[category][bill_type] = 0

        summary[category][bill_type] += amount
        if category == "收入":
            summary["收入"]["总收入"] += amount
        elif category == "支出":
            summary["支出"]["总支出"] += amount
    
    # 返回响应数据
    return {"records": records, "summary": summary}

def datetime_str_to_utc_timestamp(date_str):
    # 将字符串转换为datetime对象
    date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    # 设置为中国标准时间（UTC+8）
    tz = pytz.timezone('Asia/Shanghai')
    date_obj = tz.localize(date_obj)
    # 转换为UTC+8时间戳（毫秒）
    return int(date_obj.timestamp() * 1000)
class RecordUpdateRequest(BaseModel):
    record_id: str
    update_fields: dict

@app.post("/gpt-update-record")
async def gpt_update_record(update_request: RecordUpdateRequest, api_key: str = Depends(get_api_key)):
    # 获取访问令牌
    tenant_access_token = await get_access_token()

    # 检查并转换“创建日期”
    if "创建日期" in update_request.update_fields:
        update_request.update_fields["创建日期"] = datetime_str_to_utc_timestamp(update_request.update_fields["创建日期"])

    # 构造请求URL和头部
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/{update_request.record_id}"
    headers = {"Authorization": f"Bearer {tenant_access_token}", "Content-Type": "application/json"}

    # 发送请求
    async with httpx.AsyncClient() as client:
        resp = await client.put(url, headers=headers, json={"fields": update_request.update_fields})
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail="Failed to update record")

    # 返回响应数据
    return resp.json()


@app.post("/gpt-delete-record")
async def gpt_delete_record(record_id: str, api_key: str = Depends(get_api_key)):
    # 获取访问令牌
    tenant_access_token = await get_access_token()

    # 构造请求URL和头部
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/{record_id}"
    headers = {"Authorization": f"Bearer {tenant_access_token}"}

    # 发送请求
    async with httpx.AsyncClient() as client:
        resp = await client.delete(url, headers=headers)
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail="Failed to delete record")

    # 返回响应数据
    return resp.json()



@app.post("/create-record")
async def create_record(request: Request, api_key: str = Depends(get_api_key)):
    # 获取访问令牌
    tenant_access_token = await get_access_token()

    # 从请求中获取用户输入的完整请求体
    user_input = await request.json()

    # 构造请求头
    headers = {"Authorization": f"Bearer {tenant_access_token}", "Content-Type": "application/json"}

    # 调用飞书接口创建记录
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records"
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, headers=headers, json=user_input)
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail="Failed to create record in Feishu")

    # 返回飞书接口的响应
    return resp.json()