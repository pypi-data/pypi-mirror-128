from sqlalchemy import Column, DateTime, Text, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

__all__ = ["ChronicleModel"]


class ChronicleModel(Base):
    __tablename__ = "chronicle"

    # core information
    sym = Column(String(20), nullable=True)  # most related company
    title = Column(String(200), nullable=False)
    dt = Column(DateTime, nullable=False)  # when published
    by = Column(String(100), nullable=True)  # news agency, rr institution
    kind = Column(String(20), nullable=False)  # e.g. `ndbg`, `frontpage`, `news`, `rr`
    url = Column(Text, primary_key=True, nullable=False)  # wx url len about 500
    # meta
    path = Column(String(300), nullable=False)  # from core information, for worker
    domain = Column(String(20), nullable=False)  # from url, for simple statistics
    upd = Column(DateTime, nullable=False)  # when scraped, for simple statistics
    status = Column(String(20), nullable=True)  # cached, working, or null
