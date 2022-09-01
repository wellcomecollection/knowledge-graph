from datetime import datetime

import pandas as pd
import typer

from src.elasticsearch import yield_popular_works
from src.graph import (
    get_neo4j_session,
    ingest_event,
    ingest_exhibition,
    ingest_story,
    ingest_work,
)
from src.prismic import yield_events, yield_exhibitions
from src.utils import get_logger

log = get_logger(__name__)
app = typer.Typer()

N_STORIES = 100
N_WORKS = 1000
N_WHATS_ON = 100


def main(
    stories: bool = typer.Option(False, "--stories", help="Ingest stories"),
    works: bool = typer.Option(False, "--works", help="Ingest works"),
    whats_on: bool = typer.Option(
        False, "--whats-on", help="Ingest exhibitions and events"
    ),
    everything: bool = typer.Option(
        False, "--all", help="Ingest all nodes and relationship types"
    ),
    clear: bool = typer.Option(
        True,
        "--clear",
        help="If true, the neo4j graph will be cleared before starting the ingest",
    ),
):
    get_neo4j_session(clear=clear)

    if everything:
        stories = True
        works = True
        whats_on = True

    if stories:
        log.info("Loading stories dataset")
        df = pd.read_excel(
            pd.ExcelFile("/data/stories/stories.xlsx", engine="openpyxl"),
            sheet_name="Articles",
            dtype={"Date published": datetime},
        ).fillna("")

        log.info("Processing stories")
        for _, story in df[:N_STORIES].iterrows():
            ingest_story(story)

    if works:
        log.info("Processing works")
        for work in yield_popular_works(size=N_WORKS):
            ingest_work(work)

    if whats_on:
        log.info("Processing exhibitions")
        for exhibition in yield_exhibitions(size=N_WHATS_ON):
            ingest_exhibition(exhibition)

        log.info("Processing events")
        for event in yield_events(size=N_WHATS_ON):
            ingest_event(event)

    if not stories and not works and not whats_on:
        log.info("No data to process")

    typer.Exit()


if __name__ == "__main__":
    typer.run(main)
