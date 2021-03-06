#!/usr/bin/env python
import os
import sys
sys.path.append('/mnt/lustre/home/cusanovich/Programs/')
sys.path.append('/mnt/lustre/home/cusanovich/Programs/lib/python2.6/site-packages/')
from myfuncs import matrix_reader,ifier
import subprocess
import numpy as np
import time
import random

genodir = '/mnt/lustre/home/cusanovich/500HT/Imputed1415/'
os.chdir(genodir)
#chrm = '22'
chrm = sys.argv[1]
start = sys.argv[2]
stop = sys.argv[3]
#Number of genes * Number of SNPs less any cis associations
bonthresh = 14014*393613.0

genes = matrix_reader('../Exprs/qqnorm.500ht.gccor.newcovcor.ordered.chr' + chrm + '.genes')
tssdic = {}
tss = open('../ensemblCAGETSS_RNAseq_sorted.bed','r')
for line in tss:
	liner = line.strip().split()
	tssdic[liner[3]] = liner[0:2]

if start == '0':
	oldfam = matrix_reader(genodir + 'hutt.imputed.500ht.fam',sep=" ")
	exprs = matrix_reader('../Exprs/qqnorm.500ht.gccor.newcovcor.ordered.chr' + chrm + '.bimbam',sep=" ")
	newfam = np.column_stack((oldfam[:,0:5],exprs))
	np.savetxt('./chr' + chrm + '.fam',newfam,delimiter=" ",fmt='%s')
	copier = 'cp ./hutt.imputed.500ht.bed ./chr' + chrm + '.bed; cp ./hutt.imputed.500ht.bim ./chr' + chrm + '.bim'
	ifier(copier)
else:
	time.sleep(random.randint(120,300))

starter = str(int(start)/100)
if len(starter) == 1:
	starter = '0' + starter
pfile = open('../ByChr/chr' + chrm + '.block' + starter + '.newcovcor.trans.pvals.txt','w')
#sigfile = open('../ByChr/chr' + chrm + '.block' + starter + '.trans.sig.txt','w')
sherlockfile = open('../ByChr/chr' + chrm + '.block' + starter + '.newcovcor.sherlock.txt','w')
for gene in range(int(start),int(stop)):
#for gene in range(2):
	gemmer = ('~/Programs/gemma0.94 -bfile ./chr' + chrm + ' -km 2 -k ../addSNP.500ht.txt -lmm 2 -n ' + str(gene + 1) + ' -maf 0.05 -o chr' + chrm + '.block' + starter)
	ifier(gemmer)
	assoc = matrix_reader(genodir + 'output/chr' + chrm + '.block' + starter + '.assoc.txt')
	assoc = assoc[1:,:]
	nocis = [x[8] if 'chr' + str(x[0]) != tssdic[genes[gene][0]][0] else x[8] if abs(int(x[2]) - int(tssdic[genes[gene][0]][1])) > 1000000 else x[8] + '(cis)' for x in assoc]
	assocupdate = np.column_stack((assoc,nocis))
	#sig = [x[1] + '\t' + x[0] + ':' + x[2] + '\t' + genes[gene][0] + '\t' + chrm + ':' + tssdic[genes[gene][0]][1] + '\t' + x[8] for x in assocupdate if x[9] != 'cis' if float(x[8]) < (1/bonthresh)]
	sherlocker = ['0' if 'chr' + str(x[0]) != tssdic[genes[gene][0]][0] else '0' if abs(int(x[2]) - int(tssdic[genes[gene][0]][1])) > 1000000 else '1' for x in assoc]
	assocupdater = np.column_stack((assocupdate,sherlocker))
	transsherlocks = [genes[gene][0] + '\t' + x[1] + '\t' + x[8] + '\t' + x[10] for x in assocupdater if x[10] == '0' if float(x[8]) < 1e-3]
	cissherlocks = [genes[gene][0] + '\t' + x[1] + '\t' + x[8] + '\t' + x[10] for x in assocupdater if x[10] == '1' if float(x[8]) < 1e-1]
	if len(transsherlocks) > 0:
		print >> sherlockfile, '\n'.join(transsherlocks)
	if len(cissherlocks) > 0:
		print >> sherlockfile, '\n'.join(cissherlocks)
	if gene == 0 and chrm == '22':
		rsfile = open('./trans.rsids.txt','w')
		snpers = ['ENSGID'] + [x for x in assoc[:,1]]
		print >> rsfile, '\n'.join(snpers)
		rsfile.close()
	print >> pfile, genes[gene][0] + '\t' +' \t'.join(nocis)
#	if len(sig) > 0:
#		print >> sigfile, '\n'.join(sig)

pfile.close()
#sigfile.close()
sherlockfile.close()
dfile = open('../ByChr/chr' + chrm + '.block' + starter + '.done','w')
dfile.close()
