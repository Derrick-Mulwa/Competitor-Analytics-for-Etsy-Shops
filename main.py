import mysql.connector
import pandas as pd
from sqlalchemy import create_engine
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Frame, Paragraph, Spacer, PageBreak
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import math
from reportlab.pdfgen import canvas
from reportlab.platypus.flowables import PageBreak
from datetime import datetime, timedelta

host = 'localhost'
user = 'root'
# password = '123456'
password = 'root'

# Create a SQLAlchemy engine
engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}')

styles = getSampleStyleSheet()


def create_table(seo_r_overall, item_id, alias, item_name, most_recent_item_id, seo_ranking_page, seo_ranking_position,
                 original_price, discount_percentage, sale_price, greybg):
    item_name_style = ParagraphStyle(
        'item_name_style',
        parent=styles['Normal'],
        fontSize=7.5,
        textColor='black')

    item_name_Paragraph = Paragraph(item_name, item_name_style)

    data = [
        [str(seo_r_overall), f'${original_price}', "2,0", f'{str(discount_percentage)}%', "4,0", f'${sale_price}',
         '6,0'],
        ["0,1", str(most_recent_item_id), "2,1", str(seo_ranking_page), "4,1", str(seo_ranking_position), '6,1'],

        ["0,2", item_name_Paragraph, "2,2", "3,2", "4,2", "5,2", '6,2'],

        ["0,3", "1,3", "2,3", "3,3", "4,3", "5,3", '6,3'],

        ["0,4", "1,4", "2,4", "3,4", "4,4", "5,4", '6,4'],
        ["", str(item_id), "2,5", "3,5", "4,5", alias, '6,5']
    ]

    col_widths = [2.8 * inch / 6] * 7
    row_heights = [1.5 * inch / 5] * 6

    table = Table(data, colWidths=col_widths, rowHeights=row_heights)

    if greybg is False:
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'BOTTOM'),
            ('VALIGN', (0, 0), (0, 4), 'MIDDLE'),
            ('VALIGN', (5, 0), (5, 5), 'TOP'),
            ('VALIGN', (1, 4), (1, 6), 'TOP'),
            ('VALIGN', (0, 1), (6, 1), 'TOP'),
            ('VALIGN', (1, 0), (6, 0), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('INNERGRID', (0, 0), (-1, -1), 0.0, colors.grey),

            ('SPAN', (0, 0), (0, 4)),  # SEO
            ('SPAN', (1, 5), (4, 5)),  # ITEM_ID
            ('SPAN', (5, 5), (6, 5)),  # ALIAS
            ('SPAN', (1, 4), (6, 2)),  # Item Name
            ('SPAN', (1, 1), (2, 1)),  # Original
            ('SPAN', (3, 1), (4, 1)),  # Discount
            ('SPAN', (5, 1), (6, 1)),  # Sale 
            ('SPAN', (1, 0), (2, 0)),  # Price
            ('SPAN', (3, 0), (4, 0)),  # Percentage
            ('SPAN', (5, 0), (6, 0)),  # Price      
            ('LINEBELOW', (0, 4), (0, 4), 2, colors.white),
            ('LINEAFTER', (0, 0), (0, -1), 1, colors.grey),
            ('LINEBEFORE', (0, 0), (0, -1), 1, colors.black),

        ]))

    else:
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'BOTTOM'),
            ('VALIGN', (0, 0), (0, 4), 'MIDDLE'),
            ('VALIGN', (5, 0), (5, 5), 'TOP'),
            ('VALIGN', (1, 4), (1, 6), 'TOP'),
            ('VALIGN', (0, 1), (6, 1), 'TOP'),
            ('VALIGN', (1, 0), (6, 0), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('INNERGRID', (0, 0), (-1, -1), 0.0, colors.grey),
            ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),

            ('SPAN', (0, 0), (0, 4)),  # SEO
            ('SPAN', (1, 5), (4, 5)),  # ITEM_ID
            ('SPAN', (5, 5), (6, 5)),  # ALIAS
            ('SPAN', (1, 4), (6, 2)),  # Item Name
            ('SPAN', (1, 1), (2, 1)),  # Original
            ('SPAN', (3, 1), (4, 1)),  # Discount
            ('SPAN', (5, 1), (6, 1)),  # Sale
            ('SPAN', (1, 0), (2, 0)),  # Price
            ('SPAN', (3, 0), (4, 0)),  # Percentage
            ('SPAN', (5, 0), (6, 0)),  # Price
            ('LINEBELOW', (0, 4), (0, 4), 2, colors.lightgrey),
            ('LINEAFTER', (0, 0), (0, -1), 1, colors.grey),
            ('LINEBEFORE', (0, 0), (0, -1), 1, colors.black),
        ]))
    return table


def create_header():
    pdf.setFont('Calibri', 10)  # Font Name, Font size
    pdf.drawRightString(8 * inch, 0.4 * inch, 'Phase 3: Finding Most Recent Items Listed')
    pdf.drawString(0.5 * inch, 0.4 * inch, 'LP Chz Project: LP Etsy Shop')

    pdf.setLineWidth(2)
    pdf.setStrokeColor('black')
    pdf.line(0.4 * inch, 0.5 * inch, 8.2 * inch, 0.5 * inch)


def create_footer(page_num, total_pages):
    # Draw fooer line
    pdf.setLineWidth(2)
    pdf.setStrokeColor('black')
    pdf.line(0.6 * inch, 11 * inch, 8.2 * inch, 11 * inch)

    ## Page footer
    pdf.setFont('Calibri', 10)  # Font Name, Font size
    # pdf.drawRightString(8.1*inch,11.3*inch, f'Page {page_num} of {math.ceil(longer/5)+1}')
    pdf.drawRightString(8.1 * inch, 11.3 * inch, f'Page {page_num} of {total_pages}')
    pdf.setFont('Calibri', 10)  # Font Name, Font size

    ## Printed on
    pdf.setFont('Calibri', 10)  # Font Name, Font size
    pdf.drawString(0.7 * inch, 11.3 * inch, f'Printed on {datetime.now().strftime("%m/%d/%Y %H:%M %p")}')
    pdf.setFont('Calibri', 10)  # Font Name, Font size


etsy_shops_scraped_events_df = pd.read_sql('SELECT * FROM etsy.etsy_shops_scraped_events', engine)
tbl_etsy_shops_most_recent_items_df = pd.read_sql('Select * from etsy.tbl_etsy_shops_most_recent_items', engine)
shop_name_and_id_df = pd.read_sql('SELECT * FROM etsy.etsy_shops;', engine)

shops = etsy_shops_scraped_events_df.scraped_event_from_table[
    etsy_shops_scraped_events_df.scraped_event_from_table.str.contains('tbl_etsy_shops_most_recent_items. ')].unique()

shop_name_list = []
item_ids_list = []
most_recent_item_id_list = []
most_recent_item_scraped_datetime_list = []
shop_ids_list = []
item_name_list = []
shop_scraped_event_id_list = []
seo_ranking_page_list = []
seo_ranking_position_list = []
seo_ranking_overall_list = []
item_sale_price_list = []
item_discount_percentage_list = []
item_original_price_list = []

