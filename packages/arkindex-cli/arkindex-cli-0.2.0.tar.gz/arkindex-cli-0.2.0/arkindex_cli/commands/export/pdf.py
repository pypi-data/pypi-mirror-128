# -*- coding: utf-8 -*-

import logging
import shutil
import tempfile
from pathlib import Path

from arkindex_cli.commands.export.db import (
    Element,
    element_image,
    element_transcriptions,
    list_children,
)
from arkindex_cli.commands.export.utils import bounding_box, image_download

try:
    from PIL import Image
    from reportlab.lib import colors
    from reportlab.pdfbase.pdfmetrics import stringWidth
    from reportlab.pdfgen import canvas
except ImportError:
    DEPS_AVAILABLE = False
else:
    DEPS_AVAILABLE = True


logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def image_draw(page: Element, image_path: str, c: "canvas", temp_dir: str) -> tuple:
    """
    Draw suitable image depending on crop if it is necessary
    """
    assert DEPS_AVAILABLE, "Missing PDF export dependencies"

    # opens existing image with PIL to get its size
    image = Image.open(image_path)

    # page Element must have a polygon
    assert page.polygon is not None

    # set default imageDraw function parameters
    pdf_image_width, pdf_image_height = image.width, image.height

    # getting dimensions of page bounding box
    page_box_dim = bounding_box(page.polygon)

    if (page_box_dim.width, page_box_dim.height) != image.size:

        # handling case when to crop image
        # PIL coordinates start from top-left corner,
        # crop method gets 4-tuple defining the left, upper, right, and
        # lower pixel coordinate.
        crop_parameters = (
            page_box_dim.x,
            # absolute value is to prevent cases where bounding_box
            # y coordinate is higher than box height
            abs(page_box_dim.height - page_box_dim.y),
            page_box_dim.x + page_box_dim.width,
            page_box_dim.y,
        )

        # saving cropped file in temp_dir to be called by drawImage
        image_path = temp_dir / f"{page.name}.jpg"

        image = image.crop(crop_parameters)
        image.save(image_path, format="JPEG")

        logger.info(f"saved cropped image at: {image_path}")

        # updating drawImage and pagesize parameters to bounding box
        pdf_image_width, pdf_image_height = page_box_dim.width, page_box_dim.height

    # sizes page to fit relevant image
    c.setPageSize(image.size)

    # drawing suitable image
    c.drawImage(image_path, 0, 0, pdf_image_width, pdf_image_height, mask=None)

    return image.size


def pdf_gen(
    folder: Element,
    database_path,
    output_path,
    page_type,
    line_type,
    debug,
    **kwargs,
) -> None:
    """
    Gets the database path, argument from cli, path to the generated pdf and the
    temporary directory where to find downloaded images
    """

    assert DEPS_AVAILABLE, "Missing PDF export dependencies"

    # creating temporary directory
    temp_dir = Path(tempfile.mkdtemp())
    logger.info(f"created temporary directory: {temp_dir}")

    # chooses color depending on debug option
    selected_color = colors.transparent

    if debug:
        selected_color = colors.fuchsia

    try:
        # canvas requires the input path as string
        c = canvas.Canvas(str(Path(output_path) / f"{folder.name}.pdf"))

        for page in list_children(database_path, folder.id, page_type):
            # handling case where no url is returned
            page_image = element_image(database_path, page.id)

            if page_image is None:
                logger.warning(f"no image for page {page.name} ({page.id})")
                continue

            # downloading existing image
            existing_image = image_download(page_image.url, page_image.id, temp_dir)

            # running reportlab drawing actions through image_draw and
            # returning updated image dimensions for the next steps
            image_width, image_height = image_draw(page, existing_image, c, temp_dir)

            # getting the list of Transcriptions namedtuples for each page
            page_transcriptions = element_transcriptions(database_path, page.id)

            # creating a dictionary where keys are lines ids and values are
            # relative line transcriptions
            transcriptions_dict = {
                transcription.element_id: transcription
                for transcription in page_transcriptions
            }

            lines = list_children(database_path, page.id, line_type)
            if not lines:
                logger.warning(f"no {line_type!r} in page {page.name} ({page.id})")

            for line in lines:

                # handling case where no polygon is returned
                if line.polygon is None:
                    logger.warning(f"no polygon for line {line.name} ({line.id})")

                # getting bounding box dimensions
                line_box_dim = bounding_box(line.polygon)

                # drawing line polygon bounding box
                # as the y axis is inverted, y origin point is "height - max_y"

                # drawing line polygon bounding box
                c.rect(
                    line_box_dim.x,
                    image_height - line_box_dim.y,
                    line_box_dim.width,
                    line_box_dim.height,
                    # linebox visible according to debug value
                    stroke=debug,
                )

                # handling case where line image is different from page image
                line_image = element_image(database_path, line.id)
                if line_image.url != page_image.url:
                    logger.warning(
                        f"""
                        {line.name} ({line.id}) image different from {page.name}
                        ({page.id}) image
                        """
                    )
                    continue

                # handling case where no transcription for a textline

                if line.id not in transcriptions_dict:
                    logger.warning(f"no transcription for {line.name} ({line.id})")
                    continue

                else:
                    text_to_draw = transcriptions_dict[line.id].text

                    c.setFillColor(selected_color)

                    # get the width of a single character, arbitrarily first one
                    # Font is set to MONOSPACE one such as Courier,
                    # fontsize is arbitrarily set to 10
                    char_width = stringWidth(text_to_draw[0], "Courier", 10)

                    # calculating ratio between character height and character
                    # width to adjust fontsize, character height has been set to
                    # 10
                    char_ratio = 10 / char_width

                    # character width so the fontsize match with the line_box_width
                    # corresponds to line box width divided by total number
                    # of characters in the string
                    font_width = line_box_dim.width / len(text_to_draw)

                    # adjusts the font size to match line box width
                    c.setFont("Courier", font_width * char_ratio)

                    # as the y axis is inverted, y origin point is "height - max_y"
                    c.drawString(
                        line_box_dim.x, image_height - line_box_dim.y, text_to_draw
                    )

            # save state and prepared new possible insertion within a page
            # (force PageBreak)
            c.showPage()

        # saving the whole canvas
        c.save()
        # change the name
        logger.info(f"{folder.name} generated at {output_path}")
    finally:
        shutil.rmtree(temp_dir)
