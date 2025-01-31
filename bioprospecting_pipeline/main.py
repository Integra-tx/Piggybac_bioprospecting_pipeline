import os
import sys
import ray
import shutil
import time
import pandas as pd
from parallel_tasks import run_frehmmr, extract_dna, write_fasta_from_dataframe, batch_par, batch_write, run_palindrome, flatten_deep, sequence_cutting, parallel_paths, split_and_distribute
import yaml
import gc


def load_config():
    with open('config.yaml', 'r') as config_file:
        return yaml.safe_load(config_file)

# Example usage in main:
def main():
    config = load_config()
    
    input_path = config['input_path']
    output = config['output_path']
    pipeline_step = config['pipeline_step']
    seed = config['seed']
    orf_length = config['orf_length']
    mistake = config['mistake']
    itr = config['itr']
    motif1 = config['motif1']
    motif2 = config['motif2']
    extension = config['extension']
    full_output = config['full_output']
    ttaa_call = config['ttaa_call']
    ray_workers = config['ray_workers']
    taxonomy_file = config['taxonomy_file']
    cons_file = config['colculate_cons']
    blast_path = config['blast_path']
    blast_db = config['blast_db']
    frahmmer_aa_path = config['frahmmer_path']
    

    # Start counting the execution time of the pipeline
    start_time = time.time()
    sys.stderr.write("Bioprospecting Pipeline for the recovery of piggyBacs from genomes.\n")

    # Create directories for output
    if os.path.exists(output) is False:
    	os.mkdir(output)


    input_path = input_path.rstrip("/")

    # Check numeric inputs
    if not isinstance(mistake, int):
        if not mistake.isnumeric():
            raise TypeError("Mistakes are not whole numbers")
            
    if not isinstance(itr, int):
        if not itr.isnumeric():
            raise TypeError("ITRs are not whole numbers")
            
    if not isinstance(extension, int):
        if not extension.isnumeric():
            raise TypeError("Extension is not whole numbers")
            
    if not isinstance(orf_length, int): 
        if not orf_length.isnumeric():
            raise TypeError("Orflength is not whole numbers")
    
    mistakes_and_number = f"{mistake},{itr}"


    pipeline = int(pipeline_step) if isinstance(pipeline_step, str) and pipeline_step.isnumeric() else pipeline_step
    if pipeline not in [1, 2, 3, 4, 5]:
        raise TypeError("Pipeline number must be 1, 2, 3, 4, or 5")
        
    complete_taxonomy_dict = {}
    with open(taxonomy_file, 'r') as file:
        for line in file:
            species_name, taxonomy_class = line.split(',', 1)
            complete_taxonomy_dict[species_name] = taxonomy_class.strip()

    # Pipeline steps involving Frahmmer or genome extraction
    if pipeline in [1, 3, 4]:
        if os.path.isdir(input_path):
            if os.path.isdir(output):
                # Create empty files for output
                #create_directories(f'{output}/General_results/Frahmmer_results', individual=True)

                # Index all genomes inside the input path
                file_list = os.listdir(input_path)
                ray.init()

                # Run Frahmmer if needed
                if pipeline != 4:
                    sys.stderr.write("Running BATH\n")
                    batched_id = batch_par(file_list)
                    
                    for chunk in batched_id:
                        batch_write(file_list, extension, output, chunk, input_path, 1, seed, orf_length, complete_taxonomy_dict, blast_path, blast_db)
                    sys.stderr.write('BATH Finished\n')

                if len(file_list) == 1 and os.path.isfile(input_path + '/' + file_list[0]):
                    genome_paths = input_path + '/' + file_list[0]
                else:
                    # Parallelize the retrieval of all the genome paths and save them in a list
                    genome_paths = parallel_paths(file_list, 'genome', input_path, output)

                # Run DNA extraction
                sys.stderr.write('Starting DNA extraction\n')                
              

                # Sort and process genome reader
                
                frahmmer_list = [x for x in os.listdir(f"{output}/Frahmmer_results")]
                batch_list = batch_par(frahmmer_list)
                dataframe_pre_clustering = []
                for chunk in batch_list:
                    temporal_dataframe = batch_write(genome_paths, extension, output, chunk, input_path, 2, seed, orf_length, complete_taxonomy_dict, blast_path, blast_db)
                    dataframe_pre_clustering.append(temporal_dataframe)

                                    # Define the column names for the DataFrame
                columns = ["Accession", "Taxonomy", "Transposase", "Transposon", "CRD_motif", "DDE", "N-term", "No-nterm", "ttaa", "N_palindromes","palindromes", "SG", "Domains", "Clustered", "Full_dna"]
                flattened_list = flatten_deep(dataframe_pre_clustering)
                final_pre_clustering_dataframe = pd.DataFrame(flattened_list, columns=columns)
                final_pre_clustering_dataframe.to_csv(f'{output}/Pre_filtering_complete_data.tsv', sep='\t', index=False)
                
                write_fasta_from_dataframe(final_pre_clustering_dataframe, sequence_col="DDE", name_col="Accession", output_file=f"{output}/Complete_dde_sequences.fasta")
                sys.stderr.write('Finished DNA extraction\n')


            else:
                raise TypeError("Output path is not a directory")
        else:
            raise TypeError("Input path is not a directory")

    # Analyze Frahmmer output
    if pipeline != 1:
        
        location = frahmmer_aa_path if pipeline == 2 else f"{output}/Complete_dde_sequences.fasta"

        # Run clustering with mmseqs
        if pipeline != 5:
            sys.stderr.write('Start transposon boundary refining\n')
            os.system(f"mmseqs easy-cluster {location} clusterRes tmp --min-seq-id 0.9 -c 0.9 --cov-mode 1")
            # Save clustering results to output folder
            shutil.move("clusterRes_rep_seq.fasta", f"{output}/cluster_representative_seq.fasta")
            shutil.move("clusterRes_cluster.tsv", f"{output}/cluster_table.tsv")
            shutil.move("clusterRes_all_seqs.fasta", f"{output}/cluster_all_seqs.fasta")
        
        # Check if the complete analysis is to be run
        if full_output:
            full = 1
        else:
            full = 0
            
        # Create the path for the variable extended in case the whole pipeline is being run
        if pipeline != 2:
            extended = output + "/Extended_dna.fasta"

        if pipeline != 5:
            sys.stderr.write('Start sequence alignment\n')
            # Run the msa function with the results from the clustering
            complete_sequence_dict = {}
            with open(f"{output}/cluster_all_seqs.fasta","r") as sequence_file:
                for line in sequence_file:
                    if '>' in line:
                        accession = line.strip()[1:]
                    else:
                        sequence_line = line.strip()
                        if accession not in complete_sequence_dict:
                            dna_sequence = final_pre_clustering_dataframe.loc[final_pre_clustering_dataframe['Accession'] == accession, 'Full_dna'].values
                            dna_sequence = dna_sequence[0] if len(dna_sequence) > 0 else ""
                            complete_sequence_dict[accession] = dna_sequence

            centroid = None
            past_centroid = True
            first_pass = False
            temporal_list = []
            clustered_sequences_dict = {}
            with open(f"{output}/cluster_table.tsv", 'r') as result_file:
                for line in result_file:
                    centroid = line.split('\t')[0]
                    if centroid not in temporal_list:
                        temporal_list.append(centroid)
                    if centroid == past_centroid:
                        temporal_list.append(line.split('\t')[1])
                    else:
                        if first_pass:
                            clustered_sequences_dict[past_centroid] = temporal_list
                        temporal_list = []
                    first_pass = True
                    past_centroid = centroid
                
            
            cluster_ray = []  # List to hold remote tasks
            sequence_dict_reduced = final_pre_clustering_dataframe.set_index('Accession')['Full_dna'].to_dict()

            for centroid, members in clustered_sequences_dict.items():
                if len(members) > 1:
                    if len(members) < 40:
                      alt_centroid = members[0].strip().replace("$","").replace("'","")
                      print(alt_centroid)
                      file_name_for_msa = f'{alt_centroid}_temporal.fasta'
                      with open(file_name_for_msa,'w') as temp_file:
                        for sequence_name in members:
                            print(sequence_name)
                            full_dna_value = complete_sequence_dict[sequence_name.strip()]
                            temp_file.write('>' + sequence_name.strip() + '\n' + full_dna_value + '\n')
                      count_of_lines = len(members)
                      cluster_ray.append(sequence_cutting.remote(file_name_for_msa, centroid, cons_file, count_of_lines, alt_centroid))
                      for unique_members in members:
                        final_pre_clustering_dataframe.loc[
                        final_pre_clustering_dataframe["Accession"] == unique_members.strip(), "Clustered"] = 'True'
                    else:
                        split_members = split_and_distribute(members)
                        for chunk in split_members:
                          alt_centroid = chunk[0].strip().replace("$","").replace("'","")
                          print(alt_centroid)
                          file_name_for_msa = f'{alt_centroid}_temporal.fasta'
                          with open(file_name_for_msa,'w') as temp_file:
                            for sequence_names in chunk:
                              full_dna_value = complete_sequence_dict[sequence_names.strip()]
                              temp_file.write('>' + sequence_names + '\n' + full_dna_value + '\n')
                          count_of_lines = len(chunk)
                          cluster_ray.append(sequence_cutting.remote(file_name_for_msa, centroid, cons_file, count_of_lines, alt_centroid))
                          for unique_members in chunk:
                            final_pre_clustering_dataframe.loc[final_pre_clustering_dataframe["Accession"] == unique_members.strip(), "Clustered"] = 'True'
                else:
                    final_pre_clustering_dataframe.loc[
                        final_pre_clustering_dataframe["Accession"] == members[0].strip(), "Clustered"] = 'False'

            # Process tasks in batches
            batch_size = 5  # Adjust based on memory constraints
            task_batches = [
                cluster_ray[i:i + batch_size]
                for i in range(0, len(cluster_ray), batch_size)
            ]

            tmp_base_path = "/home/alejandro_af_integra_tx_com/Piggybac_bioprospecting_pipeline/bioprospecting_pipeline/tmp"

            newlist = []  # To store results
            for batch in task_batches:
                batch_results = ray.get(batch)  # Retrieve results for the current batch
                newlist.extend(batch_results)  # Append results to the final list
                # List all subdirectories
                subdirs = [os.path.join(tmp_base_path, d) for d in os.listdir(tmp_base_path) if os.path.isdir(os.path.join(tmp_base_path, d))]
                for subdir in subdirs:
                    try:
                        shutil.rmtree(subdir)  # Recursively delete the subdirectory
                        print(f"Deleted temporary directory: {subdir}")
                    except Exception as e:
                        print(f"Failed to delete {subdir}: {e}")

                ray.internal.free(batch)
                # Clean up batch memory
                del batch_results
                del batch
                gc.collect()


            cluster_ray = [] 
            name_files = set()
            for file_name in newlist:
                for seq_id, sequence in file_name.items():
                    if seq_id not in name_files:
                        cluster_ray.append(run_palindrome.remote(seq_id, mistake, sequence))       
                        final_pre_clustering_dataframe.loc[final_pre_clustering_dataframe["Accession"] == seq_id, "Transposon"] = sequence
                        name_files.add(seq_id)
            newlist = ray.get(cluster_ray)

            for sg_pal_dict in newlist:
                if sg_pal_dict:
                    accession_name = sg_pal_dict['Accession']
                    if 'TTAA' in sg_pal_dict:
                        ttaa_result = sg_pal_dict['TTAA'] 
                        final_pre_clustering_dataframe.loc[final_pre_clustering_dataframe["Accession"] == accession_name, "ttaa"] = ttaa_result
                    if 'SG' in sg_pal_dict:
                        sg_result = sg_pal_dict['SG']
                        final_pre_clustering_dataframe.loc[final_pre_clustering_dataframe["Accession"] == accession_name, "SG"] = sg_result
                    if 'ITRs' in sg_pal_dict:
                        itr_result = sg_pal_dict['ITRs']
                        final_pre_clustering_dataframe.loc[final_pre_clustering_dataframe["Accession"] == accession_name, "N_palindromes"] = itr_result
                    if 'Seq_itr' in sg_pal_dict:
                        itr_seq = sg_pal_dict['Seq_itr']
                        final_pre_clustering_dataframe.loc[final_pre_clustering_dataframe["Accession"] == accession_name, "palindromes"] = itr_seq                
                #os.remove(file_name)
            final_pre_clustering_dataframe.to_csv(f'{output}/Bioprospecting_results.csv')  
            sys.stderr.write('Finished transposon boundary refining\n')
        else:
            ray.init()
            sys.stderr.write('Pipeline Option 5')
            msa_results = small_reader(output)           
        

    sys.stderr.write("Program finished correctly.\n")
    shutil.rmtree('tmp')


    # Log execution time
    end_time = time.time()
    print(f"The time of execution is: {(end_time - start_time) / 60} minutes")


if __name__ == "__main__":
    main()

