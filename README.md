# kmer-extract-by-trigger-site
A script for extracting kmers (k base pair sized words) from fastq sequencing files after a specific trigger sequence.

Descritpion:
This program parses through a fastq sequence file, looking for the instance of a defined
or set of defined subsequences. These can be as small as one base, such as 'A', which
would be approximatley 1/4 sampling assuming no GC bias, or a set of long triggers, 
such as "GATTACA, ACACGTGC". The triggers can be as long or short as desired, as
long as the longest trigger is shorter than the shortest read in in the fastq file.

To Run:
./kmer-extract-by-trigger-site.py <parameters>

Parameters:
-f or -- file: The inpout fastq file
-o or --output_file: the output kmer list file
-w or --wordsize: The kmer word size desired, often 20-45 bp
-m or --mincount: The minimum number of times the kmer must be observed to make it to the output file
-t -t --triggers: A list of the triggers, must be in the form \"A,BB,CCC\" with quotation marks.

Run example
For an input file named sequences.fq, using a trigger site of the base 'G', a mincount of 5, a word size of 27, and output file of kmers-A-trigger-30bp-min5.txt the command would be:

./kmer-extract-by-trigger-site.py -f sequences.fq -o kmers-G-trigger-30bp-min5.txt -w 27 -m 5 -t "G"

The same example, but done with the triggers "ATA" and "GTGGC" would be:

./kmer-extract-by-trigger-site.py -f sequences.fq -o kmers-2_triggers-30bp-min5.txt -w 27 -m 5 -t "ATA,GTGGC"

NOTE: As the kmer counts are kept in a dictionary in main memory, 
if performed on large files this program can use a very large amount of RAM.
If running on large files or not on cluster / informatic processing server, it is advised
to break the fastq file in to chucnks, and extract the kmers from each piece.


