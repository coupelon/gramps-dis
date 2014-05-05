## Présentation
Ce projet est un plugin pour Gramps (http://gramps-project.org/) qui doit permettre l'extraction et le stockage des pages d'archives correspondant individus d'un arbre généalogique.
En effet, avec la démocratisation des archives départementales en lignes, il est commun d'effectuer ses recherches intégralement sur internet.
Pour la pérennité des recherches effectuées, nombre de généalogistes enregistrent les coordonnées des informations consultées (Type et numéro d'acte, numéro de page...), afin d'être en mesure d'y retourner par la suite. Ces étapes, indispensables pour beaucoup, sont fortement dépendantes de la disponibilité des sites d'archives, dans l'immédiat et sur le long terme.
Ce plugin permet simplement de conserver une copie, comme la prise de photos en salle d'archive, des documents concernant vos ancêtres.

## Mise en garde et conditions d'utilisation
L'utilisation d'un tel outil peut être contraire aux conditions d'utilisation des sites d'archives départementales. En tout état de cause, il incombe à chaque utilisateur de prendre connaissance de ces conditions d'utilisation, et de se référer aux archives utilisées en cas de doute. 
En outre, l'utilisation du plugin n'est pas triviale, car tous les sites ne facilitent pas cette extraction. Il est souvent nécessaire de mettre à jour le plugin pour avoir à sa disposition les derniers algorithmes d'extraction, les sites étant modifiés par leurs auteurs sans préavis.

**Aucune garantie n'est fournie quant au fonctionnement d'une extraction.**

## Appel à contribution
Le maintien des algorithmes d'extraction est un travail long étant donné le nombre de sites visés. Toute aide est la bienvenue, ce travail étant plus facilement effectué par les personnes disposant :
1. de recherches réelles sur les sites concernés, ce qui permet de balayer tous les types d'actes et de documents, et donc d'obtenir un algorithme le plus générique possible
2. de connaissance en développement informatique. Ce plugin est développé en Python, langage puissant à la fois adapté aux débutants et aux développeurs expérimentés.
Pour toute information, contactez moi : olivier [arob@se] coupelon.net

## Installation
L'installation du plugin revient à un simple copier/coller dans le dossier utilisateur de Gramps. Il faut donc avoir exécuté au moins une fois Gramps pour que ce dernier existe. Il contient un dossier plugins, dans lequel les fichiers *.py de ce projet doivent être copiés.
Sous windows 7, le dossier se trouve généralement à l'emplacement : _C:\Users\<utilisateur>\AppData\Roaming\gramps\gramps40\plugins_.
Sous linux, le dossier est généralement : _/home/<utilisateur>/.gramps/gramps40/plugins/_.

## Utilisation du plugin
L'utilisation de ce plugin est complexe. En pratique, il n'existe pas actuellement de moyen standard pour enregistrer les informations nécessaires à l'extraction des pages recherchées. La convention adoptée par le plugin est donc la suivante.

### Enregistrement pour chaque individu d'un lien vers la page
Pour associer une page d'acte à un individu, il est nécessaire d'enregistrer une adresse internet correspondant à celle qui sera utilisée par l'algorithme lors de l'extraction (voir figure ci-dessous). L'adresse de cette page peut parfois nécessiter des outils supplémentaires, car les adresses recherchées, qui permettent d'accéder directement à la page d'acte qui nous intéresse, ne sont pas toujours exposées directement par les sites web. C'est notamment le cas des sites d'archives qui ne comporte pas de liens 'permanents', qui ont pour fonction de retourner directement sur une page visitée, une sorte de marque page. Les détails pour chaque site permettant d'enregistrer une adresse utilisable par le plugin sont donnés dans la section 'Guide des archives couvertes par le plugin'.

![alt text](https://github.com/coupelon/gramps-dis/raw/master/images/gramps_saisie_site_internet.png "Saisie d'un site internet pour un individu, correspondant à l'extrait d'acte à conserver")

### Exécution de l'extraction
Une fois les liens créés pour les individus, il faut exécuter le plugin qui va alors, pour chaque individu :

1. Explorer les liens internet disponibles

2. Vérifier que pour cette personne, ce lien et cette description, qu'un fichier n'existe pas déjà

3. Télécharger l'image de la page

4. Enregistrer cette image dans la galerie de cet indidu.

## Guide des archives couvertes par le plugin
La version actuelle (1.1.1 du 05/05/2014) couvre les sites d'archives départementales suivants.


### 10 Aube
Site : http://www.archives-aube.fr

Extraction du lien d'un acte : Le site des archives de l'aube offre un bouton de téléchargement direct des actes en JPG, ce qui est peut être utilisé pour intégrer à la main des actes. Le plugin peut toutefois effectuer cette opération pour vous de la manière suivante. Il faut cliquer sur le bouton impression disponible sur la page souhaitée. Une nouvelle fenêtre s'ouvre alors dans la navigateur, il faut copier l'adresse de cette page, généralement située dans la barre d'adresse en haut de l'écran.

### 12 Aveyron
Site : http://archives.aveyron.fr

Extraction du lien d'un acte : Une fois sur la page à conserver, il suffit de copier le lien permanent disponible en haut à droite :

![alt text](https://github.com/coupelon/gramps-dis/raw/master/images/permalien_ligeo.png "Lien permanent AD12")

### 43 Haute Loire
Site : http://www.archives43.fr

Note : Les administrateurs du site travaillent à l'ajout d'un lien permanent, ce qui devrait faciliter les opérations.

Extraction du lien d'un acte : Pour trouver le lien permanent d'une page, il faut une fois sur cette dernière cliquer sur le bouton d'impression du site. Une nouvelle fenêtre s'ouvre alors dans la navigateur, il faut copier l'adresse de cette page, généralement située dans la barre d'adresse en haut de l'écran.

### 48 Lozère
Site : http://archives.lozere.fr

Extraction du lien d'un acte : Une fois sur la page à conserver, il suffit de copier le lien permanent disponible en haut à droite :

![alt text](https://github.com/coupelon/gramps-dis/raw/master/images/permalien_ligeo.png "Lien permanent AD48")

### 63 Puy-de-dôme
Site : http://www.archivesdepartementales.puydedome.fr

Extraction du lien d'un acte : Une fois sur la page à conserver, il suffit de copier le lien permanent disponible en haut à droite :

![alt text](https://github.com/coupelon/gramps-dis/raw/master/images/permalien_ligeo.png "Lien permanent AD63")

### 67 Bas-Rhin
Site : http://etat-civil.bas-rhin.fr/

Extraction du lien d'un acte : Une fois sur la page à conserver, il faut activer dans le navigateur web le mode d'analyse réseau. Voir la section 'Analyse réseau'. Il faut ensuite cliquer sur Imprimer, une adresse apparait alor dans l'analyseur réseau, il faut copier cette adresse.

### 79 Deux-Sèvres
Site : http://archives.deux-sevres.com/Archives79/default.aspx

Extraction du lien d'un acte : Le site ne dispose pas de liens permanent, mais permet d'exporter durant la session courante une page en PDF ou JPG. Il est néanmoins possible d'extraire un lien d'acte de la manière suivante. Il faut tout d'abord naviguer sur la page de l'acte à sauvegarder. Il faut ensuite ouvrir la console javascript et y coller la valeur suivante, tel que décrit dans la section 'Console JavaScript' : `alert("http://www.archinoe.fr/gramps?id=" + document.f1.lcote.value + "&p=" + document.f1.pageVisu.value)`. Une fenêtre apparait alors avec l'adresse à recopier correspondant au lien de l'acte interprétable par ce plugin. Attention, ce lien est fictif est ne peut être utilisé hors du plugin.

### 81 Tarn
Site : http://archives.tarn.fr/

Extraction du lien d'un acte : Il faut tout d'abord s'enregistrer sur le site des archives du tarn, pour obtenir un login et mot de passe qui devront être renseignés au lancement du plugin. Une fois la pages à conserver trouvée sur le site, il faut activer dans le navigateur web le mode d'analyse réseau. Voir la section 'Analyse réseau'. Ensuite, il faut recharger cette page. Enfin, dans l'analyseur réseau, il faut copier l'adresse débutant par *http://archivesenligne.tarn.fr/affichage.php?image=*.

## Analyse réseau
Le mode analyse réseau permet aux navigateurs web d'exposer les opérations qu'ils effectuent sur le réseau de manière habituellement transparante pour l'utilisateur.

Pour l'activer sous Google Chrome il faut utiliser la combinaison de touches Ctrl + Maj + I. Apparait alors une zone/fenêtre dont l'entête possède de multiples onglets. Cliquer sur l'onglet Réseau (Network). Au fur et à mesure des pages visitées sur internet, des liens vont apparaître dans la liste de cette fenêtre. Il suffit de faire un clic droit sur un des liens et de cliquer sur 'Copier le lien' (Copy link address) pour sauvegarder l'adresse d'un acte. Pour que la liste soit idéalement courte, et ne contienne que la page recherchée, il suffit d'ouvrir cette fenêtre au dernier moment et de la refermer entre chaque page.

![alt text](https://github.com/coupelon/gramps-dis/raw/master/images/chrome_copie_lien.png "Analyse des flux réseau sous Chrome")

### Console JavaScript
La console javascript permet d'exécuter et de contrôler l'exécution du code JavaScript des sites web. Dans notre cas, nous l'utilisons parfois afin d'extraire des pages web des valeurs qui seront ensuite utilisées par le plugin pour l'extraction des actes.

Pour l'activer sous Firefox, il faut utiliser la combinaison de touches Ctrl + Maj + K. Apparait alors une zone/fenêtre dont l'entête possède de multiples onglets. Assurez-vous que c'est l'onglet Console qui est sélectionné. En bas de cette console, se trouve une ligne symbolisée par deux chevrons bleu à gauche, c'est là qu'il faut saisir le code donné dans ce guide, et terminer l'exécution en appuyant sur la touche Entrée.
![alt text](https://github.com/coupelon/gramps-dis/raw/master/images/firefox_console_web.png "Console Web sous Firefox")

## Test du plugin

Le plugin, pour être testé, utilise une base de démonstration disponible dans le dossier test de ce projet. Le choix d'un chemin alternatif pour le stockage des fichiers téléchargés est supporté par le plugin, il est donc conseillé de la modifier lors des tests dans le menu 'préférences' de Gramps.
