# genie_logiciel_scum

Dans le teminal on execute le programme python : ~$python3 parser.py
le programme  cherche alors le dossier cible (/CORPUS_APPRENTISSAGE) et convertie tout les PDF en fichier .txt dans un autre dossier1(/pdftotext) puis recupere les donnnées demander dans un autre dossier (parsed_files) dans des fichiers .txt.

Dans le teminal on execute le programme python pour qu'il puisse fournir comme sortie un fichier .txt : ~$python3 parser.py NOMDUDOSSIER -t
Dans le teminal on execute le programme python pour qu'il puisse fournir comme sortie un fichier XML : ~$python3 parser.py NOMDUDOSSIER -x

Nous avons amélioré le parseur que nous avons dèja créé précédemment, pour qu’il puisse fournir aussi comme sortie un fichier XML pour chaque fichier si l’utilisateur ajoute l’argument -x, et si l’utilisateur ajoute l’argument -t, le programme fournit comme sortie un fichier txt.

