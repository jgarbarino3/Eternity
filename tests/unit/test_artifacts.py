from pathlib import Path

from eternity.artifacts import sha256_file


def test_sha256_file_is_stable(tmp_path: Path) -> None:
    path = tmp_path / "artifact.txt"
    path.write_text("eternity\n", encoding="utf-8")

    assert sha256_file(path) == "a62b6b005047be416432acf08445606cd803ee0bce5f290b63a011dd9d91c150"
