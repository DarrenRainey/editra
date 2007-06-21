############################################################################
#    Copyright (C) 2007 Cody Precord                                       #
#    cprecord@editra.org                                                   #
#                                                                          #
#    Editra is free software; you can redistribute it and#or modify        #
#    it under the terms of the GNU General Public License as published by  #
#    the Free Software Foundation; either version 2 of the License, or     #
#    (at your option) any later version.                                   #
#                                                                          #
#    Editra is distributed in the hope that it will be useful,             #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of        #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
#    GNU General Public License for more details.                          #
#                                                                          #
#    You should have received a copy of the GNU General Public License     #
#    along with this program; if not, write to the                         #
#    Free Software Foundation, Inc.,                                       #
#    59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             #
############################################################################

"""
#--------------------------------------------------------------------------#
# FILE: ed_style.py                                                        #
# AUTHOR: Cody Precord                                                     #
# LANGUAGE: Python                                                         #
# SUMMARY:                                                                 #
# Provides classes/functions to manage the document styling.               #
#                                                                          #
# CLASS: StyleItem                                                         #
# METHODS:                                                                 #
# -SetFore,SetBack,SetFace,SetSize: Set values of named attributes         #
# -SetAttrFromString: Convert a style string to a StyleItem                #
#                                                                          #
# CLASS: StyleMgr                                                          #
# METHODS:                                                                 #
# -DefaultStyleDictionary: Returns the Default Styles                      #
# -GetFontDictionary: Does a font lookup and returns a dictonary of fonts  #
# -GetStyleByName: Looksup and returns a style string by named key.        #
# -HasNamedStyle: Returns true if a named style key has been defined.      #
# -LoadStyleSheet: Loads a custom style sheet.                             #
# -MergeFonts: Merges the font dictonary into the style items.             #
#--------------------------------------------------------------------------#
"""

__revision__ = "$Id: Exp $"

#--------------------------------------------------------------------------#
# Dependancies
import os
import re
import wx
import util

# Globals
STY_ATTRIBUTES     = u"face fore back size"
STY_EX_ATTRIBUTES  = u"eol bold italic underline"
#--------------------------------------------------------------------------#

