from pathlib import Path

from orchestrator.app import run


if __name__ == "__main__":
    run(Path(__file__).resolve().parent)
