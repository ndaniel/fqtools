Python tools for FASTQ processing
---------------------------------

* **overlap.py** gives statistics about fragment length and mates overvallings

        overlap.py in.fq > out.fa

* **remove_adapter.py** detects the adapter automatically and removes it from the reads by trimming it

        remove_adapter.py in.fq > out.fa

* **remove_str.py** removes the reads which contain short tandem repeats regions

        remove_str.py in.fq > out.fa

* **compress-reads-ids.py** lossy compression of reads ids

        compress-reads-ids.py in.fq > out.fa

