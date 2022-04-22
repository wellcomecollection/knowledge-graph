from . import (
    Concept,
    Exhibition,
    Work,
    Event,
    get_description,
    get_fulltext,
    get_notes,
    get_slices,
    get_standfirst,
    get_work_data,
)

ordered_source_preferences = ["wikidata", "nlm-mesh", "lc-subjects", "lc-names"]


def format_work_for_elasticsearch(work: Work):
    work_concepts = work.concepts.all()
    concept_ids = [concept.uid for concept in work_concepts]
    concept_names = []
    for concept in work_concepts:
        preferred_name = concept.name
        for source_type in ordered_source_preferences:
            source = concept.sources.get_or_none(source_type=source_type)
            if source:
                preferred_name = source.preferred_name
                break
        concept_names.append(preferred_name)
    concept_variants = [
        variant
        for concept in work_concepts
        for source_concept in concept.sources.all()
        for variant in source_concept.variant_names
    ]

    work_contributors = work.contributors.all()
    contributor_ids = [contributor.uid for contributor in work_contributors]
    contributor_names = []
    for contributor in work_contributors:
        preferred_name = contributor.name
        for source_type in ordered_source_preferences:
            source = contributor.sources.get_or_none(source_type=source_type)
            if source:
                preferred_name = source.preferred_name
                break
        contributor_names.append(preferred_name)
    contributor_variants = [
        variant
        for contributor in work_contributors
        for source_contributor in contributor.sources.all()
        for variant in source_contributor.variant_names
    ]

    work_data = get_work_data(work.wellcome_id)
    description = get_description(work_data)
    notes = get_notes(work_data)

    return {
        "concept_ids": concept_ids,
        "concept_variants": concept_variants,
        "concepts": concept_names,
        "contributor_ids": contributor_ids,
        "contributor_variants": contributor_variants,
        "contributors": contributor_names,
        "published": work.published,
        "title": work.title,
        "description": description,
        "notes": notes,
    }


def format_story_for_elasticsearch(story: Work):
    story_concepts = story.concepts.all()
    concept_ids = [concept.uid for concept in story_concepts]
    concept_names = []
    for concept in story_concepts:
        preferred_name = concept.name
        for source_type in ordered_source_preferences:
            source = concept.sources.get_or_none(source_type=source_type)
            if source:
                preferred_name = source.preferred_name
                break
        concept_names.append(preferred_name)
    concept_variants = [
        variant
        for concept in story_concepts
        for source_concept in concept.sources.all()
        for variant in source_concept.variant_names
    ]

    story_contributors = story.contributors.all()
    contributor_ids = [contributor.uid for contributor in story_contributors]
    contributor_names = []
    for contributor in story_contributors:
        preferred_name = contributor.name
        for source_type in ordered_source_preferences:
            source = contributor.sources.get_or_none(source_type=source_type)
            if source:
                preferred_name = source.preferred_name
                break
        contributor_names.append(preferred_name)
    contributor_variants = [
        variant
        for contributor in story_contributors
        for source_contributor in contributor.sources.all()
        for variant in source_contributor.variant_names
    ]

    slices = get_slices(story.wellcome_id)
    full_text = get_fulltext(slices)
    standfirst = get_standfirst(slices)

    return {
        "concept_ids": concept_ids,
        "concept_variants": concept_variants,
        "concepts": concept_names,
        "contributor_ids": contributor_ids,
        "contributors": contributor_names,
        "contributor_variants": contributor_variants,
        "full_text": full_text,
        "published": story.published,
        "standfirst": standfirst,
        "title": story.title,
    }


def format_concept_for_elasticsearch(concept: Concept):
    concept_works = concept.works.filter(type="work")
    works = [work.title for work in concept_works]
    work_ids = [work.wellcome_id for work in concept_works]

    concept_stories = concept.works.filter(type="story")
    stories = [story.title for story in concept_stories]
    story_ids = [story.wellcome_id for story in concept_stories]

    concept_work_contributions = concept.contributed_to_work.filter(type="work")
    work_contributions = [work.title for work in concept_work_contributions]
    work_contribution_ids = [
        work.wellcome_id for work in concept_work_contributions
    ]

    concept_story_contributions = concept.contributed_to_work.filter(
        type="story"
    )
    story_contributions = [story.title for story in concept_story_contributions]
    story_contribution_ids = [
        story.wellcome_id for story in concept_story_contributions
    ]

    variants = [
        variant
        for source_concept in concept.sources.all()
        for variant in source_concept.variant_names
    ]

    concept_neighbours = concept.neighbours.all()
    neighbour_names = []
    for concept in concept_neighbours:
        preferred_name = concept.name
        for source_type in ordered_source_preferences:
            source = concept.sources.get_or_none(source_type=source_type)
            if source:
                preferred_name = source.preferred_name
                break
        neighbour_names.append(preferred_name)
    neighbour_ids = [neighbour.uid for neighbour in concept_neighbours]

    document = {
        "name": concept.name,
        "preferred_name": concept.name,
        "type": concept.type,
        "works": works,
        "work_ids": work_ids,
        "neighbour_names": neighbour_names,
        "neighbour_ids": neighbour_ids,
        "stories": stories,
        "story_ids": story_ids,
        "work_contributions": work_contributions,
        "work_contribution_ids": work_contribution_ids,
        "story_contributions": story_contributions,
        "story_contribution_ids": story_contribution_ids,
        "variants": variants,
    }

    wikidata_source = concept.sources.get_or_none(source_type="wikidata")
    lc_subjects_source = concept.sources.get_or_none(source_type="lc-subjects")
    lc_names_source = concept.sources.get_or_none(source_type="lc-names")
    mesh_source = concept.sources.get_or_none(source_type="nlm-mesh")

    if mesh_source:
        document.update(
            {
                "mesh_description": mesh_source.description,
                "mesh_id": mesh_source.source_id,
                "mesh_preferred_name": mesh_source.preferred_name,
                "preferred_name": mesh_source.preferred_name,
            }
        )
    if lc_names_source:
        document.update(
            {
                "lc_names_id": lc_names_source.source_id,
                "lc_names_preferred_name": lc_names_source.preferred_name,
                "preferred_name": lc_names_source.preferred_name,
            }
        )
    if lc_subjects_source:
        document.update(
            {
                "lc_subjects_id": lc_subjects_source.source_id,
                "lc_subjects_preferred_name": lc_subjects_source.preferred_name,
                "preferred_name": lc_subjects_source.preferred_name,
            }
        )
    if wikidata_source:
        document.update(
            {
                "wikidata_description": wikidata_source.description,
                "wikidata_id": wikidata_source.source_id,
                "wikidata_preferred_name": wikidata_source.preferred_name,
                "preferred_name": wikidata_source.preferred_name,
            }
        )

    return document


def format_exhibition_for_elasticsearch(exhibition: Exhibition):
    document = {
        "format": exhibition.format,
        "title": exhibition.title,
        "description": exhibition.description,
        "start_date": exhibition.start_date,
        "end_date": exhibition.end_date,
        "location": exhibition.location,
        "image_url": exhibition.image_url,
        "image_alt": exhibition.image_alt,
    }
    return document


def format_event_for_elasticsearch(event: Event):
    document = {
        "format": event.format,
        "title": event.title,
        "description": event.description,
        "start_date": event.start_date,
        "end_date": event.end_date,
        "location": event.location,
        "image_url": event.image_url,
        "image_alt": event.image_alt,
    }
    return document
