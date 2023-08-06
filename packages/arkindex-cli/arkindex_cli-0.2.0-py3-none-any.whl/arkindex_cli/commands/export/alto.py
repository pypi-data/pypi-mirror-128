# -*- coding: utf-8 -*-

import json
import logging
import xml.etree.ElementTree as ET
from pathlib import Path
from xml.sax.saxutils import escape

from arkindex_cli.commands.export.db import (
    Element,
    element_image,
    element_transcriptions,
    get_worker_version,
    list_children,
)
from arkindex_cli.commands.export.utils import BoundingBox

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def xml_bounding_box(polygon) -> BoundingBox:
    """
    Gets the coordinates of the a polygon and sets the coordinates of the lower
    left point at which box starts, third value is the width of the box, the last
    one is the height,
    contrary to reportlab coordinates system in alto format starts from the top
    left corner as for arkindex one
    """

    # getting polygon coordinates
    x_coords, y_coords = zip(*json.loads(polygon))

    # determining line box dimensions
    min_x, min_y = min(x_coords), min(y_coords)
    max_x, max_y = max(x_coords), max(y_coords)
    width, height = max_x - min_x, max_y - min_y

    return BoundingBox(min_x, min_y, width, height)


def alto_xml_gen(
    folder: Element,
    database_path,
    output_path: str,
    page_type,
    line_type,
    **kwargs,
):
    """
    gets the elements from the database path and creates a folder for each
    folder Element writes each page and relative lines as an alto xml file into
    the relative newly created folder at the specified output_path
    """

    children_list = list_children(database_path, folder.id, page_type)

    # validating the folder has pages, if not, no file is created
    if children_list:

        # folder path to be reused
        folder_path = Path(output_path) / folder.id
        # creating folder directory
        folder_path.mkdir()

        # setting the namespaces from alto v3
        ns_dict = {
            "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "xmlns": "http://www.loc.gov/standards/alto/ns-v4#",
            "xsi:schemaLocation": (
                "http://www.loc.gov/standards/alto/ns-v4# "
                "http://www.loc.gov/standards/alto/v4/alto-4-2.xsd"
            ),
            "xmlns:xlink": "http://www.w3.org/1999/xlink",
        }

        # preparing namespaces to be set with root element
        for prefix, uri in ns_dict.items():
            ET.register_namespace(prefix, uri)

        for count, page in enumerate(children_list, start=1):

            # defining root element of the alto doc as arkindex folder
            alto_root = ET.Element("alto", ns_dict)
            alto_description = ET.SubElement(alto_root, "Description")
            alto_unit = ET.SubElement(alto_description, "MeasurementUnit")
            # changed unit measure
            alto_unit.text = "pixel"

            # Layout markup alto subelement
            alto_layout = ET.SubElement(alto_root, "Layout")

            # initializing the set of worker ids for pages, lines and transcriptions to
            # fill description markup
            worker_set = set()

            # calling bounding_box on the page polygon to get the page dimensions
            # and fill the attributes dictionary
            page_box_dim = xml_bounding_box(page.polygon)

            # Page markup Layout subelement with specified attributes in the dictionary
            alto_page = ET.SubElement(
                alto_layout,
                "Page",
                attrib={
                    # any user-defined class but must start by a letter
                    "ID": f"page_{page.id}",
                    # PHYSICAL_IMG_NR is the number of the page within the document
                    "PHYSICAL_IMG_NR": str(count),
                    "WIDTH": str(page_box_dim.width),
                    "HEIGHT": str(page_box_dim.height),
                },
            )

            # adding page worker id in set and as page attribute if exists
            if page.worker_version_id is not None:

                worker_set.add(page.worker_version_id)
                alto_page.set("PROCESSINGREFS", f"worker_{page.worker_version_id}")

            # getting the list of Transcriptions namedtuples for each page
            page_transcriptions = element_transcriptions(database_path, page.id)

            # adding other subelements when page contains transcriptions
            if page_transcriptions is not None:

                # creating a dictionary where keys are lines ids and values are
                # relative line transcriptions
                transcriptions_dict = {
                    transcription.element_id: transcription
                    for transcription in page_transcriptions
                }

                alto_print_space = ET.SubElement(alto_page, "PrintSpace")
                alto_text_block = ET.SubElement(alto_print_space, "TextBlock")

                # For now a page can have a single text block
                alto_text_block.set("ID", f"page_{page.id}_textblock_{count}")

                for line in list_children(database_path, page.id, line_type):

                    # calling xml_bounding_box to fill textline attributes
                    line_box_dim = xml_bounding_box(line.polygon)

                    alto_line = ET.SubElement(
                        alto_text_block,
                        "TextLine",
                        attrib={
                            "HPOS": str(line_box_dim.x),
                            "VPOS": str(line_box_dim.y),
                            "WIDTH": str(line_box_dim.width),
                            "HEIGHT": str(line_box_dim.height),
                        },
                    )

                    # adding line worker id in set and as attribute if exists
                    if line.worker_version_id is not None:
                        worker_set.add(line.worker_version_id)
                        alto_line.set(
                            "PROCESSINGREFS", f"worker_{line.worker_version_id}"
                        )

                    alto_shape = ET.SubElement(alto_line, "Shape")
                    alto_polygon = ET.SubElement(alto_shape, "Polygon")

                    # creating the xml formatted string for polygon
                    xml_pol_str = " ".join(
                        f"{x},{y}" for x, y in json.loads(line.polygon)
                    )

                    alto_polygon.set("POINTS", xml_pol_str)
                    alto_string = ET.SubElement(alto_line, "String")

                    # setting default attributes
                    if line.id not in transcriptions_dict.keys():

                        alto_string.set("WC", "0")
                        alto_string.set("CONTENT", "no_content_available")
                        alto_string.set("PROCESSINGREFS", "no_processing_refs")

                    # overwriting attribute would create a new string element
                    else:
                        alto_string.set(
                            "WC", str(transcriptions_dict[line.id].confidence)
                        )
                        # by default '&', '<', and '>' are escaped in a string of
                        # data additional entity '"' is escape as it leads to close
                        # the attribute string
                        alto_string.set(
                            "CONTENT",
                            escape(transcriptions_dict[line.id].text, {'"': "&quot;"}),
                        )
                        alto_string.set(
                            "PROCESSINGREFS",
                            f"worker_{transcriptions_dict[line.id].worker_version_id}",
                        )
                        # adding transcription worker id in set
                        worker_set.add(transcriptions_dict[line.id].worker_version_id)

            # calling element_image to get the url to insert in sourceImageInformation
            # markup
            page_url = element_image(database_path, page.id).url
            alto_image_info = ET.SubElement(alto_description, "sourceImageInformation")
            alto_filename = ET.SubElement(alto_image_info, "fileName")
            alto_filename.text = page_url.split("/")[-1]
            alto_file_id = ET.SubElement(alto_image_info, "fileIdentifier")
            alto_file_id.text = page_url
            alto_doc_id = ET.SubElement(alto_image_info, "documentIdentifier")
            # document identifier is the page id
            alto_doc_id.text = page.id

            for worker_id in worker_set:
                alto_processing = ET.SubElement(alto_description, "Processing")
                # calling get_worker_version to get worker namedtuple
                worker = get_worker_version(database_path, worker_id)
                alto_processing.set("ID", f"worker_{worker.id}")
                alto_category = ET.SubElement(alto_processing, "processingCategory")
                alto_category.text = "contentGeneration"
                alto_step_desc = ET.SubElement(
                    alto_processing, "processingStepDescription"
                )
                alto_step_desc.text = worker.type
                alto_soft = ET.SubElement(alto_processing, "processingSoftware")
                alto_soft_name = ET.SubElement(alto_soft, "softwareName")
                alto_soft_name.text = worker.name
                alto_soft_ver = ET.SubElement(alto_soft, "softwareVersion")
                alto_soft_ver.text = worker.revision

            # creating the tree from the alto_page root element
            alto_tree = ET.ElementTree(alto_root)

            # filepath for the tree to be written in
            alto_file = folder_path / f"{page.id}.xml"

            # writing the tree as xml file in alto_page_path
            alto_tree.write(alto_file, encoding="utf-8", method="xml")

            logger.info(f"created alto xml file at {alto_file}")
