
Bioprospecting Pipeline
A Python-based bioinformatics pipeline for recovering piggyBac transposons and transposases from genomes.

Features
- Searches for sequences in genomes through HMM search.
- Aligns DNA sequences with MAFFT.
- Identifies palindromes and specific motifs.
- Outputs annotated sequence alignments.

Quick Start

Install dependencies:
$ pip install

Clone the repository:
$ git clone https://github.com/Integra-tx/Piggybac_bioprospecting_pipeline

Navigate into the directory:
$ cd bioprospecting_pipeline

Install the required Python packages:
$ python3 -m pip install -r requirements.txt

Run the pipeline:
$ python3 bioprospecting_pipeline/main.py

Additional Requirements

1. Update your system:
$ sudo apt-get update
$ sudo apt-get upgrade -y

2. Install Ray (Required for parallel processing):
$ pip3 install ray

3. Verify Ray installation:
$ python3 -c "import ray; ray.init()"

4. Add Python’s Local Bin Directory to PATH:
- Open the ~/.bashrc file:
$ nano ~/.bashrc
- Add the following line at the end:
$ export PATH="$HOME/.local/bin:$PATH"
- Save the file:
  Press CTRL + O to save.
  Press CTRL + X to exit the editor.
- Reload the configuration:
$ source ~/.bashrc
- Verify the change:
$ echo $PATH

5. Install EMBOSS:
- Download and install EMBOSS:
$ wget -m 'ftp://emboss.open-bio.org/pub/EMBOSS/'
- Extract and install:
$ cd emboss.open-bio.org/pub/EMBOSS/
$ gunzip EMBOSS-latest.tar.gz
$ tar xf EMBOSS-latest.tar
$ cd EMBOSS-6.0.1
$ ./configure --prefix=/usr/local/emboss --without-x
$ make
$ sudo make install

- Add EMBOSS to your PATH:
- Open ~/.bashrc:
$ nano ~/.bashrc
- Add this line:
$ PATH="$PATH:/usr/local/emboss/bin"
$ export PATH
- Reload the configuration:
$ source ~/.bashrc
- Verify the installation:
$ embossversion

6. Install BLAST:
- Install ncftp:
$ sudo apt-get install ncftp -y
- Download BLAST using ncftp:
$ ncftp ftp.ncbi.nlm.nih.gov
$ cd /blast/executables/LATEST/
$ bin
$ ls
$ get <latest BLAST tar.gz for Linux>
$ bye

- Extract and install:
$ tar zxvpf ncbi-blast-<version>-x64-linux.tar.gz
$ nano ~/.bashrc
- Add this line:
$ export PATH=$PATH:$HOME/config_files/ncbi-blast-<version>/bin
- Reload the configuration:
$ source ~/.bashrc

Install the BLAST Database
- Download the database:
$ wget ftp.ncbi.nih.gov/pub/mmdb/cdd/cdd.tar.gz
$ tar -xf cdd.tar.gz
- Create the BLAST database:
$ ./bioprospecting_pipeline/ncbi-blast-2.16.0+/bin/makeprofiledb -title Pfam.v.26.0 -in Pfam.pn -out Pfam -threshold 9.82 -scale 100.0 -dbtype rps -index true

7. Install the Frahmmer program:
$ ./configure
$ make
$ make install