for shop in shops:  ####### CHANGED ######
    print(f'Finding NIP from {shop.replace("tbl_etsy_shops_most_recent_items.", "").strip()}')
    filtered_etsy_shops_scraped_events_df = etsy_shops_scraped_events_df[
        (etsy_shops_scraped_events_df.scraped_event_from_table == shop) & (
                    etsy_shops_scraped_events_df.scraped_event_end_datetime != '0000-00-00 00:00:00.000000') & (
                    (etsy_shops_scraped_events_df.was_minuend == 0) | (
                        etsy_shops_scraped_events_df.was_subtrahend == 0))].copy()
    shop_scraped_event_ids = list(filtered_etsy_shops_scraped_events_df.shop_scraped_event_id.values)

    for current_shop_scraped_event_id_index in range(len(shop_scraped_event_ids)):  ####### CHANGED ######
        try:
            # Get pdf page 1 data
            sec_a_data_scraped_events_data = filtered_etsy_shops_scraped_events_df[
                filtered_etsy_shops_scraped_events_df.shop_scraped_event_id == shop_scraped_event_ids[
                    current_shop_scraped_event_id_index]].iloc[0]
            sec_b_data_scraped_events_data = filtered_etsy_shops_scraped_events_df[
                filtered_etsy_shops_scraped_events_df.shop_scraped_event_id == shop_scraped_event_ids[
                    current_shop_scraped_event_id_index + 1]].iloc[0]

            shop_name = sec_a_data_scraped_events_data.scraped_event_from_table.replace(
                'tbl_etsy_shops_most_recent_items.', '').strip()
            shop_id = str(shop_name_and_id_df[shop_name_and_id_df.shop_name == shop_name].iloc[0].shop_id)
            sec_a_shop_scraped_event_id = str(sec_a_data_scraped_events_data.shop_scraped_event_id)
            sec_b_shop_scraped_event_id = str(sec_b_data_scraped_events_data.shop_scraped_event_id)

            sec_a_scraped_event_start_datetime = str(sec_a_data_scraped_events_data.scraped_event_start_datetime)
            sec_b_scraped_event_start_datetime = str(sec_b_data_scraped_events_data.scraped_event_start_datetime)

            sec_a_scraped_event_end_datetime = str(sec_a_data_scraped_events_data.scraped_event_end_datetime)
            sec_b_scraped_event_end_datetime = str(sec_b_data_scraped_events_data.scraped_event_end_datetime)

            sec_a_scraped_event_elapsed_datetime = str(sec_a_data_scraped_events_data.scraped_event_elapsed_datetime)
            sec_b_scraped_event_elapsed_datetime = str(sec_b_data_scraped_events_data.scraped_event_elapsed_datetime)

            sec_a_was_minuend = ['Yes' if sec_a_data_scraped_events_data.was_minuend == 1 else 'No'][0]
            sec_b_was_minuend = ['Yes' if sec_b_data_scraped_events_data.was_minuend == 1 else 'No'][0]

            sec_a_was_subtrahend = ['Yes' if sec_a_data_scraped_events_data.was_subtrahend == 1 else 'No'][0]
            sec_b_was_subtrahend = ['Yes' if sec_b_data_scraped_events_data.was_subtrahend == 1 else 'No'][0]

            # Write this data to pdf

            pdf = canvas.Canvas(f'report1/{shop.replace("tbl_etsy_shops_most_recent_items.", "").strip()} {sec_a_shop_scraped_event_id} vs {sec_b_shop_scraped_event_id} {datetime.now().strftime("%Y%m%d_%H%M")}.pdf',
                                bottomup=0)
            pdf.saveState()
            calibri_font = TTFont('Calibri', 'Calibri.ttf')
            pdfmetrics.registerFont(calibri_font)
            calibri_bold_font = TTFont('CalibriBold', 'Calibrib.ttf')
            pdfmetrics.registerFont(calibri_bold_font)

            fonts = pdf.getAvailableFonts()

            # Header
            pdf.setFont('Calibri', 11)  # Font Name, Font size
            pdf.drawString(50, 35, 'LP Chz Project. Shops')  # (Left to right, top to bottom)

            # grey bg
            pdf.setFillColor(colors.lightgrey)
            pdf.setStrokeColor(colors.white)
            pdf.rect(inch - 1, 10 + inch, 401, -0.5 * inch, fill=1)
            pdf.setFillColor(colors.black)
            pdf.setStrokeColor(colors.black)

            # Report Title
            pdf.setFont('CalibriBold', 20)  # Font Name, Font size
            pdf.setFillColor('Black')  # Text color
            pdf.translate(inch, inch)

            pdf.drawString(0, 0, 'Finding Most Recent Items Listed (detailed)')  # (Left to right, top to bottom)
            pdf.setLineWidth(2)
            pdf.line(0, 10, 400, 10)

            ## SHOP NAME
            pdf.setFont('Calibri', 11)  # Font Name, Font size
            pdf.translate(0.6 * inch, 0.6 * inch)
            pdf.drawString(0, 0, f'Shop name:')

            pdf.setFont('CalibriBold', 15)  # Font Name, Font size
            pdf.translate(0.8 * inch, 0)
            pdf.drawString(0, 0, f'{shop_name}')

            ## Shop_ID
            pdf.setFont('Calibri', 11)  # Font Name, Font size
            pdf.translate(4 * inch, 0)
            pdf.drawString(0, 0, f'Shop id:')

            pdf.setFont('Calibri', 11)  # Font Name, Font size
            pdf.translate(0.55 * inch, 0)
            pdf.drawString(0, 0, f'{shop_id}')

            ## Section A
            pdf.translate(-5 * inch, 0.7 * inch)
            pdf.setFont('CalibriBold', 14)  # Font Name, Font size
            pdf.setFillColor('Red')  # Text color
            pdf.drawString(0, 0, 'Section A')
            pdf.setLineWidth(1.2)
            pdf.setStrokeColor('red')
            pdf.line(0, 2, 56, 2)

            ## Section B
            pdf.translate(3.4 * inch, 0)
            pdf.setFont('CalibriBold', 14)  # Font Name, Font size
            pdf.setFillColor('Red')  # Text color
            pdf.drawString(0, 0, 'Section B')
            pdf.setLineWidth(1.2)
            pdf.setStrokeColor('red')
            pdf.line(0, 2, 56, 2)

            # For section A
            # Shop scraped event ID
            pdf.translate(-1.4 * inch, 0.5 * inch)  # Left-right, top-bottom
            pdf.setFillColor('Black')  # Text color
            pdf.setFont('Calibri', 11)  # Font Name, Font size
            pdf.drawRightString(0, 0, 'shop_scraped_event_id:')

            pdf.setFont('Calibri', 10)  # Font Name, Font size
            pdf.translate(0, 0.25 * inch)  # Left-right, top-bottom
            pdf.drawRightString(0, 0, f'{sec_a_shop_scraped_event_id}')

            # scraped_event_start_datetime
            pdf.setFont('Calibri', 11)  # Font Name, Font size
            pdf.translate(0, 0.4 * inch)  # Left-right, top-bottom
            pdf.drawRightString(0, 0, 'scraped_event_start_datetime:')

            pdf.setFont('Calibri', 10)  # Font Name, Font size
            pdf.translate(0, 0.25 * inch)  # Left-right, top-bottom
            pdf.drawRightString(0, 0, f'{sec_a_scraped_event_start_datetime}')

            # scraped_event_end_datetime
            pdf.setFont('Calibri', 11)  # Font Name, Font size
            pdf.translate(0, 0.4 * inch)  # Left-right, top-bottom
            pdf.drawRightString(0, 0, 'scraped_event_end_datetime:')

            pdf.setFont('Calibri', 10)  # Font Name, Font size
            pdf.translate(0, 0.25 * inch)  # Left-right, top-bottom
            pdf.drawRightString(0, 0, f'{sec_a_scraped_event_end_datetime}')

            # scraped_event_elapsed_datetime
            pdf.setFont('Calibri', 11)  # Font Name, Font size
            pdf.translate(0, 0.4 * inch)  # Left-right, top-bottom
            pdf.drawRightString(0, 0, 'scraped_event_elapsed_datetime:')

            pdf.translate(0, 0.25 * inch)  # Left-right, top-bottom
            pdf.setFont('Calibri', 10)  # Font Name, Font size
            pdf.drawRightString(0, 0, f'{sec_a_scraped_event_elapsed_datetime}')

            # was_minuend
            pdf.setFont('Calibri', 11)  # Font Name, Font size
            pdf.translate(0, 0.4 * inch)  # Left-right, top-bottom
            pdf.drawRightString(0, 0, 'was_minuend?:')

            pdf.translate(0, 0.25 * inch)  # Left-right, top-bottom
            pdf.drawRightString(0, 0, f'{sec_a_was_minuend}')

            # was_subtrahend
            pdf.setFont('Calibri', 11)  # Font Name, Font size
            pdf.translate(0, 0.4 * inch)  # Left-right, top-bottom
            pdf.drawRightString(0, 0, 'was_subtrahend?:')

            pdf.translate(0, 0.25 * inch)  # Left-right, top-bottom
            pdf.drawRightString(0, 0, f'{sec_a_was_subtrahend}')

            # For section B
            # Shop scraped event ID
            pdf.translate(3.4 * inch, ((-0.25 * 6) - (0.4 * 5)) * inch)  # Left-right, top-bottom
            pdf.setFillColor('Black')  # Text color
            pdf.setFont('Calibri', 11)  # Font Name, Font size
            pdf.drawRightString(0, 0, 'shop_scraped_event_id:')

            pdf.setFont('Calibri', 10)  # Font Name, Font size
            pdf.translate(0, 0.25 * inch)  # Left-right, top-bottom
            pdf.drawRightString(0, 0, f'{sec_b_shop_scraped_event_id}')

            # scraped_event_start_datetime
            pdf.setFont('Calibri', 11)  # Font Name, Font size
            pdf.translate(0, 0.4 * inch)  # Left-right, top-bottom
            pdf.drawRightString(0, 0, 'scraped_event_start_datetime:')

            pdf.setFont('Calibri', 10)  # Font Name, Font size
            pdf.translate(0, 0.25 * inch)  # Left-right, top-bottom
            pdf.drawRightString(0, 0, f'{sec_b_scraped_event_start_datetime}')

            # scraped_event_end_datetime
            pdf.setFont('Calibri', 11)  # Font Name, Font size
            pdf.translate(0, 0.4 * inch)  # Left-right, top-bottom
            pdf.drawRightString(0, 0, 'scraped_event_end_datetime:')

            pdf.setFont('Calibri', 10)  # Font Name, Font size
            pdf.translate(0, 0.25 * inch)  # Left-right, top-bottom
            pdf.drawRightString(0, 0, f'{sec_b_scraped_event_end_datetime}')

            # scraped_event_elapsed_datetime
            pdf.setFont('Calibri', 11)  # Font Name, Font size
            pdf.translate(0, 0.4 * inch)  # Left-right, top-bottom
            pdf.drawRightString(0, 0, 'scraped_event_elapsed_datetime:')

            pdf.translate(0, 0.25 * inch)  # Left-right, top-bottom
            pdf.setFont('Calibri', 10)  # Font Name, Font size
            pdf.drawRightString(0, 0, f'{sec_b_scraped_event_elapsed_datetime}')

            # was_minuend
            pdf.setFont('Calibri', 11)  # Font Name, Font size
            pdf.translate(0, 0.4 * inch)  # Left-right, top-bottom
            pdf.drawRightString(0, 0, 'was_minuend?:')

            pdf.translate(0, 0.25 * inch)  # Left-right, top-bottom
            pdf.drawRightString(0, 0, f'{sec_b_was_minuend}')

            # was_subtrahend
            pdf.setFont('Calibri', 11)  # Font Name, Font size
            pdf.translate(0, 0.4 * inch)  # Left-right, top-bottom
            pdf.drawRightString(0, 0, 'was_subtrahend?:')

            pdf.translate(0, 0.25 * inch)  # Left-right, top-bottom
            pdf.drawRightString(0, 0, f'{sec_b_was_subtrahend}')

            pdf.restoreState()

            section_a = tbl_etsy_shops_most_recent_items_df[
                tbl_etsy_shops_most_recent_items_df.shop_scraped_event_id == shop_scraped_event_ids[
                    current_shop_scraped_event_id_index]].copy()
            section_a['Alias'] = section_a.seo_ranking_overall.apply(lambda x: f'A{x}')
            section_b = tbl_etsy_shops_most_recent_items_df[
                tbl_etsy_shops_most_recent_items_df.shop_scraped_event_id == shop_scraped_event_ids[
                    current_shop_scraped_event_id_index + 1]].copy()

            section_b_shop_scraped_event_id = shop_scraped_event_ids[current_shop_scraped_event_id_index + 1]

            section_a_item_ids = list(section_a.item_id.values)
            section_b_item_ids = list(section_b.item_id.values)

            section_b_alias = []
            position = 1

            for item_id in section_b_item_ids:
                if item_id in section_a_item_ids:

                    section_b_alias += [section_a[section_a.item_id == item_id].Alias.values[0]]
                else:
                    section_b_alias += [f'B{position}']
                    position += 1

            section_b['Alias'] = section_b_alias

            section_a_alias = list(section_a.Alias.values)

            ################

            table_x = 0.7
            table_y = 6.8
            longer = [len(section_b) if len(section_b) > len(section_a) else len(section_b)][0]
            page_number = 1
            num_of_pages = math.ceil(longer / 5) + 1
            for x in range(longer):
                if x == 2:
                    create_footer(page_number, num_of_pages)
                    pdf.showPage()
                    page_number += 1

                    create_header()
                    create_footer(page_number, num_of_pages)

                    table_x = 0.7
                    table_y = 1

                if (x - 2) % 5 == 0 and x != 0 and x != 2:
                    page_number += 1
                    pdf.showPage()
                    create_footer(page_number, num_of_pages)
                    create_header()
                    table_x = 0.7
                    table_y = 1
                if x % 2 == 0:
                    if_grayscale = False
                else:
                    if_grayscale = True

                try:
                    section_a_able_data = section_a.iloc[x]
                    table_sec_a = create_table(
                        section_a_able_data.seo_ranking_overall,
                        section_a_able_data.item_id,
                        section_a_able_data.Alias,
                        section_a_able_data.item_name,
                        section_a_able_data.most_recent_item_id,
                        section_a_able_data.seo_ranking_page,
                        section_a_able_data.seo_ranking_position,
                        section_a_able_data.item_original_price,
                        section_a_able_data.item_discount_percentage,
                        section_a_able_data.item_sale_price,
                        if_grayscale)

                    table_sec_a.wrapOn(pdf, 0, 0)
                    table_sec_a.drawOn(pdf, table_x * inch, table_y * inch)
                except Exception as e:
                    pass

                table_x = 4.5

                try:
                    section_b_able_data = section_b.iloc[x]

                    table_sec_b = create_table(
                        section_b_able_data.seo_ranking_overall,
                        section_b_able_data.item_id,
                        section_b_able_data.Alias,
                        section_b_able_data.item_name,
                        section_b_able_data.most_recent_item_id,
                        section_b_able_data.seo_ranking_page,
                        section_b_able_data.seo_ranking_position,
                        section_b_able_data.item_original_price,
                        section_b_able_data.item_discount_percentage,
                        section_b_able_data.item_sale_price,
                        if_grayscale)

                    table_sec_b.wrapOn(pdf, 0, 0)
                    table_sec_b.drawOn(pdf, table_x * inch, table_y * inch)
                except:
                    pass

                table_y += 1.8
                table_x = 0.7

            no_activity_block_start_position = 0
            for i in range(len(section_b_alias)):
                if section_b_alias[i] == section_a_alias[0]:
                    if section_b_alias[i + 1] == section_a_alias[1] or (section_b_alias[i + 2] == section_a_alias[2]):
                        no_activity_block_start_position = i
                    else:
                        section_a_alias.remove(section_b_alias[i])

            activiy_block_item_ids = list(section_b.iloc[:no_activity_block_start_position, :].item_id.values)

            for item_id_index in range(len(activiy_block_item_ids)):
                item_ids_list += [activiy_block_item_ids[item_id_index]]
                most_recent_item_id_list += [tbl_etsy_shops_most_recent_items_df[(
                                                                                             tbl_etsy_shops_most_recent_items_df.shop_scraped_event_id == section_b_shop_scraped_event_id) & (
                                                                                             tbl_etsy_shops_most_recent_items_df.item_id ==
                                                                                             activiy_block_item_ids[
                                                                                                 item_id_index])][
                                                 ['most_recent_item_id']].most_recent_item_id.values[0]]
                most_recent_item_scraped_datetime_list += [tbl_etsy_shops_most_recent_items_df[(
                                                                                                           tbl_etsy_shops_most_recent_items_df.shop_scraped_event_id == section_b_shop_scraped_event_id) & (
                                                                                                           tbl_etsy_shops_most_recent_items_df.item_id ==
                                                                                                           activiy_block_item_ids[
                                                                                                               item_id_index])].most_recent_item_scraped_datetime.values[
                                                               0]]

                ##### NEWWWWW #####
                shop_name_list += [shop_name]
                shop_ids_list += [tbl_etsy_shops_most_recent_items_df[(
                                                                                  tbl_etsy_shops_most_recent_items_df.shop_scraped_event_id == section_b_shop_scraped_event_id) & (
                                                                                  tbl_etsy_shops_most_recent_items_df.item_id ==
                                                                                  activiy_block_item_ids[
                                                                                      item_id_index])].iloc[0].shop_id]
                item_name_list += [tbl_etsy_shops_most_recent_items_df[(
                                                                                   tbl_etsy_shops_most_recent_items_df.shop_scraped_event_id == section_b_shop_scraped_event_id) & (
                                                                                   tbl_etsy_shops_most_recent_items_df.item_id ==
                                                                                   activiy_block_item_ids[
                                                                                       item_id_index])].iloc[
                                       0].item_name]
                shop_scraped_event_id_list += [tbl_etsy_shops_most_recent_items_df[(
                                                                                               tbl_etsy_shops_most_recent_items_df.shop_scraped_event_id == section_b_shop_scraped_event_id) & (
                                                                                               tbl_etsy_shops_most_recent_items_df.item_id ==
                                                                                               activiy_block_item_ids[
                                                                                                   item_id_index])].iloc[
                                                   0].shop_scraped_event_id]
                seo_ranking_page_list += [tbl_etsy_shops_most_recent_items_df[(
                                                                                          tbl_etsy_shops_most_recent_items_df.shop_scraped_event_id == section_b_shop_scraped_event_id) & (
                                                                                          tbl_etsy_shops_most_recent_items_df.item_id ==
                                                                                          activiy_block_item_ids[
                                                                                              item_id_index])].iloc[
                                              0].seo_ranking_page]
                seo_ranking_position_list += [tbl_etsy_shops_most_recent_items_df[(
                                                                                              tbl_etsy_shops_most_recent_items_df.shop_scraped_event_id == section_b_shop_scraped_event_id) & (
                                                                                              tbl_etsy_shops_most_recent_items_df.item_id ==
                                                                                              activiy_block_item_ids[
                                                                                                  item_id_index])].iloc[
                                                  0].seo_ranking_position]
                seo_ranking_overall_list += [tbl_etsy_shops_most_recent_items_df[(
                                                                                             tbl_etsy_shops_most_recent_items_df.shop_scraped_event_id == section_b_shop_scraped_event_id) & (
                                                                                             tbl_etsy_shops_most_recent_items_df.item_id ==
                                                                                             activiy_block_item_ids[
                                                                                                 item_id_index])].iloc[
                                                 0].seo_ranking_overall]
                item_original_price_list += [tbl_etsy_shops_most_recent_items_df[(
                                                                                             tbl_etsy_shops_most_recent_items_df.shop_scraped_event_id == section_b_shop_scraped_event_id) & (
                                                                                             tbl_etsy_shops_most_recent_items_df.item_id ==
                                                                                             activiy_block_item_ids[
                                                                                                 item_id_index])].iloc[
                                                 0].item_original_price]
                item_discount_percentage_list += [tbl_etsy_shops_most_recent_items_df[(
                                                                                                  tbl_etsy_shops_most_recent_items_df.shop_scraped_event_id == section_b_shop_scraped_event_id) & (
                                                                                                  tbl_etsy_shops_most_recent_items_df.item_id ==
                                                                                                  activiy_block_item_ids[
                                                                                                      item_id_index])].iloc[
                                                      0].item_discount_percentage]
                item_sale_price_list += [tbl_etsy_shops_most_recent_items_df[(
                                                                                         tbl_etsy_shops_most_recent_items_df.shop_scraped_event_id == section_b_shop_scraped_event_id) & (
                                                                                         tbl_etsy_shops_most_recent_items_df.item_id ==
                                                                                         activiy_block_item_ids[
                                                                                             item_id_index])].iloc[
                                             0].item_sale_price]

            pdf.save()
        except Exception as e:
            print('Finished')

