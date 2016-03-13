
#
# Unfortunately, the lpod python documentation is substantially lacking
# I've had modest good luck looking at
# the perl version of the docs here
# http://search.cpan.org/~jmgdoc/ODF-lpOD-1.126/lpOD/Style.pod
# and supplimenting them with some other python examples from
# https://github.com/lpod/lpod-python-recipes/blob/master/Examples/create_a_text_document_from_plain_text_with_layout.py
#

from lpod.document import odf_new_document
from lpod.heading import odf_create_heading
from lpod.paragraph import odf_create_paragraph
from lpod.style import odf_create_style
from lpod.element import odf_create_element


class Opendoc_Goldstandard:

  def __init__(self):
    #
    # Create the initial document object, deleting any existing default
    # styles
    self.document = odf_new_document('text')
    self.document.delete_styles()

    #
    # Now, create a page style, note that the name inside this stis is
    # later used by the _style_master. One might wonder about the 
    # small margins here. This is required to get ODT to apply the
    # background color to the full page
    #
    _style_page = odf_create_element(u"""\
      <style:page-layout style:name="MyLayout">
      <style:page-layout-properties fo:page-width="21.00cm" fo:page-height="29.70cm" \
      style:num-format="1" style:print-orientation="portrait" fo:margin-top="0.0cm" \
      fo:margin-bottom="0.0cm" fo:margin-left="0.0cm" fo:margin-right="0.0cm" \
      style:writing-mode="lr-tb" style:footnote-max-height="0cm"><style:footnote-sep \
      style:width="0.00cm" style:distance-before-sep="0.00cm" \
      style:distance-after-sep="0.10cm" style:line-style="solid" \
      style:adjustment="left" style:rel-width="25%" style:color="#000000"/>
      </style:page-layout-properties><style:footer-style>
      <style:header-footer-properties fo:min-height="0.0cm" fo:margin-left="0cm" \
      fo:margin-right="0cm" fo:margin-top="0.0cm" style:dynamic-spacing="false"/>
      </style:footer-style></style:page-layout>""")
   
    # 
    # Now create a style master
    #
    _style_master = odf_create_element(u"""\
      <style:master-page style:name="Standard" \
      style:page-layout-name="MyLayout"><style:footer><text:p text:style-name="Footer">\
      <text:tab/><text:tab/><text:page-number \
      text:select-page="current"/> / <text:page-count \
      style:num-format="1">15</text:page-count></text:p></style:footer>\
      </style:master-page>""")


    # some footer
    _style_footer = odf_create_element(u"""\
      <style:style style:name="Footer" style:family="paragraph" style:class="extra" \
      style:master-page-name=""><style:paragraph-properties style:page-number="auto" \
      text:number-lines="false" text:line-number="0"><style:tab-stops>\
      <style:tab-stop style:position="8.90cm" style:type="center"/><style:tab-stop \
      style:position="17.80cm" style:type="right"/></style:tab-stops>
      </style:paragraph-properties><style:text-properties \
      style:font-name="Liberation Sans" fo:font-size="7pt"/></style:style>""")

    p = odf_create_paragraph("The New Hampshire Liberty Alliance is a non-partisan coalition working to increase individual liberty, and encourage citizen involvement in the legislative process. Bills on the Gold Standard are evaluated based on their effects on, among other things; civil liberties, personal responsibility, property rights, accountability, constitutionality, and taxation. Roll call votes on Gold Standard bills are the foundation for our annual Liberty Rating report card.")

    _style_page.set_background(color='#dab600')
    _style_footer.set_background(color='#000000')
    self.document.insert_style(_style_page, automatic = True)
    self.document.insert_style(_style_master)
    self.document.insert_style(_style_footer)
     
    _style_master.set_footer(p)

  def Set_Bills(self, Bill_List):
    self.bill_table=odf_create_table(u"Bill Table",width=2, height=len(Bill_List)*3)
    body=document.get_body()
    body.append(self.bill_table)
    row=0
    for Bill in Bill_List:
      self.bill_table.set_cell(coord=(row,0), value=Bill.Number + ', ' + Bill.Title)
      self.bill_table.set_cell(coord=(row,1), value=Bill.Number)
      row++
      self.bill_table.set_cell(coord=(row,0), value=Bill.Committee + 'Recommendation:' + Bill.Committee_Vote)
      row++
      self.bill_table.set_cell(coord=(row,0), value=Bill.Liberty_Type + ':' + Bill.NHLA_Summary)
      self.bill_table.set_cell(coord=(row,1), value=Bill.NHLA_Recommendation)
      row++
      self.bill_table.set_cell(coord=(row,0), value=Bill.GS_Blurb)

 
  def save(self, name):
    self.document.save(target=name) 
