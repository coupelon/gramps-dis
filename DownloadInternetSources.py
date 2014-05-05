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
# python modules
#
#------------------------------------------------------------------------
import time
import base64
import urllib2
import cStringIO
import os
import Image
from urlparse import urlparse, parse_qs
import cookielib
import re
  
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
                        path = media_directory + os.sep +  dir_name
                    else:
                        path = const.USER_HOME
                    result = self.determine_cote_from_url(url, path, url.get_description())
                    if result != None and len(result) == 3:
                        # 0: relative_path, 1: title, 2: type
                        media = MediaObject()
                        media.set_description(result[1])
                        media.set_path(dir_name + os.sep + result[0])
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
        
    def determine_cote_from_url(self, url, path, description):
    	LOG.debug("Determine if url needs to be retrieved : " + url.get_path())
        o = urlparse(url.get_path())
        if o.netloc == "www.archivesdepartementales.puydedome.fr":
            image_url = self.get_image_url_from_AD63(o, path, description)
            return image_url
        if o.netloc == "etat-civil.bas-rhin.fr":
            image_url = self.get_image_url_from_AD67(o, path, description)
            return image_url            
        if o.netloc == "archives.aveyron.fr":
            image_url = self.get_image_url_from_AD12(o, path, description)
            return image_url
        if o.netloc == "archives.lozere.fr":
            image_url = self.get_image_url_from_AD48(o, path, description)
            return image_url
        if o.netloc == "archivesenligne.tarn.fr":
            image_url = self.get_image_url_from_AD81(o, path, description)
            return image_url
        if o.netloc == "www.archives-aube.fr":
            image_url = self.get_image_url_from_AD10(o, path, description)
            return image_url
        if o.netloc == "www.archinoe.fr":
            image_url = self.get_image_url_from_AD79(o, path, description)
            return image_url
        if o.netloc == "www.archives43.fr":
            image_url = self.get_image_url_from_AD43(o,url.get_path(), path, description)
            return image_url
        print "Not retrieved :" + url.get_path()
                       
    def get_image_url_from_ligeo(self,o,path,description,caller,base_url,cache_url,max_page_size, m_x, m_y):
        query_tuple = parse_qs(o.query, keep_blank_values=True)
        image_url = base_url + "/visui.php?DIR=" + ''.join(query_tuple["dir"]) + "&CACHE=" + cache_url + "&IMAGE=" + ''.join(query_tuple["image"]) #+ "&SI=img0"
        image_cote = ''.join(query_tuple["cote"])
        image_page = int(''.join(query_tuple["image"])[-max_page_size:])
        image_name = self.generate_filename_and_ensure_not_exists(path, image_cote, image_page, caller, ".jpg", description)
        if (not image_name[1]):
            image = [[Image.open(cStringIO.StringIO(urllib2.urlopen(urllib2.Request(image_url + "&SI=0/img_0" + str(k) + "_0" + str(m), None, {'User-Agent' : 'Mozilla/5.0'})).read())) for m in range(0,m_y)] for k in range(0,m_x)]
            size_y = 0;
            size_x = 0;
            for k in range(0,m_x):
                img_w,img_h=image[k][0].size
                size_y += img_w
            for m in range(0,m_y):
                img_w,img_h=image[0][m].size
                size_x += img_h
            background = Image.new('RGBA', (size_y,size_x), (255, 255, 255, 255))
            size_y = 0;
            size_x = 0;
            img_h = 0
            for k in range(0,m_x):
                for m in range(0,m_y):
                    img_w,img_h=image[k][m].size
                    background.paste(image[k][m],(size_x, size_y))
                    size_y += img_h
                size_x += img_w
                size_y = 0
            background.save(image_name[0])
            return image_name[2], image_cote + " P" + str(image_page), "image/jpeg"        

    #----------------------------------------------
    # Data retrieval for AD10 : http://www.archives-aube.fr/arkotheque/etat_civil/index.php
    #----------------------------------------------
    def get_image_url_from_AD10(self, o, path, description):
        if o.path.find("/arkotheque/arkotheque_img_print.php") == 0 :
            query_tuple = parse_qs(o.query, keep_blank_values=True)
            arkotheque_img_load = ''.join(query_tuple["arg2"])
            arko = arkotheque_img_load[arkotheque_img_load.rfind("arko=") + 5:]
            decoded = base64.b64decode(arko)
            
            # TODO: try to factorize the arko ID generation
            offset_fin_id = decoded.find(".JPG")
            offset_debut_id = decoded[:offset_fin_id].rfind("\"") + 1
            id = decoded[offset_debut_id:offset_fin_id].replace("_"," ").replace("/",",")
            
            image_name = self.generate_filename_and_ensure_not_exists(path, id, None, "AD10", ".jpg", description)
            if (not image_name[1]):
                content = urllib2.urlopen("http://www.archives-aube.fr/arkotheque/arkotheque_img_download.php?arko=" + arko).read()
                # A HTML + Javascript header ?!? is added to the downloaded file this way, so just find the raw JPG file and keep only that.
                jpeg_offset = content.find('\xff\xd8')
                file = open(image_name[0],"wb")
                file.write(content[jpeg_offset:])
                file.close()
                return image_name[2], id, "image/jpeg"
        else:
            return "Ce format d'url n'est pas supporte pour AD10"
    
    #----------------------------------------------
    # Data retrieval for AD12 : http://archives.aveyron.fr/archive/recherche/etatcivil/n:22
    #----------------------------------------------
    def get_image_url_from_AD12(self, o, path, description):
        return self.get_image_url_from_ligeo(o, path, description, "AD12", "http://archives.aveyron.fr", "/home/httpd/ad12/ligeo/app/webroot/data/files/ad12.ligeo/cache/images", 3, 4, 6)
    
    #----------------------------------------------
    # Data retrieval for AD43 : http://www.archives43.fr/arkotheque/consult_fonds/index.php?ref_fonds=3
    #----------------------------------------------
    def get_image_url_from_AD43(self,o,url, path, description):
        if o.path.find("/arkotheque/visionneuse/print_view.php") == 0 :
            doc_id_fin = url.rfind('|')
            doc_id_debut = url[:doc_id_fin].rfind('|') + 1
            page_number = int(url[doc_id_fin+1:]) + 1
            image_name = self.generate_filename_and_ensure_not_exists(path, url[doc_id_debut:doc_id_fin], page_number, "AD43", ".jpg", description)
            if (not image_name[1]):
                self.get_image_from_arko_ad43(url[doc_id_debut:doc_id_fin], str(page_number), image_name[0])
                return image_name[2], url[doc_id_debut:doc_id_fin] + " P" + str(page_number), "image/jpeg"
        elif o.path.find("/arkotheque/arkotheque_print_archives.php") == 0 :
            image_name = self.generate_filename_and_ensure_not_exists(path, "", None, "AD43", ".jpg", description)
            if (not image_name[1]):
                arko_args = url[url.find("arko_args=")+10:]

                xml_content = urllib2.urlopen("http://www.archives43.fr/arkotheque/xml_print_image.php?arko_args=" + base64.b64encode(arko_args.replace("%22",'"'))).read()
                offset_cote_debut = xml_content.find("img_titre=") + 11
                offset_cote_fin = xml_content.find('"', offset_cote_debut)
                offset_ref_debut = xml_content.find("img_ref=")+9
                offset_ref_fin = xml_content.find('"', offset_ref_debut)
                ref = xml_content[offset_ref_debut:offset_ref_fin]
                
                doc_id_fin = ref.rfind('|')
                doc_id_debut = ref[:doc_id_fin].rfind('|') + 1
                page_number = int(ref[doc_id_fin+1:]) + 1
                
                self.get_image_from_arko_ad43(ref[doc_id_debut:doc_id_fin], str(page_number), image_name[0])
                return image_name[2], url[offset_cote_debut:offset_cote_fin] + " P" + str(page_number), "image/jpeg"
        else:
            return "Ce format d'url n'est pas supporte pour AD43"
    
    def get_image_from_arko_ad43(self, doc_number_str, page_number_str, filename):
        doc_url = "http://www.archives43.fr/arkotheque/arkotheque_visionneuse_archives.php?arko=" + base64.b64encode('a:4:{s:4:"date";s:10:"2013-08-17";s:10:"type_fonds";s:11:"arko_seriel";s:4:"ref1";i:3;s:4:"ref2";i:' + doc_number_str + ';}')
        page_url = "http://www.archives43.fr/arkotheque/visionneuse/ajax_create_img.php?imgSrc=http%3A%2F%2Fwww.archives43.fr%2Farkotheque%2Fvisionneuse%2Fimg_prot.php%3Fi%3D" + page_number_str + ".jpg"
        
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        opener.open(doc_url).read()
        content = opener.open(page_url).read()
        file = open(filename,"wb")
        file.write(content)
        file.close()
    
    #----------------------------------------------
    # Data retrieval for AD48 : http://archives.lozere.fr
    #----------------------------------------------
    def get_image_url_from_AD48(self, o, path, description):
        return self.get_image_url_from_ligeo(o, path, description, "AD48", "http://archives.lozere.fr", "/home/httpd/ad48/ligeo/app/webroot/data/files/ad48.ligeo/cache/images", 3, 6, 4)

    #----------------------------------------------
    # Data retrieval for AD63 : http://www.archivesdepartementales.puydedome.fr/archives/recherche/etatcivil/n:13
    #----------------------------------------------
    def get_image_url_from_AD63(self, o, path, description):
        return self.get_image_url_from_ligeo(o, path, description, "AD63", "http://www.archivesdepartementales.puydedome.fr", "/home/httpd/ad63/portail/app/webroot/data/files//ad63.portail/cache/images", 4, 5, 4)
    
    #----------------------------------------------
    # Data retrieval for AD67 : http://etat-civil.bas-rhin.fr/
    #----------------------------------------------
    def get_image_url_from_AD67(self, o, path, description):
        if o.path.find("/adeloch/cg67_img_load.php") == 0 :
            query_tuple = parse_qs(o.query, keep_blank_values=True)
            decoded = base64.b64decode(''.join(query_tuple["arko"]))

            offset_debut_id = offset_fin_id = decoded.find(".JPG")
            offset_debut_id = decoded[:offset_debut_id].rfind("/")
            offset_debut_id = decoded[:offset_debut_id-1].rfind("/") + 1
            id = decoded[offset_debut_id:offset_fin_id].replace("_"," ").replace("/",",")
            
            image_name = self.generate_filename_and_ensure_not_exists(path, id, None, "AD67", ".jpg", description)
            if (not image_name[1]):
                content = urllib2.urlopen(o.geturl()).read()
                file = open(image_name[0],"wb")
                #Supprime les 39 caracteres d'entete flash. Note : il en reste une cinquante environ a la fin
                file.write(content[39:])
                file.close()
                return image_name[2], id, "image/jpeg"
        else:
            return "Ce format d'url n'est pas supporte pour AD67"
    
    #----------------------------------------------
    # Data retrieval for AD79 : http://archives.deux-sevres.com/Archives79/default.aspx
    #----------------------------------------------
    def get_image_url_from_AD79(self, o, path, description):
        if o.path.find("/gramps") == 0 :
            query_tuple = parse_qs(o.query, keep_blank_values=True)
            id = ''.join(query_tuple["id"])
            page = ''.join(query_tuple["p"])
            
            image_name = self.generate_filename_and_ensure_not_exists(path, id, None, "AD79", ".jpg", description)
            if (not image_name[1]):
            
                cj = cookielib.CookieJar()
                opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
                
                # 1. Get Session ID
                opener.open("http://www.archinoe.fr/cg79/registre_prepare.php?id=" + id).read()
                # 2. Get to the right archive
                opener.open("http://www.archinoe.fr/cg79/registre_prepare.php?id=" + id).read()
                # 3. Get the image location
                content = opener.open("http://www.archinoe.fr/cg79/visu_affiche_util.php?o=TILE&param=visu&x=2920&y=0&l=2600&h=2920&ol=2600&oh=2920&r=0&n=0&b=0&c=0&p=" + page).read()
                # 4. Get the image information
                content = opener.open("http://www.archinoe.fr" + content + ".txt").read()
                match = re.search('(\d+) x (\d+)', content)
                width = match.group(1)
                height = match.group(2)
                # 5. Get the full image link
                content = opener.open("http://www.archinoe.fr/cg79/visu_affiche_util.php?o=TILE&param=visu&x=0&y=0&l=" + width + "&h=" + height + "&ol=" + width + "&oh=" + height + "&r=0&n=0&b=0&c=0&p=" + page).read()
                # 6. Get the image
                content = opener.open("http://www.archinoe.fr" + content).read()
                
                file = open(image_name[0],"wb")
                file.write(content)
                file.close()
                return image_name[2], id, "image/jpeg"
        else:
            return "Ce format d'url n'est pas supporte pour AD79"
    
    #----------------------------------------------
    # Data retrieval for AD81 : http://archives.tarn.fr/
    #----------------------------------------------
    def get_image_url_from_AD81(self, o, path, description):
        ad81_login = self.options.handler.options_dict['ad81_login']
        ad81_password = self.options.handler.options_dict['ad81_password']
        if o.path.find("/affichage.php") == 0 :
            query_tuple = parse_qs(o.query, keep_blank_values=True)
            image = ''.join(query_tuple["image"])
            offset1 = image.rfind("/")
            offset2 = image.find(".JPG")
            if offset2 == -1:
                offset2 = image.find(".jpg")
            offset3 = image[:offset1].rfind("/")            
            
            image_name = self.generate_filename_and_ensure_not_exists(path, image[offset3+1:offset1], int(image[offset2-3:offset2]), "AD81", ".jpg", description)
            if (not image_name[1]):
            
                cj = cookielib.CookieJar()
                opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
                opener.open("http://archivesenligne.tarn.fr/login.php?base=").read()
                http_header = {
                    "Content-type": "application/x-www-form-urlencoded",
                }                
                opener.open(urllib2.Request("http://archivesenligne.tarn.fr/login_do.php", "LOGIN="+ ad81_login +"&PASSWORD=" + ad81_password + "&base=&envoyer.x=110&envoyer.y=4", http_header)).read()
                content = opener.open(o.geturl()).read()
                # Extract the JPG from the PDF
                stream_offset_start = content.rfind("\nstream\n")
                stream_offset_end = content.rfind("\nendstream\n")
                if (stream_offset_start != -1 and stream_offset_end != -1 ):
                    file = open(image_name[0],"wb")
                    file.write(content[stream_offset_start+8:stream_offset_end])
                    file.close()
                    return image_name[2], image[offset3+1:offset1], "image/jpeg"
                return "Erreur lors de la recuperation des donnees pour AD81. Verifier le login/mdp."
        else:
            return "Ce format d'url n'est pas supporte pour AD81"

    def generate_filename_and_ensure_not_exists(self, path, cote, page, ad, extension, description):
        if page == None:
            if cote == "":
                filename = self.remove_forbidden_characters(description) + "," + ad + extension
            else :
                filename = self.remove_forbidden_characters(description) + "," + ad + " " + self.remove_forbidden_characters(cote) + extension
        else:
            filename = self.remove_forbidden_characters(description) + "," + ad + " " + self.remove_forbidden_characters(cote) + "P" + str(page) + extension
        if not os.path.exists(path):
            os.makedirs(path)  
        return path + os.sep + filename, os.path.exists(path + os.sep + filename), filename
        
    def remove_forbidden_characters(self, input):
        # Only windows characters.
        return input.replace("/","-").replace("\\","-").replace("<","-").replace(">","-").replace(":","-").replace('"',"-").replace('|',"-").replace('?',"-").replace('*',"-")