new_item_posted_id_list = [i + 1 for i in range(len(item_ids_list))]
df = pd.DataFrame({
    'shop_name': shop_name_list,
    'shop_id': shop_ids_list,
    'item_name': item_name_list,
    'item_id': item_ids_list,
    'new_item_posted_id': new_item_posted_id_list,
    'most_recent_item_id': most_recent_item_id_list,
    'shop_scraped_event_id': shop_scraped_event_id_list,
    'most_recent_item_scraped_datetime': most_recent_item_scraped_datetime_list,
    'seo_ranking_page': seo_ranking_page_list,
    'seo_ranking_position': seo_ranking_position_list,
    'seo_ranking_overall': seo_ranking_overall_list,
    'item_sale_price': item_sale_price_list,
    'item_discount_percentage': item_discount_percentage_list,
    'item_original_price': item_original_price_list
})

timedelta_list = []
for df_length in range(df.shape[0]):
    current_item_id = item_ids_list[df_length]
    current_timestamp = most_recent_item_scraped_datetime_list[df_length]
    try:
        sliced_df = df.iloc[:df_length, :]
        previous_timestamp = sliced_df[sliced_df.item_id == current_item_id].iloc[-1].most_recent_item_scraped_datetime
        time_delta = current_timestamp - previous_timestamp
    except:
        time_delta = 'NA'

    timedelta_list += [time_delta]

