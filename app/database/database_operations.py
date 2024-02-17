from app.database.database import session_scope
from app.database.models import Word, PartOfSpeech, Origin, WordDetail


def load_existing_data(db_session):
    # Load existing words, POS, origins into memory for quick lookup
    existing_words = {word.name: word.word_id for word in db_session.query(Word).all()}
    existing_pos = {pos.name: pos.part_of_speech_id for pos in db_session.query(PartOfSpeech).all()}
    existing_origins = {origin.name: origin.origin_id for origin in db_session.query(Origin).all()}
    return existing_words, existing_pos, existing_origins


def get_or_create_entity(db, model, name, existing_cache, id_field_name):
    entity_id = existing_cache.get(name)
    if not entity_id:
        entity = model(name=name)
        db.add(entity)
        db.flush()  # Necessary to get the id for the newly created entity
        entity_id = getattr(entity, id_field_name)  # Dynamically get the id using the field name
        existing_cache[name] = entity_id
    return entity_id


def insert_data_to_database(data):
    with session_scope() as db:
        print("Database session created. Preparing data...")
        existing_words, existing_pos, existing_origins = load_existing_data(db)

        for item in data:

            word_id = get_or_create_entity(db, Word, item['word'], existing_words, 'word_id')
            pos_id = get_or_create_entity(db, PartOfSpeech, item['part_of_speech'], existing_pos, 'part_of_speech_id')
            origin_id = get_or_create_entity(db, Origin, item['origin'], existing_origins, 'origin_id')

            # Check if WordDetail already exists
            existing_detail = db.query(WordDetail).filter_by(
                word_id=word_id,
                part_of_speech_id=pos_id,
                origin_id=origin_id,
                meaning=item['meaning']
            ).first()

            if not existing_detail:
                new_word_detail = WordDetail(
                    word_id=word_id,
                    part_of_speech_id=pos_id,
                    origin_id=origin_id,
                    meaning=item['meaning'],
                    usage=item['usage']
                )
                db.add(new_word_detail)
