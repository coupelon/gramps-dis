Présentation
============
Ce projet est un plugin pour Gramps qui doit permettre l'extraction et le stockage des pages d'archives correspondant aux ancètres d'un arbre.
En effet, avec la démocratisation des archives départementales en lignes, il est commun d'effectuer ses recherche intégralement depuis son domicile.
Pour la pérennité des recherches effectuées, nombre de généalogistes enregistre les coordonnées des informations consultées (Type et numéro d'acte, numéro de page), afin d'être en mesure d'y retourner par la suite. Ces étapes, indispensables pour beaucoup, sont fortement dépendantes de la disponibilité des sites d'archives, dans l'immédiat et sur le long terme.
Ce plugin permet simplement de conserver une copie, comme la prise de photos en salle d'archive, des documents concernant vos ancêtres.

Mise en garde
=============
Comme précisé au lancement du plugin, l'utilisation d'un tel outil peut être contraire aux conditions d'utilisation des sites d'archives départementales. En tout état de cause, il incombe à chaque utilisateur de prendre connaissance de ces conditions d'utilisation, et d'en référer aux archives utilisées en cas de doute. 
En outre, l'utilisation du plugin n'est pas triviale, car tous les sites ne facilitent pas cette extraction. Il est souvent nécessaire de mettre à jour le plugin pour avoir à sa disposition les derniers algorithmes d'extraction, les sites étant modifiés par leurs auteurs sans préavis.

Appel à contribution
====================
Le maintient des algorithmes d'extraction est un travail long étant donné le nombre de sites visés. Toute aide est la bienvenue, ce travail étant plus facilement effectués par les personnes disposant
1. de recherches réelles sur les site concernant, ce qui permet de balayer tous les types d'actes et de documents, et donc d'obtenir un algorithme le plus générique possible
2. de connaissance en développement informatique. Ce plugin est développé en Python, langage puissant à la fois adapté aux débutants et aux développeurs expérimentés.
Pour toute information, contactez moi : olivier [arob@se] coupelon.net

Installation
============
L'installation du plugin revient à un simple copier/coller dans le dossier utilisateur de Gramps. Il faut donc avoir exécuter au moins une fois Gramps pour que ce dernier existe. Il contient un dossier plugins, dans lequel les fichiers *.py doivent être copiés.
Sous windows 7, le dossier se trouve généralement à l'emplacement : _C:\Users\<nom_d'utilisateur>\AppData\Roaming\gramps\gramps34\plugins_.

Utilisation du plugin
=====================
L'utilisation de ce plugin est complexe. En pratique, il n'existe pas actuellement de moyen standard pour enregistrer les informations nécessaires à l'extraction des pages recherchées. La convention adoptée par le plugin est donc la suivante.

Enregistrement pour chaque individu d'un lien vers la page
----------------------------------------------------------
Pour associer une page d'acte à un individu, il est nécessaire d'enregistrer une adresse internet correspondant à celle qui sera utilisée par l'algorithme lors de l'extraction. L'adresse de cette page peut parfois nécessiter des outils supplémentaires, car les adresses recherchées, qui permettent d'acceder directement à la page d'acte qui nous intéresse, ne sont pas toujours exposées directement par les sites web. C'est notamment le cas des sites d'archives qui ne comporte pas de liens 'permanents', qui ont pour fonction de retourner directement sur une page visitée, une sorte de marque page. Les détails permettant pour chaque site d'enregistrer une adresse utilisable par le plugin sont donnés dans la section 'Guide des archives couvertes par le plugin'.

Execution de l'extraction
-------------------------
Une fois les liens créés pour les individus, il faut executer le plugin qui va alors, pour chaque individu :
* Explorer les liens internet disponibles
* Vérifier que pour cette personne, ce lien et cette description, qu'un fichier n'existe pas déjà
* Télécharger l'image de la page
* Enregistrer cette image dans la galerie de cet indidu.

Couverture de la version actuelle
=================================
La version actuelle couvre les sites d'archives départementales suivants.

43 Haute Loire
--------------
Site: : http://www.archives43.fr

63 Puy-de-dôme
--------------
Site : http://www.archivesdepartementales.puydedome.fr

Test du plugin
==============
Le plugin, pour être testé, utilise une base de démonstration disponible dans le dossier test de ce projet.