df.set_index('new_item_posted_id', inplace=True)
df['most_recent_item_scraped_deltatime'] = timedelta_list

print('\nCoping new items posted to db')

df_to_sql = df.reset_index()[
    ['new_item_posted_id', 'most_recent_item_id', 'item_id', 'most_recent_item_scraped_datetime',
     'most_recent_item_scraped_deltatime']].copy()
df_to_sql = df_to_sql.rename(columns={'most_recent_item_scraped_deltatime': 'most_recent_item_elapsed_deltatime'})
df_to_sql.to_sql('tbl_etsy_shops_new_items_posted', con=engine, schema='etsy', if_exists='replace', index=False)

print('\n\nGenerating report 2 for each shop.\n\n')


def draw_first_page_details(canvas, doc, shop_name, shop_id, elements):
    text = "Shops New Items Posted"
    text_x = 0.7 * inch
    text_y = doc.height

    # Draw a light grey rectangle behind the text
    canvas.setStrokeColor(colors.white)
    canvas.setFillColor(colors.lightgrey)
    canvas.rect(text_x - 1, text_y, doc.width, 0.4 * inch, fill=1)

    # Draw the text
    canvas.setFillColor(colors.black)
    canvas.setFont("Helvetica-Bold", 16)
    canvas.drawString(text_x + 5, text_y + 10, text)

    # Draw a line 1 cm below the text
    canvas.setLineWidth(1)
    canvas.setStrokeColor(colors.black)
    canvas.line(text_x - 1, text_y, doc.width + 0.65 * inch, text_y)

    # Shop name and ID
    shop_id_x = 1.5 * inch
    shop_id_y = doc.height - 0.45 * inch

    canvas.setFont("Helvetica", 11)
    canvas.drawString(shop_id_x, shop_id_y, f'Shop name: ')
    canvas.setFont("Helvetica-Bold", 14)
    canvas.drawString(shop_id_x + 1 * inch, shop_id_y, current_shop_name)

    canvas.setFont("Helvetica", 11)
    canvas.drawString(shop_id_x + 5 * inch, shop_id_y, f'Shop id: ')
    canvas.setFont("Helvetica-Bold", 13)
    canvas.drawString(shop_id_x + 5.65 * inch, shop_id_y, str(current_shop_id))

    line_x = 0.7 * inch
    line_y = doc.height - 0.8 * inch

    canvas.setStrokeColor(colors.black)
    canvas.setLineWidth(2)
    canvas.line(line_x, line_y, doc.width + 0.6 * inch, line_y)


