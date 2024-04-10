Pour l'instant j'ai fait les fichier nodes indispensables pour pouvoir scripter et manipuler les donner de Blender sur CPU et GPU.

Je vais lister ici les nodes de bases qui pourront facilement être réaliser par des scripts Python/Numpy/OpenCL :

- SliceGeoNode: l'équvalent de la node Clip dans Houdini, permettant de couper la geometry en 2
- AddVariable: Ajoute une variable(attribut) à la géométrie, qui pourra être écrite par du script ultérieurement.(on points or on prim)
- ClearVariable: Supprime une variable
- Une facon de set des couleurs pour avoir un retour sur le viewport des mask/variable values etc...
- LogfileNode: pas sur que ce soit utilse ... 


Ce sont des nodes indispensables, notemment pour la visualisation, debugging etc...