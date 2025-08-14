
# Discovery and Language Model-Guided Design of Hyperactive Transposases

A Python-based bioinformatics pipeline for recovering piggyBac transposons and transposases from genomes.

## Table of Contents

- [Quick Start](#quick-start)
- [Additional Requirements](#additional-requirements)
  - [System Update](#update-system)
  - [Install Ray](#install-ray)
  - [Install EMBOSS](#install-emboss)
  - [Install BLAST](#install-blast)
  - [Install MMseqs2](#install-mmseqs2)
  - [Install MAFFT](#install-mafft)
  - [Build Frahmmer Program](#build-the-frahmmer-program)
- [Features](#features)
- [Citation](#citation)

## Quick Start

## Clone the Repository

Start by cloning the repository:

```bash
git clone https://github.com/Integra-tx/Piggybac_bioprospecting_pipeline
```

Navigate to the project directory:

```bash
cd bioprospecting_pipeline
```

Install the required Python dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Run the main pipeline:

```bash
python3 bioprospecting_pipeline/main.py
```

Before running the pipeline, configure the `config.yaml` file. Specify the following paths:
- `input_path`: The directory containing your genome files.
- `output_path`: The directory where the output will be stored.
- `rspblast_path`: The path to the `rpsblast` executable.
- `database_path`: The path to the RPSBLAST database.

## Additional Requirements

### Update System

Ensure your system is up-to-date:

```bash
sudo apt-get update
sudo apt-get upgrade -y
```

### Install Ray

Ray is used for parallel processing. To install Ray:

```bash
pip3 install ray
```

Verify the installation:

```bash
python3 -c "import ray; ray.init()"
```

### Add Python’s Local Bin Directory to PATH

Ensure that installed tools are accessible by adding Python’s local bin directory to your PATH. To do this, edit the `.bashrc` file:

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

### Install EMBOSS

To install EMBOSS, run the following commands:

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

Next, add EMBOSS to your PATH by editing `.bashrc`:

```bash
nano ~/.bashrc
```

Add the following line:

```bash
export PATH="$PATH:/usr/local/emboss/bin"
```

Save and reload the configuration:

```bash
source ~/.bashrc
```

Verify installation:

```bash
embossversion
```

### Install BLAST

To install BLAST, run the following commands:

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

Add this line to `.bashrc`:

```bash
export PATH=$PATH:$HOME/config_files/ncbi-blast-<version>/bin
source ~/.bashrc
```

To install the BLAST Database:

```bash
mkdir database
cd database
wget ftp.ncbi.nih.gov/pub/mmdb/cdd/cdd.tar.gz
tar -xf cdd.tar.gz
./bioprospecting_pipeline/ncbi-blast-2.16.0+/bin/makeprofiledb -title Pfam.v.26.0 -in Pfam.pn -out Pfam -threshold 9.82 -scale 100.0 -dbtype rps -index true
```

### Install MMseqs2

To install MMseqs2, run:

```bash
conda install -c conda-forge -c bioconda mmseqs2
```

Make sure to create a virtual environment using Conda and activate it before installing.

### Install MAFFT

To install MAFFT, use the following commands:

```bash
sudo apt install rpm
sudo rpm -Uvh mafft-7.526-gcc_fc6.x86_64.rpm
mafft --version
```

### Build the Frahmmer Program

Finally, build the Frahmmer program included in the repository:

```bash
./configure
make
make install
```

## Features

- **HMM-based Sequence Search**: Searches for sequences in genomes using BATH (Frahmmer).
  - [BATH GitHub Repository](https://github.com/TravisWheelerLab/BATH)
  - Citation: Genevieve R. Krause, Walt Shands, Travis J. Wheeler, "Sensitive and error-tolerant annotation of protein-coding DNA with BATH", *Bioinformatics Advances*, Volume 4, Issue 1, 2024, vbae088, [DOI](https://doi.org/10.1093/bioadv/vbae088).

- **Multiple Sequence Alignment**: Aligns DNA sequences using MAFFT and ClustalW.
  - Citation for ClustalW: Thompson, J. D., Higgins, D. G., & Gibson, T. J. (1994). CLUSTAL W: improving the sensitivity of progressive multiple sequence alignment through sequence weighting, position-specific gap penalties, and weight matrix choice. *Nucleic Acids Research*, 22(22), 4673–4680.
  - Citation for MAFFT: Kazutaka Katoh, Kazuharu Misawa, Kei‐ichi Kuma, Takashi Miyata, MAFFT: a novel method for rapid multiple sequence alignment based on fast Fourier transform, *Nucleic Acids Research*, Volume 30, Issue 14, 15 July 2002, Pages 3059–3066, [DOI](https://doi.org/10.1093/nar/gkf436).

- **Sequence Clustering**: Uses MMseqs2 for sequence clustering.
  - Citation: Steinegger, M., Söding, J. MMseqs2 enables sensitive protein sequence searching for the analysis of massive data sets. *Nat Biotechnol* 35, 1026–1028 (2017), [DOI](https://doi.org/10.1038/nbt.3988).

- **Palindrome and Motif Detection**: Detects palindromes and specific motifs using EMBOSS.
  - Citation: Rice P., Longden I., and Bleasby A. EMBOSS: The European Molecular Biology Open Software Suite. *Trends in Genetics*, 2000, 16(6):276-277.

- **Domain identification**: Detects RNase H-like domains using RPS-BLAST with the the Conserved Domain Database (CDD).
  - Citation: Camacho, C., Coulouris, G., Avagyan, V., Ma, N., Papadopoulos, J., Bealer, K., & Madden, T. L. (2009). BLAST+: architecture and applications. BMC Bioinformatics, 10, 421, [DOI](https://doi.org/10.1186/1471-2105-10-421)
  - Citation: Lu, S., Wang, J., Chitsaz, F., Derbyshire, M. K., Geer, R. C., Gonzales, N. R., Gwadz, M., Hurwitz, D. I., Marchler, G. H., Song, J. S., Thanki, N., Yamashita, R. A., Yang, M., Zhang, D., Zheng, C., Lanczycki, C. J., & Marchler-Bauer, A. (2020). CDD/SPARCLE: the conserved domain database in 2020. Nucleic Acids Research, 48(D1), D265–D268, [DOI](https://doi.org/10.1093/nar/gkz991)


- **Annotated Sequence Alignments**: Outputs annotated sequence alignments.

- **Clustal Calculation**: Uses the `calculate_cons` script for Clustal alignment from [fomightez/sequencework GitHub Repository](https://github.com/fomightez/sequencework.git).

## Citation

If you use this pipeline in your research, please cite the following:

- [Discovery and Language Model-Guided Design of Hyperactive Transposase](https://doi.org/10.xxxx/piggybac)
