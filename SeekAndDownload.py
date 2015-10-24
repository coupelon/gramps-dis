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
import urllib.request
import urllib.parse
from io import BytesIO
import http.cookiejar
import os
import PIL.Image
import re

import logging
LOG = logging.getLogger(".SeekAndDownload")

class SeekAndDownload :
    def determine_cote_from_url(self, url, path, description):
        LOG.debug("Determine if url needs to be retrieved : " + url)
        o = urllib.parse.urlparse(url)
        if o.netloc == "www.archivesdepartementales.puydedome.fr":
            image_url = self.get_image_url_from_AD63(o, url, path, description)
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

    def download_images_from_ligeo(self, o, path, description, caller, image_url, image_cote, image_page, m_x, m_y):
        image_name = self.generate_filename_and_ensure_not_exists(path, image_cote, image_page, caller, ".jpg", description)
        if (not image_name[1]):
            image = [[PIL.Image.open(BytesIO(urllib.request.urlopen(
                urllib.request.Request(image_url + "&SI=0/img_0" + str(k) + "_0" + str(m), None,
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
        return self.get_image_url_from_arko(o, url, path, description, 'AD10')


    # Data retrieval for AD10 : http://www.archives-aube.fr/arkotheque/etat_civil/index.php
    #----------------------------------------------
    def get_image_url_from_arko(self, o, url, path, description, source, licence=None):
        if o.path.find("/ark:") == 0:
            # 1. Download the page containing the links
            # 2. Decode the base64 ark link to determine the correct page
            # 3. Parse the page's source to determine the jpg's url
            # 4. Parse the page's source to determine the jpg's identifier
            # 5. Download the jpg
            cj = http.cookiejar.CookieJar()
            opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
            content = opener.open(url).read()
            licence_start = content.find(b'licence_clic_cartouche')
            if licence != None:
                licence_url_start = content.find(b'data-redirect=',licence_start) + 15
                licence_url_end = content.find(b"'",licence_url_start)
                licence_url = content[licence_url_start:licence_url_end].decode("utf-8")
                LOG.info("arko: licence accepted : " + licence_url)
                licence_id_start = content.find(b'data-licence=',licence_start) + 14
                licence_id_end = content.find(b"'",licence_id_start)
                licence_id = content[licence_id_start:licence_id_end]
                LOG.info(b"arko: licence id : " + licence_id)
                opener.open(licence, data=b"id="+licence_id)
                content = opener.open(licence_url).read()
            LOG.debug(b"arko content: " + content)
            reallink_debut = content.find(b'arko: ') + 7
            reallink_fin = content.find(b'"',reallink_debut)
            arko = content[reallink_debut:reallink_fin]
            LOG.debug(b"arko: real_link: " + arko)
            arko_decoded = base64.b64decode(arko).decode("utf-8")
            LOG.debug("arko_decoded: " + arko_decoded)
            page_number_start = arko_decoded.find(';i:')+3
            page_number_end = arko_decoded.find(';',page_number_start)
            page_number = str.encode(arko_decoded[page_number_start:page_number_end])
            LOG.debug(b"arko: page_number: " + page_number)
            image_link_start = content.find(b'>' + page_number + b'</span>')
            if image_link_start > 0:
                image_link_start = content.find(b'rel="', image_link_start) + 5
            else:
                image_link_start = content.find(b'thumb_active" rel="') + 19
            image_link_end = content.find(b'"',image_link_start)
            image_link = content[image_link_start:image_link_end].decode("utf-8")
            LOG.debug("arko: image_link: " + image_link)
            id_start = content.find(b"data-cote=",image_link_end) + 11
            id_end = content.find(b'"',id_start)
            id = (content[id_start:id_end] + b'_' + page_number).decode("utf-8", errors='ignore')
            image_name = self.generate_filename_and_ensure_not_exists(path, id, None, source, ".jpg", description)
            if (not image_name[1]):
                content = opener.open(image_link).read()
                file = open(image_name[0], "wb")
                file.write(content)
                file.close()
                return image_name[2], id, "image/jpeg"

        else:
            return "Ce format d'url n'est pas supporte pour " + source


    #----------------------------------------------
    # Data retrieval for AD12 : http://archives.aveyron.fr/archive/recherche/etatcivil/n:22
    #----------------------------------------------
    def get_image_url_from_AD12(self, o, path, description):
        #return self.get_image_url_from_ligeo(o, path, description, "AD12", "http://archives.aveyron.fr",
        #                                     "/home/httpd/ad12/ligeo/app/webroot/data/files/ad12.ligeo/cache/images", 3, 4,
        #                                     6)
        return "AD12 no more supported"


    #----------------------------------------------
    # Data retrieval for AD43 : http://www.archives43.fr/arkotheque/consult_fonds/index.php?ref_fonds=3
    #----------------------------------------------
    def get_image_url_from_AD43(self, o, url, path, description):
        return self.get_image_url_from_arko(o, url, path, description, 'AD43', "http://www.archives43.fr/arkotheque/licence_clic_accepter.php")

    #----------------------------------------------
    # Data retrieval for AD48 : http://archives.lozere.fr/archive/recherche/etatcivil/n:88
    #----------------------------------------------
    def get_image_url_from_AD48(self, o, path, description):
        #return self.get_image_url_from_ligeo(o, path, description, "AD48", "http://archives.lozere.fr",
        #                                     "/home/httpd/ad48/ligeo/app/webroot/data/files/ad48.ligeo/cache/images", 3, 6,
        #                                     4)
        return "AD48 no more supported"


    #----------------------------------------------
    # Data retrieval for AD63 : http://www.archivesdepartementales.puydedome.fr/archives/recherche/etatcivil/n:13
    #----------------------------------------------
    def get_image_url_from_AD63(self, o, url, path, description):
        if o.path.find("/ark:") == 0:
            content = urllib.request.urlopen(urllib.request.Request(url, None, {'User-Agent': 'Mozilla/5.0'})).read()
            xmlinfo_debut = content.find(b"xmlFile") + 12
            xmlinfo_fin = content.find(b'"', xmlinfo_debut)
            LOG.debug(b"xmlFile: " + content[xmlinfo_debut:xmlinfo_fin])
            content = urllib.request.urlopen(urllib.request.Request(content[xmlinfo_debut:xmlinfo_fin].decode("utf-8"), None, {'User-Agent': 'Mozilla/5.0'})).read()
            dir_debut = content.find(b"<dir>") + 5
            dir_end = content.find(b"<",dir_debut)
            dir_name = content[dir_debut:dir_end].decode("utf-8")
            LOG.debug("dir: " + dir_name)
            image_index_end = content.find(str.encode(url))
            image_index_start = content.rfind(b'<name>',0,image_index_end) + 6
            image_index_end =  content.find(b"<",image_index_start)
            image_cote = content[image_index_start:image_index_end].decode("utf-8")
            LOG.debug("image: " + image_cote)
            image_page_start = url.rfind('/') + 1
            image_page = int(url[image_page_start:])
            image_url = "http://www.archivesdepartementales.puydedome.fr/visui.php?DIR=" + dir_name + "&CACHE=/home/httpd/ad63/portail/app/webroot/data/files//ad63.portail/cache/images&IMAGE=" + image_cote
            return self.download_images_from_ligeo(o, path, description, "AD63", image_url, image_cote, image_page, 5, 4)

        query_tuple = urllib.parse.parse_qs(o.query, keep_blank_values=True)
        image_url = "http://www.archivesdepartementales.puydedome.fr" + "/visui.php?DIR=" + ''.join(
            query_tuple["dir"]) + "&CACHE=" + "/home/httpd/ad63/portail/app/webroot/data/files//ad63.portail/cache/images" + "&IMAGE=" + ''.join(query_tuple["image"])  #+ "&SI=img0"
        image_cote = ''.join(query_tuple["cote"])
        image_page = int(''.join(query_tuple["image"])[-4:])
        return self.download_images_from_ligeo(o, path, description, "AD63", image_url, image_cote, image_page, 5, 4)


    #----------------------------------------------
    # Data retrieval for AD64 : http://earchives.cg64.fr/etat-civil-search-form.html
    #----------------------------------------------
    def get_image_url_from_AD64(self, o, path, description):
        offset_debut_id = offset_fin_id = o.path.find(".jpg")
        offset_debut_id = o.path[:offset_debut_id].rfind("/")
        id = o.path[offset_debut_id:offset_fin_id].replace("_", " ")
        image_name = self.generate_filename_and_ensure_not_exists(path, id, None, "AD64", ".jpg", description)
        if (not image_name[1]):
            content = urllib.request.urlopen(o.geturl()).read()
            file = open(image_name[0], "wb")
            file.write(content)
            file.close()
            return image_name[2], id, "image/jpeg"


    #----------------------------------------------
    # Data retrieval for AD67 : http://etat-civil.bas-rhin.fr/
    #----------------------------------------------
    def get_image_url_from_AD67(self, o, path, description):
        if o.path.find("/adeloch/cg67_img_load.php") == 0:
            query_tuple = urllib.parse.parse_qs(o.query, keep_blank_values=True)
            decoded = base64.b64decode(''.join(query_tuple["arko"])).decode("utf-8")

            offset_debut_id = offset_fin_id = decoded.find(".JPG")
            offset_debut_id = decoded[:offset_debut_id].rfind("/")
            offset_debut_id = decoded[:offset_debut_id - 1].rfind("/") + 1
            id = decoded[offset_debut_id:offset_fin_id].replace("_", " ").replace("/", ",")

            image_name = self.generate_filename_and_ensure_not_exists(path, id, None, "AD67", ".jpg", description)
            if (not image_name[1]):
                content = urllib.request.urlopen(o.geturl()).read()
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
            query_tuple = urllib.parse.parse_qs(o.query, keep_blank_values=True)
            id = ''.join(query_tuple["id"])
            page = ''.join(query_tuple["p"])

            image_name = self.generate_filename_and_ensure_not_exists(path, id, None, "AD79", ".jpg", description)
            if (not image_name[1]):
                cj = http.cookiejar.CookieJar()
                opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

                # 1. Get Session ID
                opener.open("http://www.archinoe.fr/cg79/registre_prepare.php?id=" + id).read()
                # 2. Get to the right archive
                opener.open("http://www.archinoe.fr/cg79/registre_prepare.php?id=" + id).read()
                # 3. Get the image location
                content = opener.open(
                    "http://www.archinoe.fr/cg79/visu_affiche_util.php?o=TILE&param=visu&x=2920&y=0&l=2600&h=2920&ol=2600&oh=2920&r=0&n=0&b=0&c=0&p=" + page).read().decode("utf-8")
                # 4. Get the image information
                content = opener.open("http://www.archinoe.fr" + content + ".txt").read().decode("utf-8")
                match = re.search('(\d+) x (\d+)', content)
                width = match.group(1)
                height = match.group(2)
                # 5. Get the full image link
                content = opener.open(
                    "http://www.archinoe.fr/cg79/visu_affiche_util.php?o=TILE&param=visu&x=0&y=0&l=" + width + "&h=" + height + "&ol=" + width + "&oh=" + height + "&r=0&n=0&b=0&c=0&p=" + page).read().decode("utf-8")
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
        if o.path.find("/affichage.php") == 0:
            query_tuple = urllib.parse.parse_qs(o.query, keep_blank_values=True)
            try:
                image = ''.join(query_tuple["url_image"])
                downloadableurl = o.geturl()
            except KeyError:
                image = ''.join(query_tuple["image"])
                downloadableurl = o.geturl().replace("image=", "url_image=")
            offset1 = image.rfind("/")
            offset2 = image.find(".JPG")
            if offset2 == -1:
                offset2 = image.find(".jpg")
            offset3 = image[:offset1].rfind("/")

            image_name = self.generate_filename_and_ensure_not_exists(path, image[offset3 + 1:offset1],
                                                                      int(image[offset2 - 3:offset2]), "AD81", ".jpg",
                                                                      description)
            if (not image_name[1]):
                content = urllib.request.urlopen(downloadableurl).read()
                # Extract the JPG from the PDF
                stream_offset_start = content.rfind(b"\nstream\n")
                stream_offset_end = content.rfind(b"\nendstream\n")
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
    downloader = SeekAndDownload()
    logging.basicConfig(level=logging.DEBUG)
    folder = "/tmp"

    urls = [#["aube", "http://www.archives-aube.fr/ark:/42751/s00556835d4834b6/556835d4969d0"], 
            #["aveyron", "http://archives.aveyron.fr/archive/permalink?image=FRAD012_EC_000184_4E025977_005&dir=%2Fhome%2Fhttpd%2Fad12%2Fligeo%2Fapp%2F%2Fwebroot%2Fdata%2Ffiles%2Fad12.ligeo%2Fimages%2FFRAD012_EC%2FFRAD012_EC_000184%2FFRAD012_EC_000184_4E025977&cote=4E157-31"],
            #["basrhin", "http://etat-civil.bas-rhin.fr/adeloch/cg67_img_load.php?arko=YTo0OntzOjQ6InJlZjEiO2k6NDM3NDtzOjQ6InJlZjIiO2k6OTtzOjQ6InJlZjMiO3M6NzI6Ii9kYXRhL251bWVyaXNhdGlvbi9BRDY3X0VDX1JFVl8wMDAwLzRfRV8wMDlfMDA3L0FENjdfRUNfMDA5MDI2MDAwMDAxLkpQRyI7czo4OiJyZWZfc2VzcyI7czozMjoiOGFlYTMyOTM3ZmM3MjdhMDE5NjYwYzRhNjIxMjcwNTAiO30=&oh=1"],
            #["deuxsevres", "http://www.archinoe.fr/gramps?id=790002444&p=100"],
            #["hauteloire", "http://www.archives43.fr/arkotheque/visionneuse/print_view.php?width=1124&height=717&top=0&left=-229.671875&tw=1584&th=727&bri=0&cont=0&inv=0&rot=F&imgSrc=http%3A%2F%2Fwww.archives43.fr%2Farkotheque%2Fvisionneuse%2Fimg_prot.php%3Fi%3D31.jpg&tit=Le%20Puy-en-Velay%201881%201881%20&cot=6%20E%20178%2F238%20&ref=ark|3|2640|2640|30"],
            #["hauteloire", "http://www.archives43.fr/ark:/47539/s005396cd5d60165/5396cdb91d0dc"], 
            #["hauteloireold", "http://www.archives43.fr/arkotheque/arkotheque_print_archives.php?arko_args=a:2:{s:10:%22zoomdepart%22;d:43.8712493180578;s:10:%22img_ref_id%22;s:19:%22ark|3|3794|3794|464%22;}"],
            #["lozere", "http://archives.lozere.fr/archive/permalink?image=e0000383&dir=%2Fhome%2Fhttpd%2Fad48%2Fligeo%2Fapp%2F%2Fwebroot%2Fdata%2Ffiles%2Fad48.ligeo%2Fimages%2FEtatCivil%2Fjpeg%2F4e184001&cote=4%20E%20184%2F1"],
            #["lozere", "http://archives.lozere.fr/ark:/24967/vta54d8f60262f63/daogrp/0/layout:table/idsearch:RECH_d4cdafe331afb5bbe0db09e08cb7607e#id:534026049"],
            ["puydedome", "http://www.archivesdepartementales.puydedome.fr/archives/permalink?image=FRAD063_6E456_00010_0053&dir=%2Fhome%2Fhttpd%2Fad63%2Fportail%2Fapp%2F%2Fwebroot%2Fdata%2Ffiles%2F%2Fad63.portail%2Fimages%2FFRAD063_000050001_6%2FFRAD063_6E456%2FFRAD063_6E456_00010&cote=6%20E%20456%2F10"],
            #["pyreneeatlantique", "http://earchives.cg64.fr/img-server/FRAD064003_IR0002/LARUNS_1/5MI320-2/FRAD064012_5MI320_2_0218.jpg"],
            #["hl1","http://www.archives43.fr/ark:/47539/s0053902639b9754/53902663994f1"],
            ["pd1","http://www.archivesdepartementales.puydedome.fr/ark:/72847/vta54624d9839777/daogrp/0/43"]
            #["tarn", "http://archivesenligne.tarn.fr/affichage.php?image=/archives/4E/EC000448/4E08600606/810860013.jpg"]
            ]

    for url in urls:
        print(downloader.determine_cote_from_url(url[1],folder,url[0]))