
from sqlalchemy import Column, String, Integer, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base


class Word(Base):
    __tablename__ = "words"

    word_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    # Relationship to WordDetail
    details = relationship("WordDetail", back_populates="word")


class Origin(Base):
    __tablename__ = "origins"

    origin_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    # Relationship to WordDetail
    details = relationship("WordDetail", back_populates="origin")


class PartOfSpeech(Base):
    __tablename__ = "parts_of_speech"

    part_of_speech_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    # Relationship to WordDetail
    details = relationship("WordDetail", back_populates="part_of_speech")


class WordDetail(Base):
    __tablename__ = "words_details"
    __table_args__ = (
        UniqueConstraint('word_id', 'part_of_speech_id', 'origin_id', 'meaning', name='_word_detail_uniqueness'),)

    word_detail_id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, ForeignKey("words.word_id"))
    part_of_speech_id = Column(Integer, ForeignKey("parts_of_speech.part_of_speech_id"))
    origin_id = Column(Integer, ForeignKey("origins.origin_id"))
    meaning = Column(String)
    usage = Column(String)

    # Relationships
    word = relationship("Word", back_populates="details")
    origin = relationship("Origin", back_populates="details")
    part_of_speech = relationship("PartOfSpeech", back_populates="details")
