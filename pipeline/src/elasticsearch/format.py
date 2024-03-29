from . import (
    Person,
    Subject,
    Event,
    Exhibition,
    Work,
    get_story_data,
    get_story_fulltext,
    get_story_image,
    get_story_standfirst,
    get_work_data,
    get_work_dates,
    get_work_description,
    get_work_image,
    get_work_notes,
)

ordered_source_preferences = ["wikidata", "nlm-mesh", "lc-subjects", "lc-names"]


def format_work_for_elasticsearch(work: Work):
    work_concepts = work.concepts.all()
    concept_ids = [concept.uid for concept in work_concepts]
    concept_parent_labels = [
        concept.wellcome_parent_label
        if type(concept).__name__ == "Subject"
        else None
        for concept in work_concepts
    ]
    concept_types = [type(concept).__name__ for concept in work_concepts]

    concept_labels = []
    concept_preferred_label_sources = []
    for concept in work_concepts:
        preferred_label = concept.label
        preferred_label_source = "catalogue api"
        for source_type in ordered_source_preferences:
            source = concept.sources.get_or_none(source_type=source_type)
            if source:
                preferred_label = source.preferred_label
                preferred_label_source = source_type
                break
        concept_labels.append(preferred_label)
        concept_preferred_label_sources.append(preferred_label_source)
    concept_variants = [
        variant
        for concept in work_concepts
        for source_concept in concept.sources.all()
        for variant in source_concept.variant_labels
    ]

    work_contributors = work.contributors.all()
    contributor_ids = [contributor.uid for contributor in work_contributors]
    contributor_labels = []
    for contributor in work_contributors:
        preferred_label = contributor.label
        for source_type in ordered_source_preferences:
            source = contributor.sources.get_or_none(source_type=source_type)
            if source:
                preferred_label = source.preferred_label
                break
        contributor_labels.append(preferred_label)
    contributor_variants = [
        variant
        for contributor in work_contributors
        for source_contributor in contributor.sources.all()
        for variant in source_contributor.variant_labels
    ]

    work_data = get_work_data(work.wellcome_id)
    description = get_work_description(work_data)
    notes = get_work_notes(work_data)
    image_url = get_work_image(work_data)
    published = get_work_dates(work_data)

    return {
        "subject_ids": concept_ids,
        "subject_parent_labels": concept_parent_labels,
        "subject_variants": concept_variants,
        "subjects": concept_labels,
        "subject_types": concept_types,
        "contributor_ids": contributor_ids,
        "contributor_variants": contributor_variants,
        "contributors": contributor_labels,
        "published": published,
        "subject_preferred_label_sources": concept_preferred_label_sources,
        "title": work.title,
        "description": description,
        "notes": notes,
        "image_url": image_url,
    }


def format_story_for_elasticsearch(story: Work):
    story_concepts = story.concepts.all()
    concept_ids = [concept.uid for concept in story_concepts]
    concept_labels = []
    for concept in story_concepts:
        preferred_label = concept.label
        for source_type in ordered_source_preferences:
            source = concept.sources.get_or_none(source_type=source_type)
            if source:
                preferred_label = source.preferred_label
                break
        concept_labels.append(preferred_label)
    concept_variants = [
        variant
        for concept in story_concepts
        for source_concept in concept.sources.all()
        for variant in source_concept.variant_labels
    ]

    story_contributors = story.contributors.all()
    contributor_ids = [contributor.uid for contributor in story_contributors]
    contributor_labels = []
    for contributor in story_contributors:
        preferred_label = contributor.label
        for source_type in ordered_source_preferences:
            source = contributor.sources.get_or_none(source_type=source_type)
            if source:
                preferred_label = source.preferred_label
                break
        contributor_labels.append(preferred_label)
    contributor_variants = [
        variant
        for contributor in story_contributors
        for source_contributor in contributor.sources.all()
        for variant in source_contributor.variant_labels
    ]

    story_data = get_story_data(story.wellcome_id)
    full_text = get_story_fulltext(story_data)
    standfirst = get_story_standfirst(story_data)
    image_url = get_story_image(story_data)

    return {
        "subject_ids": concept_ids,
        "subject_variants": concept_variants,
        "subjects": concept_labels,
        "contributor_ids": contributor_ids,
        "contributors": contributor_labels,
        "contributor_variants": contributor_variants,
        "full_text": full_text,
        "published": story.published,
        "standfirst": standfirst,
        "title": story.title,
        "image_url": image_url,
    }


