if __name__=="__main__":    
    import sys
    import os
    import time
    import dna2rna_ref
    import psyco
    psyco.full()

    d = {"sep" : os.path.sep}
    for i in range(int(sys.argv[1]), int(sys.argv[2])):
        fname = "repairguide_%04d"%i
        d["fname"] = fname
        then = time.time()
        args = ["dna2rna_ref.py", "..%(sep)s..%(sep)stask%(sep)sendo.dna"%d, "..%(sep)s..%(sep)srna%(sep)s%(fname)s.rna"%d, "..%(sep)s..%(sep)sprefix%(sep)s%(fname)s.dna"%d]
        dna2rna_ref.main(args, True)
        print "Created", fname+".rna", "in", time.time() - then, "seconds."