# Create function to add page numbers and print date
def add_page_number(canvas, doc):
    page_num = canvas.getPageNumber()
    text = f"Page {page_num}"
    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(letter[0] - 0.3 * inch, 0.3 * inch, text)
    canvas.drawString(0.7 * inch, 11.10, f'Printed on {datetime.now().strftime("%m/%d/%Y %H:%M %p")}')


def firstpage_write(canvas, doc):
    add_page_number(canvas, doc)
    draw_first_page_details(canvas, doc, shop_name, str(shop_id), elements)


def write_item_name_id_nip(item_name, item_id, nip_counts):
    item_name_style = ParagraphStyle(
        'item_name_style',
        fontName='Helvetica',
        fontSize=8,
        leading=14,
        leftIndent=0.7 * inch,
        spaceAfter=10)
    para_text = f'''
    Item name: <b>{item_name}</b><br></br><br></br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Item id: <b>{item_id}</b>{"&nbsp;" * 90}
    Times this item was posted as new (NIP): <b>{nip_counts}</b>
    '''

    return Paragraph(para_text, item_name_style)


def deltatime_seconds_to_paragraph(total_seconds):
    deltatyme_style = ParagraphStyle(
        'deltatyme_style',
        fontName='Helvetica',
        fontSize=8,
        alignment=2)

    try:
        total_seconds = total_seconds.total_seconds()

        years = int(total_seconds // 31536000)
        remainder = total_seconds % 31536000
        if years < 10:
            years = f'0{years}'

        months = int(remainder // (30 * 24 * 60 * 60))
        remainder %= (30 * 24 * 60 * 60)
        if months < 10:
            months = f'0{months}'

        days = int(remainder // 86400)
        remainder %= 86400
        if days < 10:
            days = f'0{days}'

        hours = int(remainder // 3600)
        remainder %= 3600
        if hours < 10:
            hours = f'0{hours}'

        minutes = int(remainder // 60)
        if minutes < 10:
            minutes = f'0{minutes}'

        seconds = int(remainder % 60)
        if seconds < 10:
            seconds = f'0{seconds}'

        para_text = f'''<p>{years} {'&nbsp;' * 2}{months}{'&nbsp;' * 2} {days} {'&nbsp;' * 2}{hours} {'&nbsp;' * 2}{minutes}{'&nbsp;' * 3}{seconds}<br></br>
        yy {'&nbsp;'} mm{'&nbsp;' * 2}dd {'&nbsp;'} hh{'&nbsp;' * 2}  mm{'&nbsp;' * 2}ss'''

        return Paragraph(para_text, deltatyme_style), total_seconds


    except Exception as x:
        para_text = para_text = f'''   NA{'&nbsp;' * 20}<br></br>
        yy {'&nbsp;'} mm{'&nbsp;' * 2}dd {'&nbsp;'} hh{'&nbsp;' * 2}  mm{'&nbsp;' * 2}ss'''
        return Paragraph(para_text, deltatyme_style), 00


def create_and_populate_table(x):
    total_seconds = x.most_recent_item_scraped_deltatime.apply(lambda x: deltatime_seconds_to_paragraph(x)[1]).sum()
    total_seconds_paragraph = deltatime_seconds_to_paragraph(timedelta(seconds=int(total_seconds)))[0]
    x.most_recent_item_scraped_deltatime = x.most_recent_item_scraped_deltatime.apply(
        lambda x: deltatime_seconds_to_paragraph(x)[0])
    x['index'] = [i + 1 for i in range(len(x.index))]

    # x = df[df.item_id == 1156809971].reset_index()[['new_item_posted_id','most_recent_item_id','shop_scraped_event_id','most_recent_item_scraped_datetime','most_recent_item_scraped_deltatime','seo_ranking_page','seo_ranking_position','seo_ranking_overall','item_original_price','item_discount_percentage','item_sale_price']].reset_index()
    dta = [list(i) for i in list(x.values)]
    table_header_style = ParagraphStyle(
        'table_header_style',
        fontName='Helvetica-Bold',
        fontSize=6.5,
        alignment=1
    )
    data = [[Paragraph(i, table_header_style) for i in
             ['#', 'new_ item_ posted_ id', 'most_ recent_ item_ id', 'shop_ scraped _ event_ id',
              'most_ recent_ item_ scraped_ datetime', 'most_ recent_ item_ scraped_ deltatime', 'seo_ ranking_ page',
              'seo_ ranking_ position', 'seo_ ranking_ overall', 'item_ original_ price', 'item_ discount_ percentage',
              'item_ sale_ price']]] \
           + dta + [
               ['Total:', 2, 3, 4, 5, total_seconds_paragraph, 'Averages:', 8, 9, x.item_original_price.mean().round(2),
                x.item_discount_percentage.mean().round(2), x.item_sale_price.mean().round(2)]]

    col_widths = [0.25 * inch, 0.5 * inch, 0.5 * inch, 0.5 * inch, 1.5 * inch, 1.5 * inch, 0.5 * inch, 0.5 * inch,
                  0.5 * inch, 0.5 * inch,
                  0.5 * inch]  # Calculate column width based on page width and number of columns
    table = Table(data, colWidths=col_widths, hAlign='LEFT')

    # Style the table
    table.setStyle(TableStyle([
                                  ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  # Add gridlines
                                  ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Header row background color
                                  ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center-align all cells
                                  ('FONTNAME', (0, 0), (-1, 0), 'Helvetica'),  # Header font style
                                  ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font style

                                  ('FONTSIZE', (0, 0), (-1, -1), 7),  # Header font size
                                  ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),  # Body font style

                                  # Format Total
                                  ('FONTSIZE', (0, 0), (-1, 0), 5),
                                  ('ALIGN', (0, -1), (4, -1), 'RIGHT'),
                                  ('FONTNAME', (0, -1), (4, -1), 'Helvetica-Bold'),
                                  ('FONTSIZE', (0, -1), (4, -1), 10),

                                  # Format Averages
                                  ('FONTSIZE', (6, -1), (8, -1), 5),
                                  ('ALIGN', (6, -1), (8, -1), 'RIGHT'),
                                  ('FONTNAME', (6, -1), (8, -1), 'Helvetica-Bold'),
                                  ('FONTSIZE', (6, -1), (8, -1), 10),

                              ] + [('BACKGROUND', (0, i), (-1, i), colors.white) if i % 2 != 0 else (
    'BACKGROUND', (0, i), (-1, i), colors.lightgrey) for i in range(len(data))] +
                              [('SPAN', (0, -1), (4, -1)),
                               ('BACKGROUND', (0, -1), (4, -1), colors.white),
                               ('LINEBEFORE', (0, -1), (4, -1), 2, colors.white),
                               ('LINEBELOW', (0, -1), (4, -1), 2, colors.white),

                               ('SPAN', (6, -1), (8, -1)),
                               ('BACKGROUND', (6, -1), (8, -1), colors.white),
                               ('LINEBELOW', (6, -1), (8, -1), 2, colors.white)]))
    return table, total_seconds


def statistics_times(total_seconds, items):
    deltatyme_style = ParagraphStyle(
        'deltatyme_style',
        fontName='Helvetica',
        fontSize=8,
        alignment=2)

    if items != 1:
        try:
            years = int(total_seconds // 31536000)
            remainder = total_seconds % 31536000
            if years < 10:
                years = f'0{years}'

            months = int(remainder // (30 * 24 * 60 * 60))
            remainder %= (30 * 24 * 60 * 60)
            if months < 10:
                months = f'0{months}'

            days = int(remainder // 86400)
            remainder %= 86400
            if days < 10:
                days = f'0{days}'

            hours = int(remainder // 3600)
            remainder %= 3600
            if hours < 10:
                hours = f'0{hours}'

            minutes = int(remainder // 60)
            if minutes < 10:
                minutes = f'0{minutes}'

            seconds = int(remainder % 60)
            if seconds < 10:
                seconds = f'0{seconds}'

            data = [[Paragraph(f'<b>{items} items</b>', deltatyme_style), Paragraph(
                f'''{years} {'&nbsp;' * 2}{months}{'&nbsp;' * 2} {days} {'&nbsp;' * 2}{hours} {'&nbsp;' * 2}{minutes}{'&nbsp;' * 3}{seconds}<br></br>yy {'&nbsp;'} mm{'&nbsp;' * 2}dd {'&nbsp;'} hh{'&nbsp;' * 2}  mm{'&nbsp;' * 2}ss''',
                deltatyme_style)]]
            col_widths = [1 * inch, 1.5 * inch]
            table = Table(data, colWidths=col_widths, hAlign='LEFT')
            table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LINEBELOW', (0, 0), (-1, -1), 0.25, colors.white),
            ]))

            return table


        except Exception as x:
            years = '00'
            months = '00'
            days = '00'
            hours = '00'
            minutes = '00'
            seconds = '00'

            data = [[Paragraph(f'<b>{items} items</b>', deltatyme_style), Paragraph(
                f'''{years} {'&nbsp;' * 2}{months}{'&nbsp;' * 2} {days} {'&nbsp;' * 2}{hours} {'&nbsp;' * 2}{minutes}{'&nbsp;' * 3}{seconds}<br></br>yy {'&nbsp;'} mm{'&nbsp;' * 2}dd {'&nbsp;'} hh{'&nbsp;' * 2}  mm{'&nbsp;' * 2}ss''',
                deltatyme_style)]]
            col_widths = [1 * inch, 1.5 * inch]
            table = Table(data, colWidths=col_widths, hAlign='LEFT')
            table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LINEBELOW', (0, 0), (-1, -1), 0.25, colors.white),
            ]))

            return table

    else:
        years = '00'
        months = '00'
        days = '00'
        hours = '00'
        minutes = '00'
        seconds = '00'

        data = [[Paragraph(f'<b>{items} items</b>', deltatyme_style), Paragraph(
            f'''{years} {'&nbsp;' * 2}{months}{'&nbsp;' * 2} {days} {'&nbsp;' * 2}{hours} {'&nbsp;' * 2}{minutes}{'&nbsp;' * 3}{seconds}<br></br>yy {'&nbsp;'} mm{'&nbsp;' * 2}dd {'&nbsp;'} hh{'&nbsp;' * 2}  mm{'&nbsp;' * 2}ss''',
            deltatyme_style)]]
        col_widths = [inch, 1.5 * inch]
        table = Table(data, colWidths=col_widths, hAlign='LEFT')
        table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LINEBELOW', (0, 0), (-1, -1), 0.25, colors.white),
        ]))

        return table


