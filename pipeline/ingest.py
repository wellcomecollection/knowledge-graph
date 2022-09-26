
from pathlib import Path
from tqdm import tqdm
from datetime import datetime

import pandas as pd
import typer

from src.elasticsearch import yield_popular_works, yield_works
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

N_STORIES = 50
N_WORKS = 100
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
        stories_loop = tqdm(df[:N_STORIES].iterrows(), total=N_STORIES, unit="story")
        for _, story in stories_loop:
            stories_loop.set_description(f"Processing {Path(story['URL']).name}")
            ingest_story(story)

    if works:
        works_loop = tqdm(yield_works(size=N_WORKS), total=N_WORKS, unit="work")
        log.info("Processing works")
        for work in works_loop:
            works_loop.set_description(f"Processing {work['_id']}")
            ingest_work(work)

    if whats_on:
        log.info("Processing exhibitions")
        exhibitions_loop = tqdm(yield_exhibitions(size=N_WHATS_ON), total=N_WHATS_ON, unit="exhibition")
        for exhibition in exhibitions_loop:
            ingest_exhibition(exhibition)

        log.info("Processing events")
        events_loop = tqdm(yield_events(size=N_WHATS_ON), total=N_WHATS_ON, unit="event")
        for event in events_loop:
            ingest_event(event)

    if not stories and not works and not whats_on:
        log.info("No data to process")

    typer.Exit()


if __name__ == "__main__":
    typer.run(main)
