# Pour avoir cette node, il faut lui transmettre les evenements
# donc les GPU buffers qui sont transmis entres 2 nodes/kernels doivent également contenir les event
#  de la dernière opération qu'ils ont faite // de le kernel précédant
# Ca me parait très faisable !!!