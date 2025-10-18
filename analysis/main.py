from utils.loader import load_gpu_details, load_mining_data
from utils.merger import fuzzy_merge
from utils.imputer import impute_gpu_for_mining_data

def main():

    relevant_columns = ['Model_clean', 'Base Clock', 'Boost Clock',
                        'Memory Clock', 'Memory Size', 'Memory Type', 'Memory Bus',
                        'Bandwidth', 'TDP', 'L1 Cache', 'L2 Cache', 'Shading Units',
                        'FP32 (float)', 'Tensor Cores', 'Matrix Cores',  'Hashrate']

    gpu_details = load_gpu_details()

    mining_monero = load_mining_data("101-xmr-randomx")
    merged_monero = fuzzy_merge(mining_monero, gpu_details)
    merged_monero = merged_monero[relevant_columns]
    merged_monero.rename(columns={"Model_clean": "Model"}, inplace=True)
    merged_monero = impute_gpu_for_mining_data(merged_monero)
    merged_monero.drop(columns=["Matrix Cores",'Tensor Cores'], inplace=True)
    merged_monero.to_csv("gpu_merged_monero_final.csv", index=False)
    #print(merged_monero.info())

    mining_eth = load_mining_data("162-etc-etchash")
    merged_eth = fuzzy_merge(mining_eth, gpu_details)
    merged_eth = merged_eth[relevant_columns]
    merged_eth.rename(columns={"Model_clean": "Model"}, inplace=True)
    merged_eth = impute_gpu_for_mining_data(merged_eth)
    merged_eth.drop(columns=["Matrix Cores",'Tensor Cores'], inplace=True)
    #print(merged_eth.info())
    merged_eth.to_csv("gpu_merged_eth_final.csv", index=False)


if __name__ == "__main__":
    main()
