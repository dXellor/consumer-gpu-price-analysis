from utils.loader import load_gpu_details, load_mining_data
from utils.merger import fuzzy_merge
from utils.imputer import impute_gpu_for_mining_data
import pandas as pd

def pipeline(file_name: str, gpu_details: pd.DataFrame) -> pd.DataFrame:
    relevant_columns = ['Product Name', 'Base Clock', 'Boost Clock',
                        'Memory Clock', 'Memory Size', 'Memory Type', 'Memory Bus',
                        'Bandwidth', 'TDP', 'L1 Cache', 'L2 Cache', 'Shading Units',
                        'FP32 (float)', 'Tensor Cores', 'Matrix Cores',  'Hashrate', 'Revenue 24h']
    
    mining_data = load_mining_data(file_name)
    mining_data = fuzzy_merge(mining_data, gpu_details)
    mining_data = mining_data[relevant_columns]
    mining_data.rename(columns={"Product Name": "Model"}, inplace=True)
    mining_data = impute_gpu_for_mining_data(mining_data)
    mining_data.to_csv(f"gpu_merged_{file_name}_final.csv", index=False)
    print(mining_data.info())

def main():
    gpu_details = load_gpu_details()
    pipeline("101-xmr-randomx", gpu_details)
    pipeline("162-etc-etchash", gpu_details)


if __name__ == "__main__":
    main()
