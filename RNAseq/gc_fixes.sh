find /mnt/lustre/home/cusanovich/data/500HTRNAseq/ -name "*.exoncounts.txt" -exec bash -c 'echo "Rscript /mnt/lustre/home/cusanovich/500HT/Scripts/gc_fixer.R {}" | qsub -l h_vmem=1g -V -o ~/dump/ -e ~/dump/ -N "gc_fix"' \;