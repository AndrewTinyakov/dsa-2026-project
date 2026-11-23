from pathlib import Path
from tempfile import TemporaryDirectory

from .monthly_table import monthly_indicators
from .source_tables import load_sources


def main() -> None:
    data_dir = Path.cwd() / "data"
    try:
        sources = load_sources(data_dir / "raw")
    except FileNotFoundError as error:
        raise SystemExit("Run food-inflation-download to get the source CSVs.") from error

    monthly = monthly_indicators(*sources)
    output_path = data_dir / "interim" / "monthly_indicators.parquet"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(dir=output_path.parent) as directory:
        temporary = Path(directory) / output_path.name
        monthly.to_parquet(temporary)
        temporary.replace(output_path)
    print(f"Saved {len(monthly)} months to {output_path.relative_to(Path.cwd())}.")