def time_to_seconds_breakdown(total_seconds, items):
    deltatyme_style = ParagraphStyle(
        'deltatyme_style',
        fontName='Helvetica',
        fontSize=8,
        alignment=2)

    try:
        years = int(total_seconds // 31536000)
        remainder = total_seconds % 31536000
        years_string = [f'{years}y x 365d =', f'{years * 365}d x 24h =', f'{years * 365 * 24}h x 60m =',
                        f'{years * 365 * 24 * 60}m x 60s =', f'{years * 365 * 24 * 60 * 60}s', '']

        months = int(remainder // (30 * 24 * 60 * 60))
        remainder %= (30 * 24 * 60 * 60)
        months_string = [f'{months}m x (365/12)d =', f'{int(months * (365 / 12))}d x 24h =',
                         f'{int(months * (365 / 12)) * 24}h x 60m =', f'{int(months * (365 / 12)) * 24 * 60}m x 60s =',
                         f'{int(months * (365 / 12)) * 24 * 60 * 60}s', '']

        days = int(remainder // 86400)
        remainder %= 86400
        days_string = [f'', f'{days}d x 24h =', f'{days * 24}h x 60m =', f'{days * 24 * 60}m x 60s =',
                       f'{days * 24 * 60 * 60}s', '']

        hours = int(remainder // 3600)
        remainder %= 3600
        hours_string = [f'', f'', f'{hours}h x 60m =', f'{hours * 60}m x 60s =', f'{hours * 60 * 60}s', '']

        minutes = int(remainder // 60)
        minutes_string = [f'', f'', f'', f'{minutes}m x 60s =', f'{minutes * 60}s', '']

        seconds = int(remainder % 60)
        seconds_string = [f'', f'', f'', f'{seconds}s=', f'{seconds}s', '']

        equals_string = [f'', f'', f'', f'', f'--------------', '']

        total_string = [f'', f'', f'', f'', f'{(int(total_seconds)):,}s', 'Total']

        data = [years_string, months_string, days_string, hours_string, minutes_string, seconds_string, equals_string,
                total_string]

        data = [[Paragraph(j, deltatyme_style) for j in i] for i in data]

        col_widths = [1.2 * inch, 0.9 * inch, 0.9 * inch, 1.2 * inch, 0.9 * inch, 0.6 * inch]
        table = Table(data, colWidths=col_widths, hAlign='LEFT')
        table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('LINEBELOW', (0, 0), (-1, -1), 0.25, colors.white),
        ]))

        return table


    except Exception as x:
        print(x)
        years = 0
        months = 0
        days = 0
        hours = 0
        minutes = 0
        seconds = 0
        total_seconds = 0

        years_string = [f'{years}y x 365d =', f'{years * 365}d x 24h =', f'{years * 365 * 24}h x 60m =',
                        f'{years * 365 * 24 * 60}m x 60s =', f'{(years * 365 * 24 * 60 * 60):,}s', '']
        months_string = [f'{months}m x (365/12)d =', f'{int(months * (365 / 12))}d x 24h =',
                         f'{int(months * (365 / 12)) * 24}h x 60m =', f'{int(months * (365 / 12)) * 24 * 60}m x 60s =',
                         f'{(int(months * (365 / 12)) * 24 * 60 * 60):,}s', '']
        days_string = [f'', f'{days}d x 24h =', f'{days * 24}h x 60m =', f'{days * 24 * 60}m x 60s =',
                       f'{(days * 24 * 60 * 60):,}s', '']
        hours_string = [f'', f'', f'{hours}h x 60m =', f'{(hours * 60):,}m x 60s =', f'{(hours * 60 * 60):,}s', '']
        minutes_string = [f'', f'', f'', f'{minutes:,}m x 60s =', f'{(minutes * 60):,}s', '']
        seconds_string = [f'', f'', f'', f'{seconds}s=', f'{seconds}s', '']
        equals_string = [f'', f'', f'', f'', f'--------------', '']
        total_string = [f'', f'', f'', f'', f'{int(total_seconds):,}s', 'Total']

        data = [years_string, months_string, days_string, hours_string, minutes_string, seconds_string, equals_string,
                total_string]
        data = [[Paragraph(j, deltatyme_style) for j in i] for i in data]

        col_widths = [1.2 * inch, 0.9 * inch, 0.9 * inch, 1.2 * inch, 0.9 * inch, 0.6 * inch]
        table = Table(data, colWidths=col_widths, hAlign='LEFT')
        table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('LINEBELOW', (0, 0), (-1, -1), 0.25, colors.white),
        ]))

        return table