def format_subject_for_elasticsearch(subject: Subject):
    concept_works = subject.works.filter(type="work")
    works = [work.title for work in concept_works]
    work_ids = [work.wellcome_id for work in concept_works]

    concept_stories = subject.works.filter(type="story")
    stories = [story.title for story in concept_stories]
    story_ids = [story.wellcome_id for story in concept_stories]

    variants = [
        variant
        for source_concept in subject.sources.all()
        for variant in source_concept.variant_labels
    ]

    concept_neighbours = subject.neighbours.match(source="wikidata")
    neighbours_with_works = [
        neighbour
        for neighbour in concept_neighbours
        if len(neighbour.works) > 0
    ]
    neighbour_labels = []
    for neighbour_concept in neighbours_with_works:
        preferred_label = neighbour_concept.label
        for source_type in ordered_source_preferences:
            source = neighbour_concept.sources.get_or_none(
                source_type=source_type
            )
            if source:
                preferred_label = source.preferred_label
                break
        neighbour_labels.append(preferred_label)
    neighbour_ids = [neighbour.uid for neighbour in neighbours_with_works]

    document = {
        "label": subject.label,
        "preferred_label": subject.label,
        "type": "subject",
        "works": works,
        "work_ids": work_ids,
        "neighbour_labels": neighbour_labels,
        "neighbour_ids": neighbour_ids,
        "stories": stories,
        "story_ids": story_ids,
        "variants": variants,
    }

    wikidata_source = subject.sources.get_or_none(source_type="wikidata")
    lc_subjects_source = subject.sources.get_or_none(source_type="lc-subjects")
    lc_names_source = subject.sources.get_or_none(source_type="lc-names")
    mesh_source = subject.sources.get_or_none(source_type="nlm-mesh")

    if mesh_source:
        document.update(
            {
                "mesh_description": mesh_source.description,
                "mesh_id": mesh_source.source_id,
                "mesh_preferred_label": mesh_source.preferred_label,
                "preferred_label": mesh_source.preferred_label,
                "preferred_label_source": "mesh",
            }
        )
    if lc_names_source:
        document.update(
            {
                "lc_names_id": lc_names_source.source_id,
                "lc_names_preferred_label": lc_names_source.preferred_label,
                "preferred_label": lc_names_source.preferred_label,
                "preferred_label_source": "lc-names",
            }
        )
    if lc_subjects_source:
        document.update(
            {
                "lc_subjects_id": lc_subjects_source.source_id,
                "lc_subjects_preferred_label": lc_subjects_source.preferred_label,
                "preferred_label": lc_subjects_source.preferred_label,
                "preferred_label_source": "lc-subjects",
            }
        )
    if wikidata_source:
        document.update(
            {
                "wikidata_description": wikidata_source.description,
                "wikidata_id": wikidata_source.source_id,
                "wikidata_preferred_label": wikidata_source.preferred_label,
                "preferred_label": wikidata_source.preferred_label,
                "preferred_label_source": "wikidata",
            }
        )
    return document


def format_person_for_elasticsearch(person: Person):
    concept_works = person.works.filter(type="work")
    works = [work.title for work in concept_works]
    work_ids = [work.wellcome_id for work in concept_works]

    concept_stories = person.works.filter(type="story")
    stories = [story.title for story in concept_stories]
    story_ids = [story.wellcome_id for story in concept_stories]

    concept_work_contributions = person.contributions.filter(type="work")
    work_contributions = [work.title for work in concept_work_contributions]
    work_contribution_ids = [
        work.wellcome_id for work in concept_work_contributions
    ]

    concept_story_contributions = person.contributions.filter(type="story")
    story_contributions = [story.title for story in concept_story_contributions]
    story_contribution_ids = [
        story.wellcome_id for story in concept_story_contributions
    ]

    variants = [
        variant
        for source_concept in person.sources.all()
        for variant in source_concept.variant_labels
    ]

    document = {
        "label": person.label,
        "preferred_label": person.label,
        "type": "person",
        "works": works,
        "work_ids": work_ids,
        "stories": stories,
        "story_ids": story_ids,
        "work_contributions": work_contributions,
        "work_contribution_ids": work_contribution_ids,
        "story_contributions": story_contributions,
        "story_contribution_ids": story_contribution_ids,
        "variants": variants,
    }

    wikidata_source = person.sources.get_or_none(source_type="wikidata")
    lc_subjects_source = person.sources.get_or_none(source_type="lc-subjects")
    lc_names_source = person.sources.get_or_none(source_type="lc-names")
    mesh_source = person.sources.get_or_none(source_type="nlm-mesh")

    if mesh_source:
        document.update(
            {
                "mesh_description": mesh_source.description,
                "mesh_id": mesh_source.source_id,
                "mesh_preferred_label": mesh_source.preferred_label,
                "preferred_label": mesh_source.preferred_label,
            }
        )
    if lc_names_source:
        document.update(
            {
                "lc_names_id": lc_names_source.source_id,
                "lc_names_preferred_label": lc_names_source.preferred_label,
                "preferred_label": lc_names_source.preferred_label,
            }
        )
    if lc_subjects_source:
        document.update(
            {
                "lc_subjects_id": lc_subjects_source.source_id,
                "lc_subjects_preferred_label": lc_subjects_source.preferred_label,
                "preferred_label": lc_subjects_source.preferred_label,
            }
        )
    if wikidata_source:
        document.update(
            {
                "wikidata_description": wikidata_source.description,
                "wikidata_id": wikidata_source.source_id,
                "wikidata_preferred_label": wikidata_source.preferred_label,
                "preferred_label": wikidata_source.preferred_label,
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
