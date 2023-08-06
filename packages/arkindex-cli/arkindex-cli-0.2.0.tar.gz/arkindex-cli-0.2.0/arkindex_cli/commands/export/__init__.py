# -*- coding: utf-8 -*-
from enum import Enum
from pathlib import Path
from typing import List
from uuid import UUID

from arkindex_cli.commands.export.alto import alto_xml_gen
from arkindex_cli.commands.export.db import filter_folder_id, list_folders
from arkindex_cli.commands.export.pdf import pdf_gen


class ExportMode(Enum):
    PDF = "pdf"
    ALTO = "alto"


def add_export_parser(subcommands) -> None:
    parser = subcommands.add_parser(
        "export",
        help="Export elements from an exported SQLite database to other formats.",
        description="Export elements from an exported SQLite database to other formats.",
    )
    parser.add_argument(
        "database_path",
        type=Path,
        help="Path to the SQLite database exported from an Arkindex instance.",
    )
    parser.add_argument(
        "--mode",
        choices=[mode.value for mode in ExportMode],
        default=ExportMode.PDF.value,
        help="Export mode to use. Defaults to PDF.",
    )
    parser.add_argument(
        "--element-id",
        type=UUID,
        help="Restrict the exports to some element IDs. Exports all folders by default.",
        action="append",
        dest="element_ids",
    )
    parser.add_argument(
        "--page-type",
        default="page",
        type=str,
        help="Slug of an element type to use for pages. Defaults to `page`.",
    )
    parser.add_argument(
        "--folder-type",
        default="folder",
        type=str,
        help="Slug of an element type to use for folders. Defaults to `folder`.",
    )
    parser.add_argument(
        "--line-type",
        default="text_line",
        type=str,
        help="Slug of an element type to use for lines. Defaults to `text_line`.",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Make bounding boxes and transcriptions visible.",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=Path.cwd(),
        type=Path,
        help="Path to a directory where files will be exported to. Defaults to the current directory.",
        dest="output_path",
    )
    parser.set_defaults(func=run)


def run(
    database_path: Path,
    output_path: Path,
    mode: str,
    folder_type: str,
    element_ids: List[UUID] = [],
    **kwargs,
):
    database_path = database_path.absolute()
    assert database_path.is_file(), f"Database at {database_path} not found"

    output_path = output_path.absolute()
    assert output_path.is_dir(), f"Output path {output_path} is not a valid directory"

    folders = list_folders(database_path, folder_type)
    if element_ids is not None:
        folders = filter_folder_id(folders, element_ids)

    assert folders, f"No '{folder_type}' folders were found"

    gen_functions = {
        ExportMode.ALTO.value: alto_xml_gen,
        ExportMode.PDF.value: pdf_gen,
    }

    func = gen_functions.get(mode)
    assert func, f"Unsupported mode {mode}"

    for folder in folders:
        func(
            folder,
            database_path=database_path,
            output_path=output_path,
            folder_type=folder_type,
            element_ids=element_ids,
            **kwargs,
        )
