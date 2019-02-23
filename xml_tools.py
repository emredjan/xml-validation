"""
GUI app for XML tools
"""

import sys
from pathlib import Path

import wx

from xmltools import utils

WILDCARD_XML = "XML files (*.xml)|*.xml|" \
            "All files (*.*)|*.*"

WILDCARD_XSD = "XSD files (*.xsd)|*.xsd|" \
            "All files (*.*)|*.*"

WILDCARD_ALL = "All files (*.*)|*.*"

PANEL_SIZE = (800, 600)

BUTTON_SIZE = (120, 25)
TEXTBOX_SIZE = (650, 22)

COLOR_OK = (0, 175, 0)
COLOR_ER = (175, 0, 0)


class MainForm(wx.Frame):
    """
    Main class for the application
    """

    def __init__(self):

        wx.Frame.__init__(
            self,
            None,
            title='XML Tools',
            size=PANEL_SIZE,
            style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX
            | wx.CLIP_CHILDREN)

        self.init_ui()

    def init_ui(self):
        """
        Initialize the user interface
        """

        panel = wx.Panel(self, wx.ID_ANY)
        self.current_dir = Path.cwd()
        self.current_xml = None
        self.current_xsd = None
        self.xml_doc = None

        # create the buttons and bindings

        sizer = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.xml_file_txt = wx.TextCtrl(panel, size=TEXTBOX_SIZE)
        self.xml_file_txt.Bind(wx.EVT_TEXT, self.on_change_xml)
        self.current_xml = self.xml_file_txt.GetValue()
        open_xml_btn = wx.Button(
            panel, label='Select XML File..', size=BUTTON_SIZE)
        open_xml_btn.Bind(wx.EVT_BUTTON, self.on_open_xml)
        hbox1.Add(self.xml_file_txt, 0, wx.ALL | wx.CENTER, 5)
        hbox1.Add(open_xml_btn, 0, wx.ALL | wx.CENTER, 5)
        sizer.Add(
            hbox1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=5)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.xsd_file_txt = wx.TextCtrl(panel, size=TEXTBOX_SIZE)
        self.xsd_file_txt.Bind(wx.EVT_TEXT, self.on_change_xsd)
        open_xsd_btn = wx.Button(
            panel, label='Select XSD File..', size=BUTTON_SIZE)
        open_xsd_btn.Bind(wx.EVT_BUTTON, self.on_open_xsd)
        hbox2.Add(self.xsd_file_txt, 0, wx.ALL | wx.CENTER, 5)
        hbox2.Add(open_xsd_btn, 0, wx.ALL | wx.CENTER, 5)
        sizer.Add(
            hbox2, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=5)

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        tool_stx_btn = wx.Button(panel, label='Check Syntax', size=BUTTON_SIZE)
        tool_stx_btn.Bind(wx.EVT_BUTTON, self.on_syntax)
        self.tool_stx_result = wx.StaticText(
            panel, label='', size=TEXTBOX_SIZE)
        hbox3.Add(tool_stx_btn, 0, wx.ALL | wx.CENTER, 5)
        hbox3.Add(self.tool_stx_result, 0, wx.TOP | wx.LEFT | wx.CENTER, 7)
        sizer.Add(
            hbox3, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=5)

        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        tool_trim_btn = wx.Button(
            panel, label='Trim / Format XML', size=BUTTON_SIZE)
        tool_trim_btn.Bind(wx.EVT_BUTTON, self.on_trim)
        self.tool_trim_result = wx.StaticText(
            panel, label='', size=TEXTBOX_SIZE)
        hbox4.Add(tool_trim_btn, 0, wx.ALL | wx.CENTER, 5)
        hbox4.Add(self.tool_trim_result, 0, wx.TOP | wx.LEFT | wx.CENTER, 7)
        sizer.Add(
            hbox4, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=5)

        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        tool_vld_btn = wx.Button(
            panel, label='Validate with XSD', size=BUTTON_SIZE)
        tool_vld_btn.Bind(wx.EVT_BUTTON, self.on_validate)
        self.tool_vld_result = wx.StaticText(
            panel, label='', size=TEXTBOX_SIZE)
        hbox5.Add(tool_vld_btn, 0, wx.ALL | wx.CENTER, 5)
        hbox5.Add(self.tool_vld_result, 0, wx.TOP | wx.LEFT | wx.CENTER, 7)
        sizer.Add(
            hbox5, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=5)

        self.error_details = wx.TextCtrl(
            panel, style=wx.TE_MULTILINE | wx.TE_DONTWRAP | wx.TE_READONLY)
        sizer.Add(self.error_details, 1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        hbox6 = wx.BoxSizer(wx.HORIZONTAL)
        save_ed_btn = wx.Button(
            panel, label='Save Error Details', size=BUTTON_SIZE)
        save_ed_btn.Bind(wx.EVT_BUTTON, self.on_save_error)
        self.save_ed_result = wx.StaticText(panel, label='', size=TEXTBOX_SIZE)
        hbox6.Add(save_ed_btn, 0, wx.ALL | wx.CENTER, 5)
        hbox6.Add(self.save_ed_result, 0, wx.TOP | wx.LEFT | wx.CENTER, 7)
        sizer.Add(
            hbox6, flag=wx.EXPAND | wx.ALL, border=5)

        panel.SetSizer(sizer)

    def on_open_xml(self, event): #pylint: disable=unused-argument
        """
        Create and show the Open FileDialog
        """
        dlg = wx.FileDialog(
            self,
            message="Choose a file",
            defaultDir=str(self.current_dir),
            defaultFile="",
            wildcard=WILDCARD_XML,
            style=wx.FD_OPEN | wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.xml_file_txt.SetValue(path)

        dlg.Destroy()

    def on_open_xsd(self, event): #pylint: disable=unused-argument
        """
        Create and show the Open FileDialog
        """
        dlg = wx.FileDialog(
            self,
            message="Choose a file",
            defaultDir=str(self.current_dir),
            defaultFile="",
            wildcard=WILDCARD_XSD,
            style=wx.FD_OPEN | wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.xsd_file_txt.SetValue(path)
        dlg.Destroy()

    def on_change_xml(self, event): #pylint: disable=unused-argument

        self.current_xml = Path(self.xml_file_txt.GetValue())
        self.xml_doc = None

    def on_change_xsd(self, event): #pylint: disable=unused-argument

        self.current_xsd = Path(self.xsd_file_txt.GetValue())

    def on_syntax(self, event): #pylint: disable=unused-argument

        if not self.current_xml:
            self.tool_stx_result.SetForegroundColour(COLOR_ER)
            self.tool_stx_result.SetLabel('Select an XML file above.')
            return
        elif not self.current_xml.exists():
            self.tool_stx_result.SetForegroundColour(COLOR_ER)
            self.tool_stx_result.SetLabel('File I/O error, check path!')
            self.error_details.ChangeValue('')
            return

        syntax_ok, error_type, error_log, self.xml_doc = utils.check_syntax(
            str(self.current_xml))

        if syntax_ok:
            self.tool_stx_result.SetForegroundColour(COLOR_OK)
            self.tool_stx_result.SetLabel('XML well formed, syntax ok.')
            self.error_details.ChangeValue('')
        else:
            if error_type == 'IO':
                self.tool_stx_result.SetForegroundColour(COLOR_ER)
                self.tool_stx_result.SetLabel('File I/O error, check path!')
                self.error_details.ChangeValue('')
            elif error_type == 'Syntax':
                self.tool_stx_result.SetForegroundColour(COLOR_ER)
                self.tool_stx_result.SetLabel(
                    'XML syntax error, check below for details!')
                self.error_details.ChangeValue(error_log)

    def on_trim(self, event): #pylint: disable=unused-argument

        if not self.current_xml:
            self.tool_trim_result.SetForegroundColour(COLOR_ER)
            self.tool_trim_result.SetLabel('Select an XML file above.')
            return
        elif not self.current_xml.exists():
            self.tool_trim_result.SetForegroundColour(COLOR_ER)
            self.tool_trim_result.SetLabel('File I/O error, check file path!')
            self.error_details.ChangeValue('')
            return

        dlg = wx.FileDialog(
            self,
            message="Choose where to save the trimmed file",
            defaultDir=str(self.current_dir),
            defaultFile="",
            wildcard=WILDCARD_XML,
            style=wx.FD_SAVE | wx.FD_CHANGE_DIR | wx.FD_OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            xml_out = Path(dlg.GetPath())
        else:
            return

        dlg.Destroy()

        trim_ok, error_type, self.xml_doc = utils.trim_xml(
            str(self.current_xml), str(xml_out))

        if trim_ok:
            self.tool_trim_result.SetForegroundColour(COLOR_OK)
            self.tool_trim_result.SetLabel('Trimmed file written as: ' +
                                           xml_out.name)
            self.error_details.ChangeValue('')
        else:
            if error_type == 'IO':
                self.tool_trim_result.SetForegroundColour(COLOR_ER)
                self.tool_trim_result.SetLabel(
                    'File I/O error, check file paths!')
                self.error_details.ChangeValue('')
            elif error_type == 'Syntax':
                self.tool_trim_result.SetForegroundColour(COLOR_ER)
                self.tool_trim_result.SetLabel(
                    'XML syntax error, check syntax first for details!')
                self.error_details.ChangeValue('')

    def on_validate(self, event): #pylint: disable=unused-argument

        if (not self.current_xml) or (not self.current_xsd):
            self.tool_vld_result.SetForegroundColour(COLOR_ER)
            self.tool_vld_result.SetLabel('Select an XML and an XSD file above.')
            return
        elif (not self.current_xml.exists()) or (not self.current_xsd.exists()):
            self.tool_vld_result.SetForegroundColour(COLOR_ER)
            self.tool_vld_result.SetLabel('File I/O error, check file paths!')
            self.error_details.ChangeValue('')
            return

        if not self.xml_doc:
            self.tool_vld_result.SetForegroundColour(COLOR_ER)
            self.tool_vld_result.SetLabel(
                'Check / correct syntax before validating!')
            self.error_details.ChangeValue('')
            return

        schema_ok, error_type, error_log = utils.validate_xml(
            self.xml_doc, str(self.current_xsd))

        if schema_ok:
            self.tool_vld_result.SetForegroundColour(COLOR_OK)
            self.tool_vld_result.SetLabel('XML valid, schema validation ok.')
            self.error_details.ChangeValue('')
        else:
            if error_type == 'IO':
                self.tool_vld_result.SetForegroundColour(COLOR_ER)
                self.tool_vld_result.SetLabel(
                    'File I/O error, check file paths!')
                self.error_details.ChangeValue('')
            elif error_type == 'Syntax':
                self.tool_vld_result.SetForegroundColour(COLOR_ER)
                self.tool_vld_result.SetLabel(
                    'XSD syntax error, check below for details!')
                self.error_details.ChangeValue(error_log)
            elif error_type == 'Schema':
                self.tool_vld_result.SetForegroundColour(COLOR_ER)
                self.tool_vld_result.SetLabel(
                    'Schema validation error, check below for details!')
                self.error_details.ChangeValue(error_log)

    def on_save_error(self, event): #pylint: disable=unused-argument

        results = self.error_details.GetValue()

        if not results:
            self.save_ed_result.SetForegroundColour(COLOR_ER)
            self.save_ed_result.SetLabel('There\'s nothing to save!')
            return

        dlg = wx.FileDialog(
            self,
            message="Choose where to save the error results",
            defaultDir=str(self.current_dir),
            defaultFile='error_details.log',
            wildcard=WILDCARD_ALL,
            style=wx.FD_SAVE | wx.FD_CHANGE_DIR | wx.FD_OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            ed_file = Path(dlg.GetPath())
        else:
            return

        dlg.Destroy()

        try:
            with open(ed_file, 'w') as f:
                f.write(results)
            self.save_ed_result.SetForegroundColour(COLOR_OK)
            self.save_ed_result.SetLabel('Error details written as: ' +
                                           ed_file.name)
        except IOError:
            self.save_ed_result.SetForegroundColour(COLOR_ER)
            self.save_ed_result.SetLabel(
                'File I/O error, check file paths!')


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """

    parent_dir = Path(__file__).absolute().parent
    base_path = Path(getattr(sys, '_MEIPASS', str(parent_dir)))

    return str(base_path / relative_path)

# Run the program
if __name__ == "__main__":
    app = wx.App(False)
    frame = MainForm()
    frame.SetIcon(wx.Icon(resource_path('xml_tools.ico')))
    frame.Show()
    app.MainLoop()
