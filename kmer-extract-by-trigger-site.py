#!/usr/bin/env python

# Ucdavis Genome Center
# Meric Lieberman, 2014
# This work is the property of UC Davis Genome Center

# Use at your own risk. 
# We cannot provide support.
# All information obtained/inferred with this script is without any 
# implied warranty of fitness for any purpose or use whatsoever. 
#------------------------------------------------------------------------------


#This program parses through a fastq sequence file, looking for the instance of a defined
#or set of defined subsequences. These can be as small as one base, such as 'A', which
#would be approximatley 1/4 sampling assuming no GC bias, or a set of long triggers, 
#such as "GATTACA, ACACGTGC". The triggers can be as long or short as desired, as
#long as the longest trigger is shorter than the shortest read in in the fastq file.
#The kmer will be the sequence AFTER the trigger, trigger not included.

#To Run:
#./kmer-extract-by-trigger-site.py <parameters>

#Parameters:
#-f or -- file: The inpout fastq file
#-o or --output_file: the output kmer list file
#-w or --wordsize: The kmer word size desired, often 20-45 bp
#-m or --mincount: The minimum number of times the kmer must be observed to make it to the output file
#-t -t --triggers: A list of the triggers, must be in the form \"A,BB,CCC\" with quotation marks.

#Optional:
#-s or --sort_alpha: Sort the kmers by the kmer sequence


#Output
#The output will be a text file list of kmers with the number of occurances in the second column.



from optparse import OptionParser
from collections import defaultdict
import sys
import re


usage = "\n\n%prog -r "
parser = OptionParser(usage=usage)
parser.add_option("-f", "--file", dest="file", help="Input Fastq file.")
parser.add_option("-o", "--output_file", dest="dest", help="Output file name.")
parser.add_option("-w", "--wordsize", dest="word", type="int", help="Set kmer word size")
parser.add_option("-m", "--mincount", dest="mincount",type="int", help="min number of kmer occurances to be output")
parser.add_option("-t", "--triggers", dest="triggers", type="str", help="must be in form \"AAA,BBB,CCC\" with quotation marks")
parser.add_option("-s", "--sort_alpha", dest="alphasort",default=False, action="store_true", help="Sort kmers by kmer")


(opt, args) = parser.parse_args()


f = open(opt.file)
word = opt.word
triggers = opt.triggers.split(',')

tlens = list(set([len(x) for x in triggers]))

keep = defaultdict(int)


while 1:
   name = f.readline()
   if name == '':
      break
   seq = f.readline()
   plus = f.readline()
   qual = f.readline()

   cuts = set()
   for t in triggers:
      tmatch = [x.start() for x in re.finditer(t,seq)]
      for s in tmatch:
         if len(t)+s+opt.word < len(seq):
            cuts.add(seq[len(t)+s:len(t)+s+opt.word])
   
   for x in cuts:
      keep[x] += 1
   
if opt.alphasort == False:   
   o = open(opt.dest, 'w')
   for x in keep:
      tcount = keep[x]
      if tcount >= opt.mincount: 
         o.write(x+'\t'+str(tcount)+'\n')
   o.close()
else:
   o = open(opt.dest, 'w')
   ind1 = keep.keys()
   ind1.sort()
   for x in ind1:
      tcount = keep[x]
      if tcount >= opt.mincount: 
         o.write(x+'\t'+str(tcount)+'\n')
   o.close()
      