# TODO The extra Attributes should be saved as a separate attribute in the
#      StyleItem, in order to facilitate easier setting and modification
#      This currenlty causes problems when customizing values in the StyleEditor
#      Changing this is fairly easy in this class but it will require changes
#      to the StyleMgr and Editor as well.
class StyleItem:
    """A storage class for holding styling information"""
    def __init__(self, fore=wx.EmptyString, back=wx.EmptyString, 
                    face=wx.EmptyString, size=wx.EmptyString):
        """Initiliazes the Style Object.

        fore: Specifies the forground color (hex string)
        face: Specifies the font face (string face name)
        back: Specifies the background color (hex string)
        size: Specifies font point size (int/formatted string)

        SPECIFICATION:
          DATA FORMATS:
            #123456       = hex color code
            #123456,bold  = hex color code + extra style
            Monaco        = Font Face Name
            %(mono)s      = Format string to be swapped at runtime
            10            = A font point size
            %(size)s      = Format string to be swapped at runtime
        """
        if fore != wx.EmptyString:
            self.fore = fore        # Foreground color hex code
        if face != wx.EmptyString:
            self.face = face        # Font face name
        if back != wx.EmptyString:
            self.back = back        # Background color hex code
        if size != wx.EmptyString:
            self.size = size        # Font point size

    def __eq__(self, si2):
        """Defines the == operator for the StyleItem Class"""
        if str(self) == str(si2):
            return True
        else:
            return False

    def __str__(self):
        """Converts StyleItem to a string"""
        style_str = wx.EmptyString
        if hasattr(self, u'fore'):
            style_str = u"fore:%s," % self.fore
        if hasattr(self, u'back'):
            style_str += u"back:%s," % self.back
        if hasattr(self, u'face'):
            style_str += u"face:%s," % self.face
        if hasattr(self, u'size'):
            style_str += u"size:%s," % str(self.size)
        if len(style_str) and style_str[-1] == u',':
            style_str = style_str[0:-1]
        return style_str

    #---- Get Functions ----#
    def GetBack(self):
        """Returns the value of the back attribute"""
        if hasattr(self, 'back'):
            return self.back
        else:
            return wx.EmptyString

    def GetFace(self):
        """Returns the value of the face attribute"""
        if hasattr(self, 'face'):
            return self.face
        else:
            return wx.EmptyString

    def GetFore(self):
        """Returns the value of the fore attribute"""
        if hasattr(self, 'fore'):
            return self.fore
        else:
            return wx.EmptyString

    def GetSize(self):
        """Returns the value of the size attribute as a string"""
        if hasattr(self, 'size'):
            return self.size
        else:
            return wx.EmptyString

    #---- Set Functions ----#
    def SetAttrFromStr(self, style_str):
        """Takes style string and sets the objects attributes
        by parsing the string for the values. Only sets or 
        overwrites values does not zero out previously set values.
        Returning True if value(s) are set or false otherwise.

        """
        atoms = style_str.split(u',')
        last_set = wx.EmptyString
        for atom in atoms:
            attrib = atom.split(u':')
            if len(attrib) == 2 and attrib[0] in STY_ATTRIBUTES:
                last_set = attrib[0]
                setattr(self, attrib[0], attrib[1])
            elif attrib[0] in STY_EX_ATTRIBUTES and last_set != wx.EmptyString:
                l_val = getattr(self, last_set)
                setattr(self, last_set, u",".join([l_val, attrib[0]]))
            else:
                pass
        if last_set != wx.EmptyString:
            return True
        else:
            return False

    def SetBack(self, back, ex=wx.EmptyString):
        """Sets the Background Value"""
        if ex == wx.EmptyString:
            self.back = back
        else:
            self.back = u"%s,%s" % (back, ex)

    def SetFace(self, face, ex=wx.EmptyString):
        """Sets the Face Value"""
        if ex == wx.EmptyString:
            self.face = face
        else:
            self.face = u"%s,%s" % (face, ex)

    def SetFore(self, fore, ex=wx.EmptyString):
        """Sets the Foreground Value"""
        if ex == wx.EmptyString:
            self.fore = fore
        else:
            self.fore = u"%s,%s" % (fore, ex)

    def SetSize(self, size, ex=wx.EmptyString):
        """Sets the Font Size Value"""
        if ex == wx.EmptyString:
            self.size = size
        else:
            self.size = u"%s,%s" % (str(size), ex)

    def SetExAttr(self, ex_attr, set=True):
        """Adds an extra text attribute to a StyleItem. Currently
        (bold, eol, italic, underline) are supported. If the optional
        set value is set to False the attribute will be removed from
        the StyleItem.

        """
        # Get currently set attributes
        cur_str = self.__str__()
        if not set:
            cur_str = cur_str.replace(u',' + ex_attr, wx.EmptyString)
            self.SetAttrFromStr(cur_str)
        else:
            if ex_attr not in cur_str:
                attr_map = { u"fore" : self.GetFore(),
                             u"back" : self.GetBack(),
                             u"face" : self.GetFace(),
                             u"size" : self.GetSize()
                           }
                for key in attr_map:
                    if attr_map[key] != wx.EmptyString and \
                      u"," not in attr_map[key]:
                        setattr(self, key, u",".join([attr_map[key], ex_attr]))
                        break
            else:
                pass

    def SetNamedAttr(self, attr, value):
        """Sets a StyleItem attribute by named string. NOTE this is
        not intended to be used for setting extra attributes such as
        bold, eol, ect..

        """
        if hasattr(self, attr):
            cur_val = getattr(self, attr)
            if u"," in cur_val:
                tmp = cur_val.split(u",")
                tmp[0] = value
                value = u",".join(tmp)
        setattr(self, attr, value)

#-----------------------------------------------------------------------------#

