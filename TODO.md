# Road map
- Create float, veector, rotation, transform data socket, and create node
- Implement Custom kernel, Custom script
- Make a PBD kernel
- Make a detection collision kernel and add constraints(=primitives)

# Bug
- Les updates des SimInputs et SimOutputs on lieux avant leur init --> ca casse tout quand on en créer 1 et que l'autre est déjà branché (corriger en corrigeant le problème des noms enfaite)
- Dans le read graph, les data/intent entre le dernier kernel, et le SimOutput ne sont pas gérée correctement
- Le pramètre frequency, dans le SimOutput, n'est ni lu ni utilisé dans la simulation (est-ce vraiment utile ??)
- Dynamic socket creation doesn't work.
- Le read graph plante quand on a 2 inputs au même endroit, ou un truc du genre (try replace input on SimInputNode)

# Improvement
- Le post process est beaucoup trop lent pour pouvoir tirer profit du GPU --> Direct OpenGL GPU read buffer ...
- Make it work with multiple Simulation loop for computaiton on 2 or more Accélérator(GPU or unused CPU)
- Add MPI operation to allow communication betewwen the Simulation loop
- Make the computation of 1 Simulation loop on multiple Accelerator(GPU or CPU) with MPI
- Lors de la création des parameters node. Pouvoir choisir les unités ! Pour faire ca il faut un enumtypeproperty ou l'on choisit l'unité. Une fois choisis, il faut delete l'ancienne props, et la recréer avec la bonne unit, en lui réassignant les bonnes values.