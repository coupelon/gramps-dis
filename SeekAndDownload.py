#
# Download Internet Sources plugin for Gramps - SeekAndDownload
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

# ------------------------------------------------------------------------
#
# python modules
#
#------------------------------------------------------------------------
import time
import base64
import urllib2
import cStringIO
from urlparse import urlparse, parse_qs
import cookielib
import os
import PIL.Image
import re

import logging
LOG = logging.getLogger(".SeekAndDownload")

class SeekAndDownload :
    def __init__(self, ad81_login, ad81_password):
        self.ad81_login = ad81_login
        self.ad81_password = ad81_password

    def determine_cote_from_url(self, url, path, description):
        LOG.debug("Determine if url needs to be retrieved : " + url)
        o = urlparse(url)
        if o.netloc == "www.archivesdepartementales.puydedome.fr":
            image_url = self.get_image_url_from_AD63(o, path, description)
            return image_url
        if o.netloc == "earchives.cg64.fr":
            image_url = self.get_image_url_from_AD64(o, path, description)
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
            image_url = self.get_image_url_from_AD10(o, url, path, description)
            return image_url
        if o.netloc == "www.archinoe.fr":
            image_url = self.get_image_url_from_AD79(o, path, description)
            return image_url
        if o.netloc == "www.archives43.fr":
            image_url = self.get_image_url_from_AD43(o, url, path, description)
            return image_url
        print
        "Not retrieved :" + url


    def get_image_url_from_ligeo(self, o, path, description, caller, base_url, cache_url, max_page_size, m_x, m_y):
        query_tuple = parse_qs(o.query, keep_blank_values=True)
        image_url = base_url + "/visui.php?DIR=" + ''.join(
            query_tuple["dir"]) + "&CACHE=" + cache_url + "&IMAGE=" + ''.join(query_tuple["image"])  #+ "&SI=img0"
        image_cote = ''.join(query_tuple["cote"])
        image_page = int(''.join(query_tuple["image"])[-max_page_size:])
        image_name = self.generate_filename_and_ensure_not_exists(path, image_cote, image_page, caller, ".jpg", description)
        if (not image_name[1]):
            image = [[PIL.Image.open(cStringIO.StringIO(urllib2.urlopen(
                urllib2.Request(image_url + "&SI=0/img_0" + str(k) + "_0" + str(m), None,
                                {'User-Agent': 'Mozilla/5.0'})).read())) for m in range(0, m_y)] for k in range(0, m_x)]
            size_y = 0;
            size_x = 0;
            for k in range(0, m_x):
                img_w, img_h = image[k][0].size
                size_y += img_w
            for m in range(0, m_y):
                img_w, img_h = image[0][m].size
                size_x += img_h
            background = PIL.Image.new('RGBA', (size_y, size_x), (255, 255, 255, 255))
            size_y = 0;
            size_x = 0;
            img_h = 0
            for k in range(0, m_x):
                for m in range(0, m_y):
                    img_w, img_h = image[k][m].size
                    background.paste(image[k][m], (size_x, size_y))
                    size_y += img_h
                size_x += img_w
                size_y = 0
            background.save(image_name[0])
            return image_name[2], image_cote + " P" + str(image_page), "image/jpeg"

        #----------------------------------------------


    # Data retrieval for AD10 : http://www.archives-aube.fr/arkotheque/etat_civil/index.php
    #----------------------------------------------
    def get_image_url_from_AD10(self, o, url, path, description):
        if o.path.find("/ark:") == 0:
        	# 1. Download the page containing the links
        	# 2. Decode the base64 ark link to determine the correct page
        	# 3. Parse the page's source to determine the jpg's url
        	# 4. Parse the page's source to determine the jpg's identifier
        	# 5. Download the jpg
            cj = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            content = opener.open(url).read()
            reallink_debut = content.find('arko: ') + 7
            reallink_fin = content.find('"',reallink_debut)
            arko = content[reallink_debut:reallink_fin]
            arko_decoded = base64.b64decode(arko)
            page_number_start = arko_decoded.find(';i:')+3
            page_number_end = arko_decoded.find(';',page_number_start)
            page_number = arko_decoded[page_number_start:page_number_end]
            image_link_start = content.find('>' + page_number + '</span>')
            image_link_start = content.find('rel="', image_link_start) + 5
            image_link_end = content.find('"',image_link_start)
            image_link = content[image_link_start:image_link_end]
            id_start = content.find("data-cote=",image_link_end) + 11
            id_end = content.find('"',id_start)
            id = content[id_start:id_end] + '_' + page_number
            image_name = self.generate_filename_and_ensure_not_exists(path, id, None, "AD10", ".jpg", description)
            if (not image_name[1]):
                content = opener.open(image_link).read()
                file = open(image_name[0], "wb")
                file.write(content)
                file.close()
                return image_name[2], id, "image/jpeg"

        else:
            return "Ce format d'url n'est pas supporte pour AD10"


    #----------------------------------------------
    # Data retrieval for AD12 : http://archives.aveyron.fr/archive/recherche/etatcivil/n:22
    #----------------------------------------------
    def get_image_url_from_AD12(self, o, path, description):
        return self.get_image_url_from_ligeo(o, path, description, "AD12", "http://archives.aveyron.fr",
                                             "/home/httpd/ad12/ligeo/app/webroot/data/files/ad12.ligeo/cache/images", 3, 4,
                                             6)


    #----------------------------------------------
    # Data retrieval for AD43 : http://www.archives43.fr/arkotheque/consult_fonds/index.php?ref_fonds=3
    #----------------------------------------------
    def get_image_url_from_AD43(self, o, url, path, description):
        if o.path.find("/arkotheque/visionneuse/print_view.php") == 0:
            doc_id_fin = url.rfind('|')
            doc_id_debut = url[:doc_id_fin].rfind('|') + 1
            page_number = int(url[doc_id_fin + 1:]) + 1
            image_name = self.generate_filename_and_ensure_not_exists(path, url[doc_id_debut:doc_id_fin], page_number,
                                                                      "AD43", ".jpg", description)
            if (not image_name[1]):
                self.get_image_from_arko_ad43(url[doc_id_debut:doc_id_fin], str(page_number), image_name[0])
                return image_name[2], url[doc_id_debut:doc_id_fin] + " P" + str(page_number), "image/jpeg"
        elif o.path.find("/arkotheque/arkotheque_print_archives.php") == 0:
            image_name = self.generate_filename_and_ensure_not_exists(path, "", None, "AD43", ".jpg", description)
            if (not image_name[1]):
                arko_args = url[url.find("arko_args=") + 10:]

                xml_content = urllib2.urlopen(
                    "http://www.archives43.fr/arkotheque/xml_print_image.php?arko_args=" + base64.b64encode(
                        arko_args.replace("%22", '"'))).read()
                offset_cote_debut = xml_content.find("img_titre=") + 11
                offset_cote_fin = xml_content.find('"', offset_cote_debut)
                offset_ref_debut = xml_content.find("img_ref=") + 9
                offset_ref_fin = xml_content.find('"', offset_ref_debut)
                ref = xml_content[offset_ref_debut:offset_ref_fin]

                doc_id_fin = ref.rfind('|')
                doc_id_debut = ref[:doc_id_fin].rfind('|') + 1
                page_number = int(ref[doc_id_fin + 1:]) + 1

                self.get_image_from_arko_ad43(ref[doc_id_debut:doc_id_fin], str(page_number), image_name[0])
                return image_name[2], url[offset_cote_debut:offset_cote_fin] + " P" + str(page_number), "image/jpeg"
        else:
            return "Ce format d'url n'est pas supporte pour AD43"


    def get_image_from_arko_ad43(self, doc_number_str, page_number_str, filename):
        doc_url = "http://www.archives43.fr/arkotheque/arkotheque_visionneuse_archives.php?arko=" + base64.b64encode(
            'a:4:{s:4:"date";s:10:"2013-08-17";s:10:"type_fonds";s:11:"arko_seriel";s:4:"ref1";i:3;s:4:"ref2";i:' + doc_number_str + ';}')
        page_url = "http://www.archives43.fr/arkotheque/visionneuse/ajax_create_img.php?imgSrc=http%3A%2F%2Fwww.archives43.fr%2Farkotheque%2Fvisionneuse%2Fimg_prot.php%3Fi%3D" + page_number_str + ".jpg"

        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        opener.open(doc_url).read()
        content = opener.open(page_url).read()
        file = open(filename, "wb")
        file.write(content)
        file.close()


    #----------------------------------------------
    # Data retrieval for AD48 : http://archives.lozere.fr
    #----------------------------------------------
    def get_image_url_from_AD48(self, o, path, description):
        return self.get_image_url_from_ligeo(o, path, description, "AD48", "http://archives.lozere.fr",
                                             "/home/httpd/ad48/ligeo/app/webroot/data/files/ad48.ligeo/cache/images", 3, 6,
                                             4)


    #----------------------------------------------
    # Data retrieval for AD63 : http://www.archivesdepartementales.puydedome.fr/archives/recherche/etatcivil/n:13
    #----------------------------------------------
    def get_image_url_from_AD63(self, o, path, description):
        return self.get_image_url_from_ligeo(o, path, description, "AD63",
                                             "http://www.archivesdepartementales.puydedome.fr",
                                             "/home/httpd/ad63/portail/app/webroot/data/files//ad63.portail/cache/images",
                                             4, 5, 4)


    #----------------------------------------------
    # Data retrieval for AD64 : http://earchives.cg64.fr/etat-civil-search-form.html
    #----------------------------------------------
    def get_image_url_from_AD64(self, o, path, description):
        offset_debut_id = offset_fin_id = o.path.find(".jpg")
        offset_debut_id = o.path[:offset_debut_id].rfind("/")
        id = o.path[offset_debut_id:offset_fin_id].replace("_", " ")
        image_name = self.generate_filename_and_ensure_not_exists(path, id, None, "AD64", ".jpg", description)
        if (not image_name[1]):
            content = urllib2.urlopen(o.geturl()).read()
            file = open(image_name[0], "wb")
            file.write(content)
            file.close()
            return image_name[2], id, "image/jpeg"


    #----------------------------------------------
    # Data retrieval for AD67 : http://etat-civil.bas-rhin.fr/
    #----------------------------------------------
    def get_image_url_from_AD67(self, o, path, description):
        if o.path.find("/adeloch/cg67_img_load.php") == 0:
            query_tuple = parse_qs(o.query, keep_blank_values=True)
            decoded = base64.b64decode(''.join(query_tuple["arko"]))

            offset_debut_id = offset_fin_id = decoded.find(".JPG")
            offset_debut_id = decoded[:offset_debut_id].rfind("/")
            offset_debut_id = decoded[:offset_debut_id - 1].rfind("/") + 1
            id = decoded[offset_debut_id:offset_fin_id].replace("_", " ").replace("/", ",")

            image_name = self.generate_filename_and_ensure_not_exists(path, id, None, "AD67", ".jpg", description)
            if (not image_name[1]):
                content = urllib2.urlopen(o.geturl()).read()
                file = open(image_name[0], "wb")
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
        if o.path.find("/gramps") == 0:
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
                content = opener.open(
                    "http://www.archinoe.fr/cg79/visu_affiche_util.php?o=TILE&param=visu&x=2920&y=0&l=2600&h=2920&ol=2600&oh=2920&r=0&n=0&b=0&c=0&p=" + page).read()
                # 4. Get the image information
                content = opener.open("http://www.archinoe.fr" + content + ".txt").read()
                match = re.search('(\d+) x (\d+)', content)
                width = match.group(1)
                height = match.group(2)
                # 5. Get the full image link
                content = opener.open(
                    "http://www.archinoe.fr/cg79/visu_affiche_util.php?o=TILE&param=visu&x=0&y=0&l=" + width + "&h=" + height + "&ol=" + width + "&oh=" + height + "&r=0&n=0&b=0&c=0&p=" + page).read()
                # 6. Get the image
                content = opener.open("http://www.archinoe.fr" + content).read()

                file = open(image_name[0], "wb")
                file.write(content)
                file.close()
                return image_name[2], id, "image/jpeg"
        else:
            return "Ce format d'url n'est pas supporte pour AD79"


    #----------------------------------------------
    # Data retrieval for AD81 : http://archives.tarn.fr/
    #----------------------------------------------
    def get_image_url_from_AD81(self, o, path, description):
        ad81_login = self.ad81_login
        ad81_password = self.ad81_password
        if o.path.find("/affichage.php") == 0:
            query_tuple = parse_qs(o.query, keep_blank_values=True)
            image = ''.join(query_tuple["image"])
            offset1 = image.rfind("/")
            offset2 = image.find(".JPG")
            if offset2 == -1:
                offset2 = image.find(".jpg")
            offset3 = image[:offset1].rfind("/")

            image_name = self.generate_filename_and_ensure_not_exists(path, image[offset3 + 1:offset1],
                                                                      int(image[offset2 - 3:offset2]), "AD81", ".jpg",
                                                                      description)
            if (not image_name[1]):

                cj = cookielib.CookieJar()
                opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
                opener.open("http://archivesenligne.tarn.fr/login.php?base=").read()
                http_header = {
                    "Content-type": "application/x-www-form-urlencoded",
                }
                opener.open(urllib2.Request("http://archivesenligne.tarn.fr/login_do.php",
                                            "LOGIN=" + ad81_login + "&PASSWORD=" + ad81_password + "&base=&envoyer.x=110&envoyer.y=4",
                                            http_header)).read()
                content = opener.open(o.geturl()).read()
                # Extract the JPG from the PDF
                stream_offset_start = content.rfind("\nstream\n")
                stream_offset_end = content.rfind("\nendstream\n")
                if (stream_offset_start != -1 and stream_offset_end != -1 ):
                    file = open(image_name[0], "wb")
                    file.write(content[stream_offset_start + 8:stream_offset_end])
                    file.close()
                    return image_name[2], image[offset3 + 1:offset1], "image/jpeg"
                return "Erreur lors de la recuperation des donnees pour AD81. Verifier le login/mdp."
        else:
            return "Ce format d'url n'est pas supporte pour AD81"


    def generate_filename_and_ensure_not_exists(self, path, cote, page, ad, extension, description):
        if page == None:
            if cote == "":
                filename = self.remove_forbidden_characters(description) + "," + ad + extension
            else:
                filename = self.remove_forbidden_characters(
                    description) + "," + ad + " " + self.remove_forbidden_characters(cote) + extension
        else:
            filename = self.remove_forbidden_characters(description) + "," + ad + " " + self.remove_forbidden_characters(
                cote) + "P" + str(page) + extension
        if not os.path.exists(path):
            os.makedirs(path)
        return path + os.sep + filename, os.path.exists(path + os.sep + filename), filename


    def remove_forbidden_characters(self, input):
        # Only windows characters.
        return input.replace("/", "-").replace("\\", "-").replace("<", "-").replace(">", "-").replace(":", "-").replace('"',
                                                                                                                        "-").replace(
            '|', "-").replace('?', "-").replace('*', "-")


