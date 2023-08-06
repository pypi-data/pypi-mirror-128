# HEADER
#                      arg/Backend/argBackendBase.py
#               Automatic Report Generator (ARG) v. 1.0
#
# Copyright 2020 National Technology & Engineering Solutions of Sandia, LLC
# (NTESS). Under the terms of Contract DE-NA0003525 with NTESS, the U.S.
# Government retains certain rights in this software.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from this
#   software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Questions? Visit gitlab.com/AutomaticReportGenerator/arg
#
# HEADER

import abc
import datetime
from abc import ABC
from html.parser import HTMLParser
from math import sqrt
import os
import shutil
import sys

import yaml

from arg.Common.argInformationObject import argInformationObject
from arg.Common.argMultiFontStringHelper import argMultiFontStringHelper
from arg.Aggregation import argExodusAggregator, argVTKSTLAggregator


class argBackendBase:
    """A backend abstractbase class
    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, parameters=None):

        # Backend type to be provided by concrete subclasses
        self.Type = None

        # Keep track of specified report parameters
        self.Parameters = parameters

        # Internal storage for the report
        self.Report = None

        # Load supported types
        common_dir = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(common_dir, "../Common/argTypes.yml"),
                  'r',
                  encoding="utf-8") as t_file:
            self.Types = yaml.safe_load(t_file)

        # Retrieve supported verbosity levels
        self.VerbosityLevels = self.Types.get("VerbosityLevels", {})

        # Retrieve supported templates information
        self.Templates = self.Types.get("TemplateFiles", {})

    def get_type(self):
        """Convenience method to get backend type
        """

        # Return value of instance variable
        return self.Type

    def get_caption_extension(self):
        """Convenience method to get caption file extension for backend
        """

        # Return value of instance variable
        return argMultiFontStringHelper.Types.get("BackendTypes", {}).get(self.Type, {}).get("captions", '')

    @staticmethod
    def get_timestamp():
        """Convenience method to get timestamp under unified format
        """

        # Return value of instance variable
        return datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d, %H:%M:%S")

    def create_document_preamble(self, version=None):
        """Must be overwritten if concrete backend needs a preamble
        """

        # No default preamble is provided
        return

    def add_document_provenance(self, version=None):
        """Must be overwritten if concrete backend needs a document timestamp
        Add document provenance information on a new page
        """

        # No default preamble is provided
        return

    def add_document_tocs(self, version=None):
        """Must be overwritten if concrete backend needs Table of Contents, List of Figures and List of Tables
        Add document Table of Contents, List of Figures and List of Tables on new pages
        """

        # No default preamble is provided
        return

    def append_document_postamble(self):
        """Must be overwritten if concrete backend needs a postamble
        """

        # No default postamble is provided
        return

    @abc.abstractmethod
    def generate_multi_font_string(self, multi_font_string, handle=None):
        """Generate backend-end specific artifact for multi-font string
        """

    @abc.abstractmethod
    def generate_matrix_string(self, matrix):
        """Generate back-end specific string from matrix entries
        """

    @abc.abstractmethod
    def add_comment(self, comments_dict, key):
        """Add comment to the report from a dict as either text string
        or as sub-paragraph depending on number of dict values (1 or 2)
        """

    @abc.abstractmethod
    def add_paragraph(self, item):
        """Add paragraph to the report
        """

    @abc.abstractmethod
    def add_list(self, item, number_items=False):
        """Add itemization or enumeration to the report
        """

    @abc.abstractmethod
    def add_subsection(self, item, numbered=True):
        """Add subsection to the report
        """

    @abc.abstractmethod
    def add_subsubsection(self, item, numbered=True):
        """ Add sub-subsection to the report
        """

    @abc.abstractmethod
    def add_section(self, item, numbered=True):
        """Add section to the report
        """

    @abc.abstractmethod
    def add_chapter(self, item, numbered=True):
        """Add chapter to the report
        """

    @abc.abstractmethod
    def add_page_break(self):
        """Add page break to the report
        """

    @abc.abstractmethod
    def add_color_table(self, data: dict) -> None:
        """ Add colored table to the report
        """

    @abc.abstractmethod
    def add_table(self, header, body, do_verbatim, position):
        """Add table to the report
        """

    @abc.abstractmethod
    def add_figure(self, arguments):
        """Add figure to the report
        """

    @abc.abstractmethod
    def recursively_build_report(self, structure_tree):
        """Recursively navigate tree sructure to build report
        """

    @abc.abstractmethod
    def assemble(self, report_map, version=None, latex_proc=None):
        """Create a report possibly including assembler version
        """

        # Early exit if report map empty
        if not report_map:
            print("** ERROR: No content is available to populate report. Exiting")
            sys.exit(1)

        elif not "chapters" in report_map:
            print("** ERROR: Chapters are not defined in provided structure file. Exiting")
            sys.exit(1)

    def add_meta_information(self, item):
        """Add meta-information about data to the report
        """

        # Retrieve required parameters
        data_type = item["datatype"]
        data_set = item["dataset"]

        # Retrieve or assign optional verbosity parameter
        verbosity = self.VerbosityLevels.get("default")

        # Assemble data base name
        datafile = os.path.join(self.Parameters.DataDir, data_set)

        # Retrieve meta-information
        data = self.Parameters.DataFactory(
            data_type, datafile, item.get("parameters", {}))
        meta_info = data.get_meta_information()

        # Break out early if no meta-information was retrieved
        if not meta_info or not len(meta_info):
            print("*  WARNING: No meta-information for {} type available in {}".format(
                data_type, data_set))
            return

        # Generate meta-data for key/value files
        if data_type == "key-value":
            # Create table header with file name as first column
            name_str = "file name"
            other_cols = [k for k in meta_info[0] if k != name_str]
            header_list = [name_str] + other_cols

            # Create table body
            body_dict = {}
            for m in meta_info:
                key = m.get(name_str)

                # Ensure consistency of meta-information across accessors
                if not key or other_cols != [k for k in m if k != name_str]:
                    print("*  WARNING: Inconsistent meta-information for {}. Ignoring dataset {}".format(
                        data_type, data_set))
                    return

                # Update table body
                body_dict[key] = [m.get(c) for c in other_cols]

            caption_string = argMultiFontStringHelper(self)
            caption_string.append("Meta-information of ", 0)
            data_extension = item.get("parameters", {}).get("extension")
            if data_extension:
                caption_string.append(" all files with extension ", 0)
                caption_string.append(data_extension, 4)
                caption_string.append(" in data directory.", 0)
            else:
                caption_string.append(data_set, 4)
            caption_string.append(".", 0)
            self.add_table(
                header_list,
                body_dict,
                caption_string,
                True)

        # Generate meta-data for HDF5 file
        if data_type == "HDF5":
            # Iterate over per-file meta-information entries
            for m in meta_info:
                # Create caption string
                caption_string = argMultiFontStringHelper(self)
                caption_string.append("Meta-information of ", 0)
                caption_string.append(data_set, 4)

                # Generate meta-information table
                self.add_table(
                    ["property", "value"],
                    {k: ["{}".format(v)] for k, v in m.items() if k != "file name"},
                    caption_string, False)

        # Generate meta-data for Exodus mesh
        elif data_type == "ExodusII":
            # Retrieve base name of file
            file_name = os.path.basename(datafile)

            # Eliminate final extension if file name is that of a partition
            if len(meta_info) > 1:
                file_name = os.path.splitext(file_name)[0]

            # Create table of topological properties
            header_list, body_dict = data.summarize(type="topology")
            caption_string = argMultiFontStringHelper(self)
            caption_string.append("Topological properties of ", 0)
            caption_string.append(file_name, 4)
            self.add_table(header_list, body_dict, caption_string, True)

            # Create table of mesh blocks if requested and at least one exists
            if verbosity > self.VerbosityLevels.get("terse"):
                header_list, body_dict = data.summarize(type="blocks")
                if header_list:
                    caption_string.clear()
                    caption_string.append("Element blocks of ", 0)
                    caption_string.append(file_name, 4)
                    self.add_table(header_list, body_dict, caption_string, True)

            # Create table of node and side sets if requested and at least one exists
            if verbosity > self.VerbosityLevels.get("terse"):
                for set_type in ("node", "side"):
                    header_list, body_dict = data.summarize(type="sets", set_type=set_type)
                    if header_list:
                        caption_string.clear()
                        caption_string.append(set_type.title(), 0)
                        caption_string.append(" sets of ", 0)
                        caption_string.append(file_name, 4)
                        self.add_table(header_list, body_dict, caption_string, True)

            # Create table of variables if some are present
            header_list, body_list = data.summarize(type="variable")
            if body_list:
                caption_string.clear()
                caption_string.append("Variables of ", 0)
                caption_string.append(file_name, 4)
                self.add_table(header_list, body_list, caption_string, True)

    def add_information(self, item):
        """Add information about given property to report and
           restrict information to specific items if provided
        """

        # Unpack property request and bail out early if empty
        property_request = item["property_request"]
        if not property_request:
            return

        # Retrieve request parameters
        data_type = item["datatype"]
        data_set = item["dataset"]

        # At least one data property was requested
        prop_type = property_request[0]
        prop_items = property_request[1:]

        # Assemble data base name and instantiate reader
        datafile = os.path.join(self.Parameters.DataDir, data_set)
        data = self.Parameters.DataFactory(
            data_type, datafile, item.get("parameters", {}))

        # Retrieve information for given property
        prop_info = data.get_property_information(prop_type, prop_items)

        # If no property values were found report it and break out
        if not prop_info:
            # Report missing values for property type
            multi_font_string = argMultiFontStringHelper(self)
            multi_font_string.append("No values for ", 0)
            p_items = False
            for p in prop_items:
                # Report missing values for property items
                if p_items:
                    multi_font_string.append(", ", 0)
                p_items = True
                multi_font_string.append(p, 4)
            if p_items:
                multi_font_string.append(" items of ", 0)
            multi_font_string.append(prop_type, 4)
            multi_font_string.append(" property were found.", 0)
            self.add_paragraph({"string": multi_font_string})

            # Do not add anything else when values are missing
            return

        # Some specific items were requested, build a summary table
        elif isinstance(prop_info, argInformationObject):
            # Create tables depending on information type
            prop_info_type = prop_info.get_type()

            # Handle dictionary of lists of values
            if prop_info_type == "arg_dict_lists_lists":
                # Create header common to all tables
                tab_head = []
                for p_name in prop_info.get_names():
                    multi_font_string = argMultiFontStringHelper(self)
                    multi_font_string.append(p_name, 4)
                    tab_head.append(multi_font_string)

                # Iterate over property object items
                for info_key, info_value in prop_info.iterator():
                    multi_font_string = argMultiFontStringHelper(self)
                    if prop_type:
                        multi_font_string.append("Values of ", 0)
                        multi_font_string.append(prop_type, 4)
                        multi_font_string.append(" property for ", 0)
                    else:
                        multi_font_string.append("Values for ", 0)
                    multi_font_string.append(info_key, 4)
                    multi_font_string.append(".", 0)
                    self.add_table(
                        tab_head,
                        info_value,
                        multi_font_string,
                        True)

            # Unsupported type of information object
            else:
                print("*  WARNING: informtation type {} not supported by backend.".format(
                    prop_info_type))
                return

        # Some specific items were requested, build a summary table
        elif prop_items and isinstance(prop_info, dict):
            # Create table for property items only if needed
            tab_head = [argMultiFontStringHelper(self)]
            tab_head[0].append(prop_type, 4)
            tab_head += [argMultiFontStringHelper(self)
                         for _ in prop_items]
            for p in prop_items:
                tab_head.append(p)
            multi_font_string = argMultiFontStringHelper(self)
            multi_font_string.append("Values of ", 0)
            multi_font_string.append(prop_type, 4)
            multi_font_string.append(" properties.", 0)
            self.add_table(
                tab_head,
                dict(prop_info),
                multi_font_string,
                True)

        # No specific item required, build many tables
        else:
            # Iterate over of properties information list
            for props in prop_info:
                # Skip void entries
                if not props:
                    continue

                # Handle list-based properties
                if isinstance(props, list) and len(props) > 2:
                    prop_item = props[0]
                    prop_values = props[1]
                    if prop_item and prop_values and isinstance(prop_values, dict):
                        tab_head = [argMultiFontStringHelper(self),
                                    argMultiFontStringHelper(self)]
                        tab_head[0].append(prop_type, 4)
                        tab_head[1].append(prop_item, 4)
                        multi_font_string = argMultiFontStringHelper(self)
                        multi_font_string.append("Values of ", 0)
                        multi_font_string.append(prop_item, 4)
                        multi_font_string.append(" for property ", 0)
                        multi_font_string.append(prop_type, 4)
                        multi_font_string.append('.', 0)
                        self.add_table(
                            tab_head,
                            list(prop_values.items()),
                            multi_font_string,
                            True)

    def add_aggregation(self, item):
        """Add information aggregated from various backends
        """

        # Choose aggregator depending on data type
        data_type = item.get("datatype")
        if data_type == "ExodusII":
            # Instantiate ExodusII aggregator on self and execute it
            aggregator = argExodusAggregator.argExodusAggregator(self, item)
            aggregator.aggregate()
        elif data_type == "vtkSTL":
            # Instantiate vtkSNL aggregator on self and execute it
            aggregator = argVTKSTLAggregator.argVTKSTLAggregator(self, item)
            aggregator.aggregate()
        else:
            # Unsupported data type
            print("[argBackendBase] Unknown aggregation data type: {}")

    def fetch_image_and_caption(self, arguments):
        """Retrieve image and associated caption for figure creation
        """

        # A figure file is required
        figure_file = arguments.get("figure_file")
        if not figure_file:
            print("*  WARNING: no figure file name was provided.")
            return None, None

        # Determine path and file names
        figure_file_name = os.path.basename(figure_file)

        # Ensure that image file is present in output directory
        img_file = os.path.join(self.Parameters.OutputDir,
                                figure_file_name)
        if not os.path.isfile(img_file):
            # Ensure that destination directory exists
            if not os.path.exists(self.Parameters.OutputDir):
                os.makedirs(self.Parameters.OutputDir)

            # Try to copy image file from data directory
            try:
                shutil.copyfile(
                    os.path.join(self.Parameters.DataDir, figure_file),
                    img_file)
                # Could not copy picture file
            except IOError:
                print("*  WARNING: could find image file {} neither in {} nor {}. Ignoring figure.".format(
                    figure_file_name,
                    self.Parameters.DataDir,
                    self.Parameters.OutputDir))
                return None, None

        # Retrieve caption string when it is specified
        caption_string = arguments.get("caption_string")
        from_file = None
        if not caption_string:
            # Otherwise try to retrieve caption from file
            caption_file = arguments.get("caption_file")
            if caption_file:
                # Try to fetch caption string first from data then output directories
                for d in (
                        self.Parameters.DataDir,
                        self.Parameters.OutputDir):
                    try:
                        with open(os.path.join(d, caption_file), 'r') as f:
                            caption_string = f.read()
                            from_file = True
                            break
                    except IOError:
                        continue
                else:  # for d in target_dirs
                    print("*  WARNING: could find caption file {} in neither {} nor {}.".format(
                        caption_file,
                        self.Parameters.DataDir,
                        self.Parameters.OutputDir))
                    caption_string = ''

        # Return retrieve image file name
        return figure_file_name, caption_string, from_file

    def parse_headers(self, headers: list) -> list:
        """ Parses headers for color-table
        """
        ccp = self._CELL_PROPS
        headers_list = [(cell.get(ccp[0], ''), cell.get(ccp[1], ''), cell.get(ccp[2], ''), cell.get(ccp[3], ''),
                         cell.get(ccp[4], '')) for cell in headers]
        return headers_list

    def parse_rows(self, rows: list, table_columns_num: int) -> list:
        """ Parses rows for color-table
        """
        rows_list = list()
        ccp = self._CELL_PROPS
        for row in rows:
            row_list = [(cell.get(ccp[0], ''), cell.get(ccp[1], ''), cell.get(ccp[2], ''), cell.get(ccp[3], ''),
                         cell.get(ccp[4], '')) for cell in row]
            if len(row) == table_columns_num:
                rows_list.append(row_list)
            elif len(row) < table_columns_num:
                empty_cells = [('', '', '', '', '') for _ in range(table_columns_num - len(row))]
                row_list.extend(empty_cells)
                rows_list.append(row_list)
            else:
                raise Exception('Too many columns in a row!')
        return rows_list

    _CELL_PROPS = {0: 'value', 1: 'background-color', 2: 'foreground-color', 3: 'horizontal-alignment',
                   4: 'vertical-alignment'}

    @staticmethod
    def nesting_html_list(html_list: list) -> list:
        """
        Function takes html_list which is a representation of HTML document and returns nested list which corresponds to
        document structure.
        """
        nested_list = list()
        current_list = list()
        nested_active = 0
        for pos in html_list:
            if pos[0].startswith('_!') and pos[0].endswith('!_'):
                if nested_active == 0:
                    current_list = list()
                nested_active += 1
                if pos[1]:
                    current_list.append(pos[0][2:-2])
                    current_list.append({'attrs': pos[1]})
                else:
                    current_list.append(pos[0][2:-2])
            elif pos[0].startswith('!__') and pos[0].endswith('__!'):
                current_list.append({pos[0][3:-3]: pos[1]})
            elif pos[0].startswith('__!') and pos[0].endswith('!__'):
                nested_active -= 1
                if nested_active == 0:
                    nested_list.append(current_list)

        return nested_list

    def map_nested_list_to_amfsh(self, nested_list: list) -> list:
        """ Iterates over nested list and returns a final list which consists information needed to be put into Word
            document.
        """
        returned_list = list()
        tags = {'h1': {'font': 9}, 'h2': {'font': 10}, 'h3': {'font': 11}, 'h4': {'font': 12}, 'h5': {'font': 13},
                'h6': {'font': 14}}
        for html_tag in nested_list:
            amfsh = argMultiFontStringHelper()
            alignment = 'LEFT'
            indent = None
            attrs = None
            string = ''
            # Support case for headings from h1 to h6
            if html_tag[0] in tags.keys():
                if len(html_tag) == 2 and html_tag[1].get('data', None) is not None:
                    string = html_tag[1].get('data', None)
                    attrs = None
                elif len(html_tag) == 3:
                    if html_tag[1].get('data', None) is None:
                        string = html_tag[2].get('data', None)
                        attrs = html_tag[1].get('attrs', None)
                color = None
                highlight_color = None
                if attrs is not None:
                    attrs = self.decode_attrs(attrs=attrs)
                    color = attrs.get('color', None)
                    highlight_color = attrs.get('highlight_color', None)
                    if attrs.get('alignment', None) is not None:
                        alignment = attrs.get('alignment', None)
                    if attrs.get('margin-left', None) is not None:
                        indent = ['margin-left', attrs.get('margin-left', None)]
                    elif attrs.get('margin-right', None) is not None:
                        indent = ['margin-right', attrs.get('margin-right', None)]
                amfsh.append(string=string, font=tags.get(html_tag[0]).get('font'), color=color,
                             highlight_color=highlight_color)
                returned_list.append((alignment, amfsh, indent))
            # Support case for Paragraph
            elif html_tag[0] == 'p':
                font = 0
                color = None
                highlight_color = None
                attrs = None
                for elem in html_tag:
                    if isinstance(elem, str):
                        font_map = {'p': 0, 'u': 3, 'strong': 2, 'em': 1, 's': 5, 'span': 0, 'sub': 6}
                        font = font_map.get(elem, 0)
                    elif isinstance(elem, dict) and elem.get('attrs', None) is not None:
                        attrs = self.decode_attrs(attrs=elem.get('attrs'))
                        color = attrs.get('color', None)
                        highlight_color = attrs.get('highlight_color', None)
                        if attrs.get('alignment', None) is not None:
                            alignment = attrs.get('alignment', None)
                        if attrs.get('margin-left', None) is not None:
                            indent = ['margin-left', attrs.get('margin-left', None)]
                        elif attrs.get('margin-right', None) is not None:
                            indent = ['margin-right', attrs.get('margin-right', None)]
                    elif isinstance(elem, dict) and elem.get('data', None) is not None:
                        string = elem.get('data')
                        amfsh.append(string=string, font=font, color=color, highlight_color=highlight_color)
                        font = 0
                        color = None
                        highlight_color = None
                        attrs = None
                returned_list.append((alignment, amfsh, indent))
            # Supports case for Ordered/Unordered lists
            elif html_tag[0] == 'ul' or html_tag[0] == 'ol':
                list_list = list()
                list_type = None
                cur_list_word = None
                font = 0
                for elem in html_tag:
                    if isinstance(elem, str) and bool(elem == 'ul' or elem == 'ol'):
                        list_map = {'ul': 'List Bullet', 'ol': 'List Number'}
                        list_type = list_map.get(elem, None)
                    elif isinstance(elem, str) and elem == 'li':
                        cur_list_word = list()
                    elif isinstance(elem, dict) and elem.get('attrs', None) is not None:
                        attrs = self.decode_attrs(attrs=elem.get('attrs'))
                        color = attrs.get('color', None)
                        highlight_color = attrs.get('highlight_color', None)
                        if attrs.get('alignment', None) is not None:
                            alignment = attrs.get('alignment', None)
                        if attrs.get('margin-left', None) is not None:
                            indent = ['margin-left', attrs.get('margin-left', None)]
                        elif attrs.get('margin-right', None) is not None:
                            indent = ['margin-right', attrs.get('margin-right', None)]
                    elif isinstance(elem, dict) and elem.get('data', None) is not None:
                        string = elem.get('data')
                        amfsh = argMultiFontStringHelper()
                        amfsh.append(string=string, font=font, color=color, highlight_color=highlight_color)
                        cur_list_word = [alignment, amfsh, indent, list_type]
                        list_list.append(cur_list_word)
                returned_list.append(list_list)
        return returned_list

    @staticmethod
    def decode_attrs(attrs: list) -> dict:
        """ Decodes attrs list and returns a dict with more Word applicable form. """
        attrs_dict = dict()
        for attr in attrs:
            if attr[0] == 'style':
                attr_list = attr[1].split(':')
                if attr_list[0] == 'color':
                    color_hex = attr_list[1].replace('#', '')
                    r, g, b = str(int(color_hex[0:2], 16)), str(int(color_hex[2:4], 16)), str(int(color_hex[4:6], 16))
                    attrs_dict['color'] = ','.join([r, g, b])
                elif attr_list[0] == 'background-color':
                    attrs_dict['highlight_color'] = attr_list[1]
                elif attr_list[0] == 'text-align':
                    attrs_dict['alignment'] = attr_list[1].upper()
                elif attr_list[0] == 'margin-left':
                    attrs_dict['margin-left'] = int(attr_list[1].replace('px', ''))
                elif attr_list[0] == 'margin-right':
                    attrs_dict['margin-right'] = int(attr_list[1].replace('px', ''))
        return attrs_dict

    @staticmethod
    def get_closest_color(hex_str: str) -> str:
        """ Takes hex color definition. Returns a key (color name) as string.
            :param str hex_str: Just a string (text) to be added
        """
        colors = {(255.0, 255.0, 255.0): 'AUTO', (0.0, 0.0, 0.0): 'BLACK', (0.0, 0.0, 255.0): 'BLUE',
                  (0.0, 255.0, 0.0): 'BRIGHT_GREEN', (0.0, 0.0, 139.0): 'DARK_BLUE', (139.0, 0.0, 0.0): 'DARK_RED',
                  (204.0, 204.0, 0.0): 'DARK_YELLOW', (192.0, 192.0, 192.0): 'GRAY_25', (255.0, 0.0, 0.0): 'RED',
                  (128.01, 128.01, 128.01): 'GRAY_50', (0.0, 127.5, 0.0): 'GREEN', (255.0, 150.0, 180.0): 'PINK',
                  (0.0, 128.01, 128.01): 'TEAL', (64.0, 224.0, 208.0): 'TURQUOISE', (199.0, 20.0, 133.0): 'VIOLET',
                  (255.0, 255.0, 255.0): 'WHITE', (255.0, 255.0, 0.0): 'YELLOW'}
        color_hex = hex_str.replace('#', '')
        r, g, b = int(color_hex[0:2], 16), int(color_hex[2:4], 16), int(color_hex[4:6], 16)
        color_diffs = []
        for color, color_name in colors.items():
            cr, cg, cb = color
            color_diff = sqrt(abs(r - cr) ** 2 + abs(g - cg) ** 2 + abs(b - cb) ** 2)
            color_diffs.append((color_diff, color_name))
        return min(color_diffs)[1]


class ArgHTMLParser(HTMLParser, ABC):
    """
    Class based on HTMLParser, used for parsing HTML string passed in get_mapped_html method.
    Returns a list representing HTML document, which could be further processed to get the nested HTML mapped.
    """
    def __init__(self):
        super().__init__()
        self.mapped_list = list()

    def handle_starttag(self, tag, attrs):
        self.mapped_list.append((f'_!{tag}!_', attrs))

    def handle_endtag(self, tag):
        self.mapped_list.append((f'__!{tag}!__',))

    def handle_data(self, data):
        if data != ' ' and data != '\n' and data != '\n\n' and data != '\n\t':
            self.mapped_list.append(('!__data__!', data))

    def get_mapped_html(self, data_str: str) -> list:
        self.feed(data=data_str)
        return self.mapped_list
