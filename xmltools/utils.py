from typing import Optional, Tuple

from lxml import etree


def check_syntax(
        xml_file: str
) -> Tuple[bool, Optional[str], Optional[str], Optional[etree.ElementTree]]:

    # clear global error log for lxml
    etree.clear_error_log()

    # parse xml
    try:
        doc = etree.parse(xml_file)
        return (True, None, None, doc)

    except IOError:
        return (False, 'IO', 'Invalid File', None)

    except etree.XMLSyntaxError as err:
        return (False, 'Syntax', str(err.error_log), None)  #pylint: disable=no-member


def trim_xml(xml_file_in: str, xml_file_out: str
             ) -> Tuple[bool, Optional[str], Optional[etree.ElementTree]]:

    # clear global error log for lxml
    etree.clear_error_log()

    parser = etree.XMLParser(remove_blank_text=True)

    try:
        doc = etree.parse(xml_file_in, parser)

    except IOError:
        return (False, 'IO', None)

    except etree.XMLSyntaxError:
        return (False, 'Syntax', None)

    try:
        with open(xml_file_out, 'wb') as f:
            f.write(
                etree.tostring(
                    doc.getroot(), pretty_print=True, encoding='UTF-8'))
        return (True, None, doc)

    except IOError:
        return (False, 'IO', None)


def validate_xml(xml_doc: etree.ElementTree,
                 xsd_file: str) -> Tuple[bool, Optional[str], Optional[str]]:

    # clear global error log for lxml
    etree.clear_error_log()

    try:
        xmlschema_doc = etree.parse(xsd_file)
        xmlschema = etree.XMLSchema(xmlschema_doc)

    except IOError:
        return (False, 'IO', 'XSD file I/O error')

    except etree.XMLSyntaxError as err:
        return (False, 'Syntax', str(err.error_log))  #pylint: disable=no-member

    try:
        xmlschema.assertValid(xml_doc)
        return (True, None, None)

    except etree.DocumentInvalid as err:
        return (False, 'Schema', str(err.error_log))  #pylint: disable=no-member