def final_table(item_per_second_, item_sale_mean_price):
    left_aligned = ParagraphStyle(
        'deltatyme_style',
        fontName='Helvetica',
        fontSize=8,
        alignment=0)

    right_aligned = ParagraphStyle(
        'deltatyme_style',
        fontName='Helvetica',
        fontSize=8,
        alignment=2)

    center_aligned = ParagraphStyle(
        'deltatyme_style',
        fontName='Helvetica',
        fontSize=8,
        alignment=1)

    line_1 = [Paragraph(f'{item_per_second_:,.8f}', right_aligned), Paragraph('NIP/sec', left_aligned),
              Paragraph('x', center_aligned),
              Paragraph('1 sec', center_aligned), Paragraph('=', center_aligned),
              Paragraph(f'{item_per_second_:,.8f}', right_aligned), Paragraph('NIP/sec', left_aligned),
              Paragraph(f'@ ~ ${item_sale_mean_price} ea item =', right_aligned),
              Paragraph(f'~ ${(item_per_second_ * item_sale_mean_price):,.8f}', right_aligned),
              Paragraph('per sec', left_aligned)]

    line_2 = [Paragraph(f'{item_per_second_:,.8f}', right_aligned),
              Paragraph('NIP/sec', left_aligned),
              Paragraph('x', center_aligned),
              Paragraph('60 sec', center_aligned),
              Paragraph('=', center_aligned),
              Paragraph(f'{item_per_second_ * 60:,.8f}', right_aligned),
              Paragraph('NIP/min', left_aligned),
              Paragraph(f'@ ~ ${item_sale_mean_price} ea item =', right_aligned),
              Paragraph(f'~ ${(item_per_second_ * 60 * item_sale_mean_price):,.8f}', right_aligned),
              Paragraph('per min', left_aligned)]

    line_3 = [Paragraph(f'{item_per_second_ * 60:,.8f}', right_aligned),
              Paragraph('NIP/min', left_aligned),
              Paragraph('x', center_aligned),
              Paragraph('60 min', center_aligned),
              Paragraph('=', center_aligned),
              Paragraph(f'{item_per_second_ * 60 * 60:,.8f}', right_aligned),
              Paragraph('NIP/hr', left_aligned),
              Paragraph(f'@ ~ ${item_sale_mean_price} ea item =', right_aligned),
              Paragraph(f'~ ${(item_per_second_ * 60 * 60 * item_sale_mean_price):,.8f}', right_aligned),
              Paragraph('per hour', left_aligned)]

    line_4 = [Paragraph(f'{item_per_second_ * 60 * 60:,.8f}', right_aligned),
              Paragraph('NIP/hr', left_aligned),
              Paragraph('x', center_aligned),
              Paragraph('24 hr', center_aligned),
              Paragraph('=', center_aligned),
              Paragraph(f'{item_per_second_ * 60 * 60 * 24:,.8f}', right_aligned),
              Paragraph('NIP/day', left_aligned),
              Paragraph(f'@ ~ ${item_sale_mean_price} ea item =', right_aligned),
              Paragraph(f'~ ${(item_per_second_ * 60 * 60 * 24 * item_sale_mean_price):,.8f}', right_aligned),
              Paragraph('per day', left_aligned)]

    line_5 = [Paragraph(f'{item_per_second_ * 60 * 60 * 24:,.8f}', right_aligned),
              Paragraph('NIP/day', left_aligned),
              Paragraph('x', center_aligned),
              Paragraph('7 d', center_aligned),
              Paragraph('=', center_aligned),
              Paragraph(f'{item_per_second_ * 60 * 60 * 24 * 7:,.8f}', right_aligned),
              Paragraph('NIP/week', left_aligned),
              Paragraph(f'@ ~ ${item_sale_mean_price} ea item =', right_aligned),
              Paragraph(f'~ ${(item_per_second_ * 60 * 60 * 24 * 7 * item_sale_mean_price):,.8f}', right_aligned),
              Paragraph('per week', left_aligned)]

    line_6 = [Paragraph(f'{item_per_second_ * 60 * 60 * 24:,.8f}', right_aligned),
              Paragraph('NIP/day', left_aligned),
              Paragraph('x', center_aligned),
              Paragraph('365 d/12m', center_aligned),
              Paragraph('=', center_aligned),
              Paragraph(f'{item_per_second_ * 60 * 60 * 24 * (365 / 12):,.8f}', right_aligned),
              Paragraph('NIP/month', left_aligned),
              Paragraph(f'@ ~ ${item_sale_mean_price} ea item =', right_aligned),
              Paragraph(f'~ ${(item_per_second_ * 60 * 60 * 24 * (365 / 12) * item_sale_mean_price):,.8f}',
                        right_aligned),
              Paragraph('per month', left_aligned)]

    line_7 = [Paragraph(f'{item_per_second_ * 60 * 60 * 24:,.8f}', right_aligned),
              Paragraph('NIP/day', left_aligned),
              Paragraph('x', center_aligned),
              Paragraph('365 d', center_aligned),
              Paragraph('=', center_aligned),
              Paragraph(f'{item_per_second_ * 60 * 60 * 24 * 365:,.8f}', right_aligned),
              Paragraph('NIP/year', left_aligned),
              Paragraph(f'@ ~ ${item_sale_mean_price} ea item =', right_aligned),
              Paragraph(f'~ ${(item_per_second_ * 60 * 60 * 24 * 365 * item_sale_mean_price):,.8f}', right_aligned),
              Paragraph('per year', left_aligned)]

    data = [line_1, line_2, line_3, line_4, line_5, line_6, line_7]
    # data = [[Paragraph(j, deltatyme_style) for j in i] for i in data]

    col_widths = [0.8 * inch, 0.6 * inch, 0.3 * inch, 0.7 * inch, 0.3 * inch, 1.2 * inch, 0.7 * inch, 1.3 * inch,
                  1.3 * inch, 0.9 * inch]
    table = Table(data, colWidths=col_widths, hAlign='LEFT')
    table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LINEBELOW', (0, 0), (-1, -1), 0.25, colors.white),
        # ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  # Add gridlines

    ]))

    return table


