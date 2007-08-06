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
# FILE: ed_event.py
# @author: Cody Precord
# LANGUAGE: Python
# @summary:
#    Provides custom events for the editors controls/objects to utilize
#
# METHODS:
#
#
#
#--------------------------------------------------------------------------#
"""

__author__ = "Cody Precord <cprecord@editra.org>"
__cvsid__ = "$Id$"
__revision__ = "$Revision$"

#--------------------------------------------------------------------------#
# Dependancies
import wx

#--------------------------------------------------------------------------#

edEVT_UPDATE_TEXT = wx.NewEventType()
EVT_UPDATE_TEXT = wx.PyEventBinder(edEVT_UPDATE_TEXT, 1)
class UpdateTextEvent(wx.PyCommandEvent):
    """Event to signal that text needs updating"""
    def __init__(self, etype, eid, value=None):
        """Creates the event object"""
        wx.PyCommandEvent.__init__(self, etype, eid)
        self._etype = etype
        self._id = eid
        self._value = value

    def GetEvtType(self):
        """Returns the event type
        @return: this events event type (ed_event)

        """
        return self._etype

    def GetId(self):
        """Returns the event id
        @return: The Id of this event

        """
        return self._id

    def GetValue(self):
        """Returns the value from the event.
        @return: the value of this event

        """
        return self._value

#--------------------------------------------------------------------------#

edEVT_NOTIFY = wx.NewEventType()
EVT_NOTIFY = wx.PyEventBinder(edEVT_NOTIFY, 1)
class NotificationEvent(wx.PyCommandEvent):
    """General notification event"""
    def __init__(self, etype, eid, value=None, obj=None):
        wx.PyCommandEvent.__init__(self, etype, eid)
        self._etype = etype
        self._id = eid
        self._value = value
        self._obj = obj

    def GetEventObject(self):
        """Returns the object associated with this event
        @return: the object associated with this event

        """
        return self._obj

    def GetEvtType(self):
        """Returns the event type
        @return: this events event type (ed_event)

        """
        return self._etype

    def GetId(self):
        """Returns the event id
        @return: the identifier of this event

        """
        return self._id

    def GetValue(self):
        """Returns the value from the event.
        @return: the value of this event

        """
        return self._value

#--------------------------------------------------------------------------#

edEVT_MAINWINDOW_EXIT = wx.NewEventType()
EVT_MAINWINDOW_EXIT = wx.PyEventBinder(edEVT_MAINWINDOW_EXIT, 1)
class MainWindowExitEvent(wx.PyCommandEvent):
    """Event to signal that text needs updating"""
    def __init__(self, etype, eid):
        """Creates the event object"""
        wx.PyCommandEvent.__init__(self, etype, eid)
        self._etype = etype
        self._id = eid

    def GetEvtType(self):
        """Returns the event type
        @return: this events event type (ed_event)

        """
        return self._etype

    def GetId(self):
        """Returns the event id
        @return: the identifier of this event

        """
        return self._id
