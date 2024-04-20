# Road map
- Do first kernel test computation.
- Implement Custom kernel
- Make a PBD kernel
- Make a detection collision kernel and add constraints(=primitives)

# Bug
```
- The viewport isn't refresh within the run operator --> use handler: frame_change_pre()
```
- Dans le read graph, les data/intent entre le dernier kernel, et le SimOutput ne sont pas gérée correctement
- Le pramètre frequency, dans le SimOutput, n'est ni lu ni utilisé dans la simulation (est-ce vraiment utile ??)
- Dynamic socket creation doesn't work.

# Improvement
- Le post process est beaucoup trop lent pour pouvoir tirer profit du GPU --> Direct OpenGL GPU read buffer ...
- Make it work with multiple Simulation loop for computaiton on 2 or more Accélérator(GPU or unused CPU)
- Add MPI operation to allow communication betewwen the Simulation loop
- Make the computation of 1 Simulation loop on multiple Accelerator(GPU or CPU) with MPI