class StyleMgr:
    """Manages style definitions and provides them on request.
    Also provides functionality for loading custom style sheets and 
    modifying styles during run time.

    """
    FONT_TAG_TIMES     = u"times"
    FONT_TAG_MONO      = u"mono"
    FONT_TAG_HELV      = u"helv"
    FONT_TAG_OTHER     = u"other"
    FONT_TAG_SIZE      = u"size"
    FONT_TAG_SIZE2     = u"size2"

    def __init__(self, custom=wx.EmptyString):
        """Initializes the Style Manager"""

        # Attributes
        self.fonts = self.GetFontDictionary()
        self.style_set = custom
        self.LOG = wx.GetApp().GetLog()

        # Get the Style Set
        if custom != wx.EmptyString and self.LoadStyleSheet(custom):
            self.LOG("[styles] [init] Loaded custom style sheet %s" % custom)
        else:
            self.LOG("[styles] [init_error] Failed to import styles from %s" % custom)

    def DefaultStyleDictionary(self):
        """This is the default style values that are used for styling
        documents. Its used as a fallback for undefined values in a 
        style sheet.

        """
        def_dict = \
            {'brace_good' : StyleItem("#FFFFFF", "#0000FF,bold"),
             'brace_bad'  : StyleItem(back="#FF0000,bold"),
             'calltip' : StyleItem("#404040", "#FFFFB8"),
             'ctrl_char'  : StyleItem(),
             'line_num'   : StyleItem(back="#C0C0C0", face="%(other)s", size="%(size2)d"),
             'array_style': StyleItem("#EE8B02,bold", face="%(other)s"),
             'btick_style': StyleItem("#8959F6,bold", size="%(size)d"),
             'default_style': StyleItem("#000000", "#F6F6F6", "%(mono)s", "%(size)d"),
             'char_style' : StyleItem("#FF3AFF"),
             'class_style' : StyleItem("#2E8B57,bold"),
             'class2_style' : StyleItem("#2E8B57,bold"),
             'comment_style' : StyleItem("#838383"),
             'directive_style' : StyleItem("#0000FF,bold", face="%(other)s"),
             'dockey_style' : StyleItem("#0000FF"),
             'error_style' : StyleItem("#DD0101,bold", face="%(other)s"),
             'funct_style' : StyleItem("#008B8B,italic"),
             'global_style' : StyleItem("#007F7F,bold", face="%(other)s"), 
             'here_style' : StyleItem("#CA61CA,bold", face="%(other)s"),
             'ideol_style' : StyleItem("#E0C0E0", face="%(other)s"),
             'keyword_style' : StyleItem("#A52B2B,bold"),
             'keyword2_style' : StyleItem("#2E8B57,bold"),
             'keyword3_style' : StyleItem("#008B8B,bold"),
             'keyword4_style' : StyleItem("#9D2424"),
             'marker_style' : StyleItem("#FFFFFF", "#000000"),
             'folder_style' : StyleItem("#FFFFFF", "#000000"),
             'number_style' : StyleItem("#DD0101"),
             'number2_style' : StyleItem("#DD0101,bold"),
             'operator_style' : StyleItem("#000000", face="%(mono)s,bold"),
             'pre_style' : StyleItem("#AB39F2,bold"),               
             'pre2_style' : StyleItem("#AB39F2,bold", "#FFFFFF"),
             'regex_style' : StyleItem("#008B8B"),
             'scalar_style' : StyleItem("#AB37F2,bold", face="%(other)s"),
             'scalar2_style' : StyleItem("#AB37F2", face="%(other)s"),
             'string_style' : StyleItem("#FF3AFF,bold"),
             'stringeol_style' : StyleItem("#000000,bold", "#EEC0EE,eol","%(other)s"),
             'unknown_style' : StyleItem("#FFFFFF,bold", "#DD0101,eol", "%(other)s")
             }
        return def_dict

    def BlankStyleDictionary(self):
        """Returns a dictionary of unset style items based on the
        tags defined in the current dictionary.

        """
        sty_dict = self.DefaultStyleDictionary()
        for key in sty_dict:
            sty_dict[key] = StyleItem(face=u"%(mono)s", size="%(size)d")
        return sty_dict

    def GetFontDictionary(self, default=True):
        """Does a system lookup to build a default set of fonts using
        ten point fonts as the standards size.

        """
        if hasattr(self, 'fonts') and not default:
            return self.fonts
        mfont = wx.Font(10, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, 
                        wx.FONTWEIGHT_NORMAL)
        mono_font = mfont.GetFaceName()
        font = wx.Font(10, wx.FONTFAMILY_DECORATIVE, wx.FONTSTYLE_NORMAL, 
                        wx.FONTWEIGHT_NORMAL)
        time_font = font.GetFaceName()
        font = wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, 
                        wx.FONTWEIGHT_NORMAL)
        other_font = font.GetFaceName()
        font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, 
                        wx.FONTWEIGHT_NORMAL)
        helv_font = font.GetFaceName()
        faces = { self.FONT_TAG_TIMES : time_font,
                  self.FONT_TAG_MONO  : mono_font,
                  self.FONT_TAG_HELV  : helv_font,
                  self.FONT_TAG_OTHER : other_font,
                  self.FONT_TAG_SIZE  : mfont.GetPointSize(),
                  self.FONT_TAG_SIZE2 : mfont.GetPointSize()-2
                 }
        return faces

    def GetDefaultFont(self):
        """Constructs and returns a wxFont object from the settings
        of the default_style object.

        """
        if hasattr(self, "styles") and self.styles.has_key("default_style"):
            style_item = self.styles['default_style']
            face = style_item.GetFace()
            if face[0] == u"%":
                face = face % self.fonts
            size = style_item.GetSize()
            if isinstance(size, basestring):
                size = size % self.fonts
            font = wx.FFont(int(size), wx.MODERN, face=face)
        else:
            font = wx.FFont(self.fonts[self.FONT_TAG_SIZE], wx.MODERN)
        return font

    def GetDefaultForeColour(self, hex=False):
        """Gets the foreground color of the default style and returns
        a Colour object. Otherwise returns Black if the default
        style is not found.

        """
        if self.HasNamedStyle(u'default_style'):
            fore = self.styles[u'default_style'].GetFore()
            if fore == wx.EmptyString:
                fore = u"#000000"
            if not hex:
                fore = wx.ColourRGB(int(fore[1:], 16))
        else:
            fore = u"#000000"
            if not hex:
                fore = wx.NamedColor("black")
        return fore

    def GetDefaultBackColour(self, hex=False):
        """Gets the background color of the default style and returns
        a Colour object. Otherwise returns white if the default
        style is not found.

        """
        if self.HasNamedStyle(u'default_style'):
            back = self.styles[u'default_style'].GetBack()
            if back == wx.EmptyString:
                back = u"#FFFFFF"
            if not hex:
                back = wx.ColourRGB(int(back[1:], 16))
        else:
            back = u"#FFFFFF"
            if not hex:
                back = wx.NamedColor("white")
        return back

    def GetItemByName(self, name):
        """Gets and returns a style item using its name for the search"""
        if self.HasNamedStyle(name):
            if u"%" in unicode(self.styles[name]):
                val = unicode(self.styles[name]) % self.fonts
                item = StyleItem()
                item.SetAttrFromStr(val)
                return item
            else:
                return self.styles[name]
        else:
            return StyleItem()

    def GetMonoFont(self):
        """Returns the current global mono font facename"""
        return self.fonts[self.FONT_TAG_MONO]

    def GetStyleByName(self, name):
        """Gets and returns a style string using its name for the search"""
        if self.HasNamedStyle(name):
            if u"%" in unicode(self.styles[name]):
                return unicode(self.styles[name]) % self.fonts
            else:
                return unicode(self.styles[name])
        else:
            return wx.EmptyString

    def GetStyleSet(self):
        """Returns the current set of styles or the
        default set if there is no current set.

        """
        if hasattr(self, "styles"):
            return self.styles
        else:
            return self.DefaultStyleDictionary()

    def HasNamedStyle(self, name):
        """Checks if a style has been set/loaded or not"""
        if not hasattr(self, 'styles'):
            return False
        elif self.styles.has_key(name):
            return True
        else:
            return False

    def LoadStyleSheet(self, style_sheet):
        """Loads a custom style sheet and returns True on success"""
        if os.path.exists(style_sheet):
            reader = util.GetFileReader(style_sheet)
            if reader == -1:
                self.LOG("[styles] [exception] Failed to open style sheet: %s" % style_sheet)
                return False
            ret_val = self.SetStyles(self.ParseStyleData(reader.read()))
            reader.close()
            return ret_val
        else:
            self.LOG("[styles] The style sheet %s does not exists" % style_sheet)
            self.SetStyles(self.DefaultStyleDictionary())
            return False

    def MergeFonts(self, style_dict, font_dict):
        """Does any string substitution that the style dictionary
        may need to have fonts and their sizes set.

        """
        for style in style_dict:
            st_str = str(style_dict[style])
            if u'%' in st_str:
                style_dict[style].SetAttrFromStr(st_str % font_dict)
        return style_dict

    def MergeStyles(self, styles1, styles2):
        """Merges the styles from styles2 into styles1 overwriting
        any duplicate values already set in styles1 with the new
        data from styles2.

        """
        for style in styles2:
            styles1[style] = styles2[style]
        return styles1

    def PackStyleSet(self, style_set):
        """Checks the difference of each item in the style set as
        compared to the default_style tag and packs any unset value
        in the item to be equal to the default style.

        """
        if isinstance(style_set, dict) and style_set.has_key('default_style'):
            default = style_set['default_style']
            for tag in style_set:
                if style_set[tag].GetFace() == wx.EmptyString:
                    style_set[tag].SetFace(default.GetFace())
                if style_set[tag].GetFore() == wx.EmptyString:
                    style_set[tag].SetFore(default.GetFore())
                if style_set[tag].GetBack() == wx.EmptyString:
                    style_set[tag].SetBack(default.GetBack())
                if style_set[tag].GetSize() == wx.EmptyString:
                    style_set[tag].SetSize(default.GetSize())
        else:
            pass
        return style_set

    def ParseStyleData(self, style_data, strict=False):
        """Parses a string style definitions read from an Editra
        Style Sheet. If the parameter 'strict' isnt set then any
        syntax errors are ignored and only good values are returned.
        If 'strict' is set the parser will raise errors and bailout.

        """
        # Compact data into a contiguous string
        style_data = style_data.replace(u"\n", u"")
        style_data = style_data.replace(u"\t", u"")

        # Build style data tree
        styles = style_data.split(u'}')
        del style_data
        style_tree = list()

        # Tree Level 1 split tag from data
        for style in styles:
            style_tree.append(style.split(u"{"))

        if len(style_tree) and style_tree[-1][0] == wx.EmptyString:
            style_tree.pop()

        # Check for Level 1 Syntax Errors
        tmp = style_tree
        for style in tmp:
            if len(style) != 2:
                self.LOG("[styles] [syntax error] There was an error parsing "
                         "the syntax data from " + self.style_set)
                self.LOG("[styles] [syntax error] You are missing a { or } " +
                        "in Def: " + style[0].split()[0])
                if strict:
                    raise SyntaxError
                else:
                    style_tree.remove(style)

        # Tree Level 2 Build small trees of tag and style attributes
        # Tree Level 3 Branch tree into TAG => Attr => Value String
        i = j = 0
        while i < len(style_tree):
            tmp = tmp2 = list()
            tmp = style_tree[i][1].strip().split(u";") # Level 2 Break into attributes
            while j < len(tmp):
                tmp2.append(tmp[j].strip().split(u":")) # Level 3 Attribute to values
                j += 1
            j = 0
            if len(tmp2) and tmp2[-1][0] == wx.EmptyString:
                tmp2.pop()
            style_tree[i][1] = tmp2
            del tmp2
            i += 1

        # Check for L2/L3 Syntax errors and build a clean dictionary
        # of Tags => Valid Attributes
        style_dict = dict()
        for branch in style_tree:
            value = list()
            tag = branch[0].replace(u" ", u"")
            for leaf in branch[1]:
                leaf[0] = leaf[0].strip() # Remove any remaining whitespace
                if len(leaf) != 2:
                    self.LOG("[styles] [syntax_error] Missing a : or ; in the "
                             "declaration of %s" % tag)
                    if strict:
                        raise SyntaxError
                elif leaf[0] not in STY_ATTRIBUTES:
                    self.LOG(("[styles] [syntax_warning] Unknown style attribute: %s"
                             ", In declaration of %s") + (leaf[0], tag))
                    if strict:
                        raise SyntaxWarning
                else:
                    value.append(leaf)
            style_dict[tag] = value

        # Trim the leafless branches from the dictionary
        tmp = style_dict
        for style_def in tmp:
            if len(tmp[style_def]) == 0:
                style_dict.pop(style_def)

        # Validate leaf values and format into stylestring
        for style_def in style_dict:
            if not style_def[0][0].isalpha():
                self.LOG("[styles] [syntax_error] The style def %s is not a "
                         "valid name" % style_def[0])
                if strict:
                    raise SyntaxError
            else:
                style_str = wx.EmptyString
                for attrib in style_dict[style_def]:
                    values = attrib[1].split(u" ")
                    tval = list()
                    for val in values:
                        if val != wx.EmptyString:
                            tval.append(val)
                    values = tval
                    if len(values) > 2:
                        self.LOG("[styles] [syntax_warning] Only one extra " +
                                 "attribute can be set per style see " +
                                 style_def + " => " + attrib[0])
                        if strict:
                            raise SyntaxWarning

                    # Validate values
                    v1ok = v2ok = False
                    if len(values) and attrib[0] in "fore back":
                        if values[0][0] == u"#" and len(values[0]) == 7 and \
                           values[0][1:].isalnum():
                            v1ok = True
                    elif len(values) and attrib[0] in "face size": 
                        # TODO these regular expressions need work
                        match1 = re.compile("\%\([a-zA-Z0-9]*\)")
                        match2 = re.compile("[a-zA-Z0-9]*")
                        if match1.match(values[0]) or match2.match(values[0]):
                            v1ok = True
                        else:
                            self.LOG("[styles] [syntax_warning] Bad value in " + \
                                    attrib[0] + " the value %s is invalid." % values[0])

                    if len(values) == 2 and values[1] in STY_EX_ATTRIBUTES:
                        v2ok = True
                    elif len(values) == 2:
                        self.LOG("[styles] [syntax_warning] Unknown extra " + \
                                 "attribute '" + values[1] + \
                                 "' in attribute: " + attrib[0])

                    if v1ok and v2ok:
                        value = u",".join(values)
                    elif v1ok:
                        value = values[0]
                    else:
                        value = wx.EmptyString
                    
                    if value != wx.EmptyString:
                        value = u":".join([attrib[0], value])
                        style_str = u",".join([style_str, value])
                    else:
                        continue
                if style_str != wx.EmptyString:
                    style_str = style_str.strip(u",")
                    style_dict[style_def] = style_str

        # Build a StyleItem Dictionary
        for key in style_dict:
            new_item = StyleItem()
            try:
                new_item.SetAttrFromStr(style_dict[key])
                style_dict[key] = new_item
            except:
                pass
        return style_dict

    def SetGlobalFont(self, font_tag, fontface):
        """Sets one of the fonts in the global font set by tag
        and sets it to the named font. Returns true on success.

        """
        if hasattr(self, 'fonts'):
            self.fonts[font_tag] = fontface
            return True
        else:
            return False

    def SetStyleFont(self, named_style, wxFont):
        """Sets the font of a specific style"""
        if self.HasNamedStyle(named_style):
            self.styles[named_style].SetFont(wxFont.GetFaceName())
            self.styles[named_style].SetSize(wx.Font.GetPointSize())
            return True
        else:
            return False

    def SetStyleTag(self, style_tag, value):
        """Sets the value of style tag by name"""
        self.styles[style_tag] = value

    def SetStyles(self, style_dict, nomerge=False):
        """Sets the managers style data and returns True on success."""
        if nomerge:
            self.styles = self.PackStyleSet(style_dict)
            return True

        if isinstance(style_dict, dict):
            # Check for bad data
            for style in style_dict:
                try:
                    style_dict[style].GetFore()
                except AttributeError:
                    self.LOG("[styles] [error] Invalid data " \
                             "in style dictionary")
                    return False

            if not hasattr(self, "styles"):
                self.styles = self.DefaultStyleDictionary()
            self.styles = self.MergeStyles(self.styles, style_dict)
            self.styles = self.PackStyleSet(self.styles)
            return True
        else:
            self.LOG("[styles] [error] SetStyles expects a " \
                     "dictionary of StyleItems")
            return False