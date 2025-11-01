# -*- coding: utf-8 -*-

import requests
import json
from datetime import datetime, timedelta
import pytz
import time
import re
from requests.auth import HTTPBasicAuth

# 配置项 http://10.53.0.71:7180/api/v33/clusters/Cluster/services/impala/impalaQueries
CDH_API_URL = "http://10.53.0.71:7180/api/v33/clusters/Cluster/services/impala/impalaQueries"
WEBHOOK_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=34f51e63-9ab5-43fa-8621-377b7bf70064"
CHECK_INTERVAL = 1  # 检查间隔（秒）
MAX_RETRIES = 3  # 网络请求重试次数
ALERT_WINDOW = timedelta(hours=1)  # 告警窗口时间[4](@ref)

# 需要忽略的错误类型列表
IGNORED_ERRORS = [
    "expired due to client inactivity",
    "ParseException: Syntax error",
    "Encountered: FROM\nExpected:",
    "AnalysisException: Could not resolve column/field reference",
    "AnalysisException: operands of type STRING and TINYINT are not comparable",
    "AnalysisException: Column/field reference is ambiguous",
    "AnalysisException: Table already exists",
    "AnalysisException: GROUP BY expression must not contain aggregate functions",
    "AnalysisException: select list expression not produced by aggregation output",
    "AnalysisException: cannot combine",
    "AnalysisException: ORDER BY expression not produced by aggregation output",
    "AnalysisException: Could not resolve path",
    "AnalysisException: operands of type INT and STRING are not comparable",
    "ParseException: Unmatched string literal in line 3",
    "AuthorizationException: User",
    "Cancelled\n"
]

# 全局变量：存储已告警的queryId和告警时间
alerted_queries = {}  # {query_id: alert_time}

def get_running_impala_queries():
    """
    从CDH API获取正在运行的Impala查询[1,3](@ref)
    :return:
    """
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(
                CDH_API_URL,
                auth=HTTPBasicAuth('admin', 'Turing@12345'),
                timeout=15
            )
            response.raise_for_status()
            return response.json() if response.text else None
        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            print(f"[Error] 获取Impala查询失败（尝试 {attempt+1}/{MAX_RETRIES}）: {str(e)}")
            time.sleep(3)
    return None

def send_alert_via_webhook(alert_message):
    """
    通过企业微信Webhook发送告警[4](@ref)
    :param alert_message:
    :return:
    """
    payload = {
        "msgtype": "markdown",
        "markdown": {
            "content": alert_message
        }
    }
    headers = {"Content-Type": "application/json"}

    for attempt in range(MAX_RETRIES):
        try:
            response = requests.post(WEBHOOK_URL, json=payload, headers=headers, timeout=15)
            response.raise_for_status()
            print(f"[Success] 告警发送成功: {alert_message[:100]}...")
            return True
        except requests.exceptions.RequestException as e:
            print(f"[Error] 发送告警失败（尝试 {attempt+1}/{MAX_RETRIES}）: {str(e)}")
            time.sleep(3)
    return False

def convert_to_china_time(utc_time_str):
    """
    将UTC时间转换为中国时区时间
    :param utc_time_str:
    :return:
    """
    if not utc_time_str:
        return None
    try:
        # 处理可能的Z时区标识
        if utc_time_str.endswith('Z'):
            utc_time_str = utc_time_str[:-1] + '+00:00'
        utc_time = datetime.fromisoformat(utc_time_str)
        return utc_time.astimezone(pytz.timezone('Asia/Shanghai'))
    except (ValueError, TypeError) as e:
        print(f"[Warning] 时间转换失败: {str(e)}")
        return None

def bytes_to_gb(bytes_val):
    """
    将字节转换为GB
    :param bytes_val:
    :return:
    """
    try:
        if isinstance(bytes_val, str):
            return int(bytes_val) / (1024 ** 3)
        return (bytes_val or 0) / (1024 ** 3)
    except (ValueError, TypeError):
        return 0.0

def is_ignored_error(error_message):
    """
    检查错误是否在忽略列表中
    :param error_message:
    :return:
    """
    if not error_message:
        return False

    for pattern in IGNORED_ERRORS:
        if pattern in error_message:
            print(f"[Info] 忽略已知错误: {pattern}")
            return True

    return False

def calculate_duration(start_time, end_time):
    """
    计算查询耗时[4](@ref)
    :param start_time:
    :param end_time:
    :return:
    """
    if not start_time:
        return "N/A"

    if end_time:
        # 计算精确的执行时长
        duration_seconds = (end_time - start_time).total_seconds()
        return f"{duration_seconds:.2f}秒"
    else:
        # 计算从开始到现在的运行时长
        now = datetime.now(pytz.timezone('Asia/Shanghai'))
        duration_seconds = (now - start_time).total_seconds()
        return f"{duration_seconds:.2f}秒（运行中）"

