gcloud compute ssh --project=inductive-world-398313 --zone=us-east1-c generate-seqs-1
nvidia-smi
sudo apt-get update
sudo apt-get install bzip2 libxml2-dev -y
sudo apt-get install pip -y
sudo apt-get install git -y

pip install transformers
pip install tokenizers
pip install accelerate
pip install datasets
pip install evaluate
pip install biopython
pip install scikit-learn
git clone https://github.com/salesforce/progen

wget https://storage.googleapis.com/sfr-progen-research/checkpoints/progen2-base.tar.gz
mkdir -p progen2-base
tar -xvf progen2-base.tar.gz -C progen2-base

# Download own specific model
progenft_NC_bias/checkpoint-6000
mv checkpoint-6000 fwd_model
progenft_CN_bias/checkpoint-6000
mv checkpoint-6000 rev_model

### Generate sequences forward ----------------------------------------------------------------
# Download script to generate sequences
generate_sequences.py . 
chmod u+rwx generate_sequences.py

# Generate sequences
python3 ./generate_sequences.py --run_name fwd_run \
                        --model_checkpoint fwd_model \
                        --context SQRGPTRMCRNIYDPLLCFKLFFTDEIISEIVKWTNAEISLKRRESMTGA \
                        --max_length 500 \
                        --direction forward \
                        --temperature 0.5 \
                        --p 0.95 \
                        --num_runs 100 \
                        --gpu cuda:0

### Generate sequences reverse ----------------------------------------------------------------
# Download script to generate sequences
generate_sequences.py . 
chmod u+rwx generate_sequences.py

# Generate sequences
python3 ./generate_sequences.py --run_name rev_run \
                        --model_checkpoint rev_model \
                        --context DDSTEEPVTKKRTYCTYCPSKIRRKASASCKKCKKVICREHNIDMCQSCF \
                        --max_length 500 \
                        --direction reverse \
                        --temperature 0.5 \
                        --p 0.95 \
                        --num_runs 100 \
                        --gpu cuda:0

