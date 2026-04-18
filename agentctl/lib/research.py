from __future__ import annotations

import html
import json
import re
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

from .common import command_path, run_command, save_json, save_text, short_hash, slugify, strip_html, utc_now


WEB_SEARCH_URL = "https://html.duckduckgo.com/html/"


def choose_github_mode(query: str) -> str:
    lowered = query.lower()
    if any(token in lowered for token in ("is:issue", "is:pr", "label:", "assignee:", "author:", "mentions:", "state:")):
        return "issues"
    if any(token in lowered for token in ("path:", "filename:", "extension:", "repo:", "language:")):
        return "code"
    return "repos"


def _default_output_paths(mode: str, query: str, output_dir: str | None, json_out: str | None, brief_out: str | None) -> tuple[Path, Path]:
    base_dir = Path(output_dir).resolve() if output_dir else (Path.cwd() / ".codex-workflows" / "research" / f"{mode}-{slugify(query)[:48]}-{short_hash(query)}").resolve()
    evidence_path = Path(json_out).resolve() if json_out else base_dir / "evidence.json"
    brief_path = Path(brief_out).resolve() if brief_out else base_dir / "brief.md"
    return evidence_path, brief_path


def _render_brief(envelope: dict[str, Any]) -> str:
    lines = [
        f"# {envelope['track'].title()} Research Brief",
        "",
        f"- Query: `{envelope['query']}`",
        f"- Generated: `{envelope['generated_at']}`",
        f"- Provider: `{envelope['provider']['name']}`",
        "",
        "## Shortlist",
        "",
    ]
    for item in envelope.get("shortlist", []):
        lines.append(f"- [{item['title']}]({item['url']})")
        if item.get("reason"):
            lines.append(f"  - {item['reason']}")
    if envelope.get("caveats"):
        lines.extend(["", "## Caveats", ""])
        for caveat in envelope["caveats"]:
            lines.append(f"- {caveat}")
    if envelope.get("final_recommendation"):
        lines.extend(["", "## Recommendation", "", envelope["final_recommendation"]])
    return "\n".join(lines).rstrip() + "\n"


def _decode_ddg_href(href: str) -> str:
    parsed = urllib.parse.urlparse(href)
    query = urllib.parse.parse_qs(parsed.query)
    if "uddg" in query:
        return urllib.parse.unquote(query["uddg"][0])
    return href


def _search_web(query: str, limit: int) -> dict[str, Any]:
    try:
        request = urllib.request.Request(
            WEB_SEARCH_URL + "?" + urllib.parse.urlencode({"q": query}),
            headers={"User-Agent": "agentctl/1.0"},
        )
        with urllib.request.urlopen(request, timeout=20) as response:  # nosec - read-only public search fetch
            body = response.read().decode("utf-8", errors="ignore")
    except Exception as exc:
        return {
            "schema_version": 1,
            "track": "web",
            "query": query,
            "generated_at": utc_now(),
            "provider": {"name": "duckduckgo-html", "kind": "public-web-search"},
            "sources": [],
            "shortlist": [],
            "caveats": [f"Web search backend failed: {exc}"],
            "final_recommendation": "Use the browser adapter or Codex web tools for deeper verification.",
        }

    results: list[dict[str, Any]] = []
    for match in re.finditer(r'<a[^>]*class="result__a"[^>]*href="(?P<href>[^"]+)"[^>]*>(?P<title>.*?)</a>', body, re.IGNORECASE | re.DOTALL):
        href = _decode_ddg_href(html.unescape(match.group("href")))
        title = strip_html(match.group("title"))
        snippet_match = re.search(r'result__snippet[^>]*>(?P<snippet>.*?)</', body[match.end() : match.end() + 700], re.IGNORECASE | re.DOTALL)
        snippet = strip_html(snippet_match.group("snippet")) if snippet_match else ""
        results.append(
            {
                "title": title,
                "url": href,
                "domain": urllib.parse.urlparse(href).netloc,
                "snippet": snippet,
                "reason": f"Top public web result from {urllib.parse.urlparse(href).netloc}" if href else "Top public web result",
            }
        )
        if len(results) >= limit:
            break

    caveats = []
    if not results:
        caveats.append("No public web search results were parsed from the configured search backend.")
    return {
        "schema_version": 1,
        "track": "web",
        "query": query,
        "generated_at": utc_now(),
        "provider": {"name": "duckduckgo-html", "kind": "public-web-search"},
        "sources": results,
        "shortlist": results[: min(limit, 5)],
        "caveats": caveats,
        "final_recommendation": f"Start from the top {min(len(results), 3)} current web sources, then cross-check implementation details against GitHub evidence." if results else "Use the browser-capable path or Codex web tools for deeper inspection.",
    }


