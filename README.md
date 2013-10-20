Pr�sentation
============
Ce projet est un plugin pour Gramps qui doit permettre l'extraction et le stockage des pages d'archives correspondant aux anc�tres d'un arbre.
En effet, avec la d�mocratisation des archives d�partementales en lignes, il est commun d'effectuer ses recherche int�gralement depuis son domicile.
Pour la p�rennit� des recherches effectu�es, nombre de g�n�alogistes enregistre les coordonn�es des informations consult�es (Type et num�ro d'acte, num�ro de page), afin d'�tre en mesure d'y retourner par la suite. Ces �tapes, indispensables pour beaucoup, sont fortement d�pendantes de la disponibilit� des sites d'archives, dans l'imm�diat et sur le long terme.
Ce plugin permet simplement de conserver une copie, comme la prise de photos en salle d'archive, des documents concernant vos anc�tres.

Mise en garde
=============
Comme pr�cis� au lancement du plugin, l'utilisation d'un tel outil peut �tre contraire aux conditions d'utilisation des sites d'archives d�partementales. En tout �tat de cause, il incombe � chaque utilisateur de prendre connaissance de ces conditions d'utilisation, et d'en r�f�rer aux archives utilis�es en cas de doute. 
En outre, l'utilisation du plugin n'est pas triviale, car tous les sites ne facilitent pas cette extraction. Il est souvent n�cessaire de mettre � jour le plugin pour avoir � sa disposition les derniers algorithmes d'extraction, les sites �tant modifi�s par leurs auteurs sans pr�avis.

Appel � contribution
====================
Le maintient des algorithmes d'extraction est un travail long �tant donn� le nombre de sites vis�s. Toute aide est la bienvenue, ce travail �tant plus facilement effectu�s par les personnes disposant
1. de recherches r�elles sur les site concernant, ce qui permet de balayer tous les types d'actes et de documents, et donc d'obtenir un algorithme le plus g�n�rique possible
2. de connaissance en d�veloppement informatique. Ce plugin est d�velopp� en Python, langage puissant � la fois adapt� aux d�butants et aux d�veloppeurs exp�riment�s.
Pour toute information, contactez moi : olivier [arob@se] coupelon.net

Installation
============
L'installation du plugin revient � un simple copier/coller dans le dossier utilisateur de Gramps. Il faut donc avoir ex�cuter au moins une fois Gramps pour que ce dernier existe. Il contient un dossier plugins, dans lequel les fichiers *.py doivent �tre copi�s.
Sous windows 7, le dossier se trouve g�n�ralement � l'emplacement : _C:\Users\<nom_d'utilisateur>\AppData\Roaming\gramps\gramps34\plugins_.

Utilisation du plugin
=====================
L'utilisation de ce plugin est complexe. En pratique, il n'existe pas actuellement de moyen standard pour enregistrer les informations n�cessaires � l'extraction des pages recherch�es. La convention adopt�e par le plugin est donc la suivante.

Enregistrement pour chaque individu d'un lien vers la page
----------------------------------------------------------
Pour associer une page d'acte � un individu, il est n�cessaire d'enregistrer une adresse internet correspondant � celle qui sera utilis�e par l'algorithme lors de l'extraction. L'adresse de cette page peut parfois n�cessiter des outils suppl�mentaires, car les adresses recherch�es, qui permettent d'acceder directement � la page d'acte qui nous int�resse, ne sont pas toujours expos�es directement par les sites web. C'est notamment le cas des sites d'archives qui ne comporte pas de liens 'permanents', qui ont pour fonction de retourner directement sur une page visit�e, une sorte de marque page. Les d�tails permettant pour chaque site d'enregistrer une adresse utilisable par le plugin sont donn�s dans la section 'Guide des archives couvertes par le plugin'.

Execution de l'extraction
-------------------------
Une fois les liens cr��s pour les individus, il faut executer le plugin qui va alors, pour chaque individu :
* Explorer les liens internet disponibles
* V�rifier que pour cette personne, ce lien et cette description, qu'un fichier n'existe pas d�j�
* T�l�charger l'image de la page
* Enregistrer cette image dans la galerie de cet indidu.

Couverture de la version actuelle
=================================
La version actuelle couvre les sites d'archives d�partementales suivants.

43 Haute Loire
--------------
Site: : http://www.archives43.fr

63 Puy-de-d�me
--------------
Site : http://www.archivesdepartementales.puydedome.fr

Test du plugin
==============
Le plugin, pour �tre test�, utilise une base de d�monstration disponible dans le dossier test de ce projet.