if __name__ == "__main__":
    import sys
    downloader = SeekAndDownload(sys.argv[1], sys.argv[2])
    folder = "/tmp"

    urls = [["aube", "http://www.archives-aube.fr/ark:/42751/s00556835d4834b6/556835d4969d0"], 
            #["aveyron", "http://archives.aveyron.fr/archive/permalink?image=FRAD012_EC_000184_4E025977_005&dir=%2Fhome%2Fhttpd%2Fad12%2Fligeo%2Fapp%2F%2Fwebroot%2Fdata%2Ffiles%2Fad12.ligeo%2Fimages%2FFRAD012_EC%2FFRAD012_EC_000184%2FFRAD012_EC_000184_4E025977&cote=4E157-31"],
            #["basrhin", "http://etat-civil.bas-rhin.fr/adeloch/cg67_img_load.php?arko=YTo0OntzOjQ6InJlZjEiO2k6NDM3NDtzOjQ6InJlZjIiO2k6OTtzOjQ6InJlZjMiO3M6NzI6Ii9kYXRhL251bWVyaXNhdGlvbi9BRDY3X0VDX1JFVl8wMDAwLzRfRV8wMDlfMDA3L0FENjdfRUNfMDA5MDI2MDAwMDAxLkpQRyI7czo4OiJyZWZfc2VzcyI7czozMjoiOGFlYTMyOTM3ZmM3MjdhMDE5NjYwYzRhNjIxMjcwNTAiO30=&oh=1"],
            #["deuxsevres", "http://www.archinoe.fr/gramps?id=790002444&p=100"],
            #["hauteloire", "http://www.archives43.fr/arkotheque/visionneuse/print_view.php?width=1124&height=717&top=0&left=-229.671875&tw=1584&th=727&bri=0&cont=0&inv=0&rot=F&imgSrc=http%3A%2F%2Fwww.archives43.fr%2Farkotheque%2Fvisionneuse%2Fimg_prot.php%3Fi%3D31.jpg&tit=Le%20Puy-en-Velay%201881%201881%20&cot=6%20E%20178%2F238%20&ref=ark|3|2640|2640|30"],
            #["hauteloireold", "http://www.archives43.fr/arkotheque/arkotheque_print_archives.php?arko_args=a:2:{s:10:%22zoomdepart%22;d:43.8712493180578;s:10:%22img_ref_id%22;s:19:%22ark|3|3794|3794|464%22;}"],
            #["lozere", "http://archives.lozere.fr/archive/permalink?image=e0000383&dir=%2Fhome%2Fhttpd%2Fad48%2Fligeo%2Fapp%2F%2Fwebroot%2Fdata%2Ffiles%2Fad48.ligeo%2Fimages%2FEtatCivil%2Fjpeg%2F4e184001&cote=4%20E%20184%2F1"],
            #["puydedome", "http://www.archivesdepartementales.puydedome.fr/archives/permalink?image=FRAD063_6E456_00010_0053&dir=%2Fhome%2Fhttpd%2Fad63%2Fportail%2Fapp%2F%2Fwebroot%2Fdata%2Ffiles%2F%2Fad63.portail%2Fimages%2FFRAD063_000050001_6%2FFRAD063_6E456%2FFRAD063_6E456_00010&cote=6%20E%20456%2F10"],
            #["pyreneeatlantique", "http://earchives.cg64.fr/img-server/FRAD064003_IR0002/LARUNS_1/5MI320-2/FRAD064012_5MI320_2_0218.jpg"],
            #["tarn", "http://archivesenligne.tarn.fr/affichage.php?image=/archives/4E/EC000448/4E08600606/810860013.jpg"]
            ]

    for url in urls:
        print downloader.determine_cote_from_url(url[1],folder,url[0])