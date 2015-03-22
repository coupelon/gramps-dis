#
# Download Internet Sources plugin for Gramps
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#
# This Gramps plugin was started using the code from the AttachSourceTool.py,
# the GNU General Public License, from Donald N. Allingham and Brian Matherly
#

__author__ = "Olivier Coupelon"
__copyright__ = "Copyright 2014, Olivier Coupelon"
__credits__ = ["Olivier Coupelon", "Donald N. Allingham", "Brian Matherly", "Jerome Rapinat"]
__license__ = "GPL"
__version__ = "1.1.1"
__maintainer__ = "Olivier Coupelon"
__email__ = "olivier@coupelon.net"
__status__ = "Development"

  
"Download Internet Sources"
  
#------------------------------------------------------------------------
#
# GRAMPS modules
#
#------------------------------------------------------------------------
from gramps.gui.plug.tool import Tool
from gramps.gui.plug import MenuToolOptions, PluginWindows
from gramps.gen.plug.menu import StringOption, FilterOption, PersonOption, \
    EnumeratedListOption
import gramps.gen.lib
from gramps.gen.db import DbTxn
import gramps.gen.plug.report.utils as ReportUtils
from gramps.gen.display.name import displayer as name_displayer
from gramps.gen.lib.mediaobj import MediaObject
from gramps.gen.lib.mediaref import MediaRef
import gramps.gen.const
from gramps.gen.utils.grampslocale import GrampsLocale
_ = GrampsLocale().translation.gettext
import logging
LOG = logging.getLogger(".DownloadInternetSources")
  
#------------------------------------------------------------------------
#
# Plugin modules
#
#------------------------------------------------------------------------

import SeekAndDownload
  
#------------------------------------------------------------------------
#
# Tool Classes
#
#------------------------------------------------------------------------
class DownloadOptions(MenuToolOptions):
    """ Attach Source options  """
    def __init__(self, name, person_id=None, dbstate=None):
        self.__db = dbstate.get_database()
        MenuToolOptions.__init__(self, name, person_id, dbstate)
  
    def add_menu_options(self, menu):
  
        """ Add the options """
        category_name = _("Options")
        
        self.__filter = FilterOption(_("Person Filter"), 0)
        self.__filter.set_help(_("Select filter to restrict people"))
        menu.add_option(category_name, "filter", self.__filter)
        self.__filter.connect('value-changed', self.__filter_changed)
  
        self.__pid = PersonOption(_("Filter Person"))
        self.__pid.set_help(_("The center person for the filter"))
        menu.add_option(category_name, "pid", self.__pid)
        self.__pid.connect('value-changed', self.__update_filters)
  
        self.__update_filters()
        
        ad81_login = StringOption(_("AD81 Login"), "")
        ad81_login.set_help(_("Login pour le site http://archives.tarn.fr/"))
        menu.add_option(category_name, "ad81_login", ad81_login)
        self.__ad81_login = ad81_login
        
        ad81_password = StringOption(_("AD81 Password"), "")
        ad81_password.set_help(_("Mot de passe pour le site http://archives.tarn.fr/"))
        menu.add_option(category_name, "ad81_password", ad81_password)
        self.__ad81_password = ad81_password
        
    def __update_filters(self):
        """
        Update the filter list based on the selected person
        """
        gid = self.__pid.get_value()
        person = self.__db.get_person_from_gramps_id(gid)
        filter_list = ReportUtils.get_person_filters(person, False)
        self.__filter.set_filters(filter_list)
  
    def __filter_changed(self):
        """
        Handle filter change. If the filter is not specific to a person,
        disable the person option
        """
        filter_value = self.__filter.get_value()
        if filter_value in [1, 2, 3, 4]:
            # Filters 0, 2, 3, 4 and 5 rely on the center person
            self.__pid.set_available(True)
        else:
            # The rest don't
            self.__pid.set_available(False)

class DownloadWindow(PluginWindows.ToolManagedWindowBatch):
    def get_title(self):
        return _("Download Internet Sources")
  
    def initial_frame(self):
        return _("Options")
  
    def run(self):
        self.skeys = {} 
        
    	LOG.info("Browsing page sources")

        with DbTxn(_("Download Internet Sources"), self.db, batch=True) as self.trans:
            self.add_results_frame(_("Results"))
            self.results_write(_("Processing...\n"))
            self.db.disable_signals()
            
            self.filter_option =  self.options.menu.get_option_by_name('filter')
            self.filter = self.filter_option.get_filter() # the actual filter

            # FIXME: use old style for gramps31 compatible
            #    people = self.filter.apply(self.db,
            #                               self.db.iter_person_handles())
            people = self.filter.apply(self.db,
                                 self.db.get_person_handles(sort_handles=False))
  
            media_directory = self.db.get_mediapath()

            LOG.info("Chosen media directory: " + media_directory)
            
            num_people = len(people)
            self.results_write(_("Attaching sources...\n"))
            self.progress.set_pass(_('Attaching sources...'),
                                   num_people)
            count = 1
            for person_handle in people:
                self.progress.step()
                person = self.db.get_person_from_handle(person_handle)
                self.results_write("  %d) " % count)
                self.results_write_link(name_displayer.display(person),
                                        person, person_handle)
                self.results_write("\n")
                
                for url in person.get_url_list():
                    dir_name = person.get_primary_name().get_regular_name() + "-" + person.get_gramps_id()
                    if media_directory:
                        path = media_directory + os.sep + "gdis" + os.sep + dir_name
                    else:
                        path = const.USER_HOME + os.sep + "gdis" + os.sep + dir_name
                    result = SeekAndDownload(self.options.handler.options_dict['ad81_login'],self.options.handler.options_dict['ad81_password']).determine_cote_from_url(url.get_path(), path, url.get_description())
                    if result != None and len(result) == 3:
                        # 0: relative_path, 1: title, 2: type
                        media = MediaObject()
                        media.set_description(result[1])
                        media.set_path("gdis" + os.sep + dir_name + os.sep + result[0])
                        media.set_mime_type(result[2])
                        self.db.add_object(media, self.trans)
                        self.db.commit_media_object(media, self.trans)
                        
                        mediaref = MediaRef()
                        mediaref.set_reference_handle(media.handle)
                        person.add_media_reference(mediaref)
                        self.db.commit_person(person, self.trans)
                count += 1
  
        self.db.enable_signals()
        self.db.request_rebuild()
        self.results_write("Done!\n")