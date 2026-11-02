#!/usr/bin/env python3
"""采集 GitHub 公开主页事实，为个人主页 README 提供可核验数据。

只读 GitHub 公开 REST 接口，不写入任何远端数据，不打印令牌。
未认证时限流为 60 次/小时（core）与 10 次/分钟（search），脚本会在触发限流时
明确报错并提示设置 GITHUB_TOKEN，而不是静默返回空数据。

用法:
    python3 fetch_profile_facts.py --user <github-handle> --out facts.json
    python3 fetch_profile_facts.py --user <github-handle> --deep-languages --top 15

输出 JSON 结构:
    user              账号公开信息
    repos             全部公开仓库（排除 fork）
    top_repos         按 star 排序的前 N 个仓库
    languages         按仓库主语言聚合的仓库数量
    language_bytes    --deep-languages 时按字节聚合的语言分布
    merged_prs        已合并 PR：总数、按仓库分组、每组样例
    meta              抓取时间、是否触发限流、采样说明
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

API_ROOT = "https://api.github.com"
USER_AGENT = "asu-github-profile-skill"


class GitHubError(RuntimeError):
    """GitHub 接口返回的不可恢复错误。"""


def _token() -> str:
    return os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN") or ""


def api_get(path: str, token: str, params: dict | None = None, timeout: int = 30) -> tuple[object, dict]:
    """调用一次 GitHub REST 接口，返回 (解析后的 JSON, 响应头)。"""
    url = API_ROOT + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/vnd.github+json"})
    if token:
        request.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8")
            headers = {k.lower(): v for k, v in response.headers.items()}
            return (json.loads(body) if body else None), headers
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")
        message = f"GitHub 接口返回 {exc.code}"
        try:
            payload = json.loads(detail)
            message += f"：{payload.get('message', detail[:200])}"
        except json.JSONDecodeError:
            message += f"：{detail[:200]}"
        if exc.code in (403, 429):
            reset = exc.headers.get("x-ratelimit-reset") if exc.headers else None
            if reset and reset.isdigit():
                wait = max(0, int(reset) - int(time.time()))
                message += f"（限流重置约 {wait} 秒后）"
            message += "；设置 GITHUB_TOKEN 可把额度提升到 5000 次/小时"
        raise GitHubError(message) from exc
    except urllib.error.URLError as exc:
        raise GitHubError(f"网络请求失败：{exc.reason}") from exc


def fetch_user(user: str, token: str) -> dict:
    data, _ = api_get(f"/users/{urllib.parse.quote(user)}", token)
    if not isinstance(data, dict):
        raise GitHubError(f"用户 {user} 不存在或不是公开账号")
    fields = (
        "login",
        "name",
        "company",
        "blog",
        "location",
        "bio",
        "twitter_username",
        "followers",
        "following",
        "public_repos",
        "public_gists",
        "avatar_url",
        "html_url",
        "created_at",
    )
    return {key: data.get(key) for key in fields}


def fetch_repos(user: str, token: str, max_pages: int = 10) -> list[dict]:
    repos: list[dict] = []
    for page in range(1, max_pages + 1):
        data, _ = api_get(
            f"/users/{urllib.parse.quote(user)}/repos",
            token,
            {"per_page": 100, "page": page, "sort": "updated", "type": "owner"},
        )
        if not isinstance(data, list) or not data:
            break
        for repo in data:
            if repo.get("fork"):
                continue
            repos.append(
                {
                    "name": repo.get("name"),
                    "full_name": repo.get("full_name"),
                    "html_url": repo.get("html_url"),
                    "description": repo.get("description"),
                    "language": repo.get("language"),
                    "stargazers_count": repo.get("stargazers_count", 0),
                    "forks_count": repo.get("forks_count", 0),
                    "topics": repo.get("topics", []),
                    "updated_at": repo.get("updated_at"),
                }
            )
        if len(data) < 100:
            break
    return repos


def fetch_merged_prs(user: str, token: str, max_pages: int = 5, sample_per_repo: int = 3) -> dict:
    """统计已合并的上游 PR：总数按接口 total_count，样本按抓到的条数。"""
    query = f"is:pr author:{user} is:merged"
    collected: list[dict] = []
    total = 0
    for page in range(1, max_pages + 1):
        data, _ = api_get("/search/issues", token, {"q": query, "per_page": 100, "page": page})
        if not isinstance(data, dict):
            break
        total = data.get("total_count", total)
        items = data.get("items") or []
        if not items:
            break
        for item in items:
            repo_url = item.get("repository_url", "")
            collected.append(
                {
                    "repo": repo_url.rsplit("/", 1)[-1] if repo_url else "",
                    "title": item.get("title"),
                    "url": item.get("html_url"),
                    "number": item.get("number"),
                    "created_at": item.get("created_at"),
                }
            )
        if len(items) < 100:
            break
    grouped: dict[str, dict] = {}
    for pr in collected:
        entry = grouped.setdefault(pr["repo"], {"repo": pr["repo"], "count": 0, "samples": []})
        entry["count"] += 1
        if len(entry["samples"]) < sample_per_repo:
            entry["samples"].append({"title": pr["title"], "url": pr["url"], "number": pr["number"]})
    by_repo = sorted(grouped.values(), key=lambda item: (-item["count"], item["repo"]))
    return {
        "total": total,
        "sampled": len(collected),
        "by_repo": by_repo,
        "note": "total 来自 search 接口的 total_count；by_repo 的 count 只统计本次抓到的样本页。",
    }


def fetch_language_bytes(repos: list[dict], token: str, limit: int = 20) -> dict:
    """按字节统计语言分布：只统计 star 最高的若干仓库，控制 API 消耗。"""
    top = sorted(repos, key=lambda repo: repo.get("stargazers_count", 0), reverse=True)[:limit]
    totals: dict[str, int] = {}
    for repo in top:
        if not repo.get("full_name"):
            continue
        try:
            data, _ = api_get(f"/repos/{repo['full_name']}/languages", token)
        except GitHubError:
            continue
        if isinstance(data, dict):
            for language, size in data.items():
                totals[language] = totals.get(language, 0) + int(size)
    return dict(sorted(totals.items(), key=lambda item: -item[1]))


def build_facts(user: str, token: str, top: int, deep_languages: bool, max_pr_pages: int) -> dict:
    profile = fetch_user(user, token)
    repos = fetch_repos(user, token)
    merged = fetch_merged_prs(user, token, max_pages=max_pr_pages)
    languages: dict[str, int] = {}
    for repo in repos:
        if repo.get("language"):
            languages[repo["language"]] = languages.get(repo["language"], 0) + 1
    facts = {
        "user": profile,
        "repos": repos,
        "top_repos": sorted(repos, key=lambda repo: repo.get("stargazers_count", 0), reverse=True)[:top],
        "languages": dict(sorted(languages.items(), key=lambda item: -item[1])),
        "merged_prs": merged,
        "meta": {
            "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "authenticated": bool(token),
            "repo_count": len(repos),
            "pr_sample_pages": max_pr_pages,
            "note": "所有字段来自公开接口；star、PR 数会随时间变化，写入 README 时要标注数据日期。",
        },
    }
    if deep_languages:
        facts["language_bytes"] = fetch_language_bytes(repos, token)
    return facts


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="采集 GitHub 公开主页事实")
    parser.add_argument("--user", required=True, help="GitHub 用户名")
    parser.add_argument("--out", default="-", help="输出 JSON 路径，- 表示标准输出")
    parser.add_argument("--top", type=int, default=10, help="保留前 N 个高星仓库")
    parser.add_argument("--deep-languages", action="store_true", help="额外按字节统计语言分布（消耗更多 API 额度）")
    parser.add_argument("--max-pr-pages", type=int, default=5, help="抓取已合并 PR 的最大页数，每页 100 条")
    args = parser.parse_args(argv)

    try:
        facts = build_facts(args.user, _token(), args.top, args.deep_languages, args.max_pr_pages)
    except GitHubError as exc:
        print(f"采集失败：{exc}", file=sys.stderr)
        return 2

    payload = json.dumps(facts, ensure_ascii=False, indent=2)
    if args.out == "-":
        print(payload)
    else:
        with open(args.out, "w", encoding="utf-8") as handle:
            handle.write(payload + "\n")
        print(
            f"已写入 {args.out}：{facts['meta']['repo_count']} 个仓库、"
            f"{facts['merged_prs']['total']} 个已合并 PR（抓取到 {facts['merged_prs']['sampled']} 条样本）。",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
