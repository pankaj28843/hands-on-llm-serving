#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from mac_llm_ops_lab.release_readiness import (  # noqa: E402
    current_git_sha,
    load_public_release_candidate_files,
    scan_public_release_files,
    write_public_release_report,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate that public repo files exclude local/private artifacts.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("artifacts/runtime/release-readiness/public-release-check.json"),
        help="JSON report path under artifacts/runtime/.",
    )
    args = parser.parse_args()

    files = load_public_release_candidate_files(REPO_ROOT)
    report = scan_public_release_files(files, git_sha=current_git_sha(REPO_ROOT))
    output_path = write_public_release_report(
        report,
        output_root=REPO_ROOT,
        output_path=args.output,
    )
    print(
        json.dumps(
            {
                "passed": report["passed"],
                "findings_count": report["findings_count"],
                "output": str(output_path),
            },
            sort_keys=True,
        )
    )
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
