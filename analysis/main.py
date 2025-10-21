from utils.loader import load_gpu_details, load_mining_data
from utils.merger import fuzzy_merge
from utils.imputer import impute_gpu_for_mining_data
from utils.analyzer import analyze_revenue_influence
from utils.visualizer import plot_revenue_influence
from utils.predictor import predict_revenue
import pandas as pd

def pipeline(file_name: str, gpu_details: pd.DataFrame) -> pd.DataFrame:
    relevant_columns = ['Product Name', 'Base Clock', 'Boost Clock',
                        'Memory Clock', 'Memory Size', 'Memory Type', 'Memory Bus',
                        'Bandwidth', 'TDP', 'L1 Cache', 'L2 Cache', 'Shading Units',
                        'FP32 (float)', 'Tensor Cores', 'Matrix Cores', 'Revenue 24h']
    
    mining_data = load_mining_data(file_name)
    mining_data = fuzzy_merge(mining_data, gpu_details)
    mining_data = mining_data[relevant_columns]
    mining_data.rename(columns={"Product Name": "Model"}, inplace=True)
    mining_data = impute_gpu_for_mining_data(mining_data)
    print(mining_data.info())
    numeric_res, categorical_res = analyze_revenue_influence(mining_data[mining_data['Revenue 24h'].notna()])
    """  print("Najuticajniji numerički atributi po Pearson korelaciji:")
    for r in numeric_res:
      print(r)
    print("\nNajuticajniji kategorijski atributi po ANOVA testu:")
    for r in categorical_res:
      print(r)
    plot_revenue_influence(numeric_res, categorical_res) """
    df, _, _ = predict_revenue(mining_data, ['TDP', 'Bandwidth', 'FP32 (float)', 'Memory Size', 'Shading Units', 'Memory Type'])
    mining_data = df
    #mining_data.to_csv(f"gpu_merged_{file_name}_final.csv", index=False)
    print(mining_data.info())

def main():
    gpu_details = load_gpu_details()
    #pipeline("101-xmr-randomx", gpu_details)
    pipeline("162-etc-etchash", gpu_details)


if __name__ == "__main__":
    main()
