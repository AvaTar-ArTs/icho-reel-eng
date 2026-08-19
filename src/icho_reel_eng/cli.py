from __future__ import annotations

import json
from pathlib import Path

import typer

from .core import build_render_manifest, ffmpeg_available, load_json, plan_content, validate_content, write_json

app = typer.Typer(help="ichoTaKu short-form media engine")


@app.command()
def validate(content: Path) -> None:
    """Validate a content package against the repository schema."""
    data = load_json(content)
    errors = validate_content(data)
    if errors:
        for error in errors:
            typer.echo(f"ERROR {error}")
        raise typer.Exit(code=1)
    typer.echo(f"OK {content}")


@app.command()
def plan(content: Path, out: Path = Path("runs/plan.json")) -> None:
    """Create a deterministic scene plan and render manifest."""
    data = load_json(content)
    production_plan = plan_content(data)
    payload = {
        "plan": production_plan.to_dict(),
        "render_manifest": build_render_manifest(production_plan),
    }
    write_json(payload, out)
    typer.echo(str(out))


@app.command("doctor")
def doctor() -> None:
    """Check local runtime capabilities."""
    status = {
        "ffmpeg": ffmpeg_available(),
        "cwd": str(Path.cwd()),
    }
    typer.echo(json.dumps(status, indent=2))


if __name__ == "__main__":
    app()