def _search_github(query: str, limit: int) -> dict[str, Any]:
    if not command_path("gh"):
        return {
            "schema_version": 1,
            "track": "github",
            "query": query,
            "generated_at": utc_now(),
            "provider": {"name": "gh", "kind": "github-cli"},
            "sources": [],
            "shortlist": [],
            "caveats": ["GitHub CLI is not installed or not on PATH."],
            "final_recommendation": "Install or authenticate gh before using GitHub-first research.",
        }

    mode = choose_github_mode(query)
    if mode == "issues":
        command = ["gh", "search", "issues", query, "--include-prs", "--limit", str(limit), "--json", "title,url,repository,state,updatedAt"]
    elif mode == "code":
        command = ["gh", "search", "code", query, "--limit", str(limit), "--json", "path,url,repository"]
    else:
        command = ["gh", "search", "repos", query, "--limit", str(limit), "--json", "fullName,url,description,updatedAt,stargazersCount,language"]

    result = run_command(command, timeout=45)
    if not result["ok"]:
        return {
            "schema_version": 1,
            "track": "github",
            "query": query,
            "generated_at": utc_now(),
            "provider": {"name": "gh", "kind": "github-cli", "mode": mode},
            "sources": [],
            "shortlist": [],
            "caveats": [result["stderr"] or result["stdout"] or "GitHub search failed."],
            "final_recommendation": "Refine the GitHub query or verify gh authentication before retrying.",
        }

    try:
        parsed = json.loads(result["stdout"] or "[]")
    except json.JSONDecodeError as exc:
        return {
            "schema_version": 1,
            "track": "github",
            "query": query,
            "generated_at": utc_now(),
            "provider": {"name": "gh", "kind": "github-cli", "mode": mode},
            "sources": [],
            "shortlist": [],
            "caveats": [f"Failed to parse gh JSON output: {exc}"],
            "final_recommendation": "Retry with a narrower query or inspect the raw gh output.",
        }
    sources: list[dict[str, Any]] = []
    for item in parsed:
        if mode == "repos":
            title = item["fullName"]
            reason = f"Repository updated {item.get('updatedAt', 'recently')} with {item.get('stargazersCount', 0)} stars."
            url = item["url"]
        elif mode == "issues":
            repository = item.get("repository", {})
            repo_name = repository.get("nameWithOwner") or repository.get("fullName") or repository.get("name") or "unknown-repo"
            title = f"{repo_name} {item['title']}".strip()
            reason = f"{item.get('state', 'unknown')} issue/PR in {repo_name}."
            url = item["url"]
        else:
            repository = item.get("repository", {})
            repo_name = repository.get("nameWithOwner") or repository.get("fullName") or repository.get("name") or "unknown-repo"
            title = f"{repo_name}:{item['path']}"
            reason = f"Code search match in {repo_name}."
            url = item["url"]
        sources.append({"title": title, "url": url, "reason": reason, "mode": mode})

    return {
        "schema_version": 1,
        "track": "github",
        "query": query,
        "generated_at": utc_now(),
        "provider": {"name": "gh", "kind": "github-cli", "mode": mode},
        "sources": sources,
        "shortlist": sources[: min(limit, 5)],
        "caveats": [] if sources else ["No GitHub results matched the current query."],
        "final_recommendation": f"Promote the top {min(len(sources), 3)} GitHub {mode} results into the implementation brief." if sources else "Broaden the query or search a specific owner or repository.",
    }


def _search_scout(query: str, limit: int) -> dict[str, Any]:
    web = _search_web(query, limit)
    github = _search_github(query, limit)
    shortlist = web.get("shortlist", [])[: min(limit, 3)] + github.get("shortlist", [])[: min(limit, 3)]
    caveats = list(web.get("caveats", [])) + list(github.get("caveats", []))
    return {
        "schema_version": 1,
        "track": "scout",
        "query": query,
        "generated_at": utc_now(),
        "provider": {"name": "agentctl-scout", "kind": "hybrid"},
        "tracks": {"web": web, "github": github},
        "sources": shortlist,
        "shortlist": shortlist,
        "caveats": caveats,
        "final_recommendation": "Use the official/current web sources for constraints and the GitHub shortlist for field practice, then carry both into implementation.",
    }


def _research_status(envelope: dict[str, Any]) -> str:
    shortlist = envelope.get("shortlist", [])
    caveats = envelope.get("caveats", [])
    if shortlist:
        return "degraded" if caveats else "ok"
    return "error" if caveats else "degraded"


def run_research(*, mode: str, query: str, limit: int, output_dir: str | None, json_out: str | None, brief_out: str | None) -> dict[str, Any]:
    if mode == "web":
        envelope = _search_web(query, limit)
    elif mode == "github":
        envelope = _search_github(query, limit)
    elif mode == "scout":
        envelope = _search_scout(query, limit)
    else:  # pragma: no cover
        raise ValueError(f"unsupported research mode: {mode}")

    evidence_path, brief_path = _default_output_paths(mode, query, output_dir, json_out, brief_out)
    brief = _render_brief(envelope)
    save_json(evidence_path, envelope)
    save_text(brief_path, brief)
    status = _research_status(envelope)
    return {
        "status": status,
        "mode": mode,
        "query": query,
        "summary": {
            "status": status,
            "source_count": len(envelope.get("sources", [])),
            "shortlist_count": len(envelope.get("shortlist", [])),
            "caveat_count": len(envelope.get("caveats", [])),
        },
        "evidence": envelope,
        "brief": brief,
        "paths": {"json": str(evidence_path), "brief": str(brief_path)},
    }
