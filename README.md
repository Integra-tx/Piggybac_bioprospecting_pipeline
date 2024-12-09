## Bioprospecting Pipeline
A Python-based bioinformatics pipeline for recovering piggyBac transposons and transposases from genomes.

## Features
- Searches for sequences in genomes through and hmm search
- Aligns DNA sequences with MAFFT.
- Identifies palindromes and specific motifs.
- Outputs annotated sequence alignments.

## Quick Start
Install dependencies:
pip install

git clone https://github.com/Integra-tx/Piggybac_bioprospecting_pipeline

cd bioprospecting_pipeline

python3 -m pip install -r requirements.txt

python3 bioprospecting_pipeline/main.py

Additional requirements:

#Update system
sudo apt-get update
sudo apt-get upgrade -y

#Install Ray
#Ray is required for parallel processing. Install it with pip
pip3 install ray

#Verify the installation
python3 -c "import ray; ray.init()"

#Add Python’s Local Bin Directory to PATH
#Add the local Python binaries directory to your PATH to ensure all installed tools are accessible
#Open the ~/.bashrc file:

nano ~/.bashrc

#Add the following line at the end:

export PATH="$HOME/.local/bin:$PATH"

#Save the file:

Press CTRL + O to save.
Press CTRL + X to exit the editor.

#Reload the configuration:

source ~/.bashrc

#Verify the change:

echo $PATH

#Install EMBOSS

#Download and install EMBOSS:

wget -m 'ftp://emboss.open-bio.org/pub/EMBOSS/'

cd emboss.open-bio.org/pub/EMBOSS/

gunzip EMBOSS-latest.tar.gz

tar xf EMBOSS-latest.tar

cd EMBOSS-6.0.1

./configure --prefix=/usr/local/emboss --without-x

make

sudo make install

#Add EMBOSS to your PATH:

nano ~/.bashrc
# Add this line:
PATH="$PATH:/usr/local/emboss/bin"
export PATH
# Save and exit, then reload:
source ~/.bashrc

Verify the installation:

embossversion

6. Install BLAST

Download and install BLAST:

#Install ncftp:

sudo apt-get install ncftp -y

#Use ncftp to download BLAST:

ncftp ftp.ncbi.nlm.nih.gov
cd /blast/executables/LATEST/
bin
ls
get <latest BLAST tar.gz for Linux>
bye

#Extract and install:

tar zxvpf ncbi-blast-<version>-x64-linux.tar.gz
nano ~/.bashrc
# Add this line:
export PATH=$PATH:$HOME/config_files/ncbi-blast-<version>/bin
source ~/.bashrc

Install the BLAST Database

#Download the database:

wget ftp.ncbi.nih.gov/pub/mmdb/cdd/cdd.tar.gz
tar -xf cdd.tar.gz

#Create the BLAST database:

makeprofiledb -title Pfam.v.26.0 -in Pfam.pn -out Pfam -threshold 9.82 -scale 100.0 -dbtype rps -index true

#Build the Frahmmer program that comes included in the github
./configure
make
make install  


