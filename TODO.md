# Road map
- Create float, veector, rotation, transform data socket, and create node
- Implement Custom kernel, Custom script
- Make a PBD kernel or VBD kernel
- Make a detection collision kernel and add constraints(=primitives)

# Bug
- Le pramètre frequency, dans le SimOutput, n'est ni lu ni utilisé dans la simulation (est-ce vraiment utile ??)
- Redesigne the socket naming / data naming both frontend and backend
- Le read graph plante quand on a 2 inputs au même endroit, ou un truc du genre (try replace input on SimInputNode)
- Bug OpenCL, les numpy data qui sont fournis au kernel ne peuvent pas être modifier, et ne peuvent donc pas être de type inout (potentiellement problematique). Je ne sais pas comment faire ca sur OpenCL independament de mon Add-on
- Le parametre frecquency sur le SimOutput ne sert à rien.
- Il faut encore test les geometry.groups. Mais je suis pas sur qu'il soit utilisable efficacement sur GPU ?
- Object cannot be deleted as they are used in my MajaxGraph. Need to explore why, and how to overcome it.

# Improvement
- L'Operator Run devrait pas faire paus, il devrait restart la simu
- Le post process est beaucoup trop lent pour pouvoir tirer profit du GPU --> Direct OpenGL GPU read buffer ...
- Le kernel script lit le text du text editor (pas le fichier text stocker sur le disk) ce qui empeche d'écrire les kernels opencl sur une fenetre VSCode ou Vim sur une autre fenetre. Il faut mettre un autre kerenel node qui lui va lire le ficher. (ou ajouter une option dans le node panel ?)
- Make it work with multiple Simulation loop for computaiton on 2 or more Accélérator(GPU or unused CPU)
- Add MPI operation to allow communication betewwen the Simulation loop
- Make the computation of 1 Simulation loop on multiple Accelerator(GPU or CPU) with MPI
- Lors de la création des parameters node. Pouvoir choisir les unités ! Pour faire ca il faut un enumtypeproperty ou l'on choisit l'unité. Une fois choisis, il faut delete l'ancienne props, et la recréer avec la bonne unit, en lui réassignant les bonnes values.