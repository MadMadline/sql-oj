"""
判题服务对接模块

当前为 mock 版本 — 等队友 Docker 判题服务就绪后替换为实际 HTTP 调用。

约定 API 契约（需和队友确认）:
    POST {JUDGE_SERVICE_URL}/api/judge/
    Request:  {
        "sql": "...",
        "create_table_sql": "...",
        "test_cases": [{"test_input": "...", "expected_output": "..."}, ...]
    }
    Response: {
        "passed": true/false,
        "execution_status": "ACCEPTED|WRONG_ANSWER|TIMEOUT|ERROR",
        "score": 100,
        "details": [{"test_case_id": 1, "passed": true, "actual_output": "..."}, ...]
    }
"""


def judge_submission(submitted_sql, test_cases, create_table_sql=''):
    """
    调用判题服务，返回判题结果。

    当前 mock: 直接返回 ACCEPTED 满分。
    """
    # TODO: 替换为真实判题服务调用
    # import requests
    # from django.conf import settings
    # response = requests.post(
    #     f'{settings.JUDGE_SERVICE_URL}/api/judge/',
    #     json={
    #         'sql': submitted_sql,
    #         'create_table_sql': create_table_sql,
    #         'test_cases': test_cases,
    #     },
    #     timeout=30
    # )
    # return response.json()

    return {
        'passed': True,
        'execution_status': 'ACCEPTED',
        'score': 100,
        'details': [
            {
                'test_case_id': i + 1,
                'passed': True,
                'actual_output': tc.get('expected_output', ''),
            }
            for i, tc in enumerate(test_cases)
        ],
    }
