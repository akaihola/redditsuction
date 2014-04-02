from contextlib import contextmanager
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Comment


def initialize_database(database):
    engine = create_engine(database)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)


@contextmanager
def session_scope(make_session):
    """Provide a transactional scope around a series of operations."""
    session = make_session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def retrieve_comments(make_session, subreddit, after, before):
    with session_scope(make_session) as session:
        comment_jsons = fetch_comments(subreddit, after, before)
        for comment_json in comment_jsons:
            comment = Comment(id=comment_json['id'],
                              subreddit=subreddit,
                              author=comment_json['author'],
                              body=comment_json['body'])
            session.merge(comment)


def main():
    database = sys.argv[1]
    make_session = initialize_database(database)
    retrieve_comments('Bitcoin', 'a', 'b', make_session)


if __name__ == '__main__':
    main()
