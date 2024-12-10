# Discovery and language model-guided design of hyperactive transposases

A Python-based bioinformatics pipeline for recovering piggyBac transposons and transposases from genomes.

## Features
- Searches for sequences in genomes through an HMM search with BATH(Frahmmer)
  - [https://github.com/TravisWheelerLab/BATH?tab=readme-ov-file ](https://github.com/TravisWheelerLab/BATH.git)
  - Genevieve R Krause, Walt Shands, Travis J Wheeler, Sensitive and error-tolerant annotation of protein-coding DNA with BATH, Bioinformatics Advances, Volume 4, Issue 1, 2024, vbae088, https://doi.org/10.1093/bioadv/vbae088.
- Aligns DNA sequences with MAFFT and Clustalw.
  - Thompson, J. D., Higgins, D. G., & Gibson, T. J. (1994). CLUSTAL W: improving the sensitivity of progressive multiple sequence alignment through sequence weighting, position-specific gap penalties and weight matrix choice. Nucleic acids research, 22(22), 4673–4680
  - Kazutaka Katoh, Kazuharu Misawa, Kei‐ichi Kuma, Takashi Miyata, MAFFT: a novel method for rapid multiple sequence alignment based on fast Fourier transform, Nucleic Acids Research, Volume 30, Issue 14, 15 July 2002, Pages 3059–3066, https://doi.org/10.1093/nar/gkf436
- Clusters sequences with MMseqs2
  - Steinegger, M., Söding, J. MMseqs2 enables sensitive protein sequence searching for the analysis of massive data sets. Nat Biotechnol 35, 1026–1028 (2017) https://doi.org/10.1038/nbt.3988
- Identifies palindromes and specific motifs with EMBOSS.
  - Rice P., Longden I. and Bleasby A. EMBOSS: The European Molecular Biology Open Software Suite. Trends in Genetics. 2000 16(6):276-277 
- Outputs annotated sequence alignments.
- The file calculate cons for clustal was downloaded from https://github.com/fomightez/sequencework.git

## Quick Start

### Clone the Repository
Clone the Bioprospecting Pipeline repository:

```bash
git clone https://github.com/Integra-tx/Piggybac_bioprospecting_pipeline
```

Navigate to the project folder:

```bash
cd bioprospecting_pipeline
```

Install Python dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Run the main pipeline:

```bash
python3 bioprospecting_pipeline/main.py
```
In the file config.yaml, put the path to the folder with genomes in input_path, the path for where the output will be generated, the pathe for rspblast and the path for the database for rpsblast. 

## Additional Requirements

#### Update System
To update the system packages, use:

```bash
sudo apt-get update
sudo apt-get upgrade -y
```

#### Install Ray
Ray is required for parallel processing. Install it using pip:

```bash
pip3 install ray
```

Verify the installation of Ray:

```bash
python3 -c "import ray; ray.init()"
```

#### Add Python’s Local Bin Directory to PATH
To make sure all installed tools are accessible, add Python’s local bin directory to the PATH. Open the `.bashrc` file:

```bash
nano ~/.bashrc
```

Add the following line at the end:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

Save and exit the file (Press `CTRL + O` to save and `CTRL + X` to exit).

Reload the configuration:

```bash
source ~/.bashrc
```

Verify the change:

```bash
echo $PATH
```

#### Install EMBOSS
To install EMBOSS, follow these steps:

```bash
wget -m 'ftp://emboss.open-bio.org/pub/EMBOSS/'
cd emboss.open-bio.org/pub/EMBOSS/
gunzip EMBOSS-latest.tar.gz
tar xf EMBOSS-latest.tar
cd EMBOSS-6.0.1
./configure --prefix=/usr/local/emboss --without-x
make
sudo make install
```

Add EMBOSS to the PATH by editing `.bashrc`:

```bash
nano ~/.bashrc
```

Add the following line:

```bash
PATH="$PATH:/usr/local/emboss/bin"
export PATH
```

Save and exit, then reload:

```bash
source ~/.bashrc
```

Verify the installation:

```bash
embossversion
```

#### Install BLAST
To install BLAST, use the following commands:

```bash
sudo apt-get install ncftp -y
ncftp ftp.ncbi.nlm.nih.gov
cd /blast/executables/LATEST/
bin
ls
get <latest BLAST tar.gz for Linux>
bye
```

Extract and install BLAST:

```bash
tar zxvpf ncbi-blast-<version>-x64-linux.tar.gz
nano ~/.bashrc
```

Add this line:

```bash
export PATH=$PATH:$HOME/config_files/ncbi-blast-<version>/bin
source ~/.bashrc
```

To install the BLAST Database, follow these steps:

```bash
mkdir database
cd database
wget ftp.ncbi.nih.gov/pub/mmdb/cdd/cdd.tar.gz
tar -xf cdd.tar.gz
./bioprospecting_pipeline/ncbi-blast-2.16.0+/bin/makeprofiledb -title Pfam.v.26.0 -in Pfam.pn -out Pfam -threshold 9.82 -scale 100.0 -dbtype rps -index true
```
#### Instal MMseqs2
```bash
conda install -c conda-forge -c bioconda mmseqs2
```

#### Build the Frahmmer Program
Finally, build the Frahmmer program that comes with the repository:

```bash
./configure
make
make install
```

## Citation
If you use this pipeline in your research, please cite the following:

- [Discovery and language model-guided design of hyperactive transposase](https://doi.org/10.xxxx/piggybac) 
