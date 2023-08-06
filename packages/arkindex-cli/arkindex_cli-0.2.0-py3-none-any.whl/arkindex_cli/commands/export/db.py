# -*- coding: utf-8 -*-

import sqlite3
import uuid
from collections import namedtuple
from itertools import starmap
from typing import List, Optional

# creating named tuple for easier handling of list_elements returned values

Image = namedtuple("Image", ["id", "url"])
Element = namedtuple("Element", ["id", "name", "polygon", "worker_version_id"])
Transcription = namedtuple(
    "Transcription", ["id", "element_id", "text", "confidence", "worker_version_id"]
)
Worker = namedtuple("Worker", ["id", "name", "slug", "type", "revision"])


def list_elements(database_path: str, type: str) -> List[Element]:
    """
    Gets a database path, and the specified page type
    """

    # connection to the database
    connection = sqlite3.Connection(database_path)
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id, name, polygon,worker_version_id FROM element WHERE type = ?",
        (type,),
    )
    result = list(starmap(Element, cursor.fetchall()))

    cursor.close()
    connection.close()

    return result


def list_pages(database_path: str, page_type: str) -> list:
    """
    Gets a database path, and the specified page type
    """

    return list_elements(database_path, page_type)


def list_folders(database_path: str, folder_type: str) -> list:
    """
    Gets a database path, the optional folder_type as strings
    """

    return list_elements(database_path, folder_type)


def list_lines(database_path: str, line_type: str) -> list:
    """
    Gets a database path, and the specified line_type
    """

    return list_elements(database_path, line_type)


def filter_folder_id(query_result: list, element_ids: list) -> list:
    """
    Gets the optional element_id arg and filter by respective value
    """

    filtered_list = []
    for elt in query_result:
        # must convert values from query result
        # (returned as strings by cursor.fetchall) in uuid type
        if uuid.UUID(elt[0]) in element_ids:
            filtered_list.append(elt)
    return filtered_list


def list_children(database_path: str, parent_id: str, child_type: str) -> List[Element]:
    """
    Gets the absolute path to the database and the optional element_id arg (parent_id),
    the type of child element and returns the list of child elements
    """

    # connection to the database
    connection = sqlite3.Connection(database_path)
    cursor = connection.cursor()

    # query execution
    cursor.execute(
        """
        WITH RECURSIVE page_ids (id,ord) AS (
                SELECT child_id, ordering
                FROM element_path
                WHERE parent_id = ?
            UNION
                SELECT child_id, ordering
                FROM element_path
                JOIN page_ids ON (element_path.parent_id = page_ids.id)
        )
        SELECT element.id, name, polygon, worker_version_id
        FROM element
        JOIN page_ids USING (id)
        WHERE type = ?
        ORDER BY page_ids.ord;
        """,
        (parent_id, child_type),
    )

    result = list(starmap(Element, cursor.fetchall()))

    cursor.close()
    connection.close()

    return result


def element_image(database_path: str, element_id: str) -> Optional[Image]:
    """
    Gets the absolute path to the database and the element_id, and
    returns the url of the element as a string
    """
    # connection to the database
    connection = sqlite3.Connection(database_path)
    cursor = connection.cursor()

    # query execution
    cursor.execute(
        """
        SELECT image.id, url
        FROM image
        JOIN element ON image.id = element.image_id
        WHERE element.id = ?;
        """,
        (element_id,),
    )

    # gets the image id and the url corresponding to an element_id
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    if result is None:
        return
    return Image(*result)


def element_transcriptions(
    database_path: str, element_id: str
) -> Optional[Transcription]:

    # connection to the database
    connection = sqlite3.Connection(database_path)
    cursor = connection.cursor()

    # query execution
    cursor.execute(
        """
        WITH RECURSIVE child_ids (element_id) AS (
                SELECT child_id
                FROM element_path
                WHERE parent_id = ?
            UNION
                SELECT child_id
                FROM element_path
                JOIN child_ids ON (element_path.parent_id = child_ids.element_id)
        )
        SELECT
        transcription.id, transcription.element_id, text, confidence, worker_version_id
        FROM child_ids LEFT JOIN transcription
        ON child_ids.element_id = transcription.element_id;
        """,
        (element_id,),
    )

    result = cursor.fetchall()
    cursor.close()
    connection.close()
    if result is None:
        return
    return list(starmap(Transcription, result))


def get_worker_version(database_path: str, worker_version_id: str) -> Optional[Worker]:
    """
    Returns the worker namedtuple from the given element id
    """

    # connection to the database
    connection = sqlite3.Connection(database_path)
    cursor = connection.cursor()

    # query execution
    cursor.execute(
        """
        SELECT
        worker_version.id, worker_version.name, slug, worker_version.type, revision
        FROM worker_version
        WHERE worker_version.id = ?;
        """,
        (worker_version_id,),
    )

    # gets the image id and the url corresponding to an element_id
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    if result is None:
        return
    return Worker(*result)
