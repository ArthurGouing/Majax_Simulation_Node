# Ordered task
1. Add Create empty attribute node
2. Incorpore local work size option and change global work size to have 3 int places

# Road map
- Create float, veector, rotation, transform data socket, and create node
- Make a PBD kernel or VBD kernel
- Make a detection collision kernel and add constraints(=primitives)
- Make the possibility to use mutliple GPU throught 2 SimInput/Output
- Make the possiblity to use automatically on multiple GPU through 1 SimInput/Output (for batch computation)

# Bug
- Le read graph plante quand on a 2 inputs au même endroit, ou un truc du genre (try replace input on SimInputNode) (cétéait il y a longtemps, à retester)
- Bug OpenCL, les numpy data qui sont fournis au kernel ne peuvent pas être modifier, et ne peuvent donc pas être de type inout (potentiellement problematique). (il suffit de les passer en pointer -> toutes les possibilités OpenCL ne sont exploitable à travers Blender)
- Il faut encore test les geometry.groups. Mais je suis pas sur qu'il soit utilisable efficacement sur GPU ?
- Object cannot be deleted as they are used in my MajaxGraph. Need to explore why, and how to overcome it.

# Improvement
- For overight python class, make a proper unregister where I reset the base class.
- Prendre en compte le muted lorsque l'on construit les graphes.
- Faire une Loop ou un repeat. et/ou des conditions d'execution de kernel !
- Faire des conditions d'execution des buffers --> Je peux les faire dans une frame, comme le repeat !
- Faire les parametre dynamic : 
- Faire une sécurité pour embécher de nomer un argument avec "_" dans les scripts nodes car ca fait buger, ni les espaces !
- Le post process est beaucoup trop lent pour pouvoir tirer profit du GPU --> Direct OpenGL GPU read buffer ... (import gpu etc ...)
- Le kernel script lit le text du text editor (pas le fichier text stocker sur le disk) ce qui empeche d'écrire les kernels opencl sur une fenetre VSCode ou Vim sur une autre fenetre. Il faut mettre un autre kerenel node qui lui va lire le ficher. (ou ajouter une option dans le node panel ?)
- Le pramètre frequency, dans le SimOutput, n'est ni lu ni utilisé dans la simulation (est-ce vraiment utile ??)
- Redesigne the socket naming / data naming both frontend and backend
- Make it work with multiple Simulation loop for computaiton on 2 or more Accélérator(GPU or unused CPU)
- Add MPI operation to allow communication betewwen the Simulation loop
- Make the computation of 1 Simulation loop on multiple Accelerator(GPU or CPU) with MPI
- Lors de la création des parameters node. Pouvoir choisir les unités ! Pour faire ca il faut un enumtypeproperty ou l'on choisit l'unité. Une fois choisis, il faut delete l'ancienne props, et la recréer avec la bonne unit, en lui réassignant les bonnes values.