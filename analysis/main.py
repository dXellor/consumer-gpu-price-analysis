from utils.loader import load_gpu_details, load_mining_data
from utils.merger import fuzzy_merge
from utils.imputer import impute_speedup
import pandas as pd

def main():

    gpu_details = load_gpu_details()
    mining_monero = load_mining_data("101-xmr-randomx")
    mining_eth = load_mining_data("162-etc-etchash")

    merged_monero = fuzzy_merge(mining_monero, gpu_details)
    #print(merged_monero)
    #print("------------------------------------------------------------")
    merged_eth = fuzzy_merge(mining_eth, gpu_details)
    #print(merged_eth)
    #print("------------------------------------------------------------")
    gpu_all = pd.concat([merged_monero, merged_eth], ignore_index=True)
    #print(gpu_all)
    #print("------------------------------------------------------------")
    #gpu_final = impute_speedup(gpu_all)
    missing_counts = gpu_all.isna().sum()

# Percentage of missing values per column
    missing_percentage = gpu_all.isna().mean() * 100

    # Combine into one summary table
    missing_stats = pd.DataFrame({
        'missing_count': missing_counts,
        'missing_percent': missing_percentage
    }).sort_values(by='missing_count', ascending=False)

    print(missing_stats)
    gpu_all.to_csv("gpu_merged_final.csv", index=False)

if __name__ == "__main__":
    main()