shop_names_list = list(df.shop_name.unique())

for shop in shop_names_list:

    file_name = f'report2/{shop} {datetime.now().strftime("%Y%m%d_%H%M")}.pdf'

    doc = SimpleDocTemplate(
        file_name,
        pagesize=letter,
        leftMargin=0.5 * inch,
        rightMargin=0.5 * inch,
        topMargin=0.5 * inch,
        bottomMargin=0.5 * inch
    )

    elements = []
    styles = getSampleStyleSheet()

    elements.append(Spacer(2, 1.6 * inch))

    current_shop_df = df[df.shop_name == shop]
    unique_item_ids = list(current_shop_df.item_id.value_counts().index)

    for each_unique_item_id in unique_item_ids:
        df_ = current_shop_df[current_shop_df.item_id == each_unique_item_id]
        x = df_.reset_index()[
            ['new_item_posted_id', 'most_recent_item_id', 'shop_scraped_event_id', 'most_recent_item_scraped_datetime',
             'most_recent_item_scraped_deltatime', 'seo_ranking_page', 'seo_ranking_position', 'seo_ranking_overall',
             'item_original_price', 'item_discount_percentage', 'item_sale_price']].reset_index()
        current_shop_name = df_.shop_name.iloc[0]
        current_shop_id = df_.shop_id.iloc[0]
        current_item_name = df_.item_name.iloc[0]
        current_item_id = df_.item_id.iloc[0]

        elements.append(write_item_name_id_nip(current_item_name, str(current_item_id), str(len(df_))))

        table_data = create_and_populate_table(x)
        my_table = table_data[0]
        total_seconds = table_data[1]
        # Add the table to the elements list
        elements.append(my_table)

        statistics_title_style = ParagraphStyle(
            'statistics_style',
            fontName='Helvetica-Bold',
            fontSize=12, )

        statistics_title = Paragraph('<br></br><br></br><br></br><br></br><b>Statistics:</b><br></br><br></br>',
                                     statistics_title_style)

        elements.append(statistics_title)

        statistics_body = f'{current_shop_name} shop posted the same item id {current_item_id} as New Item Posted (NIP):<br></br><br></br>'

        statistics_body_style = ParagraphStyle(
            'statistics_style',
            fontName='Helvetica',
            fontSize=8, )

        statistics_body_paragraph = Paragraph(statistics_body, statistics_body_style)
        elements.append(statistics_body_paragraph)

        elements.append(statistics_times(total_seconds, (len(x))))

        next_text = f'<br></br>We need to know how many times it was listed as NIP per second:<br></br><br></br>'

        next_text_style = ParagraphStyle(
            'statistics_style',
            fontName='Helvetica',
            fontSize=8, )

        next_text_paragraph = Paragraph(next_text, next_text_style)
        elements.append(next_text_paragraph)

        elements.append(time_to_seconds_breakdown(total_seconds, len(x)))

        if total_seconds == 0:
            item_per_second = 0
        else:
            item_per_second = (len(x) / total_seconds).round(8)

        next_text = f'''<br></br>So, shop {current_shop_name} posted:<br></br><br></br>
        <b>{'&nbsp;' * 20}{str(len(x))} times as NIP in {int(total_seconds):,} secs</b><br></br><br></br>
        How many times did shop {current_shop_name} posted the article as NIP per second?<br></br><br></br>
        <b>{'&nbsp;' * 20}{str(len(x))} items / {int(total_seconds):,} secs = {item_per_second:,.8f} items/sec</b><br></br><br></br>
        So, shop {current_shop_name} listed item as NIP (New Item Posted):<br></br><br></br>'''

        next_text_style = ParagraphStyle(
            'statistics_style',
            fontName='Helvetica',
            fontSize=8, )

        next_text_paragraph = Paragraph(next_text, next_text_style)
        elements.append(next_text_paragraph)

        item_sale_mean_price = x.item_sale_price.mean().round(2)

        elements.append(final_table(item_per_second, item_sale_mean_price))

        elements.append(PageBreak())

    doc.build(elements, onFirstPage=firstpage_write, onLaterPages=add_page_number)
    print(f"PDF saved as {file_name}")

