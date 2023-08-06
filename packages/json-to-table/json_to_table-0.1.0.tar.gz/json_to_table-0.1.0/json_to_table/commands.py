from pathlib import Path

import pandas as pd
import typer
from typer import Option, Typer

app = Typer(name="Json2Table", help="Convert JSON file to CSV or XLSX")


converter = {
    "csv": lambda df, stem: df.to_csv(f"{stem}.csv", index=False),
    "xlsx": lambda df, stem: df.to_excel(f"{stem}.xlsx", index=False),
}


@app.command()
def head(file: str, n: int = Option(default=10)):
    dataframe = pd.read_json(file)
    typer.echo(dataframe.head(n))


@app.command()
def convert(file: str, t: str = Option(default="csv")):
    if t not in ["csv", "xlsx"]:
        typer.echo('Option t should be one of ["csv", "xlsx"]', err=True)
    path = Path(file)
    stem = path.stem
    dataframe = pd.read_json(file)
    converter[t](dataframe, stem)