def format_time(dt):
    """
    格式化时间显示
    :param dt:
    :return:
    """
    return dt.strftime("%Y-%m-%d %H:%M:%S") if dt else "N/A"

def cleanup_alerted_queries():
    """
    清理过期的告警记录[4](@ref)
    :return:
    """
    global alerted_queries
    now = datetime.now(pytz.timezone('Asia/Shanghai'))
    expired_ids = [qid for qid, alert_time in alerted_queries.items()
                   if now - alert_time > ALERT_WINDOW]

    for qid in expired_ids:
        del alerted_queries[qid]

    if expired_ids:
        print(f"[Cleanup] 清理过期告警记录: {len(expired_ids)}条")

def monitor_impala_queries():
    """
    监控Impala查询状态[1,4](@ref)
    :return:
    """
    global alerted_queries

    try:
        queries_data = get_running_impala_queries()
        if not queries_data or 'queries' not in queries_data:
            print("[Info] 未获取到查询数据")
            return

        # 清理过期的告警记录
        cleanup_alerted_queries()

        current_alert_ids = set()  # 本次检查需要告警的queryId

        for query in queries_data['queries']:
            attributes = query.get("attributes", {})
            query_state = query.get("queryState", "N/A")
            query_status = attributes.get("query_status", "N/A")
            query_id = query.get("queryId", "")

            # 跳过正常状态或已完成查询
            if query_status == "OK" or query_state in ["FINISHED", "RUNNING"]:
                continue

            # 检查是否已在告警窗口中
            if query_id in alerted_queries:
                continue

            # 检查是否为需要忽略的错误类型
            if is_ignored_error(query_status):
                alerted_queries[query_id] = datetime.now(pytz.timezone('Asia/Shanghai'))
                current_alert_ids.add(query_id)
                continue

            # 标记为需要告警
            alerted_queries[query_id] = datetime.now(pytz.timezone('Asia/Shanghai'))
            current_alert_ids.add(query_id)

            # 准备时间数据
            start_time = convert_to_china_time(query.get("startTime"))
            end_time = convert_to_china_time(query.get("endTime"))
            duration = calculate_duration(start_time, end_time)

            # 构造告警信息
            alert_fields = {
                "**报错状态**": f"`{query_status[:200]}`",
                "**查询ID**": query_id,
                "**查询用户**": query.get("user", "unknown"),
                "**会话ID**": attributes.get("session_id", "N/A"),
                "**开始时间**": format_time(start_time),
                "**结束时间**": format_time(end_time),
                "**查询耗时**": duration,
                "**查询主机**": attributes.get("memory_per_node_peak_node", "N/A"),
                "**使用内存**": f"{bytes_to_gb(attributes.get('estimated_per_node_peak_memory', 0)):.2f} GB"
            }

            # 构造Markdown格式的告警消息
            alert_message = "### ⚠️ Impala 查询异常告警\n" + \
                            "\n".join([f"- {key}: {value}" for key, value in alert_fields.items()])

            # 添加查询语句（截断处理）
            statement = query.get("statement", "N/A")
            truncated_statement = statement[:500] + ('...' if len(statement) > 500 else '')
            alert_message += f"\n\n**查询语句**:\n```sql\n{truncated_statement}\n```"

            # 发送告警
            send_alert_via_webhook(alert_message)

        print(f"[Debug] 当前告警查询数量: {len(alerted_queries)}")

    except Exception as e:
        print(f"[Critical] 监控过程中发生异常: {str(e)}")
        # 发送系统级告警
        error_alert = f"### ❗ Impala监控系统异常\n" \
                      f"- **错误信息**: `{str(e)}`\n" \
                      f"- **发生时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        send_alert_via_webhook(error_alert)

def main():
    print(f"🚀 启动Impala查询监控（每 {CHECK_INTERVAL} 秒检查一次）")
    print(f"🛡️ 已配置忽略的错误类型: {len(IGNORED_ERRORS)}种")
    print(f"⏳ 告警窗口时间: {ALERT_WINDOW}")

    while True:
        try:
            monitor_impala_queries()
        except KeyboardInterrupt:
            print("\n🛑 监控程序已手动停止")
            break
        except Exception as e:
            print(f"[Critical] 主循环发生未处理异常: {str(e)}")
            # 防止异常导致CPU占用过高
            time.sleep(10)
        finally:
            time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()